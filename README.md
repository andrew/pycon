# PyCon Talk: GitHub Actions Security in Python Packages

Data collection and analysis for a PyCon talk on GitHub Actions security across Python packages.

Uses [ecosyste.ms](https://packages.ecosyste.ms) to identify Python packages, then scans their GitHub Actions workflows with [zizmor](https://woodruffw.github.io/zizmor/) to find common security misconfigurations.

## Slides

The deck is `slides.md`, rendered with [Marp](https://marp.app/) and a custom theme in `theme.css`.

```
npx @marp-team/marp-cli slides.md --theme theme.css -o slides.html
npx @marp-team/marp-cli slides.md --theme theme.css -o slides.html --watch
npx @marp-team/marp-cli slides.md --theme theme.css -o slides.pdf --allow-local-files
```

Open `slides.html` in a browser. `f` for fullscreen, `p` for presenter view with speaker notes.

## Data collection

Requires [uv](https://docs.astral.sh/uv/).

```
cd collect

# run everything for a registry (fetch, scan, load, report)
uv run run.py pypi.org
uv run run.py rubygems.org --critical

# or run steps individually
uv run main.py                      # fetch packages from ecosyste.ms (resumable)
uv run scan.py                      # clone repos, run zizmor, extract actions (resumable)
uv run load_db.py                   # zizmor findings -> data/pypi_org.db
uv run report.py                    # findings report -> data/report_pypi_org.md
uv run load_actions_db.py           # action uses -> data/actions_pypi_org.db
uv run report_actions.py            # actions report -> data/report_actions_pypi_org.md
```

All scripts default to `pypi.org` and accept an optional registry argument and `--critical` flag.

`scan.py` writes per-package results to `data/zizmor_results/<registry>/<pkg>.json` with a `<pkg>.sha` sidecar recording the commit scanned. Pass `--workers N` to clone and scan N repos concurrently. Pass `--no-brief` to skip the toolchain analysis and clone `--sparse` so only `.github/` is ever materialised; use this for full-registry scans. Clones over 500 MB are skipped and recorded in `failed.json`. By default it skips any package that already has results, so an interrupted run can be resumed by re-running the same command. Pass `--force` to refresh: each repo's HEAD is checked with `git ls-remote` and only repos with new commits since the recorded SHA are re-cloned and re-scanned. Clones retry up to three times on transient errors (timeouts, early EOF, 5xx, rate limits) with a 300s per-attempt timeout.

For a clean point-in-time snapshot, move `data/zizmor_results/<registry>/` aside before running.

zizmor is pinned to a specific version in `scan.py` so results are comparable across runs.

```
uv run python -m unittest test_scan -v
```

## Restoring data on another machine

The full `collect/data/` tree is ~41 GB and not in git. A travel archive (`pycon-travel.zip`, ~585 MB) contains everything except `data/zizmor_results*/` and `data/pages/` — enough to run all reports, slide_data.py, and sqlite queries without re-scanning.

The archive paths are rooted at `pycon/`, so unzip from the parent directory of an existing clone to overlay the data:

```
git pull                    # make sure the clone is current first
cd ..                       # parent of pycon/
unzip pycon-travel.zip      # overlays collect/data/ into the clone
cd pycon/collect
uv sync
```

`git status` should be clean afterwards. If you need raw zizmor output or fetched pages, re-run `scan.py` / `main.py` — both are resumable.

## License

MIT
