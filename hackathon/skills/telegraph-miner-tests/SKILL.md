---
name: telegraph-miner-tests
description: "Use when running, extending, or diagnosing batch tests against the Telegraph miner or chatbot API, including JSON query validation, resumable JSONL collection, request failures, and coverage summaries."
---

# Telegraph Miner Tests

Run a repeatable batch of prompts against the Telegraph endpoint and produce an auditable JSONL response set.

## Workflow

1. Identify the test inputs and output file.
   - Use the repository's query fixture, normally `queries.json`.
   - Preserve the existing output file, normally `responses_*.jsonl`, so interrupted runs can resume.
   - Confirm the endpoint, model name, request timeout, and expected response format before sending requests.

2. Validate the query fixture before making network calls.
   - Load it as JSON.
   - Require a non-empty list of objects.
   - Require a non-empty unique `id` for every object.
   - Require a `query` value for every object.
   - Stop on malformed JSON, missing fields, duplicate IDs, or an empty fixture.

3. Inspect prior results for resumability.
   - Parse the output as JSONL, one record at a time.
   - Treat only records with `status: "received"` and a matching `test_id` as complete.
   - Ignore blank lines and report malformed lines without discarding valid records.
   - Reuse the exact test ID as the deduplication key.

4. Execute only pending cases.
   - Send one request per pending query using the configured model and endpoint.
   - Record an ISO-8601 UTC timestamp before each request.
   - Append one JSON object per query and flush after each record.
   - On success, persist the raw response with `status: "received"`.
   - On failure, persist `status: "error"`, the query metadata, and the error text, then continue with the remaining cases.
   - Do not mark an error as complete; a later run must retry it.

5. Report coverage and outcome.
   - Show total queries, already completed cases, newly received cases, errors, and output path.
   - Distinguish “all queries have received responses” from “the batch loop finished”.
   - When errors remain, list their test IDs and the next retry command or action.

## Decision Points

- If the output contains a received record for an ID, skip that ID unless the user explicitly requests a refresh.
- If an ID has only error records, retry it and append a new record rather than rewriting history.
- If the endpoint returns a non-JSON body, timeout, or transport error, preserve the failure as an error record and continue.
- If the response schema is unexpected but still valid JSON, retain the raw payload and flag the schema issue separately; do not silently coerce it.
- If the fixture changes IDs or queries, treat the new IDs as new work and leave historical output intact.

## Quality Checks

Before a live run:

- Compile or syntax-check the harness.
- Run a dry validation against the query fixture when available.
- Verify the endpoint is reachable with a single explicit smoke test if network access is expected.

After a run:

- Parse every non-blank output line as JSON.
- Check that each received record has `test_id`, `timestamp`, `query`, `response`, and `status`.
- Check that the number of distinct received IDs never exceeds the number of fixture IDs.
- Re-run the harness and confirm already received IDs are skipped.
- Treat remaining errors as unresolved test cases, not a successful full pass.

## Expected Result

The workflow leaves the original query fixture unchanged and produces an append-only JSONL artifact that can be resumed safely, audited per test ID, and summarized without losing failed attempts.
