# Public API POC Script

This project is a reproducible five-step technical sales demonstration using the public [httpbin](https://httpbin.org) REST API. It records one JSON object per request in `poc_results.log`, including successful and expected error responses.

### Prerequisites

- Python 3.10 or newer
- Git Bash on Windows
- Internet access to `https://httpbin.org`

### Installation

From Git Bash, clone and enter the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Environment Setup

Create the local environment file from the committed template:

```bash
cp .env.example .env
```

The default values are sufficient for this demonstration. `MOCK_API_KEY` is deliberately a dummy value and must not be replaced with a real secret. The `.env` file is ignored by Git.

### Execution

Run the complete demonstration with one command:

```bash
python poc.py
```

The script runs sequentially and recreates `poc_results.log` on each run. The expected status sequence is `200`, `200`, `200`, `404`, `401`. Steps 4 and 5 are intentional error paths and are logged without stopping the script.

### Verification

Inspect the generated artifact:

```bash
cat poc_results.log
```

The file must contain five JSON lines, one each for Steps 1 through 5. Do not commit `.env` or `poc_results.log`; both are local demo artifacts.