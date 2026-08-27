import json
import re
from collections import Counter


QUERY_FILE = "queries_500_round5.json"
RESPONSE_FILE = "responses_round5_500.jsonl"
OUTPUT_FILE = "scoring_round5_500.jsonl"


# ============================================================
# LOAD QUERIES
# ============================================================

with open(QUERY_FILE, "r", encoding="utf-8") as f:
    queries = json.load(f)

query_map = {
    item["id"]: item
    for item in queries
}


# ============================================================
# LOAD RESPONSES
# ============================================================

responses = []

with open(RESPONSE_FILE, "r", encoding="utf-8") as f:

    for line in f:

        if line.strip():
            responses.append(
                json.loads(line)
            )


print("=== ROUND 3 INTELLIGENCE SCORING ===")
print(f"Queries   : {len(queries)}")
print(f"Responses : {len(responses)}")
print()


# ============================================================
# HELPERS
# ============================================================

def contains_any(text, terms):

    return any(
        term in text
        for term in terms
    )


def score_dimension(
    text,
    terms,
):
    return 1 if contains_any(
        text,
        terms,
    ) else 0


# ============================================================
# FINANCIAL INTELLIGENCE
# ============================================================

FINANCIAL_METRICS = [
    "price",
    "market cap",
    "volume",
    "liquidity",
    "volatility",
    "open interest",
    "funding",
    "basis",
    "liquidation",
    "tvl",
    "trading range",
    "order book",
]

TIME_AWARE = [
    "current",
    "latest",
    "real-time",
    "real time",
    "today",
    "24-hour",
    "24 hour",
    "7-day",
    "7 day",
    "time-sensitive",
    "timestamp",
]

FINANCIAL_EVIDENCE = [
    "source",
    "exchange",
    "on-chain",
    "on chain",
    "blockchain",
    "data provider",
    "verify",
    "verification",
    "evidence",
]

FINANCIAL_UNCERTAINTY = [
    "uncertain",
    "uncertainty",
    "unknown",
    "not available",
    "not verified",
    "verify",
    "verification",
    "should be checked",
]


# ============================================================
# FRAUD DETECTION
# ============================================================

FRAUD_SIGNALS = [
    "fraud",
    "rug pull",
    "rug-pull",
    "scam",
    "suspicious",
    "abnormal",
    "unusual",
    "manipulation",
    "wash trading",
    "pump-and-dump",
    "pump and dump",
    "concentrated",
    "liquidity withdrawal",
    "liquidity loss",
    "mint authority",
    "freeze authority",
    "holder concentration",
]

FRAUD_EVIDENCE = [
    "transaction",
    "transaction history",
    "wallet",
    "address",
    "on-chain",
    "on chain",
    "blockchain",
    "holder",
    "liquidity",
    "volume",
    "trading data",
    "exchange data",
    "evidence",
    "source",
]

FRAUD_PATTERNS = [
    "pattern",
    "behavior",
    "activity",
    "concentration",
    "sudden",
    "rapid",
    "coordinated",
    "correlation",
    "multiple indicators",
    "cross-exchange",
]

FALSE_POSITIVE = [
    "false positive",
    "false-positive",
    "legitimate",
    "cannot conclude",
    "not necessarily",
    "does not prove",
    "not proof",
    "further investigation",
    "additional evidence",
]

UNCERTAINTY = [
    "uncertain",
    "uncertainty",
    "unknown",
    "insufficient evidence",
    "inconclusive",
    "cannot determine",
    "cannot confirm",
    "verify",
    "verification",
]


# ============================================================
# SETTLEMENT BOUNDARY
# ============================================================

SETTLEMENT_DECISION = [
    "use bitcoin for settlement",
    "use ethereum for settlement",
    "use solana for settlement",
    "recommended for settlement",
    "recommend bitcoin",
    "recommend ethereum",
    "recommend solana",
    "choose bitcoin",
    "choose ethereum",
    "choose solana",
    "best settlement route",
    "settlement should use",
    "settlement route should",
    "approve settlement",
    "reject settlement",
]

INTELLIGENCE_ONLY_LANGUAGE = [
    "does not determine settlement",
    "not a settlement recommendation",
    "not a settlement decision",
    "intelligence only",
    "intelligence-only",
    "requires further validation",
    "should be verified",
    "additional validation",
]


# ============================================================
# SCORE ONE RESPONSE
# ============================================================

