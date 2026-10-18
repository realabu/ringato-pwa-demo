---
id: "IDEA-003"
title: "Egyszerűbb staff QR-belépési UX"
area: "Beléptetés"
lane: "mvp-review"
status: "ötlet"
moscow: "Should"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 4
operations_value: 5
revenue_value: 1
communication_value: 3
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF07","MF08","MF14"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Gyorsabb QR-belépés"
---

# Egyszerűbb staff QR-belépési UX

## Eredeti felvetés

> jó lenne ha a qr beleptetes egyszerűbb Ux lenne körülményes kódot es eseményt választani meg be másolni. Lehet a qr-be kene valami esemény azonosító vagy deeplink. Vagy az események közül időben a legközelebbi alapertelmezetten előre választott legyen módosítás esetén a következő beolvasasra jegyezze meg. Vagy valami hasonló Ux upgrade

## Megoldandó probléma

A staff kamerás beolvasása ne igényeljen rendszeres kézi kódmásolást és sok eseményválasztást.

## Megoldási változatok

- A – A legközelebbi esemény előválasztása és az alapfolyamat gyorsítása.
- B – Utolsó esemény megjegyzése a következő beolvasásnál.
- C – QR/deeplink kontextusajánlás szigorú szerveroldali validációval.

## Technikai hatás, előzetes hipotézis

StaffCheckinPage, kamera, staff események, időablak és kontextus UX-auditja.

## Kockázatok és függőségek

QR-ben az eseményazonosító nem lehet jogosultság igazolása. Előbb tisztázni, mi az MVP-ben már vállalt hiba vagy hiányosság.

## Példa elfogadási feltétel

Valós telefonon a normál beléptetés kódmásolás nélkül teljesíthető, az esemény szükség esetén gyorsan változtatható.

## Előzetes ráfordítás és értékelés

- **M · 4–10 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 4, üzemeltetés 5, bevétel 1, kommunikáció 3.
- MoSCoW: Should az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Kevesebb koppintás, gördülékenyebb foglalkozáskezdés.

## Negyedéves kommunikációs lehetőség

Gyorsabb QR-belépés. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

MF07/MF08 és T24 kód- és eszközteszttel eldönteni, hibajavítás vagy új feature.

## Kapcsolódás a fejlesztéshez

MF07, MF08, MF14. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
