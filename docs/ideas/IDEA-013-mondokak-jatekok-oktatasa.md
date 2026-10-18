---
id: "IDEA-013"
title: "Mondókák és játékok tanulása a médiatárban"
area: "Oktatás és média"
lane: "later-feature"
status: "elemzett"
moscow: "Should"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 5
operations_value: 3
revenue_value: 3
communication_value: 5
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF05","MF10"]
created: "2026-10-19"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-19"
communication_angle: "Heti „Tanuld meg ezt a mondókát!” ajánló, először kézzel szerkesztett WordPress-tartalomból."
---

# Mondókák és játékok tanulása a médiatárban

## Eredeti felvetés

> lehetne oktatás workshop rész vagy media szűrő címke ami bemutatja a játékokat tanítja a mondokakat

## Megoldandó probléma

A szülő videót vagy hangfelvételt talál, de nem feltétlenül érti, hogyan játssza el a mondókát vagy mozdulatsort otthon, illetve hogyan keressen kifejezetten tanító tartalmat. A puszta címke és az új workshoptermék eltérő léptékű fejlesztés.

## Megoldási változatok

- A – WordPressből szerkeszthető „Mondókatanulás”, „Így játsszuk” címkék és szűrők a meglévő médián, rövid leírással.
- B – Lépésről lépésre tanító videó/mondókalap, mozdulat- és életkori ajánlással, kapcsolódó hanganyaggal és tematikus gyűjteménnyel (első ajánlott termékverzió).
- C – Szerkesztett mini-kurzus vagy élő workshop, saját részvételi feltételekkel és opcionális WooCommerce-termékkel; külön üzleti validáció után.

## Technikai hatás, előzetes hipotézis

- Az MF10 médiametadata/taxonómia és kereső logika bővítése; ACF Free szerkesztői szövegek/kapcsolatok, adminban kezelhető címkék.
- A videó és hanganyag marad a meglévő Bunny Stream jogosultsági modellben; új workshop-jogosultság/értékesítés csak külön döntésből.
- A címkék nem automatikus beszéd- vagy tartalomelemzésből származnak; szerkesztő által ellenőrzött pedagógiai leírás és megfelelő tartalomhasználati jog szükséges.

## Kockázatok és függőségek

- Helytelenül életkorhoz rendelt gyakorlat vagy pontatlan mozdulatleírás; a szakmai tartalmat Virág hagyja jóvá.
- Tartalom-előállítás, feliratozás és videószerkesztés külön ráfordítás; szerzői jogok és előfizetői hozzáférés tisztázandó.
- A workshop fogalma nem jelenti automatikusan időpontfoglalás, online élőóra vagy új fizetési rendszer megrendelését.

## Példa elfogadási feltétel

- Egy WordPressben címkézett oktatóvideó a felhasználónál a megadott szűrővel megtalálható; nem kap téves címkét másik tartalom.
- A leírás és oktatói instrukció WordPress-adminból, frontend build nélkül változtatható, a védett lejátszás nem kerülhető meg.
- A tartalom lehetőség szerint kis képernyőn, bekapcsolt felirattal és hang nélküli előnézetben is érthetően tájékozódható.

## Előzetes ráfordítás és értékelés

- Besorolás: later-feature, státusz: elemzett, MoSCoW: Should. Nem vállalt MVP-hiba vagy MVP-scope.
- M (4–10 AI-val támogatott fejlesztői munkanap), csak a B változat prototípusára vonatkozó durva nagyságrendi hipotézis, nem árajánlat vagy határidő; a privát forrás auditja nem történt meg.
- Értékhipotézis (1–5): ügyfél 5, üzemeltetés 3, bevétel 3, kommunikáció 5. Kockázat: közepes; becslési bizonyosság: alacsony.
- RICE nem számítható: valós reach, impact, confidence és effort bemenet nincs. A C változat extra fejlesztése, tartalomgyártás, jogok, marketing és külső szolgáltatók nincsenek a sávban.

## Virágnak szóló rövid ajánlat

Segítsünk a szülőknek nemcsak hallgatni, hanem megtanulni és otthon is játszani a Ringató-mondókákat. Először a meglévő médiát rendszerezzük; külön workshopot csak kimért érdeklődés esetén fejlesztünk.

## Negyedéves kommunikációs lehetőség

Heti „Tanuld meg ezt a mondókát!” ajánló, először kézzel szerkesztett WordPress-tartalomból. Témaötlet, nem publikált kampány vagy vállalt negyedéves dátum.

## Következő ellenőrzendő lépés

Egyeztetni 5–10 mintatartalmat, címkézési logikát, megfelelő életkori útmutatást és az első mérhető használati célt.

## Kapcsolódás a fejlesztéshez

Nem duplikátuma az IDEA-002 lejátszási listáknak vagy az IDEA-005 audioverzióknak; azok fogyasztási formátumok. Az IDEA-014 szülői kvízek már önálló interakciók. MF10 médiatár és MF05 katalógus alapok; nem módosítja a vállalt MVP-t.

MF01–MF14 és a jóváhagyott D-döntések nem változnak; új megvalósítás, adatkezelés, költség és Virágnak szóló kommunikáció csak külön emberi jóváhagyással. PWA-szerkesztői tartalom WordPress/ACF Free forrásból jön.
