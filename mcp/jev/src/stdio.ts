#!/usr/bin/env node
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { sunucuYap } from "./sunucu.js";

await sunucuYap().connect(new StdioServerTransport());
