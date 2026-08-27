import json


OUTPUT_FILE = "queries_500_round3.json"


# ============================================================
# FINANCIAL DATA
# ============================================================

financial_templates = [
    "What current financial data should be collected about {topic}?",
    "What market intelligence is relevant when evaluating {topic}?",
    "What quantitative data should an analyst obtain for {topic}?",
    "What evidence is needed to assess the current state of {topic}?",
    "What time-sensitive financial information should be checked for {topic}?"
]


financial_topics = [
    "Bitcoin price",
    "Ethereum price",
    "Solana price",
    "crypto market prices",
    "Bitcoin funding rates",
    "Ethereum funding rates",
    "USDT perpetual funding",
    "cross-exchange funding rates",
    "Bitcoin open interest",
    "Ethereum open interest",
    "USDT perpetual open interest",
    "changes in open interest",
    "one-hour open interest changes",
    "24-hour open interest changes",
    "Bitcoin realized volatility",
    "Ethereum realized volatility",
    "7-day realized volatility",
    "30-day realized volatility",
    "daily crypto trading range",
    "rapid volatility increases",
    "Bitcoin perpetual basis",
    "Ethereum perpetual basis",
    "perpetual versus spot prices",
    "crypto contango",
    "crypto backwardation",
    "rapid basis changes",
    "Bitcoin liquidations",
    "Ethereum liquidations",
    "long liquidation activity",
    "short liquidation activity",
    "liquidation concentration",
    "rapid liquidation increases",
    "largest crypto gainers",
    "largest crypto losers",
    "24-hour crypto price movers",
    "unusual crypto price movements",
    "crypto momentum conditions",
    "extreme short-term price movements",
    "DeFi total value locked",
    "protocol TVL",
    "chain TVL",
    "24-hour TVL changes",
    "7-day TVL changes",
    "DeFi liquidity",
    "protocol liquidity concentration",
    "chain liquidity concentration",
    "rapid TVL decline",
    "rapid TVL growth",
    "crypto market liquidity",
    "cross-market crypto conditions",
]


# ============================================================
# FRAUD DETECTION
# ============================================================

fraud_templates = [
    "What evidence could indicate possible fraud involving {topic}?",
    "What signals should a fraud detection system examine for {topic}?",
    "What suspicious patterns should be investigated when evaluating {topic}?",
    "What data should be collected to detect potential fraud involving {topic}?",
    "How can an analyst distinguish legitimate activity from potentially fraudulent activity involving {topic}?"
]


fraud_topics = [
    "a Solana token rug pull",
    "Solana token mint authority",
    "Solana token freeze authority",
    "Solana token holder concentration",
    "top token holder concentration",
    "top five token holder concentration",
    "top ten token holder concentration",
    "unusual token authority configuration",
    "token risk flags",
    "combined Solana token fraud risk",
    "sudden token liquidity withdrawal",
    "rapid token liquidity loss",
    "rapid token liquidity growth",
    "abnormal token trading volume",
    "abnormal token price movement",
    "extreme token price increases",
    "extreme token price decreases",
    "sudden token price collapse",
    "suspicious token launch activity",
    "concentrated token ownership",
    "large token transfers by major holders",
    "coordinated token selling",
    "possible pump-and-dump activity",
    "possible wash trading",
    "possible market manipulation",
    "unusual trading patterns",
    "abnormal exchange activity",
    "suspicious cross-exchange price differences",
    "unusual funding conditions",
    "extreme funding rates",
    "abnormal open interest growth",
    "abnormal liquidation activity",
    "unusual liquidation concentration",
    "possible liquidation manipulation",
    "suspicious short squeeze conditions",
    "suspicious long flush conditions",
    "abnormal perpetual market behavior",
    "unusual basis conditions",
    "rapid changes in market positioning",
    "extreme long-short positioning",
    "suspicious DeFi liquidity movements",
    "unusual DeFi TVL changes",
    "rapid protocol TVL decline",
    "rapid protocol TVL growth",
    "concentrated protocol liquidity",
    "suspicious token risk indicators",
    "conflicting fraud indicators",
    "incomplete fraud evidence",
    "uncertain fraud signals",
    "false positive fraud indicators",
]


# ============================================================
# GENERATION
# ============================================================

queries = []

counter = 1


for topic in financial_topics:

    for template in financial_templates:

        queries.append({
            "id": f"ROUND3_{counter:03d}",
            "intent": "FINANCIAL_DATA",
            "category": "FINANCIAL_DATA",
            "query": template.format(topic=topic),
        })

        counter += 1


for topic in fraud_topics:

    for template in fraud_templates:

        queries.append({
            "id": f"ROUND3_{counter:03d}",
            "intent": "FRAUD_DETECTION",
            "category": "FRAUD_DETECTION",
            "query": template.format(topic=topic),
        })

        counter += 1


# ============================================================
# VALIDATION
# ============================================================

if len(financial_topics) != 50:
    raise SystemExit(
        f"STOP: expected 50 financial topics, "
        f"got {len(financial_topics)}"
    )


if len(fraud_topics) != 50:
    raise SystemExit(
        f"STOP: expected 50 fraud topics, "
        f"got {len(fraud_topics)}"
    )


if len(queries) != 500:
    raise SystemExit(
        f"STOP: generated {len(queries)} queries "
        f"instead of 500"
    )


financial_count = sum(
    q["intent"] == "FINANCIAL_DATA"
    for q in queries
)


fraud_count = sum(
    q["intent"] == "FRAUD_DETECTION"
    for q in queries
)


if financial_count != 250:
    raise SystemExit(
        f"STOP: FINANCIAL_DATA count = {financial_count}"
    )


if fraud_count != 250:
    raise SystemExit(
        f"STOP: FRAUD_DETECTION count = {fraud_count}"
    )


# ============================================================
# WRITE
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        queries,
        f,
        indent=2,
        ensure_ascii=False,
    )


print("=== ROUND 3 QUERY SET ===")
print(f"Queries generated : {len(queries)}")
print(f"FINANCIAL_DATA    : {financial_count}")
print(f"FRAUD_DETECTION   : {fraud_count}")
print(f"Output             : {OUTPUT_FILE}")

print()
print("First 5:")
for item in queries[:5]:
    print(item)

print()
print("Last 5:")
for item in queries[-5:]:
    print(item)
