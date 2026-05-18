#!/usr/bin/env python3
"""
BuyerFinder v2 — PropPilot Buyer Discovery Engine
Powered by CloakBrowser — invisible to all bot detection.

Sources:
  - Facebook Groups (public posts, no login needed)
  - BiggerPockets member search
  - Local REIA directories
  - Facebook Marketplace (investor activity)

Install deps first:
  pip install cloakbrowser requests
"""

import os
import re
import json
import logging
import time
from datetime import datetime
from pathlib import Path

BASE_DIR   = Path(__file__).parent.resolve()
LOGS_DIR   = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
DB_FILE    = LOGS_DIR / "buyer_database.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [BUYER-v2] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "buyer_finder_v2.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("BuyerFinderV2")

# ── TARGET FACEBOOK GROUPS (public — no login required) ──────────────────────
FACEBOOK_GROUPS = [
    {
        "name":   "Fort Myers Real Estate Investors",
        "url":    "https://www.facebook.com/groups/fortsyersrealestateinvestors",
        "market": "Fort Myers FL",
    },
    {
        "name":   "SW Florida Wholesale Real Estate",
        "url":    "https://www.facebook.com/groups/swflwholesale",
        "market": "Fort Myers FL",
    },
    {
        "name":   "Lee County Real Estate Investors",
        "url":    "https://www.facebook.com/groups/leecountyrealestate",
        "market": "Fort Myers FL",
    },
    {
        "name":   "Cape Coral Real Estate Investors",
        "url":    "https://www.facebook.com/groups/capecoralhomes",
        "market": "Cape Coral FL",
    },
    {
        "name":   "We Buy Houses Florida",
        "url":    "https://www.facebook.com/groups/webuyhousesflorida",
        "market": "Florida",
    },
    {
        "name":   "Florida Wholesale Real Estate",
        "url":    "https://www.facebook.com/groups/floridawholesalerealestate",
        "market": "Florida",
    },
]

# ── KEYWORDS that signal a buyer ─────────────────────────────────────────────
BUYER_KEYWORDS = [
    "looking to buy", "cash buyer", "investor", "we buy",
    "looking for deals", "buying in", "interested in properties",
    "cash offer", "buy and hold", "fix and flip", "wholesaler",
    "looking for off-market", "buy houses", "buying homes",
]

# ── DATABASE ──────────────────────────────────────────────────────────────────
def load_db():
    if DB_FILE.exists():
        with open(DB_FILE) as f:
            return json.load(f)
    return {"buyers": [], "scraped_groups": []}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def already_in_db(name, db):
    return any(b.get("name","").lower() == name.lower() for b in db["buyers"])


