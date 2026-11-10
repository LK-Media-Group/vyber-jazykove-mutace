#!/usr/bin/env python3
"""Kdo drží první stránku: top 10 organických domén pro korunní dotazy kandidátních trhů.

Použití: serp.py --config config.json --out serp.json [--only ro fi] [--dry-run] [--env-file CESTA]
Bere config["serp_checks"] = {trh: [dotaz, ...]}; kódy trhu z config["markets"].
"""
import argparse, collections, json, sys, time, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import dfs

def real_domain(it):
    """Google v živých výsledcích maskuje cílové adresy (google.com/goto), skutečná doména je v breadcrumb."""
    dom = (it.get("domain") or "").lower()
    if dom and "google." not in dom:
        return dom.removeprefix("www.")
    bc = (it.get("breadcrumb") or "").split(" ")[0]
    if bc.startswith("http"):
        return urllib.parse.urlsplit(bc).netloc.lower().removeprefix("www.")
    return (it.get("website_name") or dom or "?").split("\xa0")[0].strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--env-file")
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text())
    checks = {m: q for m, q in cfg.get("serp_checks", {}).items() if not a.only or m in a.only}
    n = sum(len(q) for q in checks.values())
    print(f"Plán: {n} dotazů na {len(checks)} trzích. Odhad ceny: jednotky centů (skutečnou cenu vrací API).")
    if a.dry_run:
        for m, q in checks.items(): print(f"  {m}: {', '.join(q)}")
        return
    creds = dfs.load_creds(a.env_file); result, total = {}, 0.0
    for m, queries in checks.items():
        mk = cfg["markets"][m]; result[m] = {"queries": {}}; doms = collections.Counter()
        for q in queries:
            data = dfs.call("/v3/serp/google/organic/live/advanced",
                            [{"keyword": q, "location_code": mk["location_code"],
                              "language_code": mk.get("serp_language_code", mk["language_code"]),
                              "device": "desktop", "depth": 10}], creds)
            total += data.get("cost") or 0; rows = []
            for task in data.get("tasks", []):
                if task.get("status_code") != 20000:
                    print(f"  !! {m} / {q}: {task.get('status_message')}"); continue
                for res in task.get("result") or []:
                    for it in res.get("items") or []:
                        if it.get("type") == "organic":
                            rows.append({"pos": it.get("rank_absolute"), "domain": real_domain(it), "title": (it.get("title") or "")[:80]})
            result[m]["queries"][q] = rows
            for r in rows[:10]: doms[r["domain"]] += 1
            print(f"[{m}] {q}\n    " + ", ".join(r["domain"] or "?" for r in rows[:10]))
            time.sleep(1)
        result[m]["domains"] = doms.most_common()
    result["cost_usd"] = round(total, 4)
    Path(a.out).write_text(json.dumps(result, ensure_ascii=False, indent=1))
    print(f"\nCena DataForSEO celkem: {total:.4f} USD. Uloženo: {a.out}")

if __name__ == "__main__":
    main()
