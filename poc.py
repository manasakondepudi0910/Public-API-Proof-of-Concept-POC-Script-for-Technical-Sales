import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


PROJECT_DIR = Path(__file__).resolve().parent
LOG_FILE = PROJECT_DIR / "poc_results.log"
ENV_FILE = PROJECT_DIR / ".env"
DEFAULT_API_BASE_URL = "https://httpbin.org"
REQUEST_TIMEOUT_SECONDS = 10


def load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE entries without overwriting shell variables."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def response_body(response: requests.Response) -> Any:
    """Return JSON when available, otherwise preserve the text body."""
    try:
        return response.json()
    except ValueError:
        return response.text


def execute_request(
    step_name: str,
    method: str,
    endpoint: str,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    include_auth: bool = True,
) -> dict[str, Any]:
    """Execute one request, append one JSON record, and never crash on HTTP errors."""
    base_url = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")
    url = f"{base_url}{endpoint}"
    logged_url = requests.Request(method, url, params=params).prepare().url
    headers = {"Content-Type": "application/json"}
    if include_auth:
        headers["Authorization"] = f"Bearer {os.getenv('MOCK_API_KEY', 'demo-token')}"

    record: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "step": step_name,
        "method": method,
        "url": logged_url,
    }

    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=data,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        record.update(
            {
                "status_code": response.status_code,
                "response": response_body(response),
            }
        )
        print(f"{step_name}: {method} {response.status_code}")
    except requests.RequestException as error:
        record.update(
            {
                "status_code": None,
                "error": f"{type(error).__name__}: {error}",
            }
        )
        print(f"{step_name}: network error ({error})")

    with LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def main() -> None:
    load_env_file(ENV_FILE)
    LOG_FILE.write_text("", encoding="utf-8")

    execute_request("Step 1: Basic GET", "GET", "/get")
    execute_request(
        "Step 2: Data Mutation POST",
        "POST",
        "/post",
        data={"name": "POC Test", "role": "Sales Engineer"},
    )
    execute_request(
        "Step 3: Filtered GET",
        "GET",
        "/get",
        params={"status": "active", "limit": 10},
    )
    execute_request("Step 4: Expected Not Found", "GET", "/status/404")
    execute_request(
        "Step 5: Expected Unauthorized",
        "GET",
        "/status/401",
        include_auth=False,
    )


if __name__ == "__main__":
    main()