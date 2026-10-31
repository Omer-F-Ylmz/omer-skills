import os, sys, time
os.chdir(sys.argv[1])
from rlcd import DecisionEngine, Choice, Option
t = time.time()
engine = DecisionEngine()
print("yukleme sn", round(time.time() - t, 1))
q = Choice(id="tur", question="Bu video hangi tür araç anlatıyor?", options=[
    Option(id="mcp", description="An MCP server that gives Claude new tools"),
    Option(id="skill", description="A Claude Code skill (SKILL.md instructions)"),
    Option(id="app", description="A standalone desktop or web application"),
])
for ctx in ["Install this MCP server and Claude can query your Postgres database directly.",
            "Drop this SKILL.md into ~/.claude/skills and Claude writes better landing pages.",
            "Download the Mac app, open it, and edit your videos with AI."]:
    t = time.time()
    r = engine.evaluate(context=ctx, queries=[q]).results[0]
    print({k: v for k, v in r.model_dump().items() if not isinstance(v, (list, dict))}, f"{(time.time()-t)*1000:.0f}ms")
