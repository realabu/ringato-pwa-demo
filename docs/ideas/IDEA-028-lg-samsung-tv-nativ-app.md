---
id: "IDEA-028"
title: "Natív LG webOS és Samsung Tizen TV-alkalmazás"
area: "TV és média"
lane: "research"
status: "elemzett"
moscow: "Could"
effort_size: "XL"
effort_min_days: 26
effort_max_days: 60
user_value: 4
operations_value: 2
revenue_value: 3
communication_value: 5
risk: "magas"
estimate_confidence: "alacsony"
rice_reach: null
rice_impact: null
rice_confidence: null
rice_effort: null
related_milestones: ["MF01","MF06","MF09","MF10"]
created: "2026-11-06"
updated: "2026-11-06"
origin: "Szabad szöveges felhasználói ötlet – 2026-11-06"
communication_angle: "„Ringató a családi nagyképernyőn” – csak igazolt kompatibilitás és jóváhagyott TV-megjelenés esetén."
---

# Natív LG webOS és Samsung Tizen TV-alkalmazás

## Eredeti felvetés

> lg tv, samsung tv applikáció

## Megoldandó probléma

A családok egy része szeretné a Ringató médiát közvetlenül az LG vagy Samsung okostévéjén megnyitni és távirányítóval vezérelni, telefonos casting nélkül. Ez nem automatikus PWA támogatás: az LG webOS és Samsung Tizen külön alkalmazáscsomagolási, böngésző- és terjesztési feltételeket írhat elő. Előbb meg kell állapítani a releváns eszközállományt és a védett stream támogatását.

## Megoldási változatok

- **A** – Eszközpiac és kompatibilitási kutatás: támogatott LG webOS / Samsung Tizen generációk, valódi ügyfél-igény, böngészős PWA-használhatóság, valamint a már vizsgált IDEA-006 Cast/AirPlay kiváltási lehetőségeinek felmérése.
- **B** – Két platformon, korlátozott modelleken készített TV-proof-of-concept: távirányító-navigáció, katalógus, bejelentkezés másik eszközön generált, rövid életű párosítási kóddal és jogosult Bunny Stream-lejátszás. Csak tényleges SDK-képességek és streamvédelem igazolása után.
- **C** – Publikált, frissíthető natív LG Content Store és Samsung TV alkalmazás, teljes app review, analitika, fiókkezelés, licencek és karbantartási SLA mellett; kizárólag pozitív pilot és üzleti jóváhagyás után.

## Technikai hatás, előzetes hipotézis

- TV-specifikus telepítési/terjesztési fejlesztés webOS és Tizen környezetre; a jelenlegi React PWA nem tekinthető automatikusan telepíthető natív TV-appnak. Platformonként külön aktuális fejlesztői feltételek és támogatott készülékek vizsgálata szükséges.
- Védett Bunny Stream (D10), hozzáférési tokenek, támogatott kodek/DRM és aláírt manifest/segment hozzáférés a különböző TV böngészőmotorokban; közvetlen publikus media URL-t nem adhatunk. A két TV-platform valódi DRM-képességét tesztelni kell, nem feltételezni.
- Távirányító fókusz/logika, tízlábas UI, biztonságos belépés/párosítás, telefonról kijelentkeztetés, lejáró prémium-hozzáférés és adatminimalizált TV-cache. A WooCommerce/Barion checkout a TV-n nem automatikus, inkább webes fiókhoz kötött használat.
- A tanúsítás és app store regisztráció, frissítési ciklus, TV hardverteszt, tartalomlicenc és szolgáltatói díj nincs a fejlesztői méretbecslésben. Az IDEA-006 eszközre küldés egy olcsóbb termékalternatíva lehet.

## Kockázatok és függőségek

- Platform-fragmentáció, régiónként eltérő app store feltételek, régi TV processzor- és böngészőkorlátok, jóváhagyási/karbantartási költségek.
- Protected stream/DRM/codec inkompatibilitás: tokenes prémium streamet nem szabad megkerülni a TV működéséért.
- Távirányítón nehéz belépés, közös háztartási TV-n fiókadatok fennmaradása, lejárt előfizetés; személyes adatok és gyermekprofil nem jelenhetnek meg másik fióknak.

## Példa elfogadási feltétel

- Legalább egy kijelölt LG webOS és egy Samsung Tizen modell dokumentált mérőmátrixán a menüfókusz, katalógus és DRM-kompatibilis védett lejátszás vagy a megvalósíthatatlanság tényszerűen igazolható.
- Telefonos párosítás biztonságos, rövid életű kóddal működik, a fiók és a védett stream kijelentkezéskor / jogosultság lejártakor azonnal használhatatlanná válik.
- Nem adunk ki natív TV-alkalmazást a platform jóváhagyása, frissíthetősége, terjesztési jogosultsága, tényleges célközönség és költségjóváhagyás nélkül.
- Az IDEA-006 cast megoldást összehasonlítjuk a natív app várható elérésével és fenntarthatóságával, minden eredményt bizonyítékkal jelölve.

## Előzetes ráfordítás és értékelés

- **Besorolás:** research; MoSCoW Could; státusz elemzett (nem elfogadott fejlesztési megrendelés).
- **Durva hipotézis:** XL (26–60 AI-val támogatott munkanap) az első valós B-variáns prototípusára, a két TV-platform meglévő implementációjának auditja nélkül. Külső díj, marketing, üzemeltetés, licenc és teljes kiadás nincs benne. Becslési bizonyosság alacsony; nem ár vagy határidő.
- **Szubjektív értékhipotézis (1–5):** ügyfél 4, üzemeltetés 2, bevétel 3, kommunikáció 5. Kockázat: magas. RICE nincs, mert a reach, impact, confidence és effort megalapozott számai hiányoznak.

## Virágnak szóló rövid ajánlat

A Ringató zenei élménye a családi tévére is költözhetne, akár közvetlen LG vagy Samsung alkalmazásként. Előbb érdemes tisztázni, hány család használna ilyen megoldást, és biztonságosan lejátszható-e a védett videó a támogatott tévéken. Így nem vállalunk drága TV-fejlesztést bizonyíték nélkül.

## Negyedéves kommunikációs lehetőség

„Ringató a családi nagyképernyőn” – csak igazolt kompatibilitás és jóváhagyott TV-megjelenés esetén. Nem jóváhagyott kommunikáció, kampány vagy vállalt negyedéves szállítás.

## Következő ellenőrzendő lépés

Legalább két célmodell és a használói érdeklődés felmérése; Bunny Stream védett lejátszás és távirányítós POC előfeltételeinek leltára; a castinggal történő költség/haszon összevetése.

## Kapcsolódás a fejlesztéshez

Kapcsolódás **IDEA-006** Cast/AirPlay TV-re küldéshez, de ez **önálló TV-alkalmazás**, nem casting. MF06/MF10 médiaszolgáltatás és D10 jogvédett Stream; MF09 prémium jogosultság, MF01 PWA architektúra kiinduló, de nem natív TV-kompatibilitási garancia.

A már elfogadott MF01–MF14 és D01–D13 döntések változatlanok. Új automatikus művelet, időzítés, személyesadat-kezelés, külső költség és TV/platformterjesztés csak külön megrendelői döntés után.
