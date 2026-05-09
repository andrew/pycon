import json
import shutil
import subprocess
import unittest
from pathlib import Path
from unittest import mock

import scan


class CloneWithBackoffTests(unittest.TestCase):
    def _result(self, rc, stderr=""):
        return subprocess.CompletedProcess(args=[], returncode=rc, stdout="", stderr=stderr)

    @mock.patch("scan.time.sleep")
    @mock.patch("scan.subprocess.run")
    def test_retries_on_transient_then_succeeds(self, m_run, m_sleep):
        m_run.side_effect = [
            self._result(128, "fatal: early EOF"),
            self._result(128, "error: RPC failed; curl 56"),
            self._result(0),
        ]
        r = scan.clone_with_backoff("https://github.com/x/y", "/tmp/nope")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(m_run.call_count, 3)
        self.assertEqual(m_sleep.call_count, 2)

    @mock.patch("scan.time.sleep")
    @mock.patch("scan.subprocess.run")
    def test_no_retry_on_permanent_error(self, m_run, m_sleep):
        m_run.return_value = self._result(128, "fatal: repository not found")
        r = scan.clone_with_backoff("https://github.com/x/y", "/tmp/nope")
        self.assertEqual(r.returncode, 128)
        self.assertEqual(m_run.call_count, 1)
        m_sleep.assert_not_called()

    @mock.patch("scan.shutil.rmtree")
    @mock.patch("scan.time.sleep")
    @mock.patch("scan.subprocess.run")
    def test_timeout_is_transient(self, m_run, m_sleep, m_rmtree):
        m_run.side_effect = [
            subprocess.TimeoutExpired(cmd=["git"], timeout=300),
            self._result(0),
        ]
        r = scan.clone_with_backoff("https://github.com/x/y", "/tmp/nope")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(m_run.call_count, 2)

    @mock.patch("scan.time.sleep")
    @mock.patch("scan.subprocess.run")
    def test_gives_up_after_max_retries(self, m_run, m_sleep):
        m_run.return_value = self._result(128, "fatal: early EOF")
        r = scan.clone_with_backoff("https://github.com/x/y", "/tmp/nope")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(m_run.call_count, scan.MAX_CLONE_RETRIES)


class RemoteHeadTests(unittest.TestCase):
    @mock.patch("scan.subprocess.run")
    def test_parses_sha(self, m_run):
        m_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout="abc123def456abc123def456abc123def456abcd\tHEAD\n", stderr="",
        )
        self.assertEqual(scan.remote_head("https://github.com/x/y"),
                         "abc123def456abc123def456abc123def456abcd")

    @mock.patch("scan.subprocess.run")
    def test_returns_none_on_failure(self, m_run):
        m_run.return_value = subprocess.CompletedProcess(args=[], returncode=128, stdout="", stderr="not found")
        self.assertIsNone(scan.remote_head("https://github.com/x/y"))

    @mock.patch("scan.subprocess.run")
    def test_returns_none_on_timeout(self, m_run):
        m_run.side_effect = subprocess.TimeoutExpired(cmd=["git"], timeout=30)
        self.assertIsNone(scan.remote_head("https://github.com/x/y"))


class ScanRepoSkipTests(unittest.TestCase):
    def setUp(self):
        self.base = Path("/tmp/scan_test")
        shutil.rmtree(self.base, ignore_errors=True)
        self.results = self.base / "results"
        self.actions = self.base / "actions"
        self.brief = self.base / "brief"
        for d in (self.results, self.actions, self.brief):
            d.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def _seed(self, name, sha=None):
        (self.results / f"{name}.json").write_text("[]")
        (self.actions / f"{name}.json").write_text("[]")
        (self.brief / f"{name}.json").write_text("{}")
        if sha:
            (self.results / f"{name}.sha").write_text(sha)

    def test_skip_when_have_all_no_force(self):
        self._seed("pkg")
        status = scan.scan_repo("pkg", "https://github.com/x/y",
                                self.results, self.actions, self.brief, set(), force=False)
        self.assertEqual(status, "skip")

    @mock.patch("scan.remote_head")
    def test_force_skip_when_head_unchanged(self, m_head):
        m_head.return_value = "abc123"
        self._seed("pkg", sha="abc123")
        status = scan.scan_repo("pkg", "https://github.com/x/y",
                                self.results, self.actions, self.brief, set(), force=True)
        self.assertEqual(status, "skip")

    @mock.patch("scan.clone_with_backoff")
    @mock.patch("scan.remote_head")
    def test_force_rescan_when_head_moved(self, m_head, m_clone):
        m_head.return_value = "newsha"
        m_clone.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="x")
        self._seed("pkg", sha="oldsha")
        status = scan.scan_repo("pkg", "https://github.com/x/y",
                                self.results, self.actions, self.brief, set(), force=True)
        m_clone.assert_called_once()
        self.assertFalse((self.results / "pkg.json").exists())

    @mock.patch("scan.clone_with_backoff")
    @mock.patch("scan.remote_head")
    def test_force_rescan_when_no_sha_recorded(self, m_head, m_clone):
        m_head.return_value = "abc123"
        m_clone.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="x")
        self._seed("pkg", sha=None)
        scan.scan_repo("pkg", "https://github.com/x/y",
                       self.results, self.actions, self.brief, set(), force=True)
        m_clone.assert_called_once()

    @mock.patch("scan.clone_with_backoff")
    @mock.patch("scan.remote_head")
    def test_force_rescan_when_lsremote_fails(self, m_head, m_clone):
        m_head.return_value = None
        m_clone.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="x")
        self._seed("pkg", sha="abc123")
        scan.scan_repo("pkg", "https://github.com/x/y",
                       self.results, self.actions, self.brief, set(), force=True)
        m_clone.assert_called_once()


class ScanRepoShaWriteTests(unittest.TestCase):
    def setUp(self):
        self.base = Path("/tmp/scan_test2")
        shutil.rmtree(self.base, ignore_errors=True)
        self.results = self.base / "results"
        self.actions = self.base / "actions"
        self.brief = self.base / "brief"
        for d in (self.results, self.actions, self.brief):
            d.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    @mock.patch("scan.subprocess.run")
    @mock.patch("scan.clone_with_backoff")
    @mock.patch("scan.remote_head")
    def test_sha_written_on_success(self, m_head, m_clone, m_run):
        m_head.return_value = None
        def fake_clone(url, dest):
            wf = Path(dest) / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "ci.yml").write_text("on: push\njobs:\n  t:\n    runs-on: ubuntu-latest\n    steps: []\n")
            return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        m_clone.side_effect = fake_clone

        def fake_run(cmd, **kw):
            if "rev-parse" in cmd:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="deadbeef\n", stderr="")
            if "brief" in cmd[0]:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="{}", stderr="")
            if "sparse-checkout" in cmd:
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")
            if "zizmor" in " ".join(cmd):
                return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="", stderr="")
        m_run.side_effect = fake_run

        status = scan.scan_repo("pkg", "https://github.com/x/y",
                                self.results, self.actions, self.brief, set(), force=False)
        self.assertEqual(status, "scanned")
        self.assertEqual((self.results / "pkg.sha").read_text(), "deadbeef")
        self.assertEqual(json.loads((self.results / "pkg.json").read_text()), [])


if __name__ == "__main__":
    unittest.main()
