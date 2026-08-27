import json
import os
import urllib.request
from datetime import datetime, timezone


TELEGRAPH_CHATBOT_URL = "http://13.237.89.59:8080/v1/chat/completions"

INPUT_FILE = "queries_500_round2.json"
OUTPUT_FILE = "responses_round2_500.jsonl"


def ask_telegraph(query):
    payload = {
        "model": "telegraph-chatbot",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        TELEGRAPH_CHATBOT_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def load_completed_ids():
    """
    Read previously collected responses so the harness can resume safely.
    Only records with status='received' are considered completed.
    """

    completed = set()

    if not os.path.exists(OUTPUT_FILE):
        return completed

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            try:
                record = json.loads(line)

                if record.get("status") == "received":
                    test_id = record.get("test_id")

                    if test_id:
                        completed.add(test_id)

            except json.JSONDecodeError:
                print("WARNING: Ignoring invalid JSONL line.")

    return completed


def main():

    # ---------------------------------------------------------
    # Load queries
    # ---------------------------------------------------------

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        queries = json.load(f)

    print("=== TELEGRAPH TEST HARNESS ===")
    print(f"Queries loaded : {len(queries)}")
    print(f"Endpoint       : {TELEGRAPH_CHATBOT_URL}")
    print(f"Output         : {OUTPUT_FILE}")
    print()

    # ---------------------------------------------------------
    # Basic validation
    # ---------------------------------------------------------

    if not queries:
        raise SystemExit("ERROR: queries.json is empty.")

    ids = [item.get("id") for item in queries]

    if any(not test_id for test_id in ids):
        raise SystemExit("ERROR: One or more queries have no ID.")

    if len(ids) != len(set(ids)):
        raise SystemExit("ERROR: Duplicate query IDs detected.")

    # ---------------------------------------------------------
    # Load already completed queries
    # ---------------------------------------------------------

    completed_ids = load_completed_ids()

    print(f"Already completed: {len(completed_ids)}")
    print()

    # ---------------------------------------------------------
    # Open output in append mode
    # ---------------------------------------------------------

    with open(OUTPUT_FILE, "a", encoding="utf-8") as output:

        for number, item in enumerate(queries, start=1):

            test_id = item["id"]
            query = item["query"]

            # -------------------------------------------------
            # Resume support
            # -------------------------------------------------

            if test_id in completed_ids:

                print(
                    f"[{number:03d}/{len(queries):03d}] "
                    f"{test_id} SKIP (already received)"
                )

                continue

            print(
                f"[{number:03d}/{len(queries):03d}] "
                f"{test_id} Sending..."
            )

            timestamp = datetime.now(timezone.utc).isoformat()

            try:

                response = ask_telegraph(query)

                record = {
                    "test_id": test_id,
                    "timestamp": timestamp,
                    "source": "Telegraph",
                    "model": "telegraph-chatbot",
                    "query": query,
                    "response": response,
                    "status": "received"
                }

                output.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    ) + "\n"
                )

                output.flush()

                completed_ids.add(test_id)

                print(
                    f"[{number:03d}/{len(queries):03d}] "
                    f"{test_id} RECEIVED"
                )

            except Exception as e:

                record = {
                    "test_id": test_id,
                    "timestamp": timestamp,
                    "source": "Telegraph",
                    "model": "telegraph-chatbot",
                    "query": query,
                    "response": None,
                    "status": "error",
                    "error": str(e)
                }

                output.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    ) + "\n"
                )

                output.flush()

                print(
                    f"[{number:03d}/{len(queries):03d}] "
                    f"{test_id} ERROR: {e}"
                )

    # ---------------------------------------------------------
    # Final summary
    # ---------------------------------------------------------

    print()
    print("=== TEST COMPLETE ===")
    print(f"Queries loaded      : {len(queries)}")
    print(f"Successful responses: {len(completed_ids)}")
    print(f"Responses saved to  : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()