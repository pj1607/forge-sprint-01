"""
detector.py — deterministic SEO issue detection from a Screaming Frog internal_all.csv.

STARTER IMPLEMENTATION. It already detects several issues so the pipeline runs end to
end. Your job in the Sprint is to COMPLETE the rulebook (see rulebook.md): add the
missing detectors, handle edge cases, and improve accuracy against the hidden export.

Standard library only (csv). Detection is plain Python on purpose — the model is for
judgment (rewriting titles, choosing redirect targets), not for counting rows.
"""

from __future__ import annotations
import csv
import os
from collections import defaultdict


def load_rows(export_dir: str) -> list[dict]:
    path = os.path.join(export_dir, "internal_all.csv")
    with open(path, encoding="utf-8-sig", newline="") as f:
        lines = f.readlines()
    if not lines:
        return []

    header = lines[0]
    first_quote = header.find('"')
    if first_quote != -1:
        lines[0] = header[first_quote:]

    reader = csv.DictReader(lines)
    rows = []
    for row in reader:
        sanitized_row = {}
        for k, v in row.items():
            if k is None: continue
            clean_k = k.strip()

            # Map using exact matches or most specific patterns first
            if clean_k == "Address": sanitized_row["Address"] = v
            elif "Title 1 Pixel Width" in clean_k: sanitized_row["Title 1 Pixel Width"] = v
            elif "Title 1 Length" in clean_k: sanitized_row["Title 1 Length"] = v
            elif "Title 1" in clean_k: sanitized_row["Title 1"] = v
            elif "Meta Description 1 Length" in clean_k: sanitized_row["Meta Description 1 Length"] = v
            elif "Meta Description 1 Pixel Width" in clean_k: sanitized_row["Meta Description 1 Pixel Width"] = v
            elif "Meta Description 1" in clean_k: sanitized_row["Meta Description 1"] = v
            elif "Content Type" in clean_k: sanitized_row["Content Type"] = v
            elif "Status Code" in clean_k: sanitized_row["Status Code"] = v
            elif "Indexability Status" in clean_k: pass # ignore
            elif "Indexability" in clean_k: sanitized_row["Indexability"] = v
            elif "H1-1" in clean_k: sanitized_row["H1-1"] = v
            elif "H1-2" in clean_k: sanitized_row["H1-2"] = v
            elif "Canonical Link Element 1" in clean_k or "Canonical URL" in clean_k: sanitized_row["Canonical Link Element 1"] = v
            elif "Word Count" in clean_k: sanitized_row["Word Count"] = v
            elif "Inlinks" in clean_k: sanitized_row["Inlinks"] = v
            elif "Response Time" in clean_k: sanitized_row["Response Time"] = v
            elif "Redirect URL" in clean_k: sanitized_row["Redirect URL"] = v
            else:
                sanitized_row[clean_k] = v
        rows.append(sanitized_row)
    return rows


def _int(v, default=0):
    try:
        return int(float(str(v).strip()))
    except Exception:
        return default


def _float(v, default=0.0):
    try:
        return float(str(v).strip())
    except Exception:
        return default


def is_html(r):  return "text/html" in (r.get("Content Type", "") or "").lower()
def is_200(r):   return _int(r.get("Status Code")) == 200
def indexable(r): return (r.get("Indexability", "") or "").strip().lower() == "indexable"


