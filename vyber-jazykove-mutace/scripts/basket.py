#!/usr/bin/env python3
"""Košík poptávky: hledanost stejných témat na více trzích (DataForSEO Labs keyword_overview).

Použití:
  basket.py --config config.json --out basket.json [--only ro fi] [--dry-run] [--env-file CESTA]

Na koncept se bere MAXIMUM přes varianty klíčového slova (ne součet).
Domácí koncepty trhu se vyřadí a košík se dopočítá na plný počet konceptů.
"""
import argparse, json, statistics, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import dfs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--env-file")
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text())
    markets, basket = cfg["markets"], cfg["basket"]
    out_path = Path(a.out)
    out = json.loads(out_path.read_text()) if (a.only and out_path.exists()) else {"markets": {}, "cost_usd": 0}
    todo = [m for m in markets if not a.only or m in a.only]
    plan = {m: sorted({v.lower() for c in basket.values() for v in c.get(m, [])}) for m in todo}
    missing = [(m, c) for m in todo for c in basket if not basket[c].get(m)]
    print(f"Plán: {len(todo)} trhů, {sum(len(v) for v in plan.values())} klíčových slov, {len(basket)} konceptů.")
    print("Odhad ceny: řádově 0,02–0,03 USD na trh (skutečnou cenu vrací API a skript ji sečte).")
    if missing:
        print("POZOR, chybí varianty:", ", ".join(f"{m}/{c}" for m, c in missing))
    if a.dry_run:
        for m, k in plan.items():
            print(f"  {m}: {', '.join(k)}")
        return
    creds = dfs.load_creds(a.env_file)
    total = float(out.get("cost_usd") or 0)
    for m in todo:
        mk = markets[m]
        data = dfs.call("/v3/dataforseo_labs/google/keyword_overview/live",
                        [{"keywords": plan[m], "language_code": mk["language_code"],
                          "location_code": mk["location_code"], "include_serp_info": False}], creds)
        total += data.get("cost") or 0
        vols = {}
        for task in data.get("tasks", []):
            if task.get("status_code") != 20000:
                print(f"  !! {m}: {task.get('status_message')}"); continue
            for res in task.get("result") or []:
                for it in res.get("items") or []:
                    ki = it.get("keyword_info") or {}
                    vols[(it.get("keyword") or "").lower()] = {"volume": ki.get("search_volume") or 0, "cpc": ki.get("cpc") or 0}
        dom = set(mk.get("domestic", []))
        concepts = {}
        for c, per in basket.items():
            best_kw, best = None, {"volume": 0, "cpc": 0}
            for v in [x.lower() for x in per.get(m, [])]:
                d = vols.get(v, {"volume": 0, "cpc": 0})
                if d["volume"] >= best["volume"]:
                    best_kw, best = v, d
            concepts[c] = {"kw": best_kw, **best, "domestic": c in dom}
        outb = [c for c in concepts.values() if not c["domestic"]]
        outbound = sum(c["volume"] for c in outb)
        norm = round(outbound * len(basket) / len(outb)) if outb else 0
        vs = [c["volume"] for c in outb if c["volume"]]
        med = statistics.median(vs) if vs else 0
        # podezřelé koncepty hlásíme až od 8 konceptů; u menšího košíku je velký podíl jednoho tématu běžný
        flags = [k for k, c in concepts.items() if len(outb) >= 8 and not c["domestic"] and outbound and
                 (c["volume"] > 0.4 * outbound or (med and c["volume"] > 5 * med))]
        zero = [k for k, c in concepts.items() if not c["volume"]]
        out["markets"][m] = {"name": mk.get("name", m), "role": mk.get("role", "candidate"), "concepts": concepts,
                             "total": sum(c["volume"] for c in concepts.values()), "outbound": outbound,
                             "basket_normalized": norm, "check_outliers": flags, "zero_volume": zero}
        print(f"{m:6s} {mk.get('name', m):22s} košík {norm:9,d}".replace(",", " ")
              + (f"   ZKONTROLUJ (homonymum / domácí téma?): {', '.join(flags)}" if flags else "")
              + (f"   bez dat: {', '.join(zero)}" if zero else ""))
        time.sleep(1)
    out["cost_usd"] = round(total, 4); out["n_concepts"] = len(basket)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"\nCena DataForSEO celkem: {total:.4f} USD. Uloženo: {out_path}")

if __name__ == "__main__":
    main()
