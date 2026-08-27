/**
 * Phase 10.2
 * Telegraph Test Mining Agent
 *
 * Purpose:
 *     Test Telegraph Subnet 402 as an intelligence source
 *     for the AI-assisted BRICS settlement system.
 *
 * IMPORTANT:
 *
 *     This is a TEST MINING AGENT.
 *
 *     It does NOT:
 *         - determine settlement eligibility
 *         - determine regulatory compliance
 *         - select settlement routes
 *         - override deterministic validation
 *         - act as the BRICS settlement engine
 *
 *     Telegraph is an experimental intelligence source only.
 *
 *     Existing real data sources remain authoritative for
 *     their respective data.
 *
 *     The deterministic settlement engine remains authoritative
 *     for the final decision.
 */

import "dotenv/config";

import { loadConfig } from "../src/config.js";
import { createPaymentAwareFetch } from "../src/x402.js";
import { callSubnet } from "../src/client.js";


// ============================================================
// CONFIGURATION
// ============================================================

const SUBNET_ID = "402";

const ENDPOINT = {
  path: "/trade-context",
  method: "GET",
};


// ============================================================
// TYPES
// ============================================================

interface TelegraphIntelligence {
  source: string;
  authority: string;

  status: string;

  subnet: string;
  endpoint: string;

  payment: string;

  intelligence: unknown;

  raw_response: unknown;

  errors: string[];
}


// ============================================================
// HELPERS
// ============================================================

function isObject(
  value: unknown
): value is Record<string, any> {

  return (
    typeof value === "object" &&
    value !== null
  );
}


function buildIntelligenceRecord(
  response: unknown
): TelegraphIntelligence {

  return {

    source:
      "Telegraph Subnet 402",

    authority:
      "INTELLIGENCE_ONLY",

    status:
      "AVAILABLE",

    subnet:
      SUBNET_ID,

    endpoint:
      ENDPOINT.path,

    payment:
      "X402_SUCCESS",

    intelligence:
      response,

    raw_response:
      response,

    errors:
      [],
  };
}


// ============================================================
// SUMMARY
// ============================================================

function printSummary(
  intelligence: TelegraphIntelligence
) {

  console.log();
  console.log(
    "=== TELEGRAPH MINING INTELLIGENCE ==="
  );

  console.log();

  console.log(
    `Source: ${intelligence.source}`
  );

  console.log(
    `Subnet: ${intelligence.subnet}`
  );

  console.log(
    `Endpoint: ${intelligence.endpoint}`
  );

  console.log(
    `Status: ${intelligence.status}`
  );

  console.log(
    `Payment: ${intelligence.payment}`
  );

  console.log();

  const data = intelligence.intelligence;

  if (!isObject(data)) {

    console.log(
      "Intelligence response:"
    );

    console.log(
      JSON.stringify(
        data,
        null,
        2
      )
    );

    return;
  }


  // ----------------------------------------------------------
  // MARKET SENTIMENT
  // ----------------------------------------------------------

  if (isObject(data.fear_greed)) {

    console.log(
      "Market sentiment:"
    );

    console.log(
      `  Classification: ${data.fear_greed.classification}`
    );

    console.log(
      `  Value: ${data.fear_greed.value}`
    );

    console.log(
      `  Source: ${data.fear_greed.source}`
    );

    console.log();
  }


  // ----------------------------------------------------------
  // PRICES
  // ----------------------------------------------------------

  if (isObject(data.prices)) {

    console.log(
      "Prices:"
    );

    for (
      const [asset, value]
      of Object.entries(data.prices)
    ) {

      if (isObject(value)) {

        console.log(
          `  ${asset.toUpperCase()}: ${value.price}`
        );

        if (value.source) {

          console.log(
            `    Source: ${value.source}`
          );
        }
      }
    }

    console.log();
  }


  // ----------------------------------------------------------
  // FUNDING
  // ----------------------------------------------------------

  if (isObject(data.funding)) {

    console.log(
      "Funding:"
    );

    for (
      const [asset, value]
      of Object.entries(data.funding)
    ) {

      if (isObject(value)) {

        console.log(
          `  ${asset.toUpperCase()}:`
        );

        console.log(
          `    Funding 8h equivalent: ${value.funding_rate_8h_equiv}`
        );

        console.log(
          `    Mark price: ${value.mark_price}`
        );

        console.log(
          `    Open interest: ${value.open_interest}`
        );
      }
    }

    console.log();
  }


  // ----------------------------------------------------------
  // POSITIONING
  // ----------------------------------------------------------

  if (isObject(data.positioning)) {

    console.log(
      "Positioning:"
    );

    for (
      const [asset, value]
      of Object.entries(data.positioning)
    ) {

      if (
        isObject(value) &&
        isObject(value.long_short_ratio)
      ) {

        console.log(
          `  ${asset.toUpperCase()}:`
        );

        console.log(
          `    Long: ${value.long_short_ratio.long_pct}%`
        );

        console.log(
          `    Short: ${value.long_short_ratio.short_pct}%`
        );
      }
    }

    console.log();
  }


  // ----------------------------------------------------------
  // LIQUIDATIONS
  // ----------------------------------------------------------

  if (isObject(data.liquidations)) {

    console.log(
      "Liquidation intelligence:"
    );

    for (
      const [asset, value]
      of Object.entries(data.liquidations)
    ) {

      if (
        isObject(value) &&
        isObject(value["1h"])
      ) {

        console.log(
          `  ${asset.toUpperCase()} 1h:`
        );

        console.log(
          `    Total liquidations: $${value["1h"].total_usd}`
        );

        console.log(
          `    Long liquidations: $${value["1h"].longs_liquidated_usd}`
        );

        console.log(
          `    Short liquidations: $${value["1h"].shorts_liquidated_usd}`
        );
      }
    }

    console.log();
  }


  // ----------------------------------------------------------
  // SOURCE
  // ----------------------------------------------------------

  if (data.ts !== undefined) {

    console.log(
      `Telegraph timestamp: ${data.ts}`
    );

    console.log();
  }
}


