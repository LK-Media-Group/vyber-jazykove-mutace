# Metodika a poučení

## Proč košík témat
Počet mluvčích ani velikost ekonomiky výsledek nepředpovídají. Velké světové jazyky často končí na chvostu výnosu na článek, protože v nich je obrovská konkurence, zatímco menší trhy se slabší první stránkou Googlu dopadají výrazně lépe. Rozhoduje, jestli tamní lidé hledají stejná témata, jaká web už má, a jestli se dá předběhnout konkurence. Košík proto měří poptávku po tom, co web **už má**, stejnou sadou konceptů na všech trzích.

## Sestavení košíku
- 10–15 konceptů; méně je náchylné na jednu odchylku, víc už pořadí nemění.
- Vybírej témata, která webu skutečně nosí návštěvnost a peníze, ne ta, která by sis přál.
- Na koncept 1–3 varianty a bere se maximum. Sčítání variant by zvýhodnilo jazyky s více pravopisnými podobami.
- Stejný koncept musí znamenat totéž na všech trzích. Obecné slovo („pojištění“) nahraď přesným („cestovní pojištění“).

## Typické chyby
- **Homonyma.** „kréta“ znamená v maďarštině i křídu a hledanost je pak mnohonásobně vyšší než u ostrova. Vždy projdi čísla po jednotlivých konceptech; u podezřelých použij jednoznačnou frázi.
- **Domácí témata.** Národní park je pro obyvatele dané země domácí výlet, ne zahraniční cesta. Vyřaď a normalizuj, jinak trh vypadá větší, než je.
- **Domácí komerční dotazy.** Obecný dotaz typu „půjčovna aut“ může na velkém trhu mířit hlavně na domácí služby, které web nenabízí.
- **Kliknutí ze zahraničí.** Návštěvy ze země, pro kterou web nemá jazykovou verzi, bývají stávající čtenáři na cestách, ne místní poptávka.
- **Úroveň angličtiny.** Hypotéza „kde umí anglicky, překlad nepotřebují“ se v praxi nepotvrzuje; i na trzích s výbornou angličtinou lidé hledají a čtou v mateřštině.
- **Kódy.** Kód jazyka v DataForSEO nemusí sedět se zkratkou webu (norština `nb`). Ověř přes `check_access.py --find`.
- **Makrodata bez košíku.** Statistiky výjezdů, útrat nebo kupní síly umí doporučit trh, který po změření košíku a konkurence spadne v pořadí o několik míst.

## Kalibrace
Efektivita = kliknutí z vyhledávání za den ÷ (košík ÷ 100 000).

- Původní jazyk webu a jazyky jemu velmi blízké mají efektivitu řádově vyšší než překlady. Do scénářů nepatří (`"native": true`).
- Mezi překladovými mutacemi téhož webu bývá několikanásobný rozdíl. Proto tři scénáře, ne jedno číslo.
- Do scénářů počítej jen mutace starší aspoň 2–3 měsíce; čerstvé jsou ještě v náběhu.
- Vysoký scénář dávej jen trhům s tematickou shodou a slabou první stránkou.
- Výchozí hodnoty v `reference_efficiency` jsou hrubé orientační pásmo pro web bez vlastních mutací. Závisí na autoritě webu a oboru; mluv pak o řádu, ne o čísle, a po spuštění první mutace je nahraď vlastním měřením.

## Přepočet na peníze
Výnos na kliknutí = výnos kanálu ÷ kliknutí z vyhledávání za stejné období. `value_multiplier` upravuje hodnotu objednávky na trhu (bohatší trhy výš, trhy s bariérami níž). Odhad výnosu je hrubší než odhad kliknutí; konverze se mezi jazyky běžně liší až dvojnásobně.

## Co od modelu čekat
Model spolehlivě určí pořadí kandidátů a řád výsledku. Skutečnost se od středního scénáře běžně liší o desítky procent oběma směry. Na rozhodnutí „který jazyk dřív“ to stačí; na rozpočet s přesností na desítky procent ne.

## Hranice a spuštění
- Hranice si napiš před spuštěním a odvoď je ze scénářů: kolem středního scénáře pokračovat, blízko vysokého zrychlit další jazyk, pod polovinou nízkého zastavit. Vyhodnoť po 30 dnech.
- Začni třemi zkušebními články, zkontroluj šablony, měnu, odkazy, měření.
- U vzdálenějších trhů přelož jen část katalogu, která tam má poptávku, a vynech témata, která jsou pro trh domácí.
- Počítej s údržbou: každý jazyk znamená další opravy a aktualizace. Levný první překlad může být drahý na provoz.

## Zpětné vyhodnocení
- **Roboti.** Surová návštěvnost z analytiky nových mutací bývá z velké části automatická, protože čerstvé stránky procházejí roboti. Ber kliknutí ze Search Console, nebo návštěvy očisti: přímé návštěvy bez zapojení nepočítej a kombinace země × měsíc s průměrnou dobou pod 5 s vyřaď.
- **Storna.** Čerstvé výnosy jsou nadhodnocené; trhy, kde lidé nakupují s dlouhým předstihem, ruší víc.
- **Poměry.** Sleduj výnos na 1 000 návštěv a výnos na článek za měsíc, ne jen součty. Rozlož výnos na konverzi a průměrnou hodnotu.
- **Malé vzorky.** Pod zhruba 50 objednávek nebo rezervací z poměrů nic nevyvozuj.
