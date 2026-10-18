---
id: "IDEA-002"
title: "Több saját és tematikus lejátszási lista"
area: "Média"
lane: "later-feature"
status: "ötlet"
moscow: "Could"
effort_size: "M"
effort_min_days: 4
effort_max_days: 10
user_value: 4
operations_value: 2
revenue_value: 2
communication_value: 4
risk: "alacsony"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF06","MF10"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Saját Ringató lejátszási listák"
---

# Több saját és tematikus lejátszási lista

## Eredeti felvetés

> jó lenne több lejatszasi lista később

## Megoldandó probléma

Az egyetlen lejátszási sor nem őrzi meg külön az esti, utazós és egyéb összeállításokat.

## Megoldási változatok

- A – Több elnevezett, mentett személyes lista.
- B – Virág tematikus ajánlott listái és másolható sablonjai.
- C – Megosztható családi listák külön jogosultságokkal.

## Technikai hatás, előzetes hipotézis

PlayList és PlayListItem adattárolás, React szerkesztő, API, régi sor migrációja.

## Kockázatok és függőségek

Régi lista ne vesszen el, más fiók ne kapjon prémium médiahozzáférést.

## Példa elfogadási feltétel

Két külön lista sorrendje és tartalma kijelentkezés után is megmarad.

## Előzetes ráfordítás és értékelés

- **M · 4–10 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 4, üzemeltetés 2, bevétel 2, kommunikáció 4.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Saját esti és utazós Ringató-válogatások egyetlen mozdulattal.

## Negyedéves kommunikációs lehetőség

Saját Ringató lejátszási listák. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

Egy sor és több lista átmenetét pontosítani.

## Kapcsolódás a fejlesztéshez

MF06, MF10. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
