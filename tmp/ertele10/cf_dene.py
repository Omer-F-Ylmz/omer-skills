import json, os, urllib.request
u = f"https://api.cloudflare.com/client/v4/accounts/{os.environ['CLOUDFLARE_ACCOUNT_ID']}/ai/run/@cf/baai/bge-m3"
r = urllib.request.Request(u, data=json.dumps({"text": ["reklam bütçesi denetimi", "audit ad budget"]}).encode(),
    headers={"Authorization": "Bearer " + os.environ["CLOUDFLARE_API_KEY"], "Content-Type": "application/json"})
j = json.load(urllib.request.urlopen(r, timeout=60))
print(j["success"], list(j["result"].keys()), len(j["result"]["data"]), len(j["result"]["data"][0]))
import numpy as np; a, b = np.array(j["result"]["data"]); print(a @ b / np.linalg.norm(a) / np.linalg.norm(b))
