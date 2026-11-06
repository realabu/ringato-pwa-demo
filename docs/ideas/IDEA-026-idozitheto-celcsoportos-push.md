---
id: "IDEA-026"
title: "Célcsoportos pushkampányok előre időzített küldése"
area: "Értesítések és kampánymenedzsment"
lane: "later-feature"
status: "elemzett"
moscow: "Should"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 4
operations_value: 5
revenue_value: 4
communication_value: 4
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF13"]
created: "2026-11-06"
updated: "2026-11-06"
origin: "Szabad szöveges felhasználói ötlet – 2026-11-06"
communication_angle: "„Készítsd elő a hétvégi családi ajánlót!” – Virág időzített, jóváhagyott üzenetekkel dolgozhat."
---

# Célcsoportos pushkampányok előre időzített küldése

## Eredeti felvetés

> időzíthető push küldés célcsoportnak

## Megoldandó probléma

Virág WordPress-adminból jelenleg kézzel előnézheti és indíthatja a kampányt egyéni felhasználóknak, egy vagy több saját csoportnak vagy minden regisztráltnak. Jó lenne a kampányt előre összeállítani és meghatározott időpontban automatikusan kiküldeni anélkül, hogy Virágnak akkor be kellene lépnie. Ez nem azonos az eseményállapotból automatikusan kiváltott IDEA-025 emlékeztetővel.

## Megoldási változatok

- **A** – Kézzel indítható meglévő D06 kampány felületen dátumos „küldés később” mentés, időzítés csak tervezetként; a tényleges küldést továbbra is Virág indítja el, új job nélkül.
- **B** – WordPress-adminban dátum/időzóna szerinti ütemezett kampány, állapotokkal (piszkozat / jóváhagyva és ütemezve / elküldve / visszavonva / sikertelen), szerkesztés/lemondás küldés előtt, idempotens háttérküldéssel; ajánlott első valódi kiterjesztés.
- **C** – Ismétlődő vagy több lépéses kampánysorozatok csoportonként, opcionális időzóna/gyakorisági preferenciával, előnézeti és auditfolyamattal; csak külön üzleti/adatkezelési döntéssel.

## Technikai hatás, előzetes hipotézis

- A jóváhagyott D06 WordPress Users/user_meta címzettcsoport-kezelés és kampányelőnézet újrahasznosul. A meglévő felület szövegeinek és mezőinek módosítása WordPress-adminon belül történjen; ne készüljön új mobiladmin.
- Egy kampányhoz rögzített tervezett Europe/Budapest helyi időpont, ütemezési verzió, küldési státusz, audit és egyedi kiküldési kulcs; párhuzamos job nem dupláz, és a megerősített küldés csak egyszer kerül a fiókok értesítési előzményeibe.
- Külön eldöntendő, hogy a célcsoporttagság pillanatképe jóváhagyáskor vagy a tényleges küldés előtt keletkezzen; a jelenlegi D06 küldéskori deduplikált címzettpillanatképét explicit módon megőrizendőnek javasoljuk, ha nincs más jóváhagyott döntés.
- WP-Cron / Action Scheduler terhelési és késési próba, idempotens retry, külön kezelendő küldéskori opt-out, törölt eszköz, módosult csoport és D12 adatvédelmi feladatok; nem küldünk háttérben inaktív vagy elutasított push-előfizetésre.
- Nem keverendő a D13 kézi szavazásnyitással/zárással és az új szavazásról tiltott automatikus pushküldéssel; külön csak marketingkampányként kezelhető a D06 szabályai szerint, ha azt Virág kifejezetten létrehozza.

## Kockázatok és függőségek

- Rossz időzóna, áramszünet, késő cron, több példányról párhuzamos futás, utólag törölt vagy megváltozott célcsoport, végleges szerkesztés-védelem.
- Tervezett kampány jogszerű célzás és releváns kommunikációs hozzájárulás nélkül; felnőtt címzettekre, jóváhagyott csoportokra korlátozva, gyerekadatok nélkül.
- Túl sűrű kampányok és együttes automatikus eseményemlékeztetők; közös frekvencialimit későbbi döntés tárgya. A web push tényleges mobilkézbesítése nem garantált.

## Példa elfogadási feltétel

- Virág képes kampányt előre ütemezni, még küldés előtt módosítani vagy visszavonni; a szerkesztett/lemondott kampány nem küldődik tévesen.
- Ugyanazon ütemezett kampány párhuzamos jobok és újrapróbálkozás mellett is legfeljebb egy címzett-receiptet hoz létre fiókonként; a kézi D06 küldés eredménye változatlan.
- Küldéskori célcsoport-pillanatkép, deduplikáció, hozzáférés-ellenőrzés, push-opt-in és audit tesztelhető, nem kap más csoport titkos adatait a címzett.
- Időzóna/DST, elmaradt job, hibás push eszköz és cron-késés esetén dokumentált, ellenőrizhető státusz jelenik meg WordPress-adminban.

## Előzetes ráfordítás és értékelés

- **Besorolás:** later-feature; MoSCoW Should; státusz elemzett (nem elfogadott fejlesztési megrendelés).
- **Durva hipotézis:** M (4–10 AI-val támogatott munkanap) az első valós B-variáns prototípusára, a WordPress/PWA meglévő implementációjának auditja nélkül. Külső díj, marketing, üzemeltetés, licenc és teljes kiadás nincs benne. Becslési bizonyosság alacsony; nem ár vagy határidő.
- **Szubjektív értékhipotézis (1–5):** ügyfél 4, üzemeltetés 5, bevétel 4, kommunikáció 4. Kockázat: közepes. RICE nincs, mert a reach, impact, confidence és effort megalapozott számai hiányoznak.

## Virágnak szóló rövid ajánlat

Virág előre elkészítheti a családoknak szóló üzeneteket, kiválaszthatja a WordPressben kezelt csoportokat, majd nyugodtan rábízhatja az előre egyeztetett időpontot a rendszerre. A küldést előre jóváhagyja, és szükség esetén visszavonhatja.

## Negyedéves kommunikációs lehetőség

„Készítsd elő a hétvégi családi ajánlót!” – Virág időzített, jóváhagyott üzenetekkel dolgozhat. Nem jóváhagyott kommunikáció, kampány vagy vállalt negyedéves szállítás.

## Következő ellenőrzendő lépés

Küldéskori címzettpillanatkép, időzóna, szerkesztési zárolás és cron megbízhatósága tisztázandó, majd egy tesztkampány ütemezése és visszavonása.

## Kapcsolódás a fejlesztéshez

D06/MF13 ma kézi küldést és kézzel kezelt WP-csoportokat biztosít. Ez a javaslat csak kézzel jóváhagyott kampány későbbi automatikus **időzített végrehajtása**, nem automatikus célcsoport-képzés. IDEA-025 a programspecifikus trigger, és a két időzítő ütközését későbbi szabály kezelheti.

A már elfogadott MF01–MF14 és D01–D13 döntések változatlanok. Új automatikus művelet, időzítés, személyesadat-kezelés, külső költség és TV/platformterjesztés csak külön megrendelői döntés után.
