#!/usr/bin/env python3
"""Resolve DOI URLs from refs_gpt.bib and write a reproducibility audit."""

from __future__ import annotations

import json
import re
import socket
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper" / "latex_gpt"
BIB = PAPER / "refs_gpt.bib"
OUT = PAPER / "source_data" / "manifest_bib_doi_resolution_20260501.json"

entry_re = re.compile(r"@\w+\s*\{\s*([^,]+),(.*?)(?=\n@|\Z)", re.S)
doi_re = re.compile(r"\bdoi\s*=\s*[\{\"]([^\}\"]+)[\}\"]", re.I)
url_re = re.compile(r"\burl\s*=\s*[\{\"]([^\}\"]+)[\}\"]", re.I)

socket.setdefaulttimeout(10)


def normalize_doi(raw: str) -> str:
    raw = raw.strip().rstrip(",")
    raw = raw.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return raw


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


def resolve_one(key: str, doi: str | None, url: str | None) -> dict:
    target = f"https://doi.org/{doi}" if doi else url
    result = {"key": key, "doi": doi, "url": url, "target": target, "status": "not_checked", "http_status": None, "final_url": None, "error": None}
    if not target:
        result["status"] = "no_doi_or_url"
        return result

    # For DOI entries, verifying that doi.org returns a redirect is enough for
    # endpoint existence. Following the publisher redirect creates false
    # negatives because several publishers block automated HEAD/GET requests.
    opener = urllib.request.build_opener(NoRedirect) if doi else urllib.request.build_opener()
    request = urllib.request.Request(target, method="HEAD", headers={"User-Agent": "Codex DOI audit; mailto:none@example.com"})
    try:
        with opener.open(request, timeout=12) as response:
            result["http_status"] = response.status
            result["final_url"] = response.geturl()
            result["status"] = "resolved" if 200 <= response.status < 400 else "http_error"
            return result
    except urllib.error.HTTPError as exc:
        result["http_status"] = exc.code
        result["final_url"] = exc.headers.get("Location")
        if doi and exc.code in {301, 302, 303, 307, 308} and result["final_url"]:
            result["status"] = "doi_redirected"
            return result
        result["error"] = repr(exc)
        result["status"] = "resolution_failed"
        return result
    except Exception as exc:  # noqa: BLE001 - audit should record all network failures.
        result["error"] = repr(exc)
        result["status"] = "resolution_failed"
        return result


entries = []
text = BIB.read_text(encoding="utf-8", errors="ignore")
for key, body in entry_re.findall(text):
    doi_match = doi_re.search(body)
    url_match = url_re.search(body)
    doi = normalize_doi(doi_match.group(1)) if doi_match else None
    url = url_match.group(1).strip() if url_match else None
    entries.append((key.strip(), doi, url))

results = []
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(resolve_one, key, doi, url) for key, doi, url in entries]
    for future in as_completed(futures):
        results.append(future.result())
results.sort(key=lambda row: row["key"])

status_counts: dict[str, int] = {}
for row in results:
    status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1

summary = {
    "generated_by": str(Path(__file__).relative_to(ROOT)),
    "bib_file": str(BIB.relative_to(ROOT)),
    "scope_note": "Network DOI/URL resolution audit only. A resolved DOI/URL is evidence that the reference endpoint exists; it is not a full semantic bibliography review.",
    "entry_count": len(entries),
    "status_counts": status_counts,
    "results": results,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps({"entry_count": len(entries), "status_counts": status_counts, "output": str(OUT.relative_to(ROOT))}, indent=2))
failed = [row for row in results if row["status"] not in {"resolved", "doi_redirected", "no_doi_or_url"}]
if failed:
    print(json.dumps({"failed": failed[:10], "failed_count": len(failed)}, indent=2))
