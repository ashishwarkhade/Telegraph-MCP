import json


OUTPUT_FILE = "queries_500_round4.json"


# ============================================================
# FINANCIAL INTELLIGENCE
# Target: deeper market/liquidity/derivatives intelligence
# ============================================================

financial_templates = [
    "What current financial data should be collected about {topic}?",
    "What quantitative market intelligence is relevant when evaluating {topic}?",
    "What evidence should be collected to assess the current state of {topic}?",
    "What changes over time should a financial intelligence system monitor for {topic}?",
    "What data sources or measurements should be compared when evaluating {topic}?"
]


financial_topics = [
    "Bitcoin spot price and liquidity",
    "Ethereum spot price and liquidity",
    "Solana spot price and liquidity",
    "Bitcoin trading volume",
    "Ethereum trading volume",
    "Solana trading volume",
    "cross-exchange Bitcoin price differences",
    "cross-exchange Ethereum price differences",
    "cross-exchange Solana price differences",
    "abnormal crypto trading volume",
    "rapid crypto volume increases",
    "rapid crypto volume decreases",
    "token liquidity depth",
    "token liquidity concentration",
    "protocol liquidity concentration",
    "chain liquidity concentration",
    "sudden token liquidity withdrawal",
    "rapid protocol TVL decline",
    "rapid protocol TVL growth",
    "24-hour protocol TVL changes",
    "7-day protocol TVL changes",
    "Bitcoin open interest and price",
    "Ethereum open interest and price",
    "rapid open interest growth",
    "rapid open interest decline",
    "Bitcoin funding and positioning",
    "Ethereum funding and positioning",
    "extreme positive funding",
    "extreme negative funding",
    "cross-exchange funding spreads",
    "Bitcoin perpetual basis",
    "Ethereum perpetual basis",
    "rapid basis changes",
    "crypto contango conditions",
    "crypto backwardation conditions",
    "Bitcoin liquidation activity",
    "Ethereum liquidation activity",
    "liquidation concentration",
    "rapid liquidation increases",
    "long versus short liquidation imbalance",
    "Bitcoin volatility and liquidity",
    "Ethereum volatility and liquidity",
    "Solana volatility and liquidity",
    "rapid volatility increases",
    "extreme short-term price movements",
    "market positioning concentration",
    "long-short positioning imbalance",
    "crypto market stress indicators",
    "combined liquidity and leverage conditions",
    "combined market risk indicators",
]


# ============================================================
# FRAUD DETECTION
# Target: Round-3 weak areas
# ============================================================

fraud_templates = [
    "What evidence could indicate possible fraud involving {topic}?",
    "What signals should a fraud detection system examine for {topic}?",
    "What suspicious patterns should be investigated when evaluating {topic}?",
    "What on-chain or market data should be collected to detect potential fraud involving {topic}?",
    "What independent evidence should corroborate a possible fraud signal involving {topic}?"
]


fraud_topics = [
    # Token ownership / concentration
    "top ten token holder concentration",
    "top five token holder concentration",
    "top token holder concentration",
    "concentrated token ownership",
    "rapid increase in holder concentration",
    "large token balances controlled by related wallets",
    "large transfers between major token holders",
    "coordinated selling by major token holders",
    "sudden changes in token holder distribution",
    "unusual wallet concentration after token launch",

    # Token authorities
    "Solana token mint authority",
    "Solana token freeze authority",
    "unusual Solana token authority configuration",
    "unexpected changes to token authority",
    "centralized control of token minting",
    "centralized control of token freezing",

    # Liquidity
    "sudden token liquidity withdrawal",
    "rapid token liquidity loss",
    "rapid token liquidity growth",
    "concentrated protocol liquidity",
    "suspicious protocol liquidity movements",
    "rapid protocol TVL decline",
    "rapid protocol TVL growth",
    "unusual DeFi TVL changes",
    "liquidity withdrawal by major token holders",
    "liquidity concentration in a small number of pools",

    # Trading manipulation
    "abnormal token trading volume",
    "sudden token volume spikes",
    "abnormal token price movement",
    "extreme token price increases",
    "extreme token price decreases",
    "sudden token price collapse",
    "possible pump-and-dump activity",
    "possible wash trading",
    "possible market manipulation",

    # Market behavior
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

    # Combined / evidence quality
    "unusual basis conditions",
    "conflicting token fraud indicators",
    "conflicting market fraud indicators",
    "incomplete fraud evidence",
    "uncertain fraud signals",
]


# ============================================================
# GENERATION
# ============================================================

queries = []
counter = 1


for topic in financial_topics:

    for template in financial_templates:

        queries.append({
            "id": f"ROUND4_{counter:03d}",
            "intent": "FINANCIAL_DATA",
            "category": "FINANCIAL_DATA",
            "query": template.format(topic=topic),
        })

        counter += 1


for topic in fraud_topics:

    for template in fraud_templates:

        queries.append({
            "id": f"ROUND4_{counter:03d}",
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


if len(set(q["query"] for q in queries)) != 500:
    raise SystemExit(
        "STOP: duplicate queries detected"
    )


if len(set(q["id"] for q in queries)) != 500:
    raise SystemExit(
        "STOP: duplicate IDs detected"
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


print("=== ROUND 4 QUERY SET ===")
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
