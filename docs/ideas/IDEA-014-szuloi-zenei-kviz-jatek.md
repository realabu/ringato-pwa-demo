---
id: "IDEA-014"
title: "Szülőknek szóló mondókás és zenei mini-játékok"
area: "Tanulás és interakció"
lane: "later-feature"
status: "elemzett"
moscow: "Could"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 4
operations_value: 3
revenue_value: 3
communication_value: 5
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF06","MF10"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "Heti szülői zenei fejtörő és a hozzá kapcsolódó mondóka bemutatása."
---

# Szülőknek szóló mondókás és zenei mini-játékok

## Eredeti felvetés

> lehetne valami beépített játék a szülőnek is a mondokakrol vagy ismeretterjesztő dolog zenéről vagy nevelesrol

## Megoldandó probléma

A szülők passzívan fogyaszthatnak tartalmat, de nincs játékos visszajelzés arról, mennyire ismerik a mondókákat, ritmusokat vagy az életkornak megfelelő zenei játékokat. A szülői tanulás nem azonos a gyerek teljesítményének mérésével.

## Megoldási változatok

- A – Rövid, szerkesztett 3–5 kérdéses kvízkártyák a média mellett, bejelentkezés és ranglista nélkül.
- B – Ritmusfelismerő/mondókakiegészítő mini-játékok, válasz utáni magyarázattal és opcionális saját haladással; ajánlott kísérlet.
- C – Szakértői zenei és gyermeknevelési mikrotanfolyamok kihívásokkal, szülőnek szóló virtuális jelvényekkel; külön pedagógiai felülvizsgálattal.

## Technikai hatás, előzetes hipotézis

- Kvízkérdés-tár WordPressben, szerkesztői workflow-val és ACF Free kompatibilis mezőkkel; tartalom és helyes válasz nem a React-szövegekbe beégetve.
- Véletlenszerű kérdés és pontozás egymástól elválasztva; privát, opcionális progresshez új szerveroldali jogosultság és adattakarékosság kell.
- Hang-/ritmusfeladatnál böngészős médiatámogatás, feliratos/hang nélkül megoldható alternatíva és mobil érintéses UX szükséges.

## Kockázatok és függőségek

- Ne legyen gyermekdiagnosztika, nevelési tanácsként túlzó állítás vagy szégyenítő ranglista.
- A D13 „Virág kérdezi” szavazás végleges, adminra korlátozott eredményei nem használhatók kvíz- és eredményrendszerként; külön modult igényel.
- Játékos pontszámhoz nem jár automatikusan pénzbeli kupon; az IDEA-007 kuponpolitikája külön.

## Példa elfogadási feltétel

- Szülő válaszolhat, javíthat és rövid magyarázatot olvashat; a kvíz nem módosítja a D13 szavazatot.
- A kérdések szerkeszthetők, hibás/nem publikált kérdés nem jelenik meg; az akadálymentes alternatíva a hangos feladatnál elérhető.
- Privát eredmény nem látható más felhasználó számára, kijelentkezés után nem szivárog klienscache-ből.

## Előzetes ráfordítás és értékelés

- Besorolás: later-feature, státusz: elemzett, MoSCoW: Could. Nem vállalt MVP-hiba vagy MVP-scope.
- L (11–25 AI-val támogatott fejlesztői munkanap), csak a B változat prototípusára vonatkozó durva nagyságrendi hipotézis, nem árajánlat vagy határidő; a privát forrás auditja nem történt meg.
- Értékhipotézis (1–5): ügyfél 4, üzemeltetés 3, bevétel 3, kommunikáció 5. Kockázat: közepes; becslési bizonyosság: alacsony.
- RICE nem számítható: valós reach, impact, confidence és effort bemenet nincs. A C változat extra fejlesztése, tartalomgyártás, jogok, marketing és külső szolgáltatók nincsenek a sávban.

## Virágnak szóló rövid ajánlat

A szülők rövid, vidám játékokon keresztül ismerhetik meg a mondókákat és a zenei nevelés alapjait – versenyeztetés és kötelező szereplés nélkül.

## Negyedéves kommunikációs lehetőség

Heti szülői zenei fejtörő és a hozzá kapcsolódó mondóka bemutatása. Témaötlet, nem publikált kampány vagy vállalt negyedéves dátum.

## Következő ellenőrzendő lépés

Virággal és szakmai közreműködővel egy 5 kérdéses, tanító célú pilot összeállítása, a visszajelző szövegek validálása.

## Kapcsolódás a fejlesztéshez

Az IDEA-013 tanító médiacímkéi a tartalmi alapot adhatják; IDEA-007 csak későbbi önkéntes jutalmazás. MF04/MF06/MF10 kapcsolódás, D13 szavazás változatlan.

MF01–MF14 és a jóváhagyott D-döntések nem változnak; új megvalósítás, adatkezelés, költség és Virágnak szóló kommunikáció csak külön emberi jóváhagyással. PWA-szerkesztői tartalom WordPress/ACF Free forrásból jön.
