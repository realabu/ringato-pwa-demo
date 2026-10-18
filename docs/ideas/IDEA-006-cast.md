---
id: "IDEA-006"
title: "Videó és audio küldése TV-re"
area: "Média"
lane: "later-feature"
status: "ötlet"
moscow: "Could"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 4
operations_value: 1
revenue_value: 3
communication_value: 4
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF06","MF10"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Ringató a tévén"
---

# Videó és audio küldése TV-re

## Eredeti felvetés

> lehetne hogy a videót streamelje arra alkalmas eszközre pl tv vagy Apple tv vagy Google chromecast vagy hasonloakra

## Megoldandó probléma

Sok család közös tévén vagy hangrendszeren szeretne lejátszani.

## Megoldási változatok

- A – Natív AirPlay képességek használata kompatibilis eszközön.
- B – Google Cast integráció támogatott böngészőkön.
- C – Többplatformos eszközválasztó és lejátszásvezérlés.

## Technikai hatás, előzetes hipotézis

AirPlay és Cast SDK, vevőeszköz, protected stream grant, eszközmátrix és valós tesztek.

## Kockázatok és függőségek

iOS PWA és Android eltérései, tokenvédelem a fogadó eszközön és változó SDK-k.

## Példa elfogadási feltétel

Igazolt támogatott eszközökön működik, a prémium forrás nem válik publikussá.

## Előzetes ráfordítás és értékelés

- **L · 11–25 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 4, üzemeltetés 1, bevétel 3, kommunikáció 4.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Közös Ringató-élmény a családi tévé nagy képernyőjén.

## Negyedéves kommunikációs lehetőség

Ringató a tévén. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

Valós készülékmátrix, nem univerzális cast-ígéret.

## Kapcsolódás a fejlesztéshez

MF06, MF10. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
