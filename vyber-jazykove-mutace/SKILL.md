---
name: vyber-jazykove-mutace
description: Datový výběr dalšího jazyka nebo trhu pro web, blog či e-shop a odhad, kolik návštěv a peněz nová jazyková mutace přinese. Změří poptávku po stejných tématech na kandidátních trzích (DataForSEO), zkontroluje konkurenci na první stránce Googlu, zkalibruje odhad na stávajících mutacích webu a vrátí pořadí kandidátů se scénáři nízký / střední / vysoký, odhadem návratnosti a hranicemi pro pokračování nebo zastavení. Použij VŽDY, když někdo řeší „do jakého jazyka přeložit web“, „který trh dřív“, „vyplatí se nám němčina / polština / maďarština“, „kam expandovat s obsahem“, „odhad návštěvnosti nové jazykové verze“, „další mutace“, „international SEO prioritizace“ nebo chce vyhodnotit, jestli spuštěný jazyk plní očekávání. Potřebuje přístup k DataForSEO API — pokud chybí, skill si o něj řekne. NEpoužívej pro samotný překlad textů, jazykovou korekturu, technické nastavení hreflang ani běžný keyword research v jednom jazyce.
---

# Výběr jazykové mutace

Skill odpovídá na otázku „který jazyk přidat jako další a co od něj čekat“. Vychází z postupu ověřeného na vícejazyčném obsahovém webu. Rozdělení práce: **skripty měří a počítají, ty vybíráš témata, překládáš klíčová slova, kontroluješ nesmysly v datech a píšeš doporučení.**

Proč takhle a ne podle počtu mluvčích: velikost trhu výsledek nepředpovídá. Rozhoduje, jestli lidé na daném trhu hledají **témata, která web už má**, a jestli se dá předběhnout konkurence na první stránce. Podrobnosti a chyby, kterým se vyhnout, jsou v `references/metodika.md` — přečti ji před prvním během.

## Krok 0 — přístup k DataForSEO

Spusť `python3 scripts/check_access.py`. Když skončí chybou o chybějících údajích, **požádej uživatele o DataForSEO API login a API heslo** (app.dataforseo.com → API Access; API heslo není heslo do účtu) a ulož je do `~/.config/dataforseo/.env`:

```
DATAFORSEO_LOGIN=...
DATAFORSEO_PASSWORD=...
```

Soubor nastav na `chmod 600`. Údaje nikdy nezapisuj do skillu, do konfigurace běhu ani do repozitáře a nevypisuj je do chatu. Skripty je čtou z prostředí, z `--env-file`, z `.env` v pracovním adresáři nebo z `~/.config/dataforseo/.env`.

Celý běh stojí obvykle do 1 USD i při dvou desítkách trhů. Skripty před placeným voláním vypíšou plán, umí `--dry-run` a po běhu sečtou skutečnou cenu z odpovědí API. Uživateli řekni odhad předem.

## Krok 1 — vstupy od uživatele

Zjisti si sám, co jde (web, analytika, Search Console, dřívější exporty). Ptej se jen na to, co nedohledáš:

| Vstup | K čemu | Když chybí |
|---|---|---|
| Web a jeho původní jazyk | výběr témat | nutné |
| 10–15 nosných témat webu | košík | navrhni z nejnavštěvovanějších stránek a nech potvrdit |
| Kandidátní trhy | co porovnáváme | navrhni 8–15 podle geografie a podobnosti zákazníků |
| Stávající mutace a jejich kliknutí z vyhledávání za den (posledních 28 dní) | kalibrace | použijí se orientační výchozí hodnoty, výsledek je pak jen hrubý řád |
| Výnos na kliknutí z vyhledávání (tržby nebo provize ÷ kliknutí) | přepočet na peníze | model vrátí jen kliknutí |
| Náklad na spuštění jazyka | návratnost | vynech |

## Krok 2 — konfigurace

Zkopíruj `assets/config.example.json` do pracovní složky běhu (mimo skill) a vyplň:

