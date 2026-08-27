"""
Phase 10.3
Telegraph Mining Intelligence Adapter

Purpose:
    Convert Telegraph Subnet 402 mining output into a
    small normalized intelligence record.

IMPORTANT:

    Telegraph remains INTELLIGENCE_ONLY.

    This module does NOT:
        - determine settlement eligibility
        - determine regulatory compliance
        - select settlement routes
        - calculate settlement scores
        - override deterministic validation
"""

from typing import Any, Dict


def _get(data: Dict[str, Any], *keys, default=None):
    """
    Safely retrieve nested dictionary values.
    """

    current = data

    for key in keys:

        if not isinstance(current, dict):
            return default

        current = current.get(key)

    return current


def normalize_mining_response(
    response: Dict[str, Any],
) -> Dict[str, Any]:

    return {

        "source": "Telegraph",

        "authority": "INTELLIGENCE_ONLY",

        "subnet": "402",

        "status": "AVAILABLE",

        "market_context": {

            "fear_greed": _get(
                response,
                "fear_greed",
                "value",
            ),

            "fear_greed_classification": _get(
                response,
                "fear_greed",
                "classification",
            ),

            "btc_price": _get(
                response,
                "prices",
                "btc",
                "price",
            ),

            "sol_price": _get(
                response,
                "prices",
                "sol",
                "price",
            ),

            "btc_funding": _get(
                response,
                "funding",
                "btc",
                "funding_rate_8h_equiv",
            ),

            "sol_funding": _get(
                response,
                "funding",
                "sol",
                "funding_rate_8h_equiv",
            ),
        },

        "positioning": {

            "btc_long_pct": _get(
                response,
                "positioning",
                "btc",
                "long_short_ratio",
                "long_pct",
            ),

            "btc_short_pct": _get(
                response,
                "positioning",
                "btc",
                "long_short_ratio",
                "short_pct",
            ),

            "sol_long_pct": _get(
                response,
                "positioning",
                "sol",
                "long_short_ratio",
                "long_pct",
            ),

            "sol_short_pct": _get(
                response,
                "positioning",
                "sol",
                "long_short_ratio",
                "short_pct",
            ),
        },

        "open_interest": {

            "btc_usd": _get(
                response,
                "positioning",
                "btc",
                "open_interest",
                "usd",
            ),

            "sol_usd": _get(
                response,
                "positioning",
                "sol",
                "open_interest",
                "usd",
            ),
        },

        "liquidations": {

            "btc_24h_usd": _get(
                response,
                "liquidations",
                "btc",
                "24h",
                "total_usd",
            ),

            "sol_24h_usd": _get(
                response,
                "liquidations",
                "sol",
                "24h",
                "total_usd",
            ),
        },

        "provenance": {

            "provider": "Telegraph",

            "endpoint":
                "/miner-dispatcher/v1/402/trade-context",

            "experimental": True,
        },
    }


def print_mining_intelligence(
    intelligence: Dict[str, Any],
):

    print()
    print("=== NORMALIZED TELEGRAPH MINING INTELLIGENCE ===")
    print()

    print(
        f"Source: {intelligence['source']}"
    )

    print(
        f"Authority: {intelligence['authority']}"
    )

    print(
        f"Subnet: {intelligence['subnet']}"
    )

    print(
        f"Status: {intelligence['status']}"
    )

    print()

    print("Market context:")

    for key, value in intelligence[
        "market_context"
    ].items():

        print(
            f"  {key}: {value}"
        )

    print()

    print("Positioning:")

    for key, value in intelligence[
        "positioning"
    ].items():

        print(
            f"  {key}: {value}"
        )

    print()

    print("Open interest:")

    for key, value in intelligence[
        "open_interest"
    ].items():

        print(
            f"  {key}: {value}"
        )

    print()

    print("Liquidations:")

    for key, value in intelligence[
        "liquidations"
    ].items():

        print(
            f"  {key}: {value}"
        )

    print()

    print("Provenance:")

    for key, value in intelligence[
        "provenance"
    ].items():

        print(
            f"  {key}: {value}"
        )


if __name__ == "__main__":

    print(
        "This module expects the raw Telegraph "
        "mining response."
    )
