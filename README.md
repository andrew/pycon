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

## License

MIT
