---
id: "IDEA-001"
title: "Önkiszolgáló QR-belépési állomás"
area: "Beléptetés"
lane: "later-feature"
status: "ötlet"
moscow: "Could"
effort_size: "L"
effort_min_days: 11
effort_max_days: 25
user_value: 5
operations_value: 5
revenue_value: 2
communication_value: 5
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF07","MF08","MF14"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Gyorsabb és kényelmesebb érkezés"
---

# Önkiszolgáló QR-belépési állomás

## Eredeti felvetés

> jó lenne később megoldani hogy a foglalkozáskor egy staff nélküli telefon folyamatosan okvasson es az alá tartott jegyeket bérleteket értékelje az ugyfelnel is jelezze zölddel pirossal az ervenyessegte es Virag lássa kik es hányan léptek be eddig.

## Megoldandó probléma

Staff nélkül használható, gyors érkeztetés és élő létszám-áttekintés.

## Megoldási változatok

- A – Felügyelt, folyamatos kamerás olvasó egyszerű eredményjelzéssel.
- B – Kioszk automatikus inspect/redeem folyamattal és zöld/piros állapottal.
- C – Több kioszkos, valós idejű belépési dashboard Virágnak.

## Technikai hatás, előzetes hipotézis

PWA scanner, kioszk-hitelesítés, Core inspect/redeem, valós idejű állapot-API, idempotencia és szerveroldali audit.

## Kockázatok és függőségek

Eszközbiztonság, QR-fotó, duplázás, hibás hálózat, érzékeny személyes adatok kijelzése; az automatikus beváltás külön vizsgálatot igényel.

## Példa elfogadási feltétel

Párhuzamos scan és visszatérés nem fogyaszt újra, az élő összesítő szerverrekordokból épül.

## Előzetes ráfordítás és értékelés

- **L · 11–25 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 5, üzemeltetés 5, bevétel 2, kommunikáció 5.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Kevesebb sorban állás, több figyelem a családokra, az érkezéseket Virág élőben követheti.

## Negyedéves kommunikációs lehetőség

Gyorsabb és kényelmesebb érkezés. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

Egy felügyelt helyszíni pilot és biztonsági próba.

## Kapcsolódás a fejlesztéshez

MF07, MF08, MF14. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
