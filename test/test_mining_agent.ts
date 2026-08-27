import "dotenv/config";

import { loadConfig } from "../src/config.js";
import { createPaymentAwareFetch } from "../src/x402.js";
import { callSubnet } from "../src/client.js";

async function main() {
  console.log();
  console.log("=== TELEGRAPH TEST MINING AGENT ===");
  console.log();

  const config = loadConfig();

  console.log(`Node: ${config.nodeUrl}`);
  console.log("Subnet: 402");
  console.log();

  const paidFetch =
  await createPaymentAwareFetch(config);

  const fetchWithPayment = async (
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<Response> => {

  const response = await paidFetch(input, init);

  console.log();
  console.log("=== X402 FINAL RESPONSE ===");
  console.log("HTTP status:", response.status);
  console.log(
    "PAYMENT-RESPONSE:",
    response.headers.get("PAYMENT-RESPONSE")
  );
  console.log(
    "X-PAYMENT-RESPONSE:",
    response.headers.get("X-PAYMENT-RESPONSE")
  );
  console.log("===========================");
  console.log();

  return response;
};
   

  console.log("Mining trade context...");
  console.log();

  const endpoint = {
    path: "/trade-context",
    method: "GET",
  };

  const result = await callSubnet(
    fetchWithPayment,
    config.nodeUrl,
    "402",
    endpoint,
    {}
  );

  console.log(
    JSON.stringify(result, null, 2)
  );

  console.log();
  console.log("Mining agent status: SUCCESS");
}

main().catch((err) => {
  console.error();
  console.error("Mining agent status: FAILED");
  console.error(err.message || err);
  process.exit(1);
});
