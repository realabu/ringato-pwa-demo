---
id: "IDEA-015"
title: "Többnyelvű támogatás nem magyar anyanyelvű szülőknek"
area: "Hozzáférhetőség és nyelv"
lane: "later-feature"
status: "elemzett"
moscow: "Should"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 5
operations_value: 3
revenue_value: 4
communication_value: 5
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF05","MF10"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "„Ringató magyarul tanuló családoknak” – először ellenőrzött angol tájékoztató, nem teljes angol Ringató-ígéret."
---

# Többnyelvű támogatás nem magyar anyanyelvű szülőknek

## Eredeti felvetés

> lehetne valamilyen támogatás idegen ajkú szülőknek expatoknak

## Megoldandó probléma

Az idegen nyelvű, Magyarországon élő vagy a tartalmat külföldről elérő szülőknek nehéz lehet az alkalmazás használata, a magyar mondókák megértése és a foglalkozásokon való részvétel. Teljes nyelvi lokalizáció helyett fokozatos segítség is sokat érhet.

## Megoldási változatok

- A – Rövid, WordPressből szerkeszthető angol „hogyan működik?” útmutató, alapvető vásárlási és részvételi információ, kapcsolati segítség.
- B – Választható angol felületi szövegek, a mondókák rövid, jogtisztázott magyarázata és felirat/átirat, kiejtési támpont; ajánlott második lépcső.
- C – Többnyelvű médiaválogatások, célzott új családi onboarding és partneri segítség más nyelveken, megkérdezett célközönség alapján.

## Technikai hatás, előzetes hipotézis

- ACF Free mezők és WordPress szerkesztői workflow több nyelven; statikus UI- és hibaüzenetek, checkout/Barion/WooCommerce folyamat tényleges nyelvi viselkedése külön tesztelendő.
- A hangfelvétel eredeti magyar szövege mellett kulturális magyarázat/transzliteráció külön tartalomtípus lehet; automatikus fordítás legfeljebb szerkesztői piszkozat.
- Képernyőolvasó nyelvi jelölései, mobil szöveghossz, dátum/pénznem és videófelirat kompatibilitása ellenőrizendő.

## Kockázatok és függőségek

- A helyszíni foglalkozások nyelvi befogadóképességéről ne állítsunk általános ígéretet.
- A mondókák fordításának szerzői és pedagógiai megfelelősége egyenként jóváhagyandó; gyenge gépi fordítás félrevezető lehet.
- Teljes checkout- és ügyfélszolgálati lokalizáció nem következik egy angol landingoldal bevezetéséből.

## Példa elfogadási feltétel

- Egy nem magyarul beszélő szülő a fő feladatokat legalább tájékoztatási szinten megérti; magyar módba visszaváltás nem veszít fiókadatot.
- Publikált fordítás visszakereshető a jóváhagyott magyar forráshoz; hiány esetén korrekt nyelvi fallback látszik.
- A belépés, vásárlás, jogosultság és prémiumvédelem nyelvtől függetlenül változatlanul működik.

## Előzetes ráfordítás és értékelés

- Besorolás: later-feature, státusz: elemzett, MoSCoW: Should. Nem vállalt MVP-hiba vagy MVP-scope.
- L (11–25 AI-val támogatott fejlesztői munkanap), csak a B változat prototípusára vonatkozó durva nagyságrendi hipotézis, nem árajánlat vagy határidő; a privát forrás auditja nem történt meg.
- Értékhipotézis (1–5): ügyfél 5, üzemeltetés 3, bevétel 4, kommunikáció 5. Kockázat: közepes; becslési bizonyosság: alacsony.
- RICE nem számítható: valós reach, impact, confidence és effort bemenet nincs. A C változat extra fejlesztése, tartalomgyártás, jogok, marketing és külső szolgáltatók nincsenek a sávban.

## Virágnak szóló rövid ajánlat

A magyar mondókák szépségét azok a családok is könnyebben megtalálhatják, akik még tanulják a nyelvet. Egy kis, angol nyelvű segítséggel kezdünk, és a valós érdeklődés alapján bővítünk.

## Negyedéves kommunikációs lehetőség

„Ringató magyarul tanuló családoknak” – először ellenőrzött angol tájékoztató, nem teljes angol Ringató-ígéret. Témaötlet, nem publikált kampány vagy vállalt negyedéves dátum.

## Következő ellenőrzendő lépés

Interjú néhány nem magyar anyanyelvű szülővel; az első öt kritikus útvonal és a leggyakoribb nyelvi akadály kiválasztása.

## Kapcsolódás a fejlesztéshez

IDEA-013 oktatómédia és IDEA-009 érdeklődői belépési súrlódás kiegészítő témái. MF04–MF05–MF10; külön lokalizációs döntés, nincs automatikus MVP-scope változás.

MF01–MF14 és a jóváhagyott D-döntések nem változnak; új megvalósítás, adatkezelés, költség és Virágnak szóló kommunikáció csak külön emberi jóváhagyással. PWA-szerkesztői tartalom WordPress/ACF Free forrásból jön.
