# Expected Results

The live response can contain runtime-specific headers and timestamps. The samples below are intentionally redacted and describe the contract of each step.

## Step 1: Basic GET

- Method: `GET`
- Endpoint: `/get`
- Expected status: `200 OK`
- Redacted response sample: `{ "args": {}, "headers": { "Authorization": "Bearer [REDACTED_TOKEN]" }, "url": "https://httpbin.org/get" }`

## Step 2: Data Mutation POST

- Method: `POST`
- Endpoint: `/post`
- Expected status: `200 OK`
- Redacted response sample: `{ "json": { "name": "[REDACTED_NAME]", "role": "[REDACTED_ROLE]" }, "headers": { "Authorization": "Bearer [REDACTED_TOKEN]" } }`

## Step 3: Filtered GET

- Method: `GET`
- Endpoint: `/get?status=active&limit=10`
- Expected status: `200 OK`
- Redacted response sample: `{ "args": { "limit": "10", "status": "active" }, "url": "https://httpbin.org/get?status=active&limit=10" }`

## Step 4: Expected Not Found

- Method: `GET`
- Endpoint: `/status/404`
- Expected status: `404 Not Found`
- Redacted response sample: `{ "status": 404, "body": "[REDACTED_ERROR_BODY]" }`

## Step 5: Expected Unauthorized

- Method: `GET`
- Endpoint: `/status/401`
- Authorization header: omitted intentionally
- Expected status: `401 Unauthorized`
- Redacted response sample: `{ "status": 401, "body": "[REDACTED_ERROR_BODY]" }`