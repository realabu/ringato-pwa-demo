---
id: "IDEA-004"
title: "Offline jegyek, bérletek és médiák"
area: "Offline"
lane: "research"
status: "ötlet"
moscow: "Could"
effort_size: "XL"
effort_min_days: 26
effort_max_days: 60
user_value: 4
operations_value: 4
revenue_value: 3
communication_value: 4
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF07","MF10","MF14"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Ringató útközben is"
---

# Offline jegyek, bérletek és médiák

## Eredeti felvetés

> jó lenne ha offline is működne egy ideig az app legalább a jegyek bérletek kapcsán. De akar valamennyi media is lehetne offline, esetleg előfizetői szinthez kötve.

## Megoldandó probléma

Hálózatkimaradáskor a jegyek és a médiák használhatósága korlátozott.

## Megoldási változatok

- A – Utolsó ismert jegystátusz megjelenítése nem friss jelzéssel, beváltási jog nélkül.
- B – Aláírt, időleges offline beléptetés konfliktus- és duplikációkezeléssel.
- C – Prémium média kontrollált, licencelt offline letöltése és lejárata.

## Technikai hatás, előzetes hipotézis

Service worker, lokális biztonságos tároló, offline bizonyíték, reconciliation, streaming és DRM/licenc vizsgálat.

## Kockázatok és függőségek

Két offline scanner duplázhat; eszközvesztés és prémium letöltések szerződéses korlátja.

## Példa elfogadási feltétel

Offline kijelzés nem állít téves érvényességet; szinkron után nincs dupla redemption.

## Előzetes ráfordítás és értékelés

- **XL · 26–60 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 4, üzemeltetés 4, bevétel 3, kommunikáció 4.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

A Ringató akkor is elérhetőbb, ha az internet éppen gyenge.

## Negyedéves kommunikációs lehetőség

Ringató útközben is. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

Olvasás, valódi offline beváltás és média-letöltés külön PoC.

## Kapcsolódás a fejlesztéshez

MF07, MF10, MF14. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
