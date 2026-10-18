# Ringató ötlettár – AI-együttműködési szabályok

Ez a dokumentum a `docs/ideas/` ötlettár, generátora és HTML-felülete szerkesztésére vonatkozik. A projekt más részein a meglévő specifikáció, döntési napló és munkarend az irányadó.

## Új szabad szöveges ötlet feldolgozása

1. Olvasd el a `docs/ideas/README.md`, `SCHEMA.md`, `TEMPLATE.md` fájlokat és az érintett `docs/implementation-plan/` dokumentumokat.
2. Ellenőrizd a `docs/ideas/IDEA-*.md` állományt. Átfedő ötletnél lehetőleg bővítsd a meglévő ID-t; újnál adj következő szabad, stabil `IDEA-XXX` számot.
3. Őrizd meg a felvetés eredeti szövegét az „Eredeti felvetés” részben. Az AI továbbgondolásai és értékbecslései különüljenek el ettől.
4. Dolgozz ki legalább 2–3 változatot, problémát, technikai hatást, kockázatokat, elfogadási próbát, ügyfélértéket, Virágnak szóló sales pitch-et és kommunikációs témát.
5. A frontmatter és a kötelező szakaszok feleljenek meg a `SCHEMA.md`-nek.
6. Vizsgáld meg, hogy valódi hiba, már vállalt MVP UX, külön fizetős továbbfejlesztés vagy üzleti kísérlet-e. `mvp-review` **nem jelent automatikus scope-változást**. MF01–MF14 és a jóváhagyott D-döntések csak külön jóváhagyással módosíthatók.
7. Ne találj ki közvetlenül nem ellenőrzött kódmódosítási mennyiséget, szállítási időt vagy forintárat. RICE csak mind a négy megalapozott bemenettel számolható. A privát fejlesztői forrás vizsgálata nélkül az effort-becslés alacsony bizonyosságú hipotézis.
8. Futtasd: `python3 -m unittest discover -s scripts -p 'test_build_ideas.py'` és `python3 scripts/build_ideas.py --output docs/ideas/catalog.json`.
9. `catalog.json` generált adat: nem szerkesztendő és nem commitolandó. A GitHub Pages a meglévő `dev-status.yml` workflow-ból újragenerálja.
10. Kollégák branchen/PR-ben dolgozzanak, ha több szerkesztő van. Megrendelést, külső költséget, éles adatot vagy Virágnak szóló kommunikációt csak emberi jóváhagyással kezelj.

**Használható AI-kérés:** „Olvasd el az AGENTS.md és docs/ideas/README.md szabályait, majd ezt a szabad szöveges ötletet dolgozd fel: … Keress átfedéseket, bővítsd a megfelelő Markdown-lapot és validáld a katalógust.”

A hiteles forrás a Markdown. A HTML megjelenítő, nem külön adatbázis.
