import json

INPUT_FILE = "queries.json"

query_templates = {
    "BRICS": [
        "What information should be collected before evaluating {topic} for a BRICS cross-border settlement?",
        "What risks should be evaluated when considering {topic} for a BRICS transaction?",
        "What facts, assumptions, and uncertainties should be separated when assessing {topic}?",
        "What data would a deterministic settlement engine need before evaluating {topic}?",
        "What information about {topic} should be verified independently before relying on it?"
    ],

    "BITCOIN": [
        "What information should be collected about {topic} before evaluating Bitcoin settlement?",
        "What risks and uncertainties are associated with {topic}?",
        "Which parts of an assessment of {topic} require live data?",
        "What evidence would be needed before using {topic} in settlement intelligence?",
        "How should an automated system evaluate {topic} without making a settlement recommendation?"
    ],

    "USDC": [
        "What information should be collected about {topic} before evaluating USDC settlement?",
        "What risks and uncertainties are associated with {topic}?",
        "Which aspects of {topic} require current or independently verified information?",
        "What evidence would be needed before using {topic} as settlement intelligence?",
        "How should an automated system evaluate {topic} without making a route recommendation?"
    ],

    "EVM": [
        "What information should be collected about {topic} before evaluating an EVM settlement route?",
        "What risks should be considered when assessing {topic}?",
        "Which claims about {topic} require live network data?",
        "What evidence should validate information about {topic}?",
        "What information would a deterministic engine require before considering {topic}?"
    ],

    "BANKING": [
        "What information should be collected about {topic} before comparing bank settlement with blockchain settlement?",
        "What risks are associated with {topic} in cross-border payments?",
        "Which aspects of {topic} depend on the banks and jurisdictions involved?",
        "What evidence should be collected before relying on information about {topic}?",
        "What information would an automated settlement system need about {topic}?"
    ],

    "FX": [
        "What information should be collected about {topic} before evaluating a cross-border settlement?",
        "What risks arise from {topic} in international payments?",
        "Which parts of an assessment of {topic} require live market data?",
        "What evidence would validate information about {topic}?",
        "What information should a settlement engine receive about {topic} before making a decision?"
    ],

    "MARKET": [
        "What information should be collected about {topic} before evaluating a crypto settlement route?",
        "What risks can arise from {topic}?",
        "Which information about {topic} is time-sensitive?",
        "How should an automated system validate claims about {topic}?",
        "What evidence is required before market information about {topic} can influence a settlement assessment?"
    ],

    "MINING": [
        "What information should be collected about {topic} when evaluating Bitcoin network conditions?",
        "What risks and uncertainties are associated with {topic}?",
        "Which aspects of {topic} require current network data?",
        "What evidence should validate claims about {topic}?",
        "How could information about {topic} be used as external intelligence without directly making a settlement decision?"
    ],

    "RISK": [
        "What information should be collected to evaluate {topic} in cross-border settlement?",
        "What are the main failure modes associated with {topic}?",
        "Which risks related to {topic} can be measured objectively?",
        "What evidence is required before relying on an assessment of {topic}?",
        "How should a deterministic engine treat uncertainty surrounding {topic}?"
    ],

    "REGULATORY": [
        "What information should be collected to evaluate {topic}?",
        "What regulatory uncertainties should be identified when assessing {topic}?",
        "Which claims about {topic} require jurisdiction-specific verification?",
        "What evidence should be obtained before relying on information about {topic}?",
        "How should an automated settlement system treat unverified information about {topic}?"
    ]
}


