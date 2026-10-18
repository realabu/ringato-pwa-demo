---
id: "IDEA-008"
title: "Ringató merchandise és ajándékok"
area: "Kereskedelem"
lane: "business-experiment"
status: "ötlet"
moscow: "Could"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 2
operations_value: 2
revenue_value: 4
communication_value: 4
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF05","MF07"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Ringató ajándékötletek"
---

# Ringató merchandise és ajándékok

## Eredeti felvetés

> lehetne valami merchendise shop esetleg. Bár ez inkább webes feature nem biztos hogy ez minket erősít.

## Megoldandó probléma

Kapcsolódó ajándékok értékesíthetők, de lehet, hogy erre elég a már létező WooCommerce.

## Megoldási változatok

- A – Új termékkategória a jelenlegi webshopban.
- B – Merch-kiemelés a PWA terméklistájában.
- C – Ajándékcsomag-landing és tematikus kampány.

## Technikai hatás, előzetes hipotézis

WooCommerce termékadmin, opcionális PWA kártya, checkout regresszió.

## Kockázatok és függőségek

Készlet, teljesítés, beszerzés és ügyfélszolgálat túlmutat a szoftveren.

## Példa elfogadási feltétel

Egyetlen checkout marad; merch nem változtatja meg a jegy/előfizetés-jogosultságot.

## Előzetes ráfordítás és értékelés

- **M · 4–10 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 2, üzemeltetés 2, bevétel 4, kommunikáció 4.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Apró ajándékokkal a Ringató-élmény otthon is folytatódhat.

## Negyedéves kommunikációs lehetőség

Ringató ajándékötletek. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

Előbb webshopos üzleti validáció és csak utána külön PWA scope.

## Kapcsolódás a fejlesztéshez

MF05, MF07. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
