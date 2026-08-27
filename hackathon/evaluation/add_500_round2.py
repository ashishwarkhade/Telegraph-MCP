import json

OUTPUT_FILE = "queries_500_round2.json"

templates = [
    "What information does a financial intelligence system need about {topic}?",
    "What current data should be collected to evaluate {topic}?",
    "What risks can be identified from {topic}?",
    "How could {topic} affect cryptocurrency market or settlement risk?",
    "What evidence should be collected before relying on {topic}, and do not make a settlement recommendation?"
]

topics = {
    "TVL": [
        "DeFi total value locked",
        "protocol TVL",
        "chain TVL",
        "TVL changes over 24 hours",
        "TVL changes over 7 days",
        "DeFi liquidity",
        "protocol liquidity concentration",
        "chain liquidity concentration",
        "rapid TVL decline",
        "rapid TVL growth"
    ],

    "TRADE_CONTEXT": [
        "crypto market prices",
        "crypto funding conditions",
        "market positioning",
        "fear and greed conditions",
        "crypto liquidations",
        "overall market state",
        "Bitcoin market conditions",
        "Ethereum market conditions",
        "large crypto market movements",
        "combined crypto market risk indicators"
    ],

    "OPEN_INTEREST": [
        "Bitcoin open interest",
        "Ethereum open interest",
        "USDT perpetual open interest",
        "changes in open interest",
        "one-hour open interest changes",
        "24-hour open interest changes",
        "rapid open interest growth",
        "rapid open interest decline",
        "open interest and market price",
        "open interest as a leverage indicator"
    ],

    "FUNDING": [
        "Bitcoin funding rates",
        "Ethereum funding rates",
        "USDT perpetual funding",
        "funding differences between exchanges",
        "Bybit funding rates",
        "OKX funding rates",
        "Hyperliquid funding rates",
        "cross-exchange funding spreads",
        "extreme positive funding",
        "extreme negative funding"
    ],

    "VOLATILITY": [
        "Bitcoin realized volatility",
        "Ethereum realized volatility",
        "7-day realized volatility",
        "30-day realized volatility",
        "daily trading range",
        "rapid volatility increases",
        "unusually low volatility",
        "unusually high volatility",
        "volatility and settlement risk",
        "volatility as a market stress indicator"
    ],

    "BASIS": [
        "Bitcoin perpetual basis",
        "Ethereum perpetual basis",
        "perpetual versus spot prices",
        "crypto contango",
        "crypto backwardation",
        "positive perpetual basis",
        "negative perpetual basis",
        "rapid basis changes",
        "basis and leverage conditions",
        "basis as a market risk indicator"
    ],

    "TOP_MOVERS": [
        "largest crypto gainers",
        "largest crypto losers",
        "24-hour crypto price movers",
        "large percentage price increases",
        "large percentage price decreases",
        "unusual crypto price movements",
        "high-liquidity crypto movers",
        "low-liquidity crypto movers",
        "crypto momentum conditions",
        "extreme short-term price movements"
    ],

    "LIQUIDATIONS": [
        "Bitcoin liquidations",
        "Ethereum liquidations",
        "largest crypto liquidation events",
        "long liquidation activity",
        "short liquidation activity",
        "liquidation concentration by symbol",
        "rapid liquidation increases",
        "liquidation activity across perpetual markets",
        "liquidations as a market stress signal",
        "liquidation imbalance"
    ],

    "SQUEEZE": [
        "Bitcoin short squeeze risk",
        "Bitcoin long flush risk",
        "Ethereum short squeeze risk",
        "Ethereum long flush risk",
        "crypto squeeze scores",
        "short squeeze conditions",
        "long flush conditions",
        "extreme squeeze indicators",
        "squeeze risk and open interest",
        "squeeze risk and funding rates"
    ],

    "TOKEN_RISK": [
        "Solana token rug risk",
        "Solana token mint authority",
        "Solana token freeze authority",
        "Solana token holder concentration",
        "top token holder concentration",
        "top five token holder concentration",
        "top ten token holder concentration",
        "unusual token authority configuration",
        "token risk flags",
        "combined Solana token fraud risk"
    ]
}


queries = []

counter = 1

for category, subjects in topics.items():

    for subject in subjects:

        for template in templates:

            queries.append({
                "id": f"ROUND2_{counter:03d}",
                "category": category,
                "query": template.format(topic=subject)
            })

            counter += 1


if len(queries) != 500:
    raise SystemExit(
        f"STOP: generated {len(queries)} queries instead of 500"
    )


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(queries, f, indent=2, ensure_ascii=False)


print("=== ROUND 2 QUERY SET ===")
print(f"Queries generated: {len(queries)}")
print(f"Output: {OUTPUT_FILE}")

print()
print("First 10:")

for item in queries[:10]:
    print(item)
