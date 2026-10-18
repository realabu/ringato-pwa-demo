---
id: "IDEA-016"
title: "Okosóra-kiterjesztés lehetőségeinek felmérése"
area: "Eszközintegráció"
lane: "research"
status: "elemzett"
moscow: "Could"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 2
operations_value: 2
revenue_value: 2
communication_value: 4
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF01","MF06","MF10","MF13"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "Kezet szabadon hagyó zenehallgatási élmény – kizárólag támogatott eszközökön végzett próba után kommunikálható."
---

# Okosóra-kiterjesztés lehetőségeinek felmérése

## Eredeti felvetés

> lehetne esetleg valami okos óra kiterjesztése az app-nak

## Megoldandó probléma

Egyes szülőknek kényelmes lenne a telefon elővétele nélkül látni a következő foglalkozást vagy vezérelni a zenét, de az órás kiterjesztés értéke és a meglévő PWA platformképessége nem igazolt.

## Megoldási változatok

- A – Meglévő telefonos rendszer-értesítések és média-távvezérlés eszközönkénti felmérése, új órás alkalmazás nélkül.
- B – Kompatibilis órákra optimalizált, szűk információs companion-prototípus (következő esemény, lejátszási vezérlés) külön natív watchOS/Wear OS megvalósíthatósági próbával.
- C – Teljesebb, külön telepíthető órás kliens a jogosultsági és fiókellenőrzéshez igazítva; csak igazolt igény, eszközarány és fenntartható támogatás után.

## Technikai hatás, előzetes hipotézis

- A React PWA nem tekinthető automatikusan natív okosóra-alkalmazásnak; az Apple Watch és a Wear OS külön fejlesztési és terjesztési korlátokkal járhat.
- Először támogatott telefon–óra párosokon megvizsgálandó a médiavezérlés, értesítés és esetleges közelgő esemény megjelenése; csak alátámasztott képességre tervezünk.
- Nincs új háttérkövetés, mozgás-, pulzus-, egészség- vagy gyermekadat; minimális token-/eszközjogosultság.

## Kockázatok és függőségek

- Eszköz- és OS-fragmentáció, fejlesztői fiókok, terjesztési és karbantartási költségek; a jelenlegi PWA önmagában nem garantál órás működést.
- Értesítési és médiavezérlési API-k eltérhetnek; telefon nélkül offline órás prémiumlejátszást nem ígérünk.
- Kis felhasználói elérés mellett az órás kliens drága fenntartás lehet.

## Példa elfogadási feltétel

- Dokumentált kompatibilitási mátrix legalább egy-egy kijelölt Apple Watch és Wear OS esethez: mi működik ténylegesen, mi nem.
- A prototípus nem tárja fel a gyermek adatait, nem módosít WooCommerce-jogosultságot, és kijelentkezésnél megszűnik a hozzáférés.
- Fejlesztésre csak a validált funkciólista és a külön költséghatár jóváhagyásával lépünk.

## Előzetes ráfordítás és értékelés

- Besorolás: research, státusz: elemzett, MoSCoW: Could. Nem vállalt MVP-hiba vagy MVP-scope.
- M (4–10 AI-val támogatott fejlesztői munkanap), csak a B változat prototípusára vonatkozó durva nagyságrendi hipotézis, nem árajánlat vagy határidő; a privát forrás auditja nem történt meg.
- Értékhipotézis (1–5): ügyfél 2, üzemeltetés 2, bevétel 2, kommunikáció 4. Kockázat: magas; becslési bizonyosság: alacsony.
- RICE nem számítható: valós reach, impact, confidence és effort bemenet nincs. A C változat extra fejlesztése, tartalomgyártás, jogok, marketing és külső szolgáltatók nincsenek a sávban.

## Virágnak szóló rövid ajánlat

Megvizsgálhatjuk, hogy az óra valóban kényelmesebb eszközzé válhat-e a zenék vezérlésére vagy a foglalkozás előtti emlékeztetőre. Először a telefon meglévő képességeit használjuk ki.

## Negyedéves kommunikációs lehetőség

Kezet szabadon hagyó zenehallgatási élmény – kizárólag támogatott eszközökön végzett próba után kommunikálható. Témaötlet, nem publikált kampány vagy vállalt negyedéves dátum.

## Következő ellenőrzendő lépés

Megkérdezni, mennyien használnak órát és mire; két konkrét eszközpáros működéspróbája a natív fejlesztési döntés előtt.

## Kapcsolódás a fejlesztéshez

MF06/MF10 lejátszó és MF13 értesítési logika; nem módosítja a D06 push-engedélykérési szabályokat. Nem azonos az IDEA-006 TV-cast funkcióval.

MF01–MF14 és a jóváhagyott D-döntések nem változnak; új megvalósítás, adatkezelés, költség és Virágnak szóló kommunikáció csak külön emberi jóváhagyással. PWA-szerkesztői tartalom WordPress/ACF Free forrásból jön.
