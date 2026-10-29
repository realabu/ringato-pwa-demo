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
8. A kész ötletlapot **közvetlenül a `main` ágba** írd, ha jogosult vagy rá: csak a validált `docs/ideas/IDEA-*.md` fájlt, nem a specifikációt. Ha PR/feature branch munkafolyamatot használsz, a `.github/workflows/auto-publish-ideas.yml` automatikusan átmásolja kizárólag a jóváhagyásra nem váró, érvényes IDEA Markdownokat a `main` ágba. A megrendelés vagy MVP-scope ettől nem válik jóváhagyottá.
9. Futtasd: `python3 -m unittest discover -s scripts -p 'test_build_ideas.py'` és `python3 scripts/build_ideas.py --output docs/ideas/catalog.json` (az automatizmus is validál). Az új ID a `main` aktuálisan legnagyobb IDEA-azonosítójából számítandó; ne támaszkodj régi sablonra.
10. A generált `catalog.json` nem commitolandó. Közvetlen `main` commit után a Pages push job, automatikus PR-ötletátemelés után az explicit `workflow_dispatch` újragenerálja és publikálja a HTML-katalógust; az óránkénti Pages job tartalék frissítés.
11. **Specifikációs, üzleti döntési, teljesítési és fejlesztési fájlokat SOHA ne emelj át automatikusan a PR-ből.** Azok külön PR-ben, jóváhagyási kapuval maradnak. Vegyes PR-ből is csak az IDEA-lapok kerülhetnek `main`-be; a PR maga nem lesz automatikusan merge-ölve. Draft/fork PR nem kerül automatikusan publikálásra. Külső költséget, éles adatot és Virágnak szóló kommunikációt továbbra is ember hagy jóvá.

**Használható AI-kérés:** „Olvasd el az AGENTS.md és docs/ideas/README.md szabályait, majd ezt a szabad szöveges ötletet dolgozd fel: … Keress átfedéseket, bővítsd a megfelelő Markdown-lapot és validáld a katalógust.”

A hiteles forrás a Markdown. A HTML megjelenítő, nem külön adatbázis.
