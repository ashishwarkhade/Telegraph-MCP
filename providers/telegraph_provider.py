"""
Phase 10.3
Telegraph Intelligence Provider

Purpose:
    Provide Telegraph intelligence to the BRICS settlement
    intelligence layer through a provider-independent boundary.

IMPORTANT:

    Telegraph is an intelligence provider only.

    It does NOT:
        - determine settlement eligibility
        - determine regulatory compliance
        - rank settlement routes
        - authorize payments
        - override deterministic decisions

Architecture:

    PaymentIntent
          |
          v
    Intelligence Provider
          |
          v
    Telegraph
          |
          v
    Raw intelligence
          |
          v
    Intelligence Normalizer
          |
          v
    Deterministic Decision Engine
"""


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_ENDPOINT = "/trade-context"


# ============================================================
# PROVIDER
# ============================================================

class TelegraphProvider:
    """
    Provider-independent interface to Telegraph intelligence.

    The provider does not contain settlement decision logic.
    """

    def __init__(
        self,
        base_url,
        subnet_id="402",
        timeout=90,
    ):
        self.base_url = base_url.rstrip("/")
        self.subnet_id = str(subnet_id)
        self.timeout = timeout

    # --------------------------------------------------------
    # Endpoint
    # --------------------------------------------------------

    def build_endpoint_url(
        self,
        path=DEFAULT_ENDPOINT,
    ):
        """
        Build the Telegraph subnet endpoint.

        Example:

            http://node/miner-dispatcher/v1/402/trade-context
        """

        if not path.startswith("/"):
            path = "/" + path

        return (
            f"{self.base_url}"
            f"/miner-dispatcher/v1/"
            f"{self.subnet_id}"
            f"{path}"
        )

    # --------------------------------------------------------
    # Intelligence request
    # --------------------------------------------------------

    def get_trade_context(self):
        """
        Retrieve Telegraph trade-context intelligence.

        This method deliberately does not interpret the result.
        """

        raise NotImplementedError(
            "Transport must be supplied by the Telegraph bridge"
        )

    # --------------------------------------------------------
    # Generic intelligence request
    # --------------------------------------------------------

    def get_intelligence(
        self,
        path=DEFAULT_ENDPOINT,
    ):
        """
        Retrieve raw intelligence from Telegraph.

        The returned data must remain raw until it enters
        the intelligence normalizer.
        """

        raise NotImplementedError(
            "Transport must be supplied by the Telegraph bridge"
        )

    # --------------------------------------------------------
    # Provider metadata
    # --------------------------------------------------------

    def provider_metadata(self):
        """
        Return provider identity and authority boundary.
        """

        return {
            "provider": "Telegraph",
            "provider_type": "INTELLIGENCE",
            "subnet_id": self.subnet_id,
            "authority": "INTELLIGENCE_ONLY",
            "settlement_authority":
                "DETERMINISTIC_ENGINE",
        }
