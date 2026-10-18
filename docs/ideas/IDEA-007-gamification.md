---
id: "IDEA-007"
title: "Önkéntes mérföldkövek és jutalmak"
area: "Elköteleződés"
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
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF06","MF07","MF08","MF11","MF13"]
created: "2026-10-18"
updated: "2026-10-19"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Rendszeresen járó családok elismerése – átlátható, önkéntes hűségjutalom"
---

# Önkéntes mérföldkövek és jutalmak

## Eredeti felvetés

> lehetne esetleg valami gamification pl ki hallgatta a legtöbb médiát ki lépett be a leggyakrabban ki válaszolt a legtöbb kérdésre. A nyertesek kaphatnának valami kedvezményt pl.

> azokat lenne érdemes jutalmazni kuponnal / gamificationnel akik sokat járnak hamar lejarjak a berletuket ezért a sorozatokat kene nézni.

## Megoldandó probléma

A felfedezést ösztönözheti játékos visszajelzés, de a családok nyilvános versenyeztetése kockázatos. A 2026-10-19-i pontosítás célja nem az összesített lejátszások és kattintások versenyeztetése, hanem az **igazolt, rendszeres foglalkozáslátogatási sorozat** és a **rövid idő alatt felhasznált bérlet** elismerése. A bérlet szabály szerinti lejárata (D02) és a jutalomra jogosító gyors felhasználás két külön dolog: a bérlet lejárati idejét nem rövidítjük és nem írjuk át.

## Megoldási változatok

- **A – Privát részvételi sorozatok.** A család csak saját, igazolt foglalkozáslátogatásait látja: például egymást követő látogatott hetek, több sikeres alkalom egy időszakban. Nem versenyeztetünk más családokkal; szünet/betegség esetén a kihívás emberbarát szabályokkal újrakezdhető.
- **B – Gyors bérletfelhasználás elismerése (ajánlott pilot).** Bérlet első érvényes beváltásától az utolsó felhasznált alkalomig mért időtartam; az adott bérlet szabályos összes alkalma a D03 szerint pontosan egyszer számíthat. Az admin állíthat be előzetesen egy objektív időablakot (például 8 alkalom 10 héten belül – **csak szemléltető küszöb, nem elfogadott szabály**), és kivételkezelést. Szerveroldali bérletforrás és check-in alapján, nem kézi frontend-számlálással.
- **C – Virág által jóváhagyott kupon vagy jelvény.** A B feltételt teljesítő család kaphat egyszer használható, korlátozott érvényességű WooCommerce-kuponkódot vagy nem pénzbeli digitális jelvényt. A kedvezmény mértéke, jogosult termékköre, költségkerete és adminisztrációja külön üzleti döntés; nincs automatikus kuponkibocsátás a szabályok jóváhagyása előtt.

## Technikai hatás, előzetes hipotézis

A jelenlegi Core hitelesített check-in és bérletadatainak csak szerveroldali, idempotens aggregálása; D03 szerint ugyanazon eseményre visszatérés nem ad második alkalmat. D02 bérlet-élettartam és felhasználható alkalomszám érintetlen, a gyors felhasználás *elemzési jelzés*, nem új lejárati vagy fizetési logika. A családazonosító D04 szerint családszintű; nincs szükség gyermek szintű profilozásra. Verziózott, adminból beállítható kihívásszabályok, opt-in és naplózott jutalmazás; a kupon a WooCommerce meglévő képességein keresztül jár, idempotens kiosztással és visszaélésvédelemmel. Az eredeti ötlet média-/szavazásalapú mechanikái csak későbbi, külön döntésű alváltozatok; D13 végleges szavazási szabály nem változik.

## Kockázatok és függőségek

Kockázat a gyermekek aktivitásának profilozása, a ranglistákból eredő nyomás, a gyakori megjelenés egészségtelen ösztönzése és az előre nem tervezett kuponköltség. Az igazolt, családszintű részvétel önkéntes elismerése legyen a cél, ne a gyerek teljesítménye vagy az online hallgatási idő hajszolása. Párhuzamos beváltás, QR-visszatérés, manuális korrekció, refund és különböző bérletek összeszámolása duplázást vagy tisztázatlan jogosultságot okozhat; az értékelési időszak és az esetleges szüneteltetési szabály előzetesen rögzítendő. Marketingcélú adatfelhasználást az adatkezelő külön hagyja jóvá.

## Példa elfogadási feltétel

Alapértelmezetten nincs publikus személyes rangsor, az opt-in visszavonható. Ugyanazon foglalkozásra újrabelépés, ismételt webhook vagy kétszer lefutó értékelés nem növelheti a sorozatot, és nem adhat második kupont. Az időablakot hiteles beváltási napokból, rögzített Europe/Budapest szabály szerint számoljuk. Egy bérlet gyors teljes felhasználása egy jutalmazási esemény; új bérlet új jogosultság, de a D02 jogszerű lejárat nem változik. Ki- és visszajelentkezésnél csak a saját család privát kihívásai láthatók; ugyanaz a szavazat nem használható második jutalomra.

## Előzetes ráfordítás és értékelés

- **L · 11–25 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív, validálatlan értékhipotézisek 1–5 a részvételi sorozatok pontosítása után: ügyfél 4, üzemeltetés 3, bevétel 4, kommunikáció 5.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

A rendszeresen hozzánk járó családoknak külön szeretnénk megköszönni a hűségüket. Egy diszkrét, önkéntes sorozatjelzőből indulnánk; ha valóban értékes, Virág előre jóváhagyott WooCommerce-kuponnal is elismerheti a gyorsan felhasznált bérleteket. A gyermekeket nem versenyeztetjük.

## Negyedéves kommunikációs lehetőség

„A közös zenélés sorozatai – köszönjük, hogy visszajártok!” Hűségkampány csak külön szabály- és költségjóváhagyás után; nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

A D02/D03/D04 bérlet- és beléptetési adatokból kézi, anonimizált/tesztadatú mintán igazolni, hogy mérhető-e a valódi részvételi sorozat és a gyors bérletfelhasználás. Virág döntse el a jutalmazás küszöbét, költségplafonját, szünetek kezelését és hogy kupon vagy csak jelvény legyen. A kísérlet MVP-n túli, nem automatikus megrendelés.

## Kapcsolódás a fejlesztéshez

MF07 (jegyek/bérletek és check-in), MF08 (foglalkozásadatok), opcionálisan MF10 (média), MF11 (szavazás) és MF13 (jóváhagyott értesítések). D02/D03/D04/D13 változatlan. IDEA-017 Zeneovi-jelvények, IDEA-019 oklevelek/matricák és IDEA-020 közösségi feed külön modulok, csak jóváhagyott integráció esetén kapcsolódnak. Nem MVP-hiba; lehetséges későbbi fizetős üzleti kísérlet.
