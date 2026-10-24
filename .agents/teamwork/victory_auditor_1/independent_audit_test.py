#!/usr/bin/env python3
"""
Independent Victory Auditor Verification Test
Independently verifies 14 project pages, images, semantic structure,
and live HTTP server responses with zero shared code.
"""

import os
import sys
import glob
import re
import time
import threading
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

root = Path("/Users/sooyeol/Desktop/Code/ws_noah").resolve()
errors = []

print("=== [AUDITOR INDEPENDENT TEST START] ===")

# 1. 14 Project HTML files check
html_files = sorted(glob.glob(str(root / "projects" / "*.html")))
if len(html_files) != 14:
    errors.append(f"Expected 14 HTML files in projects/, found {len(html_files)}")
else:
    print(f"[PASS] Found exactly 14 project HTML files.")

SECTIONS = [
    r"1\.\s*하는\s*일",
    r"2\.\s*해결한\s*문제",
    r"3\.\s*시스템\s*아키텍처",
    r"4\.\s*핵심\s*구현\s*기능",
    r"5\.\s*엔지니어링\s*교훈"
]

all_img_urls = []

for hf in html_files:
    fname = os.path.basename(hf)
    with open(hf, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Check file size
    sz = len(html.encode("utf-8"))
    if sz < 8000:
        errors.append(f"{fname}: File size too small ({sz} bytes)")
    
    # Check 5 sections
    for sec_pattern in SECTIONS:
        if not re.search(sec_pattern, html):
            errors.append(f"{fname}: Missing section matching {sec_pattern}")
            
    # Check figure and figcaption (except boothy which has no images)
    if fname != "boothy-photo-booth.html":
        if "<figure" not in html or "<figcaption" not in html:
            errors.append(f"{fname}: Missing <figure> or <figcaption>")
            
    # Check blockquote
    if "<blockquote" not in html:
        errors.append(f"{fname}: Missing <blockquote>")
        
    # Check links
    if "../style.css" not in html:
        errors.append(f"{fname}: Missing ../style.css link")
    if "../theme.js" not in html:
        errors.append(f"{fname}: Missing ../theme.js script")
        
    # Extract images
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    for src in imgs:
        if src.startswith("../"):
            img_path = (Path(hf).parent / src).resolve()
            if not img_path.exists():
                errors.append(f"{fname}: Broken image path {src}")
            elif img_path.stat().st_size < 10000:
                errors.append(f"{fname}: Suspiciously small image {src} ({img_path.stat().st_size} bytes)")
            rel_to_root = img_path.relative_to(root)
            all_img_urls.append(str(rel_to_root))

print(f"[PASS] Project HTML structural analysis completed. Total image references extracted: {len(all_img_urls)}")

# 2. index.html check
with open(root / "index.html", "r", encoding="utf-8") as f:
    idx_html = f.read()

proj_links = re.findall(r'href=["\'](\./projects/[^"\']+\.html)["\']', idx_html)
if len(proj_links) != 14:
    errors.append(f"index.html: Expected 14 project links, found {len(proj_links)}")
else:
    print(f"[PASS] index.html links exactly 14 project pages.")

# 3. Live HTTP server test on independent port (38912)
class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(root), **kwargs)
    def log_message(self, format, *args):
        pass

PORT = 38912
httpd = ThreadingHTTPServer(("127.0.0.1", PORT), QuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
time.sleep(0.3)

try:
    # Test index.html
    with urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=3) as res:
        _ = res.read()
        if res.status != 200:
            errors.append(f"HTTP GET /index.html returned {res.status}")
        else:
            print("[PASS] HTTP GET /index.html -> 200 OK")

    # Test all 14 project pages
    for pl in sorted(list(set(proj_links))):
        clean_path = pl.replace("./", "")
        with urlopen(f"http://127.0.0.1:{PORT}/{clean_path}", timeout=3) as res:
            _ = res.read()
            if res.status != 200:
                errors.append(f"HTTP GET /{clean_path} returned {res.status}")
    print(f"[PASS] HTTP GET all 14 project pages -> 200 OK")

    # Test all image URLs
    unique_imgs = sorted(list(set(all_img_urls)))
    for img_rel in unique_imgs:
        with urlopen(f"http://127.0.0.1:{PORT}/{img_rel}", timeout=3) as res:
            _ = res.read()
            if res.status != 200:
                errors.append(f"HTTP GET /{img_rel} returned {res.status}")
    print(f"[PASS] HTTP GET all {len(unique_imgs)} images -> 200 OK")

    # Test negative 404 behavior
    try:
        with urlopen(f"http://127.0.0.1:{PORT}/projects/non-existent-page.html", timeout=3) as res:
            errors.append("Negative 404 test failed: non-existent page did not throw 404")
    except HTTPError as e:
        if e.code == 404:
            print("[PASS] HTTP GET non-existent page -> 404 Not Found (Negative test confirmed)")
        else:
            errors.append(f"Negative test unexpected code: {e.code}")

finally:
    httpd.shutdown()
    httpd.server_close()

print(f"\nTotal Errors Found: {len(errors)}")
if errors:
    for e in errors:
        print("  - FAIL:", e)
    sys.exit(1)
else:
    print("=== [AUDITOR INDEPENDENT TEST: 100% PASS (ALL CRITERIA VERIFIED)] ===")
    sys.exit(0)
