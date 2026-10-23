# claude-infinite-memory (DaWTq7aKSKq)

**Amaç:** Give Claude infinite persistent memory using NotebookLM and MCP server
**Araçlar:** Claude, NotebookLM, notebooklm-mcp server

**Adımlar**
1. [] Go to notebooklm.google.com and create a free notebook called Claude Memory
2. [] Connect Claude to NotebookLM with the free notebooklm-mcp server, one command in your terminal
3. [] Add the wrap-up skill so every session gets saved into your notebook when you’re done
4. [] Drop the routing rule into your CLAUDE.md so Claude checks the notebook before anything else
5. [] Next session, Claude pulls exactly what it needs with semantic search instead of reloading everything

**Prompt/kod/ayar:** notebooklm-mcp server
**Sonuç:** Persistent memory across every session with lower token costs
**Bizde (öneri, modelden):** kurulu araçlarla nasıl
**Daha iyi (öneri):** 
