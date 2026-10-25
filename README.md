# Sosmed Scanner



![CI](https://github.com/Nuzuli/-Sosmed-Scanner-/actions/workflows/ci.yml/badge.svg)



A small Python command-line tool that checks whether a username exists on public profile pages. It uses only the standard library and reads public information only.

## Features

- Checks GitHub, GitLab, Reddit, Medium, and DEV.
- Three clear statuses: `found`, `not_found`, and `unknown` (for blocked or failed requests).
- Plain text or JSON output.
- Polite by default: sends a descriptive User-Agent, uses a timeout, and waits between requests.
- No third-party runtime dependencies.

## Architecture

- `sosmed_scanner/network.py`: HTTP request helper. Network errors are returned as data, never raised.
- `sosmed_scanner/scanner.py`: platform list, username validation, and the scan loop.
- `sosmed_scanner/cli.py`: argument parsing and output formatting.
- `tests/`: unit tests that use mocks, so no real network access is needed.

## Installation

Python 3.8 or newer is required. The tool itself has no dependencies. To run the tests and checks, install the development tools:

`pip install -r requirements-dev.txt`

## Usage

Run from the repository root:

`python -m sosmed_scanner.cli target_username`

Options:

- `-p`, `--platform NAME`: scan only this platform (repeatable), for example `-p github -p dev`
- `--json`: print results as JSON
- `--delay SECONDS`: pause between requests (default `0.5`)

Example output:

```
GitHub     found      https://github.com/alice
GitLab     not_found  https://gitlab.com/alice
Reddit     unknown    https://www.reddit.com/user/alice  (HTTP 429)
```

## Exit Codes

- `0`: scan finished
- `2`: invalid input (bad username or unknown platform)

## Understanding Results

- `found`: the profile page returned HTTP 200.
- `not_found`: the profile page returned HTTP 404.
- `unknown`: anything else, such as rate limiting, blocking, or a network error. The `detail` field explains why.

## Development

Run the checks locally:

```
ruff check sosmed_scanner tests
mypy sosmed_scanner
pytest -v --cov=sosmed_scanner --cov-fail-under=80
```

The same checks run on every push through GitHub Actions.

## Responsible Use

Use this tool only for lawful purposes, such as checking your own username or brand. It reads public pages only. Respect each platform's terms of service and do not use it for harassment or profiling people.

## License

MIT License. See `LICENSE`.