---
id: "IDEA-011"
title: "Közös családi jogosultság, két szülői profil"
area: "Fiók és család"
lane: "later-feature"
status: "ötlet"
moscow: "Could"
effort_size: "XL"
effort_min_days: 26
effort_max_days: 60
user_value: 5
operations_value: 4
revenue_value: 3
communication_value: 5
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF04","MF07","MF08","MF10"]
created: "2026-10-18"
updated: "2026-10-18"
origin: "Szabad szöveges ötlet – 2026-10-18"
communication_angle: "Közös családi Ringató-fiók"
---

# Közös családi jogosultság, két szülői profil

## Eredeti felvetés

> lehetne családi account külön apa-anya account de egy előfizetés csak külön kezelt listák. De közös jegyek bérletek

## Megoldandó probléma

A D04 szerinti V1 egy családhoz egy fiókot rendel; a külön szülői profilok nem osztozhatnak automatikusan a jegyeken.

## Megoldási változatok

- A – Második szülő meghívásos hozzáférése a családi jegyekhez.
- B – Többszereplős családtagság saját listákkal, közös belépőkkel.
- C – Közös prémium előfizetés saját profilokkal és hozzáférés-visszavonással.

## Technikai hatás, előzetes hipotézis

Family membership, meghívó, WP user és family ACL, entitlement scope, személyes média-preferenciák.

## Kockázatok és függőségek

Hozzáférés-visszavonás, családi változások, duplikált belépés és előfizetési licenc.

## Példa elfogadási feltétel

Két szülő ugyanazt a jegyet látja, második beváltás nem dupláz, saját listáik elkülönülnek.

## Előzetes ráfordítás és értékelés

- **XL · 26–60 AI-val támogatott fejlesztői munkanap** (ajánlott változat, rendkívül előzetes hipotézis; nem ár és nem határidő).
- A privát `nmarton/ringato-dev` forráskód közvetlen auditja még nem történt meg; a becslés bizonyossága **alacsony**. Külső szolgáltatói/licenc költség külön vizsgálandó.
- Szubjektív értékhipotézisek 1–5: ügyfél 5, üzemeltetés 4, bevétel 3, kommunikáció 5.
- MoSCoW: Could az ötlettárban, nem jóváhagyott MVP-prioritás. RICE: **nem pontozható** Reach/Impact/Confidence/Effort valós adatai nélkül.

## Virágnak szóló rövid ajánlat

Külön anya- és apa-profilokkal is egy közös Ringató-család.

## Negyedéves kommunikációs lehetőség

Közös családi Ringató-fiók. Témaötlet, nem vállalt szállítási dátum.

## Következő ellenőrzendő lépés

D04 kizárását megőrizni, külön megvalósítási szerződés és adatmodell.

## Kapcsolódás a fejlesztéshez

MF04, MF07, MF08, MF10. Az MF-mérföldkövek és D-döntések nem változnak külön jóváhagyás nélkül.
