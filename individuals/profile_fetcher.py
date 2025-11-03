#!/usr/bin/env python3
"""
Profile fetcher (DDG-first) that produces JSON-only output with status logs.

- Primary data source: DuckDuckGo Instant Answer API
- Optional: Serper (Google) to resolve a better Wikipedia title hint (via SERPER_API_KEY env)

Usage:
  python3 profile_fetcher.py "Full Name" [occupation] [--output file.json]

Output: JSON to stdout and (optionally) written to --output (or <name>.json by default)
"""

from __future__ import annotations
import sys
import os
import time
import json
import argparse
from typing import Any, Dict, List, Optional
import urllib.parse
import requests


USER_AGENT = "ProfileFetcher-DDG/1.0 (contact: youremail@example.com)"
DUCKDUCKGO_INSTANT = "https://api.duckduckgo.com/"
SERPER_ENDPOINT = "https://google.serper.dev/search"


# In-memory status log
STATUS_LOG: List[Dict[str, Any]] = []


def log_status(event: str, **fields: Any) -> None:
    try:
        STATUS_LOG.append({"event": event, "ts": int(time.time() * 1000), **fields})
    except Exception:
        pass


def query_duckduckgo(query: str) -> Optional[Dict[str, Any]]:
    try:
        t0 = time.time()
        params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1}
        resp = requests.get(DUCKDUCKGO_INSTANT, params=params, headers={"User-Agent": USER_AGENT}, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        # Consider it usable if we have a heading, abstract, infobox or related topics
        if data.get("Heading") or data.get("AbstractText") or data.get("Infobox") or data.get("RelatedTopics"):
            log_status("duckduckgo_ok", elapsedMs=int((time.time() - t0) * 1000))
            return data
    except requests.RequestException as exc:
        log_status("duckduckgo_error", error=str(exc))
    return None


def resolve_title_via_serper(query: str, api_key: str) -> Optional[str]:
    try:
        t0 = time.time()
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        }
        payload = {"q": query, "num": 5}
        resp = requests.post(SERPER_ENDPOINT, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("organic", []) or []:
            link = item.get("link", "")
            if isinstance(link, str) and link.startswith("https://en.wikipedia.org/wiki/"):
                title = urllib.parse.unquote(link.rsplit("/", 1)[-1])
                log_status("serper_title_resolved", title=title, elapsedMs=int((time.time() - t0) * 1000))
                return title
    except requests.RequestException as exc:
        log_status("serper_error", error=str(exc))
    return None


def build_profile_from_duckduckgo(ddg: Dict[str, Any], name: str) -> Dict[str, Any]:
    def to_list(v: Any) -> List[str]:
        if not v:
            return []
        if isinstance(v, list):
            return [str(i) for i in v if i]
        return [str(v)]

    heading = ddg.get("Heading") or name
    abstract = ddg.get("AbstractText") or ddg.get("Abstract") or None
    raw_infobox = ddg.get("Infobox") or []
    # Normalize infobox to a list of dicts
    if isinstance(raw_infobox, dict):
        infobox = [raw_infobox]
    elif isinstance(raw_infobox, list):
        infobox = [i for i in raw_infobox if isinstance(i, dict)]
    else:
        infobox = []

    raw_related = ddg.get("RelatedTopics") or []
    related: List[Dict[str, Any]] = []
    if isinstance(raw_related, list):
        for t in raw_related:
            if isinstance(t, dict) and "Text" in t:
                related.append(t)
            elif isinstance(t, dict) and isinstance(t.get("Topics"), list):
                for tt in t["Topics"]:
                    if isinstance(tt, dict) and "Text" in tt:
                        related.append(tt)

    profile: Dict[str, Any] = {
        "label": heading,
        "description": abstract,
        "birth": {"date": None, "place": None},
        "death": {"date": None, "place": None},
        "nationalities": [],
        "family": {"spouses": [], "children": [], "father": None, "mother": None, "siblings": []},
        "relatives": [],
        "education": {"schools": [], "degrees": [], "fieldsOfWork": []},
        "career": {"occupations": [], "employers": [], "positionsHeld": [], "parties": [], "memberships": [], "affiliations": []},
        "links": {"wikipedia": ddg.get("AbstractURL") or None},
        "summary": abstract,
    }

    # Parse DDG infobox items: list of {label, value}
    for item in infobox:
        if not isinstance(item, dict):
            continue
        label = (item.get("label") or "").strip().lower()
        value = item.get("value")
        if not label:
            continue
        if label in ("born", "date of birth") and isinstance(value, str):
            profile["birth"]["date"] = value
        if label in ("place of birth",) and isinstance(value, str):
            profile["birth"]["place"] = value
        if label in ("died", "date of death") and isinstance(value, str):
            profile["death"]["date"] = value
        if label in ("nationality",):
            profile["nationalities"] = sorted(set(profile["nationalities"] + to_list(value)))
        if label in ("occupation", "profession"):
            profile["career"]["occupations"] = sorted(set(profile["career"]["occupations"] + to_list(value)))
        if label in ("education", "alma mater", "educated at"):
            profile["education"]["schools"] = sorted(set(profile["education"]["schools"] + to_list(value)))
        if label in ("employer", "employers"):
            profile["career"]["employers"] = sorted(set(profile["career"]["employers"] + to_list(value)))
        if label in ("political party", "party"):
            profile["career"]["parties"] = sorted(set(profile["career"]["parties"] + to_list(value)))
        if label in ("spouse", "spouses"):
            profile["family"]["spouses"] = sorted(set(profile["family"]["spouses"] + to_list(value)))
        if label == "children":
            profile["family"]["children"] = sorted(set(profile["family"]["children"] + to_list(value)))
        if label == "father":
            vals = to_list(value)
            if vals and not profile["family"]["father"]:
                profile["family"]["father"] = vals[0]
        if label == "mother":
            vals = to_list(value)
            if vals and not profile["family"]["mother"]:
                profile["family"]["mother"] = vals[0]
        if label == "relatives":
            for v in to_list(value):
                profile["relatives"].append({"name": v, "relation": "relative", "shortBio": None, "links": {}})

    # Related topics: add obvious relations hints
    for topic in related:
        if not isinstance(topic, dict):
            continue
        text = topic.get("Text") or ""
        url = topic.get("FirstURL") or ""
        if not text:
            continue
        lt = text.lower()
        if any(k in lt for k in ["spouse", "wife", "husband", "son", "daughter", "father", "mother", "sibling", "brother", "sister"]):
            profile["relatives"].append({"name": text.split(" - ")[0], "relation": "related", "shortBio": None, "links": {"url": url} if url else {}})

    return profile


def get_person_profile(name: str, occupation: Optional[str]) -> Dict[str, Any]:
    phrase = f"{name} {occupation}" if occupation else name
    log_status("duckduckgo_profile_start", query=phrase)
    ddg = query_duckduckgo(phrase)
    if not ddg and occupation:
        # Try again with just the name
        log_status("duckduckgo_profile_retry", query=name)
        ddg = query_duckduckgo(name)
    if not ddg:
        # Try Serper to find a Wikipedia title, then ask DDG again with that title
        api_key = os.getenv("SERPER_API_KEY")
        if api_key:
            log_status("serper_hint_start", query=phrase)
            title = resolve_title_via_serper(phrase, api_key)
            if title:
                log_status("serper_hint_ok", title=title)
                ddg = query_duckduckgo(title)
    if not ddg:
        log_status("duckduckgo_profile_failed", query=phrase)
        return {"query": {"name": name, "occupation": occupation}, "error": "No results from DuckDuckGo", "status": STATUS_LOG}

    profile = build_profile_from_duckduckgo(ddg, name)
    profile["query"] = {"name": name, "occupation": occupation}
    profile["status"] = STATUS_LOG
    return profile


def _safe_filename_from_name(name: str) -> str:
    base = name.strip().replace(" ", "_")
    base = "".join(ch for ch in base if ch.isalnum() or ch in ("_", "-"))
    return base or "result"


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("name", nargs="?")
    parser.add_argument("occupation", nargs="?")
    parser.add_argument("--output", "-o", dest="output", default=None)
    parser.add_argument("--help", action="help", help="show this help message and exit")
    args = parser.parse_args()

    if not args.name:
        err = {"error": "Usage: python profile_fetcher.py 'Full Name' [occupation] [--output file.json]"}
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(1)

    name = args.name
    occupation = args.occupation

    try:
        STATUS_LOG.clear()
        result = get_person_profile(name=name, occupation=occupation)
        out_path = args.output or f"{_safe_filename_from_name(name)}.json"
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            log_status("written_output", path=out_path)
            print(json.dumps({"output": out_path, "ok": "error" not in result}, ensure_ascii=False))
        except OSError as fs_exc:
            log_status("write_failed", path=out_path, error=str(fs_exc))
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as exc:
        log_status("fatal_error", error=str(exc))
        err = {"query": {"name": name, "occupation": occupation}, "error": str(exc), "status": STATUS_LOG}
        print(json.dumps(err, indent=2, ensure_ascii=False))
        sys.exit(2)


if __name__ == "__main__":
    main()


