"""
Phase 10.3
Telegraph Normalized Intelligence Adapter

Purpose:
    Normalize intelligence received from Telegraph subnet 402.

IMPORTANT:

    Telegraph is an experimental intelligence source.

    Telegraph does NOT:
        - determine settlement eligibility
        - determine regulatory compliance
        - select the final settlement route
        - override deterministic validation
        - become the source of truth

    Existing real data sources remain authoritative
    for their respective data.

    The deterministic settlement engine remains
    authoritative for the final decision.
"""

from datetime import datetime, timezone


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_telegraph_response(raw_response):
    """
    Convert a successful Telegraph mining response into a
    normalized intelligence record.

    No settlement decision is performed here.
    """

    if not isinstance(raw_response, dict):

        return {
            "source": "Telegraph",
            "authority": "INTELLIGENCE_ONLY",
            "status": "INVALID",
            "data": None,
            "error": "Telegraph response is not an object.",
        }

    return {

        "source": "Telegraph",

        "authority":
            "INTELLIGENCE_ONLY",

        "status":
            "REAL_EXTERNAL_INTELLIGENCE",

        "retrieved_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "data": {

            "fear_greed":
                raw_response.get(
                    "fear_greed"
                ),

            "funding":
                raw_response.get(
                    "funding"
                ),

            "liquidations":
                raw_response.get(
                    "liquidations"
                ),

            "positioning":
                raw_response.get(
                    "positioning"
                ),

            "prices":
                raw_response.get(
                    "prices"
                ),

            "timestamp":
                raw_response.get(
                    "ts"
                ),
        },

        # Preserve the complete Telegraph response
        # for audit/debugging.
        "raw_response":
            raw_response,
    }


# ============================================================
# DISPLAY
# ============================================================

def print_telegraph_intelligence(
    intelligence,
):

    print(
        "=== NORMALIZED TELEGRAPH INTELLIGENCE ==="
    )

    print()

    print(
        f"Source: "
        f"{intelligence['source']}"
    )

    print(
        f"Authority: "
        f"{intelligence['authority']}"
    )

    print(
        f"Status: "
        f"{intelligence['status']}"
    )

    print()

    data = intelligence.get(
        "data",
        {}
    )

    fear_greed = data.get(
        "fear_greed"
    )

    if fear_greed:

        print("Market sentiment:")

        print(
            f"  Classification: "
            f"{fear_greed.get('classification')}"
        )

        print(
            f"  Value: "
            f"{fear_greed.get('value')}"
        )

        print(
            f"  Source: "
            f"{fear_greed.get('source')}"
        )

        print()

    prices = data.get(
        "prices"
    )

    if prices:

        print("Prices:")

        for asset, value in prices.items():

            print(
                f"  {asset.upper()}: "
                f"{value.get('price')} "
                f"({value.get('source')})"
            )

        print()

    positioning = data.get(
        "positioning"
    )

    if positioning:

        print("Positioning:")

        for asset in (
            "btc",
            "sol",
        ):

            item = positioning.get(
                asset
            )

            if not item:
                continue

            ratio = item.get(
                "long_short_ratio",
                {}
            )

            print(
                f"  {asset.upper()}: "
                f"long {ratio.get('long_pct')}% / "
                f"short {ratio.get('short_pct')}%"
            )

        print()

    print(
        "Settlement recommendation: "
        "NOT_PERFORMED"
    )

    print(
        "Decision authority: "
        "DETERMINISTIC_ENGINE"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "Telegraph normalization adapter"
    )

    print(
        "Waiting for Telegraph response input."
    )