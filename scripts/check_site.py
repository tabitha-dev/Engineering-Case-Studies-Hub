#!/usr/bin/env python3
"""Static SEO, AI-discoverability and accessibility regression checks.

This supplements, but cannot replace, browser-based WCAG, keyboard,
screen-reader and performance audits.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HOME = "https://tabitha-dev.github.io/Engineering-Case-Studies-Hub/"
ERRORS = []


def check(condition, label):
    print(("PASS" if condition else "FAIL") + "  " + label)
    if not condition:
        ERRORS.append(label)


class PageMeta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas = {}
        self.links = []
        self.h1_count = 0
        self.lang = None
        self.has_main = False
        self.has_skip = False
        self.title_count = 0
        self.in_title = False
        self.title_text = ""

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.lang = d.get("lang")
        if tag == "meta":
            self.metas[d.get("name") or d.get("property")] = d.get("content")
        if tag == "link":
            self.links.append(d)
        if tag == "h1":
            self.h1_count += 1
        if tag == "main" and d.get("id") == "main-content":
            self.has_main = True
        if tag == "a" and d.get("class") == "skip-to-main" and d.get("href") == "#main-content":
            self.has_skip = True
        if tag == "title":
            self.in_title = True
            self.title_count += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data


html = (ROOT / "index.html").read_text(encoding="utf-8")
page = PageMeta()
page.feed(html)
check(page.lang == "en", "HTML language")
check(page.title_count == 1 and "Engineering Case Studies" in page.title_text, "Descriptive page title")
check(len(page.metas.get("description", "")) >= 90, "Meaningful description")
check(page.metas.get("robots", "").startswith("index, follow"), "Indexing directives")
check(any(x.get("rel") == "canonical" and x.get("href") == HOME for x in page.links), "Canonical URL")
check(page.metas.get("og:url") == HOME and page.metas.get("og:image", "").startswith("https://"), "Open Graph URL and image")
check(page.metas.get("twitter:card") == "summary_large_image" and bool(page.metas.get("twitter:image:alt")), "Social cards and image alt")
check(page.has_skip and page.has_main and page.h1_count == 1, "Skip link, main landmark, one static heading")

logo = ROOT / "assets" / "tk-monogram.svg"
check(logo.exists() and '<svg' in logo.read_text(encoding="utf-8") and "TK monogram" in logo.read_text(encoding="utf-8"), "Shared TK logo exists")
check(html.count("assets/tk-monogram.svg") >= 5 and 'rel="icon" type="image/svg+xml"' in html, "Header, footer, fallback, favicon and metadata use shared TK")

matches = re.findall(r'<script type="application/ld\\+json">([\\s\\S]*?)</script>', html)
try:
    data = json.loads(matches[0]) if matches else None
except json.JSONDecodeError:
    data = None
graph = data.get("@graph", []) if isinstance(data, dict) else []
kinds = {item.get("@type") for item in graph}
check({"CollectionPage", "Person", "ItemList", "WebSite", "BreadcrumbList"}.issubset(kinds), "Structured content, owner and breadcrumbs")
lists = [node for node in graph if node.get("@type") == "ItemList"]
positions = [i.get("position") for i in lists[0].get("itemListElement", [])] if lists else []
check(positions == list(range(1, 17)), "16 ordered machine-readable cases")
check(html.count("<article><h3>") == 16, "16 crawlable static project summaries")
check('role="dialog"' in html and 'aria-modal="true"' in html and 'aria-describedby=' in html, "Named descriptive case-study dialog")
check('const trapFocus = (event) =>' in html and 'lastCaseTriggerRef.current.focus' in html, "Focus trap and return-to-card logic")
check('aria-haspopup="dialog"' in html and 'onKeyDown={(e)' in html, "Keyboard-operable project cards")
check('aria-live="polite"' in html and 'aria-pressed={activeCategory === cat}' in html, "Accessible filter status and state")
check('prefers-reduced-motion: reduce' in html and 'aria-hidden="true"' in html, "Motion reduction and decorative content")
check('aria-label="Social and contact links"' in html and 'aria-label="Email Tabitha Khadse"' in html, "Labeled contact navigation")

for fn in ("portfolio.md", "llms.txt", "sitemap.xml"):
    check((ROOT / fn).is_file(), f"{fn} exists")
try:
    tree = ET.parse(ROOT / "sitemap.xml")
    urls = {node.text for node in tree.iter() if node.tag.endswith("loc")}
except ET.ParseError:
    urls = set()
check(HOME in urls and HOME + "portfolio.md" in urls, "Valid index sitemap")
for bad in ("https://tabitha-dev.github.io/portfolio/", "Tabitha_Khadse_Resume_2026.pdf", "tabitha@ieee.org", 'HIPAA Compliance", value: "100%"'):
    check(bad not in html, f"No outdated reference: {bad}")
check('https://code.tabitha.dev/Tabitha_Khadse_Frontend_Engineer_Resume.pdf' in html, "Current resume link")
print(f"\\n{len(ERRORS)} failure(s) across site regression checks.")
sys.exit(1 if ERRORS else 0)
