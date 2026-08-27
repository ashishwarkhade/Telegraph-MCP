/**
 * Phase 10.2
 * Telegraph Test Mining Agent
 *
 * Purpose:
 *     Provide a small deterministic mining-agent prototype
 *     for testing Telegraph miner/evaluation behavior.
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
 *     It exists only to retrieve intelligence.
 */

import "dotenv/config";

import { loadConfig } from "./src/config.js";
import { createPaymentAwareFetch } from "./src/x402.js";
import { callSubnet } from "./src/client.js";


// ============================================================
// CONFIGURATION
// ============================================================

const SUBNET_ID = "402";


// ============================================================
// MINING FUNCTIONS
// ============================================================

async function mineTradeContext(
  fetchWithPayment: ReturnType<
    typeof createPaymentAwareFetch
  > extends Promise<infer T>
    ? T
    : never,
  nodeUrl: string
) {

  return callSubnet(
    fetchWithPayment,
    nodeUrl,
    SUBNET_ID,
    {
      path: "/trade-context",
      method: "GET",
    },
    {}
  );
}


// ============================================================
// MAIN TEST
// ============================================================

async function main() {

  console.log();
  console.log("=== TELEGRAPH TEST MINING AGENT ===");
  console.log();

  const config = loadConfig();

  console.log(`Node: ${config.nodeUrl}`);
  console.log(`Subnet: ${SUBNET_ID}`);
  console.log();

  console.log(
    "Creating x402 payment-aware client..."
  );

  const fetchWithPayment =
    await createPaymentAwareFetch(config);

  console.log();

  console.log(
    "Mining trade context..."
  );

  console.log();

  const result = await mineTradeContext(
    fetchWithPayment,
    config.nodeUrl
  );

  console.log(
    JSON.stringify(
      result,
      null,
      2
    )
  );

  console.log();

  console.log(
    "Mining agent status: SUCCESS"
  );

  console.log();

  console.log(
    "Telegraph authority: INTELLIGENCE_ONLY"
  );

  console.log(
    "Settlement authority: DETERMINISTIC_ENGINE"
  );

  console.log(
    "Settlement recommendation: NOT_PERFORMED"
  );
}


// ============================================================
// ERROR HANDLING
// ============================================================

main().catch((err: unknown) => {

  console.error();

  console.error(
    "Mining agent status: FAILED"
  );

  if (err instanceof Error) {

    console.error(
      `Error: ${err.message}`
    );

  } else {

    console.error(
      `Error: ${String(err)}`
    );
  }

  process.exit(1);
});
