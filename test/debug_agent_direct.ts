import "dotenv/config";

import { loadConfig } from "../src/config.js";
import { createPaymentAwareFetch } from "../src/x402.js";

const SUBNET_ID = "402";

async function main() {
  console.log();
  console.log("=== AGENT DIRECT X402 DEBUG ===");
  console.log();

  const config = loadConfig();

  console.log(`Node: ${config.nodeUrl}`);
  console.log(`Subnet: ${SUBNET_ID}`);
  console.log();

  const fetchWithPayment = await createPaymentAwareFetch(config);

  const url =
    `${config.nodeUrl}/miner-dispatcher/v1/${SUBNET_ID}/trade-context`;

  console.log("Calling:");
  console.log(url);
  console.log();

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);

  try {
    const res = await fetchWithPayment(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal: controller.signal,
    });

    console.log("FINAL STATUS:", res.status);
    console.log("STATUS TEXT:", res.statusText);
    console.log();

    console.log("BODY:");
    console.log(await res.text());
  } finally {
    clearTimeout(timeout);
  }
}

main().catch((err) => {
  console.error();
  console.error("AGENT DIRECT X402 DEBUG FAILED");
  console.error(err);
  process.exit(1);
});
