# Výběr jazykové mutace — skill pro Claude

Skill pro Claude Code, který pomáhá rozhodnout, **do jakého jazyka přeložit web jako další** a co od nové jazykové verze čekat. Místo odhadu podle počtu mluvčích měří poptávku po tématech, která web už má, a kalibruje odhad na vlastních datech webu.

## Co umí

1. **Košík poptávky** — změří hledanost stejných 10–15 témat na všech kandidátních trzích (DataForSEO), vyřadí domácí témata a upozorní na podezřelá čísla (homonyma).
2. **Konkurence** — ukáže, kdo drží první stránku Googlu u nejsilnějších dotazů.
3. **Model** — z výkonu stávajících jazykových verzí spočítá tři scénáře kliknutí, výnosu a návratnosti pro každého kandidáta.
4. **Doporučení** — pořadí jazyků, hranice pro pokračování nebo zastavení po 30 dnech a postup spuštění.
5. **Zpětné vyhodnocení** — porovnání už spuštěného jazyka s odhadem, včetně očištění návštěvnosti o roboty.

## Instalace

```bash
git clone https://github.com/LK-Media-Group/vyber-jazykove-mutace.git
cp -r vyber-jazykove-mutace/vyber-jazykove-mutace ~/.claude/skills/
```

Potom v Claude Code stačí napsat například „do jakého jazyka máme přeložit web jako další?“.

## Co je potřeba

- **Claude Code** a Python 3.9+ (skripty nemají žádné další závislosti).
- **Účet DataForSEO** s API přístupem. Skill si o přihlašovací údaje řekne při prvním spuštění a uloží je do `~/.config/dataforseo/.env`. Celá analýza stojí obvykle do 1 USD.
- Ideálně data ze Search Console o stávajících jazykových verzích. Bez nich skill použije orientační výchozí hodnoty a výsledek je jen hrubý řád.

## Obsah

```
vyber-jazykove-mutace/
├── SKILL.md                    postup pro Clauda
├── references/metodika.md      proč to funguje a typické chyby
├── assets/config.example.json  ukázková konfigurace (smyšlená čísla)
└── scripts/
    ├── check_access.py         ověření přístupu a kódy trhů
    ├── basket.py               košík poptávky
    ├── serp.py                 konkurence na první stránce
    └── model.py                scénáře a návratnost
```

## Licence

MIT. Vytvořilo [LK Media](https://lkmedia.cz).