def detect(rows: list[dict]) -> list[dict]:
    """Return a list of issue dicts: {type, severity, affected_urls, count, explanation}.
    STARTER set — extend to the full rulebook for a high score."""
    # Filter out rows missing Address
    rows = [r for r in rows if r.get("Address")]
    issues = []

    def add(t, sev, urls, explanation):
        urls = sorted(set(urls))
        if urls:
            issues.append({"type": t, "severity": sev, "affected_urls": urls,
                           "count": len(urls), "explanation": explanation})

    html = [r for r in rows if is_html(r)]
    idx200 = [r for r in html if is_200(r) and indexable(r)]



    # --- Titles ---
    add("missing_title", "High",
        [r.get("Address", "") for r in idx200 if not (r.get("Title 1", "") or "").strip()],
        "Indexable pages with no title tag.")

    # duplicate titles (indexable only)
    by_title = defaultdict(list)
    for r in idx200:
        t = (r.get("Title 1", "") or "").strip()
        if t:
            by_title[t].append(r.get("Address", ""))
    dup_t = [u for urls in by_title.values() if len(urls) > 1 for u in urls]
    add("duplicate_title", "High", dup_t, "Pages sharing an identical title.")

    add("title_too_long", "Medium",
        [r.get("Address", "") for r in idx200
         if _int(r.get("Title 1 Pixel Width")) > 561 or _int(r.get("Title 1 Length")) > 60],
        "Titles likely truncated in search results.")

    add("title_too_short", "Low",
        [r.get("Address", "") for r in idx200
         if (r.get("Title 1", "") or "").strip() and _int(r.get("Title 1 Length")) < 30],
        "Titles that are too short to be effective.")

    # --- Meta Descriptions ---
    add("missing_meta_description", "Medium",
        [r.get("Address", "") for r in idx200 if not (r.get("Meta Description 1", "") or "").strip()],
        "Indexable pages with no meta description.")

    by_meta = defaultdict(list)
    for r in idx200:
        m = (r.get("Meta Description 1", "") or "").strip()
        if m:
            by_meta[m].append(r.get("Address", ""))
    dup_m = [u for urls in by_meta.values() if len(urls) > 1 for u in urls]
    add("duplicate_meta_description", "Medium", dup_m, "Pages sharing an identical meta description.")

    add("meta_description_too_long", "Low",
        [r.get("Address", "") for r in idx200 if _int(r.get("Meta Description 1 Length")) > 155],
        "Meta descriptions likely truncated in search results.")

    # --- H1s ---
    add("missing_h1", "Medium",
        [r.get("Address", "") for r in idx200 if not (r.get("H1-1", "") or "").strip()],
        "Pages with no H1 tag.")

    add("multiple_h1", "Medium",
        [r.get("Address", "") for r in idx200 if (r.get("H1-2", "") or "").strip()],
        "Pages with more than one H1 tag.")

    by_h1 = defaultdict(list)
    for r in idx200:
        h = (r.get("H1-1", "") or "").strip()
        if h:
            by_h1[h].append(r.get("Address", ""))
    dup_h1 = [u for urls in by_h1.values() if len(urls) > 1 for u in urls]
    add("duplicate_h1", "Low", dup_h1, "Indexable pages sharing an identical H1.")

    # --- Canonicals ---
    add("missing_canonical", "Low",
        [r.get("Address", "") for r in idx200 if not (r.get("Canonical Link Element 1", "") or "").strip()],
        "Indexable pages missing a canonical tag.")

    add("canonical_mismatch", "Low",
        [r.get("Address", "") for r in idx200 if (r.get("Canonical Link Element 1", "") or "").strip() and r.get("Canonical Link Element 1") != r.get("Address", "")],
        "Canonical URL does not match the page address.")

    # --- Other ---
    add("broken_link", "High",
        [r.get("Address", "") for r in rows if 400 <= _int(r.get("Status Code")) <= 499],
        "URLs returning a client error (4xx).")
    add("server_error", "High",
        [r.get("Address", "") for r in rows if 500 <= _int(r.get("Status Code")) <= 599],
        "URLs returning a server error (5xx).")
    add("redirect", "Medium",
        [r.get("Address", "") for r in rows if 300 <= _int(r.get("Status Code")) <= 399],
        "URLs that redirect (3xx).")

    # --- Redirect Chains and Loops ---
    redirect_map = {r.get("Address", ""): r.get("Redirect URL") for r in rows if 300 <= _int(r.get("Status Code")) <= 399}

    chain_urls = []
    loop_urls = []

    for start_url in redirect_map:
        path = []
        curr = start_url
        while curr in redirect_map:
            path.append(curr)
            next_url = redirect_map[curr]
            if not next_url:
                break
            if next_url in path:
                loop_urls.append(start_url)
                break
            curr = next_url
            if len(path) > 10:
                loop_urls.append(start_url)
                break
        else:
            # If it didn't loop, check if it was a chain
            # a chain exists when a redirect target is itself another redirecting URL
            # i.e., the path had more than 1 element.
            if len(path) > 1:
                chain_urls.append(start_url)

    add("redirect_chain", "High", chain_urls, "URLs that are part of a redirect chain (multiple hops).")
    add("redirect_loop", "High", loop_urls, "URLs that are part of a redirect loop.")

    add("thin_content", "Low",
        [r.get("Address", "") for r in idx200 if _int(r.get("Word Count")) < 200],
        "Indexable pages with low word count.")

    add("orphan_page", "Medium",
        [r.get("Address", "") for r in idx200 if _int(r.get("Inlinks")) == 0],
        "Indexable pages with zero internal links in.")

    add("non_indexable_but_linked", "Medium",
        [r.get("Address", "") for r in rows if (r.get("Indexability", "") or "").strip().lower() == "non-indexable" and _int(r.get("Inlinks")) > 0],
        "Non-indexable pages that are still linked internally.")

    add("slow_page", "Low",
        [r.get("Address", "") for r in rows if _float(r.get("Response Time")) > 1.0],
        "Pages with slow response times.")


    return issues


def summarize(issues: list[dict]) -> dict:
    by_sev = defaultdict(int)
    for i in issues:
        by_sev[i["severity"]] += 1
    return {"total_issues": len(issues),
            "by_severity": {"High": by_sev["High"], "Medium": by_sev["Medium"], "Low": by_sev["Low"]}}


if __name__ == "__main__":
    import sys, json
    d = sys.argv[1] if len(sys.argv) > 1 else "../sample-export"
    rows = load_rows(d)
    iss = detect(rows)
    print(f"Loaded {len(rows)} rows, detected {len(iss)} issue types.")
    print(json.dumps(summarize(iss), indent=2))
    for i in iss:
        print(f"  [{i['severity']:<6}] {i['type']:<24} x{i['count']}")
