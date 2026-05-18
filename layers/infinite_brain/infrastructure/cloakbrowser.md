# CloakBrowser — ScoutPrime Stealth Engine

## What It Is
Stealth Chromium that passes every bot detection test.
NOT a config patch or JS injection — 57 C++ source-level patches compiled into the binary.
Drop-in Playwright/Puppeteer replacement. Same API, 3-line swap.

- **Repo:** https://github.com/CloakHQ/CloakBrowser
- **Stars:** 13.8K | **Forks:** 1.1K
- **Status:** Actively maintained — last commit today (2026-05-17)
- **Version:** v0.3.28 (Chromium 146.0.7680.177.4)

## Install
```bash
pip install cloakbrowser        # Python
npm install cloakbrowser        # Node.js
```
Binary (~200MB) auto-downloads on first run.

## Quick Start
```python
from cloakbrowser import launch

browser = launch(humanize=True)   # humanize=True = human mouse/keyboard behavior
page = browser.new_page()
page.goto("https://protected-site.com")
browser.close()
```

## Bot Detection Results (30/30 tests)
| Test | Result |
|---|---|
| reCAPTCHA v3 score | **0.9** (human-level) |
| Cloudflare Turnstile | **PASS** |
| FingerprintJS | **PASS** |
| BrowserScan | **NORMAL (4/4)** |
| navigator.webdriver | **false** |
| CDP detection | **Not detected** |

## Key Features
- **57 C++ patches** — canvas, WebGL, audio, fonts, GPU, WebRTC, CDP, screen, timing
- **humanize=True** — Bézier mouse curves, per-character typing, realistic scroll
- **Persistent profiles** — cookies/localStorage survive restarts, avoids incognito detection
- **SOCKS5 proxy support** — native, not Playwright wrapper
- **GeoIP auto-detect** — matches timezone/locale to proxy exit IP
- **Fixed fingerprint seed** — same seed = same identity across sessions (for returning visitor behavior)
- **MCP server available** — `pip install cloakbrowsermcp` (v2.0.4)

## Pantheon Use Cases
- **ScoutPrime** — scrape tax deed / foreclosure / realtor sites without blocks
- **ZeusPrime** — market research on Polymarket, prediction sites
- **OrionPrime** — GSA fleet, property databases, auction sites
- **PropPilot** — lead scraping, competitor research
- **Any site using Cloudflare/reCAPTCHA** — solved

## Termux Compatibility
- pip install works in Termux (DexClaw proot Linux)
- Binary is ~200MB — ensure storage space before install
- `python -m cloakbrowser install` to pre-download

## Comparison
| Tool | reCAPTCHA v3 | Cloudflare | Patch Level |
|---|---|---|---|
| playwright-stealth | 0.3-0.5 | Sometimes | JS injection |
| undetected-chromedriver | 0.3-0.7 | Sometimes | Config patches |
| Camoufox | 0.7-0.9 | Pass | C++ (Firefox) |
| **CloakBrowser** | **0.9** | **Pass** | **C++ (Chromium)** |

## Notes
- Does NOT solve CAPTCHAs — it PREVENTS them from appearing
- Bring your own proxies
- Use fixed `--fingerprint=seed` when hitting the same site repeatedly
- MCP integration: `pip install cloakbrowsermcp` — ZapiaPrime can call it as a tool
