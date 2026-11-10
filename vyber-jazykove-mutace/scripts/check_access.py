#!/usr/bin/env python3
"""Ověří přístup k DataForSEO (zdarma) a volitelně vypíše kódy trhů: check_access.py [--find Norway] [--env-file CESTA]"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import dfs
ap = argparse.ArgumentParser(); ap.add_argument("--find"); ap.add_argument("--env-file"); a = ap.parse_args()
creds = dfs.load_creds(a.env_file)
u = dfs.call("/v3/appendix/user_data", None, creds)
bal = (((u.get("tasks") or [{}])[0].get("result") or [{}])[0].get("money") or {}).get("balance")
print(f"Přístup funguje. Zůstatek: {bal} USD")
if a.find:
    d = dfs.call("/v3/dataforseo_labs/locations_and_languages", None, creds)
    for r in (d.get("tasks") or [{}])[0].get("result") or []:
        if a.find.lower() in (r.get("location_name") or "").lower():
            print(r.get("location_code"), r.get("location_name"), [(l.get("language_code"), l.get("language_name")) for l in r.get("available_languages") or []])
