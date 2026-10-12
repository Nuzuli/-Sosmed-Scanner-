# Sosmed Scanner

A high-performance Python CLI tool designed to verify username availability across popular social media platforms utilizing safe, structured standard library HTTP operations.

## Architecture & Design
- **Single-Responsibility Principle:** Modularized functions split between networking lookups (`cek_platform`) and sequence control (`jalankan_pencarian`).
- **Structured Logging:** Utilizes Python's native `logging` framework instead of dirty stdout prints.
- **Robust Exception Abstraction:** Explicit classification of network anomalies protecting execution states against `HTTPError` and `URLError`.

## Installation & Setup
1. Clone the repository into a clean environment.
2. Development tools setup:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Usage Execution
Run the scanning utility directly from your command-line interface:
```bash
python sosmed_scanner.py your_target_username
```

## Running Automated Tests
The repository features fully mocked automated unit testing managed via `pytest`:
```bash
pytest -v
```
