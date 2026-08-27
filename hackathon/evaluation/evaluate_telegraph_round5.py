import json
from collections import Counter

INPUT_FILE = "responses_round5_500.jsonl"
OUTPUT_FILE = "evaluation_round5_500.jsonl"

records = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            records.append(json.loads(line))

print("=== TELEGRAPH RESPONSE EVALUATION ===")
print(f"Total records: {len(records)}")
print()

status_counts = Counter(r.get("status") for r in records)

print("STATUS")
for status, count in status_counts.items():
    print(f"  {status}: {count}")

print()

evaluation_records = []

for r in records:

    test_id = r.get("test_id")
    query = r.get("query", "")
    response = r.get("response")

    print("=" * 80)
    print(test_id)
    print("Query:", query)

    if not response:

        print("RESULT: NO RESPONSE")

        evaluation_records.append({
            "test_id": test_id,
            "query": query,
            "classification": "REJECTED",
            "flags": ["NO_RESPONSE"],
            "response_length": 0
        })

        continue

    try:
        content = response["choices"][0]["message"]["content"]

    except (KeyError, IndexError, TypeError):

        print("RESULT: INVALID RESPONSE FORMAT")

        evaluation_records.append({
            "test_id": test_id,
            "query": query,
            "classification": "REJECTED",
            "flags": ["INVALID_RESPONSE_FORMAT"],
            "response_length": 0
        })

        continue

    text = content.lower()

    flags = []

    if any(x in text for x in [
        "current", "live", "real-time", "today", "latest"
    ]):
        flags.append("TIME_SENSITIVE_CLAIMS")

    if any(x in text for x in [
        "regulation", "regulatory", "rbi", "sanction",
        "compliance", "kyc", "aml"
    ]):
        flags.append("REGULATORY")

    if any(x in text for x in [
        "bitcoin", "btc"
    ]):
        flags.append("BITCOIN")

    if any(x in text for x in [
        "usdc", "stablecoin", "evm"
    ]):
        flags.append("EVM_USDC")

    if any(x in text for x in [
        "bank", "swift", "correspondent"
    ]):
        flags.append("BANKING")

    if any(x in text for x in [
        "miner", "mining", "hashrate", "hash rate"
    ]):
        flags.append("MINING")

    if any(x in text for x in [
        "liquidity", "volume", "market", "price", "fee"
    ]):
        flags.append("MARKET_FINANCIAL")

    if any(x in text for x in [
        "uncertain", "uncertainty", "unknown",
        "not available", "not specified"
    ]):
        flags.append("ACKNOWLEDGES_UNCERTAINTY")

    print("Response length:", len(content))
    print("Flags:", ", ".join(flags) if flags else "NONE")

    print()
    print("Preview:")
    print(content[:500].replace("\n", " "))
    print()

    # IMPORTANT:
    # Telegraph output is still external intelligence.
    # It is NOT yet validated for use by the settlement engine.

    evaluation_records.append({
        "test_id": test_id,
        "query": query,
        "classification": "REFERENCE_ONLY",
        "flags": flags,
        "response_length": len(content)
    })


# Save evaluation results
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    for item in evaluation_records:
        f.write(
            json.dumps(item, ensure_ascii=False) + "\n"
        )

print("=" * 80)
print("EVALUATION COMPLETE")
print(f"Evaluation saved to: {OUTPUT_FILE}")