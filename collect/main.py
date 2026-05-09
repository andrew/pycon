import json
import sys
import time
from pathlib import Path

import httpx

BASE_URL = "https://packages.ecosyste.ms/api/v1"
PER_PAGE = 100
PAGES_DIR = Path("data/pages")
HEADERS = {"User-Agent": "pycon-talk-research (andrew@ecosyste.ms)"}
MAX_RETRIES = 5


def fetch_with_backoff(client: httpx.Client, url: str, params: dict) -> httpx.Response:
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.get(url, params=params)
        except httpx.ReadTimeout:
            wait = 2 ** attempt * 10
            print(f"  timeout, retrying in {wait}s...")
            time.sleep(wait)
            continue
        if resp.status_code == 429:
            remaining = resp.headers.get("x-ratelimit-remaining", "0")
            reset = resp.headers.get("x-ratelimit-reset")
            if reset:
                wait = max(int(reset) - int(time.time()), 1)
            else:
                wait = 2 ** attempt * 30
            print(f"  rate limited (remaining={remaining}), waiting {wait}s...")
            time.sleep(wait)
            continue
        if 500 <= resp.status_code < 600:
            wait = 2 ** attempt * 10
            print(f"  server error {resp.status_code}, retrying in {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp
    raise RuntimeError(f"Failed after {MAX_RETRIES} retries")


def registry_slug(registry: str, critical: bool = False) -> str:
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    return slug


def fetch_packages(registry: str, critical: bool = False):
    pages_dir = PAGES_DIR / registry_slug(registry, critical)
    pages_dir.mkdir(parents=True, exist_ok=True)

    params = {"per_page": PER_PAGE, "sort": "downloads", "order": "desc"}
    if critical:
        params["critical"] = "true"

    # find where we left off
    existing = sorted(pages_dir.glob("page_*.json"))
    if existing:
        last_page = int(existing[-1].stem.split("_")[1])
        # check if last page was full
        last_data = json.loads(existing[-1].read_text())
        if len(last_data) < PER_PAGE:
            print(f"Already complete at page {last_page} ({len(last_data)} items on last page)")
            return
        start_page = last_page + 1
    else:
        start_page = 1

    page = start_page
    with httpx.Client(timeout=120, headers=HEADERS) as client:
        while True:
            params["page"] = page
            page_path = pages_dir / f"page_{page:04d}.json"

            print(f"Fetching page {page}...", end=" ", flush=True)
            resp = fetch_with_backoff(client, f"{BASE_URL}/registries/{registry}/packages", params)
            batch = resp.json()
            print(f"{len(batch)} packages")

            if not batch:
                break

            page_path.write_text(json.dumps(batch, indent=2))
            page += 1
            time.sleep(0.5)

    total_pages = page - 1
    total = sum(len(json.loads(p.read_text())) for p in pages_dir.glob("page_*.json"))
    print(f"Done: {total} packages across {total_pages} pages")


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv

    print(f"Fetching packages from {registry}" + (" (critical only)" if critical else "") + "...")
    fetch_packages(registry, critical=critical)


if __name__ == "__main__":
    main()
