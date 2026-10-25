# Changelog

All notable changes to this project are documented in this file.
The format follows Keep a Changelog.

## [Unreleased]

### Added
- Logging through the standard `logging` module, with a `-v/--verbose` flag for debug output on stderr.
- End-to-end integration tests covering the CLI, scanner, and network layers with a mocked HTTP call.

### Changed
- Invalid input is now reported as a logged `ERROR` message instead of a bare print.

## [0.2.0] - 2026-10-25

### Changed
- Rewrote the scanner into three focused modules: network, scanner, and CLI.
- Network errors are now reported as results instead of raised.
- Tests now use mocks and no longer require internet access.
- Development tools are pinned in `requirements-dev.txt`.

### Added
- `--platform` option to limit a scan to chosen platforms.
- `--json` output and `--delay` option.
- Username validation and exit code `2` for invalid input.
- CI with ruff, mypy, and pytest with an 80 percent coverage gate.
- Grouped monthly Dependabot updates.