- **`basket`** — 10–15 konceptů. Většina jsou nosná témata webu, 2–3 obecné komerční dotazy oboru (u cestování pojištění, letenky, půjčovna aut). Pro každý trh 1–3 varianty klíčového slova tak, jak to místní skutečně hledají: místní názvy míst a produktů, varianty s diakritikou i bez. Varianty se nesčítají, bere se nejsilnější.
- **`markets`** — kandidáti i stávající jazyky (ty jsou potřeba pro kalibraci). Kódy ověř: `python3 scripts/check_access.py --find Norway`. Pozor, kód jazyka nemusí odpovídat zkratce, kterou používá web (norština je `nb`).
- **`domestic`** — koncepty, které jsou pro daný trh domácí téma. Vyřadí se a košík se dopočítá. Bez toho vyjde nesmysl: Chorvatsko vypadalo skvěle jen proto, že Plitvice jsou pro Chorvaty výlet za humna.
- **`calibration`** — kliknutí za den u stávajících mutací; původnímu jazyku dej `"native": true`.
- **`candidates`** — `fit` (true jen tehdy, když trh hledá stejná témata a první stránku drží porazitelné weby; vyplň až po kroku 4), `value_multiplier` (poměr hodnoty objednávky nebo rezervace proti průměru webu), poznámka.

## Krok 3 — košík

```
python3 scripts/basket.py --config config.json --out basket.json --dry-run   # kontrola plánu
python3 scripts/basket.py --config config.json --out basket.json
```

Pak **ručně projdi každý trh**, hlavně řádky označené „ZKONTROLUJ“:

- Jedno slovo, které dělá přes 40 % košíku, bývá homonymum (maďarské „kréta“ znamená i křídu) nebo domácí téma. Nahraď ho jednoznačnou frází nebo ho dej do `domestic` a trh přepočítej: `--only hu`.
- Koncept s nulou obvykle znamená špatně zvolený místní název, ne nulový zájem. Zkus jinou variantu.

## Krok 4 — konkurence

Do `serp_checks` dej 3–4 nejsilnější dotazy pro 3–5 nejlepších kandidátů z košíku a spusť:

```
python3 scripts/serp.py --config config.json --out serp.json
```

Roztřiď domény z první desítky: malé blogy a nadšenecké weby (dají se předběhnout) versus velké portály, srovnávače, Wikipedia a oficiální weby. Podle toho nastav `fit` a poznámku u kandidáta.

## Krok 5 — model

```
python3 scripts/model.py --config config.json --basket basket.json --out model.json
```

Model spočítá u stávajících mutací efektivitu (kliknutí za den na 100 000 hledání v košíku) a z ní tři scénáře: nízký = medián překladových mutací, střední = horní kvartil, vysoký = nejlepší mutace (jen pro kandidáty s `fit`). S méně než čtyřmi vlastními mutacemi použije orientační výchozí hodnoty z konfigurace a napíše to do výstupu — v tom případě to uživateli řekni výslovně.

## Krok 6 — kontroly mimo model

Než cokoli doporučíš, ověř u nejlepších kandidátů:

1. **Jde tam vydělat?** Fungují na trhu partnerské programy, platby, doprava, lokalizace nástrojů, které web používá?
2. **Nekanibalizuje to existující mutaci?** Portugalština pro Portugalsko versus brazilská portugalština, němčina pro Rakousko apod. se řeší spíš nastavením stávající verze než novým překladem.
3. **Kliknutí ze země bez jazykové verze nejsou důkaz poptávky.** Bývají to stávající čtenáři v zahraničí.

## Krok 7 — výstup

Odpověz stručně, daty napřed:

1. Doporučené pořadí (1–3 jazyky) a jednou větou proč.
2. Tabulka kandidátů: košík, kliknutí za den nízký / střední / vysoký, odhad výnosu a návratnosti, konkurence, poznámka.
3. Tabulka kalibrace, aby bylo vidět, z čeho odhad vychází.
4. **Hranice pro vyhodnocení po 30 dnech**, stanovené předem: pokračovat (kolem středního scénáře), zrychlit další jazyk (blízko vysokého), zastavit (pod polovinou nízkého).
5. Postup spuštění: nejdřív 3 zkušební články a kontrola šablon, odkazů a měření; potom celý katalog nebo jen vybraná část, kde má trh poptávku. Rezervace a objednávky označ jazykem od prvního dne, jinak nepůjde výnos mutace změřit.
6. Co je nejisté: malé vzorky, orientační kalibrace, sezóna, neověřené partnerské programy.

Chce-li uživatel dokument, udělej z toho jednu přehlednou stránku; jinak stačí odpověď v chatu a soubory `basket.json`, `serp.json`, `model.json` v pracovní složce.

## Vyhodnocení už spuštěného jazyka

Stejné nástroje slouží i zpětně: porovnej skutečná kliknutí za den a výnos s uloženým `model.json`. Návštěvnost ber ze Search Console nebo z analytiky **očištěné o roboty** (nové jazykové verze jich přitahují nejvíc), čerstvé výnosy sniž o očekávaná storna. Postup je v `references/metodika.md`.
