"""
Phase 10.2
Telegraph Test Mining Agent

Purpose:
    Provide a small deterministic mining-agent prototype
    for testing Telegraph miner/evaluation behavior.

IMPORTANT:

    This is a TEST MINING AGENT.

    It does NOT:
        - determine settlement eligibility
        - determine regulatory compliance
        - select settlement routes
        - override deterministic validation
        - act as the BRICS settlement engine

    It exists only to produce intelligence answers.
"""

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

TELEGRAPH_NODE_URL = (
    "http://13.237.89.59:7044"
)

SUBNET_ID = "402"

OUTPUT_FILE = (
    Path(__file__).resolve().parent
    / "mining_trade_context.json"
)


# ============================================================
# HTTP
# ============================================================

def http_get(url, params=None, timeout=20):

    if params:

        query = urllib.parse.urlencode(params)

        url = f"{url}?{query}"

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json",
        },
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:

            body = response.read().decode(
                "utf-8"
            )

            return json.loads(body)

    except urllib.error.HTTPError as exc:

        body = exc.read().decode(
            "utf-8",
            errors="replace"
        )

        raise RuntimeError(
            f"HTTP {exc.code}: {body}"
        )

    except Exception as exc:

        raise RuntimeError(
            f"Request failed: {exc}"
        )


# ============================================================
# TELEGRAPH MINER ENDPOINT
# ============================================================

def call_miner(
    endpoint,
    params=None,
):

    url = (
        f"{TELEGRAPH_NODE_URL}"
        f"/miner-dispatcher/v1/"
        f"{SUBNET_ID}"
        f"{endpoint}"
    )

    return http_get(
        url,
        params=params,
    )


# ============================================================
# MINING FUNCTIONS
# ============================================================

def mine_trade_context():

    return call_miner(
        "/trade-context"
    )


def mine_open_interest():

    return call_miner(
        "/open-interest"
    )


def mine_funding_cross():

    return call_miner(
        "/funding-cross"
    )


def mine_volatility():

    return call_miner(
        "/volatility"
    )


def mine_basis():

    return call_miner(
        "/basis"
    )


def mine_top_movers():

    return call_miner(
        "/top-movers"
    )


def mine_liquidation_leaders():

    return call_miner(
        "/liquidation-leaders"
    )


def mine_squeeze_score():

    return call_miner(
        "/squeeze-score"
    )


def mine_tvl():

    return call_miner(
        "/tvl"
    )


# ============================================================
# SAVE RAW RESPONSE
# ============================================================

def save_mining_response(
    result,
):
    """
    Save the raw Telegraph mining response.

    This preserves the original intelligence response
    before any normalization or interpretation.
    """

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            result,
            file,
            indent=2,
        )

    return OUTPUT_FILE


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=== TELEGRAPH TEST MINING AGENT ===")
    print()

    print(
        f"Node: {TELEGRAPH_NODE_URL}"
    )

    print(
        f"Subnet: {SUBNET_ID}"
    )

    print()
    print("Mining trade context...")
    print()

    try:

        result = mine_trade_context()

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        output_path = save_mining_response(
            result
        )

        print()
        print(
            "Raw mining response saved to:"
        )

        print(
            output_path
        )

        print()
        print(
            "Mining agent status: SUCCESS"
        )

    except Exception as exc:

        print()
        print(
            "Mining agent status: FAILED"
        )

        print(
            f"Error: {exc}"
        )

        raise SystemExit(1)