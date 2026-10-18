---
id: "IDEA-017"
title: "Zeneovi-modul, gyermekbarát haladás és jelvények"
area: "Zeneovi és család"
lane: "later-feature"
status: "elemzett"
moscow: "Could"
effort_size: "XL"
effort_min_days: 26
effort_max_days: 60
user_value: 5
operations_value: 3
revenue_value: 4
communication_value: 5
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF05","MF07","MF08"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "„A zeneoviban ma ezt fedeztük fel!” – élményalapú, szülőnek címzett pozitív kommunikáció."
---

# Zeneovi-modul, gyermekbarát haladás és jelvények

## Eredeti felvetés

> be lehetne vonni strukturalisan a zene ovit, ott külön funkció a gyerek fejlődési vagy haladási trackje, gyereknek motivációs badge gyűjtés meg haladás jelző.

## Megoldandó probléma

A Zeneovi külön foglalkozástípus és pedagógiai élethelyzet lehet, amelynek programjai, tagsága, részvétele és pozitív visszajelzése nem fér bele automatikusan a Ringató jelenlegi jegy- és eseménylogikájába. A „haladás” nem lehet a gyermekek normatív fejlettségi rangsora.

## Megoldási változatok

- A – Zeneovi önálló menüpont és szerkesztett programinformáció, akár a jelenlegi WordPress-tartalomstruktúrát újrahasznosítva, gyermekprofil és mérés nélkül.
- B – Bejelentkezett család Zeneovi-részvételi története, önkéntes, nem versengő élményjelvények, egyszerű „mit próbáltunk ki?” haladásjelző; szakmai és adatkezelési pilot után.
- C – Külön csoport- és tanári admin, foglalkozásterv és személyre szóló tanulási útvonal, csak Zeneovi működési modell, fenntartói jogosultság és valódi igény igazolása után.

## Technikai hatás, előzetes hipotézis

- Először tisztázandó, a Zeneovi Virág meglévő szolgáltatása, önálló szervezet vagy partner, és a tartalom/részvételi adat kihez tartozik; nem feltételezhető közös tulajdon vagy azonos szerepkör.
- D04-ben az MVP-ben egy WP-fiók egy family_id, gyermeknév/születési adat nem szükséges. B/C esetén a külön gyermektag, tanári jogosultság és többgyermekes családi nézet **új**, engedélyezendő modell, nem csendes V1-módosítás.
- Szerveroldali, egyszer hitelesített részvétel alapján készülhet családi haladásjelzés; ugyanarra a foglalkozásra visszatérés nem dupláz. Nem azonos a pedagógiai megfigyelési naplóval (IDEA-018).
- A menük, tájékoztatók, jelvényszövegek WordPress/ACF Free szerkesztői tartalmak; a bizalmas gyermekprofil és napló nem kerülhet nyilvános content API-ba.

## Kockázatok és függőségek

- Kiskorúakhoz kötődő személyes adatok kezelése; törvényes képviselet, célhoz kötöttség, tárolási idő, szerepkörök és hozzáférés jogi/adatkezelői döntése nélkül csak személyadatmentes bemutató készíthető.
- Jutalmazás ne tegyen fejlődési normát, ne rangsorolja a gyermekeket és ne büntesse az eltérő fejlődést vagy kimaradt alkalmakat.
- Zeneovi-operáció (csoportok, tanárok, díjszabás, jelenléti adatok) jelenleg nincs igazoltan feltérképezve; nagy a scope-növekedés.

## Példa elfogadási feltétel

- A Zeneovi nézet külön kapcsolható, a meglévő Ringató jegy-/bérletjogokat nem módosítja és nem ad ki automatikusan új jogosultságot.
- Egy család csak a saját engedélyezett jelvényeit látja; más gyermek vagy másik család azonosítóinak manipulálása sikertelen.
- Egy ténylegesen igazolt részvétel nem számít kétszer; a jelvény szövege pozitív, nem diagnosztikus és szükség esetén kikapcsolható.

## Előzetes ráfordítás és értékelés

- Besorolás: later-feature; státusz: elemzett, nem elfogadott; MoSCoW: Could. Nem vállalt MVP-hiba vagy alapvető UX-scope.
- XL (26–60 AI-val támogatott fejlesztői munkanap) kizárólag a B változat prototípusának durva, alacsony bizonyosságú hipotézise, nem árajánlat vagy határidő. A privát fejlesztői forrás közvetlen auditja nem történt meg.
- Szubjektív értékhipotézisek (1–5): ügyfél 5, üzemeltetés 3, bevétel 4, kommunikáció 5. Kockázat: magas.
- RICE-pontszám nincs: Reach, Impact, Confidence és Effort megalapozott bemenetei hiányoznak. A C változat, külső szolgáltató, pedagógiai tartalom, fizikai előállítás, marketing és üzemeltetés külön becslendő.

## Virágnak szóló rövid ajánlat

Ha a Zeneovi is megjelenik az alkalmazásban, a család egy helyen követheti az alkalmakat, és a gyerekek örömteli, személyes jelvényekkel idézhetik fel a közös zenélést. Nem teljesítményvizsgát vagy fejlődési rangsort építünk.

## Negyedéves kommunikációs lehetőség

„A zeneoviban ma ezt fedeztük fel!” – élményalapú, szülőnek címzett pozitív kommunikáció. Kommunikációs hipotézis, nem jóváhagyott publikáció, megrendelés vagy vállalt dátum.

## Következő ellenőrzendő lépés

A Zeneovi szervezeti/üzleti határa, a tanári feladatok, a tényleges gyermekadat-igény és a szülői beleegyezés folyamata tisztázandó, mielőtt profil készül.

## Kapcsolódás a fejlesztéshez

Kapcsolódik IDEA-007 családi jutalmazáshoz, IDEA-018 védett pedagógiai naplóhoz, IDEA-019 oklevelekhez; de az IDEA-017 az alap Zeneovi modul és gyermekbarát élménykövetés. MF04/05/07/08 bázis, egyik elfogadott D04 vagy D05 szabályt sem írja át.

A vállalt MF01–MF14 és a jóváhagyott D-döntések változatlanok. Új gyermekadat, új integráció, külső költség és szerkesztői/marketingközlés csak külön emberi jóváhagyás után. A PWA szerkesztői tartalmai WordPressből, ACF Free mezőkből kezelendők.