topics = {
    "BRICS": [
        "India-China settlement",
        "India-Russia settlement",
        "India-Brazil settlement",
        "India-South Africa settlement",
        "BRICS currency conversion",
        "BRICS payment routing",
        "BRICS settlement liquidity",
        "BRICS settlement finality",
        "BRICS transaction monitoring",
        "BRICS payment interoperability"
    ],

    "BITCOIN": [
        "Bitcoin transaction fees",
        "Bitcoin confirmation time",
        "Bitcoin mempool congestion",
        "Bitcoin liquidity",
        "Bitcoin price volatility",
        "Bitcoin settlement finality",
        "Bitcoin custody",
        "Bitcoin wallet security",
        "Bitcoin exchange liquidity",
        "Bitcoin network reliability"
    ],

    "USDC": [
        "USDC liquidity",
        "USDC depeg risk",
        "USDC issuer risk",
        "USDC redemption",
        "USDC transfer finality",
        "USDC EVM transactions",
        "USDC smart contract risk",
        "USDC custody",
        "USDC exchange liquidity",
        "USDC fiat conversion"
    ],

    "EVM": [
        "EVM gas costs",
        "EVM network congestion",
        "EVM transaction finality",
        "EVM smart contracts",
        "EVM wallet security",
        "EVM bridge risk",
        "EVM network reliability",
        "EVM transaction monitoring",
        "EVM settlement infrastructure",
        "EVM transaction failure recovery"
    ],

    "BANKING": [
        "SWIFT transfers",
        "correspondent banking",
        "international wire transfers",
        "bank settlement fees",
        "bank FX spreads",
        "bank settlement timing",
        "payment recalls",
        "bank compliance checks",
        "bank counterparty risk",
        "bank operational failures"
    ],

    "FX": [
        "INR exchange rates",
        "USD exchange rates",
        "CNY exchange rates",
        "foreign exchange spreads",
        "FX liquidity",
        "FX volatility",
        "currency conversion costs",
        "stablecoin FX conversion",
        "crypto-to-fiat conversion",
        "cross-border FX settlement"
    ],

    "MARKET": [
        "crypto market liquidity",
        "crypto trading volume",
        "market volatility",
        "funding rates",
        "open interest",
        "basis",
        "liquidations",
        "market depth",
        "order book conditions",
        "crypto market risk"
    ],

    "MINING": [
        "Bitcoin mining",
        "Bitcoin hashrate",
        "Bitcoin mining difficulty",
        "Bitcoin miner economics",
        "mining profitability",
        "mining fees",
        "block production",
        "miner incentives",
        "network security",
        "proof-of-work economics"
    ],

    "RISK": [
        "settlement risk",
        "counterparty risk",
        "custody risk",
        "smart contract risk",
        "bridge risk",
        "fraud risk",
        "operational risk",
        "cybersecurity risk",
        "liquidity risk",
        "market risk"
    ],

    "REGULATORY": [
        "India crypto regulation",
        "India cross-border payment rules",
        "stablecoin regulation",
        "crypto KYC requirements",
        "crypto AML requirements",
        "sanctions screening",
        "digital asset licensing",
        "cross-border compliance",
        "crypto tax considerations",
        "jurisdictional regulatory risk"
    ]
}


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    existing = json.load(f)

print("=== TELEGRAPH QUERY EXPANSION ===")
print("Existing queries:", len(existing))

if len(existing) != 30:
    raise SystemExit(
        f"STOP: Expected 30 existing queries, found {len(existing)}"
    )

existing_ids = {item["id"] for item in existing}

if len(existing_ids) != 30:
    raise SystemExit("STOP: Existing query IDs are not unique")


new_queries = []
next_id = 31

for category in query_templates:

    for topic in topics[category]:

        for template in query_templates[category]:

            new_queries.append({
                "id": f"MINER_{next_id:03d}",
                "category": category,
                "query": template.format(topic=topic)
            })

            next_id += 1


if len(new_queries) != 500:
    raise SystemExit(
        f"STOP: Generated {len(new_queries)} instead of 500"
    )


all_queries = existing + new_queries

if len(all_queries) != 530:
    raise SystemExit(
        f"STOP: Final count is {len(all_queries)}, expected 530"
    )


with open(INPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_queries, f, indent=2, ensure_ascii=False)
    f.write("\n")


print()
print("SUCCESS")
print("Existing preserved:", len(existing))
print("New queries added: ", len(new_queries))
print("Total queries:     ", len(all_queries))
print()
print("First:", all_queries[0]["id"])
print("30th:", all_queries[29]["id"])
print("31st:", all_queries[30]["id"])
print("Last:", all_queries[-1]["id"])
print()
print("queries.json updated.")
