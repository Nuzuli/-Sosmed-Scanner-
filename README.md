# Sosmed Scanner

A professional Python command-line utility designed to verify username availability across multiple social media platforms securely using standard library HTTP modules.

## Architecture Description
The project adheres to a clean modular architecture structure:
- `sosmed_scanner/network.py`: Handles low-level networking primitives and protocol abstractions.
- `sosmed_scanner/scanner.py`: Handles loop automation orchestration across target endpoints.
- `sosmed_scanner/cli.py`: Handles command-line arguments parsing and logging initialization.

## Environment Variables
- No environment variables required. Designed strictly as a zero-dependency, standard library standard runtime tool.

## Installation & Setup
1. Clone the repository to your local drive.
2. Install testing configurations:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Usage Execution
Execute the package module directly using Python's CLI:
```bash
python -m sosmed_scanner.cli target_username
```

## Running Automated Tests
Run automated mock test verification with forced strict coverage rules:
```bash
pytest -v --cov=sosmed_scanner --cov-fail-under=80
```