# ── CLOAKBROWSER FACEBOOK SCRAPER ─────────────────────────────────────────────
class FacebookBuyerScraper:
    """
    Uses CloakBrowser to hit Facebook public groups without login.
    Extracts posts from people identifying themselves as buyers/investors.
    """

    def __init__(self):
        try:
            from cloakbrowser import launch
            self.browser = launch(humanize=True)
            log.info("✅ CloakBrowser launched — Ghost Mode active")
            self.available = True
        except ImportError:
            log.warning("⚠️ CloakBrowser not installed. Run: pip install cloakbrowser")
            self.browser = None
            self.available = False

    def scrape_group(self, group: dict, max_posts: int = 30) -> list:
        """Scrape public posts from a Facebook group."""
        if not self.available:
            log.warning("CloakBrowser not available — skipping Facebook scrape")
            return []

        buyers = []
        page = self.browser.new_page()

        try:
            log.info(f"Scraping: {group['name']}")
            page.goto(group["url"], timeout=30000)
            time.sleep(3)

            # Scroll to load posts
            for _ in range(5):
                page.evaluate("window.scrollBy(0, 1500)")
                time.sleep(1.5)

            # Get all text content
            content = page.inner_text("body")
            lines = content.split("\n")

            current_name = None
            for i, line in enumerate(lines):
                line_clean = line.strip()
                if not line_clean:
                    continue

                # Check if this line contains buyer keywords
                if any(kw.lower() in line_clean.lower() for kw in BUYER_KEYWORDS):
                    # Look back a few lines for a name
                    context = "\n".join(lines[max(0, i-5):i+3])

                    # Extract potential names (capitalized words)
                    names = re.findall(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b', context)
                    if names:
                        name = names[0]
                        if not already_in_db(name, load_db()):
                            buyers.append({
                                "name":       name,
                                "market":     group["market"],
                                "source":     f"Facebook: {group['name']}",
                                "group_url":  group["url"],
                                "signal":     line_clean[:120],
                                "found_at":   datetime.now().isoformat(),
                                "contact":    "Facebook DM via group",
                                "status":     "new",
                            })
                            log.info(f"  🎯 Buyer signal: {name} — '{line_clean[:60]}...'")

                if len(buyers) >= max_posts:
                    break

        except Exception as e:
            log.error(f"Scrape failed for {group['name']}: {e}")
        finally:
            page.close()

        return buyers

    def close(self):
        if self.browser:
            self.browser.close()


# ── FACEBOOK SEARCH SCRAPER (no group join needed) ────────────────────────────
class FacebookSearchScraper:
    """
    Uses CloakBrowser to search Facebook for investor posts publicly.
    Searches: 'cash buyer Fort Myers', 'buy houses Lee County', etc.
    """

    SEARCH_QUERIES = [
        "cash buyer Fort Myers FL",
        "real estate investor Fort Myers",
        "buy houses Lee County Florida",
        "fix and flip Fort Myers",
        "wholesale deals Fort Myers",
        "cash offer Cape Coral",
    ]

    def __init__(self, browser):
        self.browser = browser

    def search(self) -> list:
        if not self.browser:
            return []

        buyers = []
        page = self.browser.new_page()

        for query in self.SEARCH_QUERIES:
            try:
                search_url = f"https://www.facebook.com/search/posts?q={query.replace(' ', '%20')}"
                log.info(f"Searching: {query}")
                page.goto(search_url, timeout=30000)
                time.sleep(3)

                for _ in range(3):
                    page.evaluate("window.scrollBy(0, 1500)")
                    time.sleep(1.5)

                content = page.inner_text("body")
                lines = content.split("\n")

                for i, line in enumerate(lines):
                    line_clean = line.strip()
                    if any(kw.lower() in line_clean.lower() for kw in BUYER_KEYWORDS):
                        context = "\n".join(lines[max(0,i-3):i+3])
                        names = re.findall(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b', context)
                        if names:
                            name = names[0]
                            db = load_db()
                            if not already_in_db(name, db):
                                buyers.append({
                                    "name":     name,
                                    "market":   "Fort Myers FL",
                                    "source":   f"Facebook Search: {query}",
                                    "signal":   line_clean[:120],
                                    "found_at": datetime.now().isoformat(),
                                    "contact":  "Facebook DM",
                                    "status":   "new",
                                })
                                log.info(f"  🎯 {name} — via search: {query}")

            except Exception as e:
                log.error(f"Search failed for '{query}': {e}")
            finally:
                time.sleep(2)

        page.close()
        return buyers


# ── REPORT ────────────────────────────────────────────────────────────────────
def print_report(db):
    buyers = db["buyers"]
    new    = [b for b in buyers if b.get("status") == "new"]
    fb     = [b for b in buyers if "Facebook" in b.get("source","")]
    total  = len(buyers)

    print("\n" + "═"*52)
    print("   🔱 PROPPILOT BUYER DATABASE — REPORT")
    print("═"*52)
    print(f"   Total Buyers:        {total}")
    print(f"   New (uncontacted):   {len(new)}")
    print(f"   From Facebook:       {len(fb)}")
    print("═"*52)
    if new:
        print("\n   🎯 NEW BUYERS TO CONTACT:")
        for b in new[:10]:
            print(f"   → {b['name']:<25} | {b['market']:<20} | {b['source'][:30]}")
    print("═"*52 + "\n")


# ── MAIN ──────────────────────────────────────────────────────────────────────
class BuyerFinderV2:
    def __init__(self):
        self.fb_scraper = FacebookBuyerScraper()
        self.search_scraper = FacebookSearchScraper(
            self.fb_scraper.browser if self.fb_scraper.available else None
        )

    def run(self, groups: list = None, search: bool = True):
        db = load_db()
        all_new = []

        # 1. Scrape target groups
        target_groups = groups or FACEBOOK_GROUPS
        for group in target_groups:
            buyers = self.fb_scraper.scrape_group(group)
            all_new.extend(buyers)
            time.sleep(2)  # polite delay between groups

        # 2. Search scraper
        if search:
            search_buyers = self.search_scraper.search()
            all_new.extend(search_buyers)

        # 3. Deduplicate and save
        for buyer in all_new:
            if not already_in_db(buyer["name"], db):
                db["buyers"].append(buyer)

        db["last_run"] = datetime.now().isoformat()
        save_db(db)

        log.info(f"✅ Scan complete — {len(all_new)} new buyers found")
        print_report(db)

        self.fb_scraper.close()
        return len(all_new)

    def mark_contacted(self, name: str):
        db = load_db()
        for b in db["buyers"]:
            if b["name"].lower() == name.lower():
                b["status"] = "contacted"
                b["contacted_at"] = datetime.now().isoformat()
        save_db(db)
        log.info(f"✅ Marked {name} as contacted")

    def show_db(self):
        db = load_db()
        print_report(db)


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    finder = BuyerFinderV2()

    if "--show" in sys.argv:
        finder.show_db()
    elif "--contacted" in sys.argv:
        idx = sys.argv.index("--contacted")
        name = sys.argv[idx+1] if len(sys.argv) > idx+1 else ""
        if name:
            finder.mark_contacted(name)
    else:
        count = finder.run()
        print(f"\n🔱 BuyerFinder v2: {count} new buyers added to database.")
