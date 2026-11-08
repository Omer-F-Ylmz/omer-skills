# Security Penetration Test Report

**Generated:** 2026-10-28 07:21:14 UTC

# Executive Summary

An external security assessment of the web application at `http://host.docker.internal:4180` identified two **Medium** severity vulnerabilities. The target is a static frontend demo application ("VEHİM — Safran Gece & Tuz Çiçeği") served by Python's built-in `http.server` (SimpleHTTP/0.6) on Python 3.12.10. There is no backend, database, authentication, or server-side processing — the entire application consists of static HTML, CSS, JavaScript, and vendor libraries.

**Overall risk posture: Low to Moderate** — The application itself poses minimal risk as a client-side demo with no sensitive data or business logic. However, the identified misconfigurations would be significant if this server configuration were used in a production environment.

**Key findings:**
- **Directory listings enabled** on multiple paths (`/vendor/`, `/vendor/three/`, `/vendor/gsap/`, `/vendor/lenis/`, `/js/`, `/docs/`) exposing full file tree and library versions (Three.js r170, GSAP 3.12.5, Lenis)
- **Missing security headers** (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy) with Server header disclosing Python version

No critical or high-severity vulnerabilities were found. Path traversal, SQL injection, XSS, SSRF, authentication bypass, and other common web vulnerabilities are not applicable due to the static-only nature of the application.

# Methodology

Conducted per the **OWASP Web Security Testing Guide (WSTG)** and **PTES** (Penetration Testing Execution Standard) frameworks.

**Engagement type:** Black-box external assessment (no source code provided, only URL).

**Scope:** `http://host.docker.internal:4180` — single web application endpoint.

**Activities performed:**
1. **Reconnaissance & Attack Surface Mapping**: Technology fingerprinting (Python http.server, Three.js, GSAP, Lenis), endpoint enumeration, directory listing discovery, client-side code review
2. **Static File Server Testing**: Directory listing enumeration, path traversal attempts, security header analysis, Server header disclosure
3. **Client-Side Code Review**: Analysis of `main.js` (ES Module) for DOM XSS, unsafe `innerHTML` usage, prototype pollution, and client-side logic flaws
4. **Dependency Version Analysis**: Library version identification via directory listings (Three.js r170, GSAP 3.12.5, Lenis)
5. **Vulnerability Validation**: Path traversal attempts confirmed blocked by Python's path normalization; no server-side injection vectors exist

# Technical Analysis

**Severity model** reflects exploitability × impact for this specific target (static demo application).

**Confirmed findings:**

1. **Directory Listings Enabled on Static File Server** (Medium, CVSS 5.3, CWE-548)
   - Python `http.server` serves directory indexes by default when no index file is present
   - Affected paths: `/vendor/`, `/vendor/three/`, `/vendor/gsap/`, `/vendor/lenis/`, `/js/`, `/docs/`
   - Impact: Full file tree enumeration, library version disclosure (Three.js r170, GSAP 3.12.5, Lenis), facilitates targeted CVE searches

2. **Missing Security Headers on Static File Server** (Medium, CVSS 5.3, CWE-693)
   - No security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
   - Server header discloses: `SimpleHTTP/0.6 Python/3.12.10`
   - Impact: Reduced defense-in-depth against client-side attacks, technology stack disclosure

**Ruled out / Not applicable:**
- **Path Traversal / LFI**: Python's `http.server` normalizes paths in `translate_path()` preventing directory escape — all traversal attempts returned 404
- **SQL Injection / RCE / SSRF / XXE / Deserialization**: No server-side parsers, databases, or dynamic code execution
- **Authentication / Authorization / IDOR / BFLA / CSRF / JWT**: No auth mechanisms, sessions, or user accounts exist
- **Client-side XSS**: Code review of `main.js` shows safe patterns — uses `textContent` and `dataset`, no `eval` or `innerHTML` with user input
- **Race Conditions / Business Logic Flaws**: No state-changing server operations

**Systemic themes:** Default development server configuration used in a context where production hardening would be expected; lack of defense-in-depth headers; directory indexing as default-on behavior.

# Recommendations

**Immediate**
1. **Disable directory listings** — Subclass `SimpleHTTPRequestHandler` and override `list_directory()` to return 403/404, or add `index.html` files to all directories, or deploy behind a production web server (nginx, Apache) with `autoindex off`
2. **Add security headers** — Implement via custom handler `end_headers()` override, reverse proxy, or production web server. Minimum: `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`

**Short-term**
3. **Replace Python http.server with production web server** — Python's `http.server` is explicitly documented as not for production use. Use nginx, Apache, Caddy, or a proper static hosting service
4. **Monitor vendor library CVEs** — Three.js r170, GSAP 3.12.5, Lenis — subscribe to security advisories and update regularly
5. **Consider Subresource Integrity (SRI)** — Add integrity hashes for vendor libraries if served from external sources (currently served locally)

**Medium-term**
6. **Implement CSP** — Define a strict Content Security Policy appropriate for the application (no inline scripts, restricted font/image sources)
7. **Remove Server header** — Configure web server to hide version information (`ServerTokens Prod` in Apache, `server_tokens off` in nginx)

**Retest & validation guidance:** Re-test immediate items to confirm directory listings return 403/404 and security headers are present in all responses. Verify path traversal remains blocked.

