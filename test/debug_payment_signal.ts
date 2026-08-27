import "dotenv/config";

import { loadConfig } from "../src/config.js";
import { createPaymentAwareFetch } from "../src/x402.js";

async function main() {
  const config = loadConfig();

  console.log("=== X402 PAYMENT DEBUG ===");
  console.log(`Node: ${config.nodeUrl}`);
  console.log(`Network: ${config.evmNetwork}`);
  console.log();

  const fetchWithPayment =
    await createPaymentAwareFetch(config);

  const url =
    `${config.nodeUrl}/miner-dispatcher/v1/402/trade-context`;

  console.log("Calling:");
  console.log(url);
  console.log();

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);

  const response = await fetchWithPayment(url, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    signal: controller.signal,
  });

  clearTimeout(timeout);

  console.log("FINAL STATUS:", response.status);
  console.log("STATUS TEXT:", response.statusText);
  console.log();

  console.log("HEADERS:");

  for (const [key, value] of response.headers.entries()) {
    console.log(`${key}: ${value}`);
  }

  console.log();

  console.log("BODY:");

  console.log(await response.text());
}

main().catch((err) => {
  console.error();
  console.error("X402 DEBUG FAILED");
  console.error(err);
  process.exit(1);
});
