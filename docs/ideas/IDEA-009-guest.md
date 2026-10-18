---
id: "IDEA-009"
title: "Korlátozott érdeklődői vendégmód"
area: "Fiók és konverzió"
lane: "later-feature"
status: "ötlet"
moscow: "Could"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 4
operations_value: 2
revenue_value: 4
communication_value: 4
risk: "közepes"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF05","MF10"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Próbáld ki a Ringatót regisztráció nélkül"
---

# Korlátozott érdeklődői vendégmód

## Eredeti felvetés

> lehetne Guest belépés megtobb korláttal érdeklődőknek

## Megoldandó probléma

A regisztráció visszatarthatja az érdeklődőket a kipróbálástól.

## Megoldási változatok

- A – Publikus tartalmak felfedezése bejelentkezés nélkül.
- B – Korlátozott vendégfunkciók csak helyi preferenciával.
- C – Vendégélményből biztonságos fiókregisztrációs átadás.

## Technikai hatás, előzetes hipotézis

Public allowlist, auth guard, guest navigáció, prémiumvédelem és konverziós UX.

## Kockázatok és függőségek

Nem azonos a WooCommerce guest checkouttal; privát rendelés/jegy/media nem szivároghat.

## Példa elfogadási feltétel

Guest nem lát személyes fiókadatot vagy fizetett streamet.

## Előzetes ráfordítás és értékelés

- **M · 4–10 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 4, üzemeltetés 2, bevétel 4, kommunikáció 4.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Előbb megismerhetik az alkalmazást, és csak utána regisztrálnak.

## Negyedéves kommunikációs lehetőség

Próbáld ki a Ringatót regisztráció nélkül. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

Publikus tartalmak és konverziós cél meghatározása.

## Kapcsolódás a fejlesztéshez

MF04, MF05, MF10. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
