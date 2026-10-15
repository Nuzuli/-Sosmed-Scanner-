# Contributing Guide

Thank you for your interest in improving Sosmed Scanner! Please follow these development onboarding procedures before opening any pull requests.

## Local Development Lifecycle
1. Clone the repository setup.
2. Install local QA tools:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Pre-commit Verification
Always ensure your locally running code satisfies code style limits and tests execute cleanly:
- **Linting Verification:** `flake8 .`
- **Testing Assertions:** `pytest -v --cov=sosmed_scanner`
