---
id: "IDEA-019"
title: "Nyomtatható oklevelek és gyűjthető Ringató-matricák"
area: "Jutalmazás és ajándék"
lane: "business-experiment"
status: "elemzett"
moscow: "Could"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 4
operations_value: 3
revenue_value: 4
communication_value: 5
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF05","MF07","MF08","MF10"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "„Gyűjtsük a közös zenés pillanatokat!” – saját illusztrációval, játékos és nem versenyeztető hangon."
---

# Nyomtatható oklevelek és gyűjthető Ringató-matricák

## Eredeti felvetés

> nyomtatható oklevél a gyerekeknek havonta vagy megvásárolható valamilyen matrica egy ringato virággal “lutra albumba” úgy hogy a foglalkozasra jarassal is össze legyen kapcsolva vagy online hallgatással.

## Megoldandó probléma

A családoknak örömteli, kézzelfogható emlék lehet a rendszeres zenélés: nyomtatható oklevél vagy matricagyűjtő album. A jutalom kiváltó eseménye (részvétel, visszatérés, online zenehallgatás) és a fizikai teljesítés azonban nem azonos a meglévő jegyrendszerrel.

## Megoldási változatok

- A – Havi, önkéntesen letölthető, szülő által nyomtatható általános oklevélsablon, amelyben a gyermek neve helyben adható meg vagy név nélkül is működik.
- B – Ellenőrzött családi részvétel-/lejátszási eseményeken alapuló gyűjthető digitális matricák és opcionálisan nyomtatható albumlapok; lehetőség szerint nincs gyermekprofil szükség.
- C – Fizikai Ringató-matricaalbum és vásárolható/ajándék matricacsomagok WooCommerce-termékként, készlet-, szállítási és gyártási munkával; önálló költség- és márkakoncepció után.

## Technikai hatás, előzetes hipotézis

- A megvalósítás a D03 szerint egyszeresen beváltott, hiteles foglalkozási eseményekből aggregálhat családi részvételt; egy foglalkozásra újra belépés nem ad új jutalmat.
- Online lejátszásnál a kliensindítás nem megbízható fogyasztási bizonyíték; kerülendő a háttérben némán futtatásra ösztönző metrika. Külön engedélyezett, nem túlzott aktivitásjelzés szükséges.
- A generált PDF/nyomtatható anyag csak az adott családnak, kiszivárgó nyilvános token vagy gyermeknév-kötelezettség nélkül. Fizikai termék esetén jelenlegi WC-shop/checkout, nem külön kassza.
- A „Lutra album” létező kereskedelmi gyűjtőalbumként mintául szolgálhat, de annak nevét, grafikáit és matricáit nem másoljuk. Példa: https://www.lidl.hu/c/lutra-album/s10100886; saját Ringató-arculat és felhasználási engedély szükséges.

## Kockázatok és függőségek

- A matricák apró fizikai tárgyak lehetnek; gyermekbiztonsági/életkori figyelmeztetés, csomagolás, gyártás és logisztika külön szakmai feladat.
- Szülő és gyermek túlzott képernyő- vagy lejátszási aktivitásra ösztönzése kerülendő; minőségi közös élményt jutalmazzunk, ne a percek hajszolását.
- Jogvédett márkák és illusztrációk; fizikai gyártás, készletezés, postázás és ügyfélszolgálat költsége nincs az IT-becslésben.
- Kuponok, kedvezmények és más jutalmak az IDEA-007 szabályaival külön egyeztetendők.

## Példa elfogadási feltétel

- Egy hiteles foglalkozás legfeljebb egy jutalmazható eseménynek számít; hibás/refundolt/meg nem történt részvétel nem növeli a gyűjteményt.
- A szülő név nélkül is kérhet nyomtatható oklevelet, idegen család oklevele vagy névadata nem férhető hozzá.
- A digitális gyűjtés fizikai vásárlás nélkül is kipróbálható, és a WC-shopos matrica külön termékként kezelhető, a jegyjogok módosítása nélkül.

## Előzetes ráfordítás és értékelés

- Besorolás: business-experiment; státusz: elemzett, nem elfogadott; MoSCoW: Could. Nem vállalt MVP-hiba vagy alapvető UX-scope.
- L (11–25 AI-val támogatott fejlesztői munkanap) kizárólag a B változat prototípusának durva, alacsony bizonyosságú hipotézise, nem árajánlat vagy határidő. A privát fejlesztői forrás közvetlen auditja nem történt meg.
- Szubjektív értékhipotézisek (1–5): ügyfél 4, üzemeltetés 3, bevétel 4, kommunikáció 5. Kockázat: közepes.
- RICE-pontszám nincs: Reach, Impact, Confidence és Effort megalapozott bemenetei hiányoznak. A C változat, külső szolgáltató, pedagógiai tartalom, fizikai előállítás, marketing és üzemeltetés külön becslendő.

## Virágnak szóló rövid ajánlat

A közös zenélésből legyen kézzelfogható emlék: egy havi oklevél vagy saját Ringató-matricagyűjtemény. Előbb kipróbáljuk a digitális élményt, és csak igény esetén készítünk fizikai albumot.

## Negyedéves kommunikációs lehetőség

„Gyűjtsük a közös zenés pillanatokat!” – saját illusztrációval, játékos és nem versenyeztető hangon. Kommunikációs hipotézis, nem jóváhagyott publikáció, megrendelés vagy vállalt dátum.

## Következő ellenőrzendő lépés

Dönteni a szülőknek szóló név nélküli oklevél pilotról, a résztvevő családi események megengedett használatáról és a saját arculatú album jogosultságairól.

## Kapcsolódás a fejlesztéshez

IDEA-007 jutalomlogika és IDEA-017 Zeneovi-jelvények ide kapcsolódnak; IDEA-008 fizikai merchandise a shopcsatorna, de a részvételhez kötött gyűjtemény önálló élmény.

A vállalt MF01–MF14 és a jóváhagyott D-döntések változatlanok. Új gyermekadat, új integráció, külső költség és szerkesztői/marketingközlés csak külön emberi jóváhagyás után. A PWA szerkesztői tartalmai WordPressből, ACF Free mezőkből kezelendők.
