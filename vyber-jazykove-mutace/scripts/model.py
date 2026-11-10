#!/usr/bin/env python3
"""Odhad kliknutí a výnosu pro kandidátní jazyky: košík × efektivita změřená na stávajících mutacích.

Použití: model.py --config config.json --basket basket.json --out model.json

Efektivita = kliknutí z vyhledávání za den na 100 000 hledání v košíku.
Scénáře: low = medián překladových mutací, base = horní kvartil, high = nejlepší překladová mutace
(high se počítá jen kandidátům s "fit": true). Bez vlastních mutací se použijí orientační výchozí
hodnoty z config["reference_efficiency"] a výstup to výslovně uvede.
"""
import argparse, json, statistics
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--basket", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = json.loads(Path(a.config).read_text()); bk = json.loads(Path(a.basket).read_text())["markets"]
    cal = {}
    for lang, c in (cfg.get("calibration") or {}).items():
        if lang not in bk or not bk[lang]["basket_normalized"]:
            print(f"  (kalibrace {lang}: chybí košík, přeskočeno)"); continue
        b = bk[lang]["basket_normalized"]; cd = c["clicks_per_day"]
        cal[lang] = {"basket": b, "clicks_day": cd, "eff": round(cd / (b / 100000), 1),
                     "native": bool(c.get("native")), "note": c.get("note", "")}
    tr = sorted(v["eff"] for v in cal.values() if not v["native"])
    ref = cfg.get("reference_efficiency") or {"low": 10, "base": 25, "high": 60}
    if len(tr) >= 4:
        q = statistics.quantiles(tr, n=4)
        scen = {"low": round(statistics.median(tr), 1), "base": round(q[2], 1), "high": round(max(tr), 1)}; src = "vlastní mutace"
    else:
        scen = ref; src = "ORIENTAČNÍ výchozí hodnoty (méně než 4 vlastní překladové mutace) — ber jako hrubý řád"
    rpc = cfg.get("revenue_per_click"); cur = cfg.get("currency", "USD")
    print("=== Kalibrace: kliknutí/den na 100 000 hledání v košíku ===")
    for l, v in sorted(cal.items(), key=lambda x: -x[1]["eff"]):
        print(f"  {l:6s} košík {v['basket']:>9}  kliknutí/den {v['clicks_day']:>7}  efektivita {v['eff']:>6}{'  (původní jazyk, do scénářů se nepočítá)' if v['native'] else ''}")
    print(f"\nScénáře ({src}): low {scen['low']} / base {scen['base']} / high {scen['high']}")
    rows = []
    for lang, c in (cfg.get("candidates") or {}).items():
        if lang not in bk: print(f"  (kandidát {lang}: chybí košík)"); continue
        u = bk[lang]["basket_normalized"] / 100000; mult = c.get("value_multiplier", 1.0)
        low, base, high = scen["low"] * u, scen["base"] * u, (scen["high"] * u if c.get("fit") else None)
        r = {"lang": lang, "name": bk[lang]["name"], "basket": bk[lang]["basket_normalized"], "clicks_day_low": round(low),
             "clicks_day_base": round(base), "clicks_day_high": round(high) if high else None, "value_multiplier": mult,
             "fit": bool(c.get("fit")), "note": c.get("note", ""), "check_outliers": bk[lang].get("check_outliers", [])}
        if rpc:
            r["revenue_month_base"] = round(base * rpc * mult * 30); r["revenue_month_high"] = round(high * rpc * mult * 30) if high else None
            cost = c.get("launch_cost") or cfg.get("launch_cost")
            if cost and r["revenue_month_base"]: r["payback_months_base"] = round(cost / r["revenue_month_base"], 1)
        rows.append(r)
    rows.sort(key=lambda r: -(r.get("revenue_month_base") or r["clicks_day_base"]))
    print("\n=== Kandidáti ===")
    for r in rows:
        hi = r["clicks_day_high"] if r["clicks_day_high"] is not None else "—"
        rev = f"  výnos/měs base {r.get('revenue_month_base')} {cur}, high {r.get('revenue_month_high') or '—'}" if rpc else ""
        pb = f", návratnost {r['payback_months_base']} měs." if r.get("payback_months_base") else ""
        warn = f"  !! zkontroluj košík: {', '.join(r['check_outliers'])}" if r["check_outliers"] else ""
        print(f"  {r['lang']:6s} košík {r['basket']:>9}  kliknutí/den {r['clicks_day_low']}/{r['clicks_day_base']}/{hi}{rev}{pb}  ×{r['value_multiplier']}  {r['note']}{warn}")
    Path(a.out).write_text(json.dumps({"calibration": cal, "scenarios": scen, "scenario_source": src, "revenue_per_click": rpc,
                                       "currency": cur, "candidates": rows}, ensure_ascii=False, indent=1))
    print(f"\nUloženo: {a.out}")

if __name__ == "__main__":
    main()