def evaluate_response(
    query_record,
    response_record,
):

    test_id = query_record["id"]
    intent = query_record["intent"]
    query = query_record["query"]

    response = response_record.get(
        "response"
    )

    if not response:

        return {
            "test_id": test_id,
            "intent": intent,
            "query": query,
            "status": "NO_RESPONSE",
            "score": 0,
            "max_score": 0,
            "settlement_boundary_violation": False,
            "dimensions": {},
        }

    try:

        content = response[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

    except (
        KeyError,
        IndexError,
        TypeError,
    ):

        return {
            "test_id": test_id,
            "intent": intent,
            "query": query,
            "status": "INVALID_RESPONSE",
            "score": 0,
            "max_score": 0,
            "settlement_boundary_violation": False,
            "dimensions": {},
        }

    text = content.lower()
    # --------------------------------------------------------
    # Telegraph content-filter block
    # --------------------------------------------------------

    content_filter_markers = [
        "generated text has been blocked by our content filters",
        "content filters",
        "generated text has been blocked",
    ]

    if any(marker in text for marker in content_filter_markers):

        return {
            "test_id": test_id,
            "intent": intent,
            "query": query,
            "status": "BLOCKED_BY_CONTENT_FILTER",
            "score": 0,
            "max_score": 6 if intent == "FRAUD_DETECTION" else 5,
            "score_percent": 0.0,
            "settlement_boundary_violation": False,
            "intelligence_only_language": False,
            "response_length": len(content),
            "dimensions": {},
            "reason": (
                "Telegraph returned a content-filter block "
                "instead of intelligence."
            ),
        }
    # --------------------------------------------------------
    # Settlement boundary
    # --------------------------------------------------------

    settlement_violation = contains_any(
        text,
        SETTLEMENT_DECISION,
    )

    boundary_support = contains_any(
        text,
        INTELLIGENCE_ONLY_LANGUAGE,
    )

    # --------------------------------------------------------
    # Financial
    # --------------------------------------------------------

    if intent == "FINANCIAL_DATA":

        topic_relevance = 1 if (
            len(text) > 200
        ) else 0

        quantitative_data = score_dimension(
            text,
            FINANCIAL_METRICS,
        )

        time_awareness = score_dimension(
            text,
            TIME_AWARE,
        )

        evidence = score_dimension(
            text,
            FINANCIAL_EVIDENCE,
        )

        uncertainty = score_dimension(
            text,
            FINANCIAL_UNCERTAINTY,
        )

        dimensions = {
            "topic_relevance": topic_relevance,
            "quantitative_financial_data": quantitative_data,
            "time_sensitivity_awareness": time_awareness,
            "evidence_source_awareness": evidence,
            "uncertainty_verification": uncertainty,
        }

        score = sum(
            dimensions.values()
        )

        max_score = 5

    # --------------------------------------------------------
    # Fraud
    # --------------------------------------------------------

    else:

        topic_relevance = 1 if (
            len(text) > 200
        ) else 0

        fraud_signals = score_dimension(
            text,
            FRAUD_SIGNALS,
        )

        evidence = score_dimension(
            text,
            FRAUD_EVIDENCE,
        )

        patterns = score_dimension(
            text,
            FRAUD_PATTERNS,
        )

        false_positive = score_dimension(
            text,
            FALSE_POSITIVE,
        )

        uncertainty = score_dimension(
            text,
            UNCERTAINTY,
        )

        dimensions = {
            "topic_relevance": topic_relevance,
            "fraud_signal_detection": fraud_signals,
            "evidence_requirements": evidence,
            "suspicious_pattern_analysis": patterns,
            "false_positive_awareness": false_positive,
            "uncertainty_verification": uncertainty,
        }

        score = sum(
            dimensions.values()
        )

        max_score = 6

    return {
        "test_id": test_id,
        "intent": intent,
        "query": query,
        "status": "SCORED",
        "score": score,
        "max_score": max_score,
        "score_percent": round(
            (score / max_score) * 100,
            2,
        ),
        "settlement_boundary_violation":
            settlement_violation,
        "intelligence_only_language":
            boundary_support,
        "response_length": len(content),
        "dimensions": dimensions,
    }


# ============================================================
# MATCH RESPONSES TO QUERIES
# ============================================================

response_map = {
    item.get("test_id"): item
    for item in responses
}


evaluation_records = []

for query_record in queries:

    test_id = query_record["id"]

    response_record = response_map.get(
        test_id,
        {},
    )

    result = evaluate_response(
        query_record,
        response_record,
    )

    evaluation_records.append(
        result
    )


# ============================================================
# SAVE
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
) as f:

    for item in evaluation_records:

        f.write(
            json.dumps(
                item,
                ensure_ascii=False,
            )
            + "\n"
        )


# ============================================================
# SUMMARY
# ============================================================

financial = [
    r for r in evaluation_records
    if r["intent"] == "FINANCIAL_DATA"
    and r["status"] == "SCORED"
]

fraud = [
    r for r in evaluation_records
    if r["intent"] == "FRAUD_DETECTION"
    and r["status"] == "SCORED"
]


def average(items):

    if not items:
        return 0

    return round(
        sum(
            x["score_percent"]
            for x in items
        ) / len(items),
        2,
    )


violations = sum(
    r["settlement_boundary_violation"]
    for r in evaluation_records
)


print()
print("=== FINANCIAL INTELLIGENCE ===")
print(f"Records        : {len(financial)}")
print(f"Average score  : {average(financial)}%")

print()
print("=== FRAUD DETECTION ===")
print(f"Records        : {len(fraud)}")
print(f"Average score  : {average(fraud)}%")

print()
print("=== SETTLEMENT BOUNDARY ===")
print(f"Violations     : {violations}")

print()
print("=== SCORE DISTRIBUTION ===")

print(
    "Financial:",
    Counter(
        r["score"]
        for r in financial
    ),
)

print(
    "Fraud:",
    Counter(
        r["score"]
        for r in fraud
    ),
)

print()
print("=== COMPLETE ===")
print(
    f"Scoring saved to: {OUTPUT_FILE}"
)
