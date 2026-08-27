import "dotenv/config";

const url =
  "http://13.237.89.59:7044/miner-dispatcher/v1/402/trade-context";

console.log("URL:", url);
console.log();

const response = await fetch(url, {
  method: "GET",
  headers: {
    Accept: "application/json",
  },
});

console.log("STATUS:", response.status);
console.log("STATUS TEXT:", response.statusText);
console.log();

console.log("HEADERS:");

for (const [key, value] of response.headers.entries()) {
  console.log(`${key}: ${value}`);
}

console.log();

console.log("BODY:");

console.log(await response.text());
