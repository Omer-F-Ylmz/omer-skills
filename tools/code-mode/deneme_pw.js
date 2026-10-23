const s = x => typeof x === "string" ? x : JSON.stringify(x);
pw.pw_browser_navigate({ url: "https://example.com" });
const snap = s(pw.pw_browser_snapshot({}));
pw.pw_browser_close({});
const baslik = (snap.match(/heading "([^"]+)"/) || [])[1];
return { snapshot_karakter: snap.length, baslik };
