---
id: "IDEA-005"
title: "Automatikus audioverzió videókból"
area: "Média"
lane: "later-feature"
status: "ötlet"
moscow: "Could"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 4
operations_value: 4
revenue_value: 2
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
communication_angle: "Ringató csak hanggal"
---

# Automatikus audioverzió videókból

## Eredeti felvetés

> jó lenne ha a videokbol esetleg automatikusan tudna csak Audiot generálni

## Megoldandó probléma

A videók hangja gyakran képernyő nélkül is hasznos, de külön audioformátum nem mindig elérhető.

## Megoldási változatok

- A – Audio-only lejátszás ugyanabból a médiastreamből.
- B – Admin által indított és jóváhagyott konverzió.
- C – Automatikus, háttérben előálló audio szerkesztői jóváhagyással.

## Technikai hatás, előzetes hipotézis

Bunny Stream audio-only teszt, konverzió/storage, metadata és jogosultságkezelés.

## Kockázatok és függőségek

Nem minden videó érthető hangként; költségek és prémium fájl védelme.

## Példa elfogadási feltétel

Az audio ugyanazt a jogosultságot igényli, mint a forrásvideó, és minősége ellenőrzött.

## Előzetes ráfordítás és értékelés

- **M · 4–10 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 4, üzemeltetés 4, bevétel 2, kommunikáció 4.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Ugyanaz a Ringató-tartalom képernyő nélkül is elkíséri a családot.

## Negyedéves kommunikációs lehetőség

Ringató csak hanggal. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

Audio-only stream vs. új fájl előállítása külön becsülendő.

## Kapcsolódás a fejlesztéshez

MF06, MF10. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
