import urllib.request, ssl, sys, os
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\ssl_test.log", "w", encoding="utf-8")
print("SSL_CERT_FILE", os.environ.get("SSL_CERT_FILE"), "REQUESTS_CA_BUNDLE", os.environ.get("REQUESTS_CA_BUNDLE"), "HTTPS_PROXY", os.environ.get("HTTPS_PROXY"), file=out)
print("varsayilan", ssl.get_default_verify_paths(), file=out)
for u in ["https://api.github.com", "https://www.sqlite.org", "https://openrouter.ai/api/v1/models", "https://api.groq.com", "https://pypi.org/simple/"]:
    try:
        r = urllib.request.urlopen(u, timeout=20); print("OK", r.status, u, file=out)
    except Exception as e:
        print("HATA", u, repr(e)[:180], file=out)
try:
    import certifi; print("certifi", certifi.where(), file=out)
except Exception as e: print("certifi yok", e, file=out)
out.close()
