
import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const PROVIDER_URL = (
  process.env.BRICS_PROVIDER_URL || "http://127.0.0.1:8091"
).replace(/\/$/, "");

const TIMEOUT_MS = 10000;

async function getJson(path: string): Promise<unknown> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const response = await fetch(`${PROVIDER_URL}${path}`, {
      method: "GET",
      signal: controller.signal,
    });

    const text = await response.text();

    if (!response.ok) {
      throw new Error(`Provider returned HTTP ${response.status}: ${text}`);
    }

    try {
      return JSON.parse(text) as unknown;
    } catch {
      throw new Error("Provider returned invalid JSON");
    }
  } finally {
    clearTimeout(timeout);
  }
}

function success(data: unknown) {
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(data, null, 2),
      },
    ],
  };
}

function failure(error: unknown) {
  const message =
    error instanceof Error ? error.message : String(error);

  return {
    content: [
      {
        type: "text" as const,
        text: `BRICS provider error: ${message}`,
      },
    ],
    isError: true,
  };
}

export function registerBricsTools(server: McpServer): void {
  server.registerTool(
    "tg_brics_health",
    {
      description:
        "Check the health and record counts of the local BRICS data catalogue. Read-only; no payment required.",
      inputSchema: z.object({}),
      annotations: { readOnlyHint: true, openWorldHint: false },
    },
    async () => {
      try {
        return success(await getJson("/health"));
      } catch (error) {
        return failure(error);
      }
    }
  );

  server.registerTool(
    "tg_brics_search",
    {
      description:
        "Search the local BRICS data catalogue using text, pagination, and exact filters. Supported filters: intent, category, scenario, source_country, destination_country, boundary_mode, source_file, dataset, source_role, original_id.",
      inputSchema: z.object({
        q: z.string().optional(),
        limit: z.number().int().min(1).max(100).default(20),
        offset: z.number().int().min(0).default(0),
        intent: z.string().optional(),
        category: z.string().optional(),
        scenario: z.string().optional(),
        source_country: z.string().optional(),
        destination_country: z.string().optional(),
        boundary_mode: z.string().optional(),
        source_file: z.string().optional(),
        dataset: z.string().optional(),
        source_role: z.string().optional(),
        original_id: z.string().optional(),
      }),
      annotations: { readOnlyHint: true, openWorldHint: false },
    },
    async (args) => {
      try {
        const params = new URLSearchParams();

        for (const [key, value] of Object.entries(args)) {
          if (value !== undefined && value !== "") {
            params.set(key, String(value));
          }
        }

        return success(
          await getJson(`/records?${params.toString()}`)
        );
      } catch (error) {
        return failure(error);
      }
    }
  );

  server.registerTool(
    "tg_brics_get_record",
    {
      description:
        "Retrieve a catalogue record by catalogue ID or original ID. Duplicate original IDs return all matching records. Read-only; no payment required.",
      inputSchema: z.object({
        id: z.string().min(1).max(256),
      }),
      annotations: { readOnlyHint: true, openWorldHint: false },
    },
    async ({ id }) => {
      try {
        return success(
          await getJson(`/records/${encodeURIComponent(id)}`)
        );
      } catch (error) {
        return failure(error);
      }
    }
  );
}
