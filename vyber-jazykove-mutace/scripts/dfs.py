"""Sdílené volání DataForSEO. Přihlašovací údaje jen z prostředí nebo --env-file, nikdy z kódu."""
import base64, json, os, sys, urllib.request, urllib.error
from pathlib import Path

API = "https://api.dataforseo.com"

def load_creds(env_file=None):
    login, password = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    candidates = [env_file] if env_file else []
    candidates += [".env", str(Path.home() / ".config" / "dataforseo" / ".env")]
    for c in candidates:
        if login and password:
            break
        p = Path(c).expanduser() if c else None
        if p and p.is_file():
            for line in p.read_text().splitlines():
                if line.startswith("DATAFORSEO_LOGIN="):
                    login = login or line.split("=", 1)[1].strip().strip('"\'')
                elif line.startswith("DATAFORSEO_PASSWORD="):
                    password = password or line.split("=", 1)[1].strip().strip('"\'')
    if not (login and password):
        sys.exit("Chybí DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD. Požádej uživatele o přístup k DataForSEO API "
                 "(app.dataforseo.com → API Access) a ulož je do ~/.config/dataforseo/.env (chmod 600) "
                 "nebo předej přes --env-file. Do skillu ani do repozitáře je nezapisuj.")
    return login, password

def call(path, payload=None, creds=None, timeout=120):
    tok = base64.b64encode(f"{creds[0]}:{creds[1]}".encode()).decode()
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode() if payload is not None else None,
                                 headers={"Authorization": "Basic " + tok, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            sys.exit("DataForSEO odmítlo přihlášení (401). Zkontroluj login a API heslo (není to heslo do účtu).")
        sys.exit(f"DataForSEO HTTP {e.code}: {e.read()[:300]!r}")
