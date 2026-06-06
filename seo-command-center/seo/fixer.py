"""
fixer.py — AI-powered fix generation for SEO issues detected in Screaming Frog exports.
"""

from __future__ import annotations
import os
from collections import defaultdict

def _int(v, default=0):
    try:
        return int(float(str(v).strip()))
    except Exception:
        return default

def is_html(r):
    return "text/html" in (r.get("Content Type", "") or "").lower()

def is_200(r):
    return _int(r.get("Status Code")) == 200

def indexable(r):
    return (r.get("Indexability", "") or "").strip().lower() == "indexable"

class ModelClient:
    """
    Interface for the LLM. In a production environment, this would
    call the Anthropic API. For this module, we provide a base class
    that the orchestrator can extend or provide an implementation for.
    """
    def rewrite(self, prompt: str) -> str:
        # This is a placeholder. The orchestrator (SKILL.md) will likely
        # provide the actual model implementation.
        return "REWRITTEN_CONTENT"

def generate_fixes(issues: list[dict], rows: list[dict], model_client: ModelClient = None) -> dict:
    """
    Generates fixes for detected SEO issues.

    Args:
        issues: List of issue dicts from detector.py
        rows: All rows from internal_all.csv
        model_client: Optional client to handle LLM calls. If None, logic is skipped or mocked.

    Returns:
        {
            "titles": [{"url": str, "old": str, "new": str}, ...],
            "meta": [{"url": str, "old": str, "new": str}, ...],
            "redirect_map": [{"from": str, "to": str}, ...]
        }
    """
    if model_client is None:
        # If no client is provided, we can't rewrite text, but we can still do redirects.
        model_client = None

    # Index rows for fast lookup
    addr_map = {r["Address"]: r for r in rows}

    # Filter for indexable 200 HTML pages (the only ones we fix content for)
    idx200_urls = [
        r["Address"] for r in rows
        if is_html(r) and is_200(r) and indexable(r)
    ]

    results = {
        "titles": [],
        "meta": [],
        "redirect_map": []
    }

    # --- 1. Redirect Map (Deterministic) ---
    # Only for broken_link (4xx)
    broken_links = []
    for i in issues:
        if i["type"] == "broken_link":
            broken_links.extend(i["affected_urls"])

    if broken_links:
        # We want to map each 4xx URL to the best 200 URL
        # Priority: 1. Same path prefix, 2. Highest inlinks
        valid_targets = [url for url in addr_map if is_200(addr_map[url])]

        for url in broken_links:
            best_target = None
            max_inlinks = -1
            longest_prefix = ""

            # Simple prefix matching logic
            # e.g. /products/shoes-123 matches /products/shoes
            u_path = url.split('?')[0].rstrip('/')

            for target in valid_targets:
                t_path = target.split('?')[0].rstrip('/')
                if u_path.startswith(t_path) and t_path != "":
                    prefix_len = len(t_path)
                    inlinks = _int(addr_map[target].get("Inlinks"))

                    # If we find a longer prefix, it's a better match
                    if prefix_len > len(longest_prefix):
                        longest_prefix = t_path
                        best_target = target
                        max_inlinks = inlinks
                    # If prefixes are same length, use inlinks as tiebreaker
                    elif prefix_len == len(longest_prefix):
                        if inlinks > max_inlinks:
                            best_target = target
                            max_inlinks = inlinks

            # Fallback: If no prefix match, pick the most authoritative page (highest inlinks)
            if not best_target and valid_targets:
                # This is a naive fallback; in reality, we might look for keyword similarity
                # But the prompt specifies "same path prefix OR highest inlinks similarity"
                # We'll find the overall target with the most inlinks.
                best_target = max(valid_targets, key=lambda u: _int(addr_map[u].get("Inlinks")))

            if best_target:
                results["redirect_map"].append({"from": url, "to": best_target})

    # --- 2. Title Fixes (Model-based) ---
    if model_client:
        title_issues = ["missing_title", "duplicate_title", "title_too_long", "title_too_short"]
        affected_titles = set()
        for i in issues:
            if i["type"] in title_issues:
                affected_titles.update(i["affected_urls"])

        for url in affected_titles:
            if url not in idx200_urls:
                continue

            row = addr_map[url]
            old_title = (row.get("Title 1", "") or "").strip()

            # Infer primary keyword from Address or Title
            # Simple extraction: take the last part of the path, remove hyphens
            path_segment = url.split('/')[-1].split('?')[0].split('#')[0]
            keyword = path_segment.replace('-', ' ').replace('_', ' ') if path_segment else "SEO"

            prompt = (
                f"Rewrite the SEO title for the following page:\n"
                f"URL: {url}\n"
                f"Current Title: {old_title}\n"
                f"Inferred Keyword: {keyword}\n"
                f"Constraints:\n"
                f"- Maximum 60 characters\n"
                f"- Must include the primary keyword: {keyword}\n"
                f"- Must be compelling and optimized for CTR\n"
                f"Return ONLY the new title text."
            )

            new_title = model_client.rewrite(prompt)
            # Validate length constraint (Hard rule)
            if len(new_title) > 60:
                new_title = new_title[:57] + "..."

            results["titles"].append({"url": url, "old": old_title, "new": new_title})

    # --- 3. Meta Description Fixes (Model-based) ---
    if model_client:
        meta_issues = ["missing_meta_description", "duplicate_meta_description", "meta_description_too_long"]
        affected_meta = set()
        for i in issues:
            if i["type"] in meta_issues:
                affected_meta.update(i["affected_urls"])

        for url in affected_meta:
            if url not in idx200_urls:
                continue

            row = addr_map[url]
            old_meta = (row.get("Meta Description 1", "") or "").strip()

            # Infer keyword for the meta description
            path_segment = url.split('/')[-1].split('?')[0].split('#')[0]
            keyword = path_segment.replace('-', ' ').replace('_', ' ') if path_segment else "SEO"

            prompt = (
                f"Rewrite the SEO meta description for the following page:\n"
                f"URL: {url}\n"
                f"Current Meta: {old_meta}\n"
                f"Inferred Keyword: {keyword}\n"
                f"Constraints:\n"
                f"- Maximum 155 characters\n"
                f"- Must include the primary keyword: {keyword}\n"
                f"- Must be an inviting summary that encourages clicks\n"
                f"Return ONLY the new meta description text."
            )

            new_meta = model_client.rewrite(prompt)
            # Validate length constraint (Hard rule)
            if len(new_meta) > 155:
                new_meta = new_meta[:152] + "..."

            results["meta"].append({"url": url, "old": old_meta, "new": new_meta})

    return results