// ============================================================
// MAIN
// ============================================================

async function main() {

  console.log();

  console.log(
    "=== TELEGRAPH TEST MINING AGENT ==="
  );

  console.log();


  // ----------------------------------------------------------
  // CONFIGURATION
  // ----------------------------------------------------------

  const config =
    loadConfig();

  console.log(
    `Node: ${config.nodeUrl}`
  );

  console.log(
    `Subnet: ${SUBNET_ID}`
  );

  console.log();


  // ----------------------------------------------------------
  // PAYMENT-AWARE CLIENT
  // ----------------------------------------------------------

  const fetchWithPayment =
    await createPaymentAwareFetch(
      config
    );


  // ----------------------------------------------------------
  // MINING
  // ----------------------------------------------------------

  console.log(
    "Mining trade context..."
  );

  console.log();


  try {

    const response =
      await callSubnet(
        fetchWithPayment,
        config.nodeUrl,
        SUBNET_ID,
        ENDPOINT,
        {}
      );


    const intelligence =
      buildIntelligenceRecord(
        response
      );


    printSummary(
      intelligence
    );


    // --------------------------------------------------------
    // RAW NORMALIZED RECORD
    // --------------------------------------------------------

    console.log();

    console.log(
      "=== NORMALIZED INTELLIGENCE RECORD ==="
    );

    console.log();

    console.log(
      JSON.stringify(
        intelligence,
        null,
        2
      )
    );


    // --------------------------------------------------------
    // AUTHORITY
    // --------------------------------------------------------

    console.log();

    console.log(
      "Telegraph authority:"
    );

    console.log(
      "  INTELLIGENCE_ONLY"
    );

    console.log();

    console.log(
      "Settlement authority:"
    );

    console.log(
      "  DETERMINISTIC_ENGINE"
    );

    console.log();

    console.log(
      "Settlement recommendation:"
    );

    console.log(
      "  NOT_PERFORMED"
    );

    console.log();

    console.log(
      "Mining agent status: SUCCESS"
    );

  } catch (error) {

    console.error();

    console.error(
      "Mining agent status: FAILED"
    );

    console.error(
      error instanceof Error
        ? error.message
        : error
    );

    process.exit(1);
  }
}


main();
