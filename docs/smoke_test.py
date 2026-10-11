#!/usr/bin/env python3
"""Browser click regression suite: verify DOM handlers, not only callable JavaScript."""
from pathlib import Path
import functools
import http.server
import threading
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parent.parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def test():
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',8831),functools.partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    failures=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
            page.on('pageerror',lambda e:failures.append(str(e)))
            page.goto('http://127.0.0.1:8831/app.html',wait_until='load')
            expect(page.locator('#content .card')).to_have_count(4)
            # MEDIA: a real click on a media card must open the single-item audio player.
            page.locator('#content .card').first.click()
            expect(page.locator('#modal')).to_have_class('modal on')
            expect(page.locator('#sheet')).to_contain_text('Hinta, palinta')
            expect(page.locator('#sheet')).to_contain_text('Hangfelvétel')
            page.evaluate('hideModal()')
            # FAVORITES: real heart press must persist a favorite.
            page.locator('#content .card .heart').first.click()
            assert page.evaluate('state.favorites.includes("hinta")'), f"Favorite was not saved. favorites={page.evaluate('state.favorites')} onclick={page.locator('#content .card .heart').first.get_attribute('onclick')} pageErrors={failures}"
            page.evaluate('go("library")')
            expect(page.locator('#mediaList .listrow')).to_have_count(8)
            # Media row click, and a second favorite via its nested icon.
            page.locator('#mediaList .listrow').first.click()
            expect(page.locator('#sheet')).to_contain_text('Hinta, palinta')
            page.evaluate('hideModal()')
            page.locator('#mediaList .listrow').nth(1).locator('button').click()
            assert page.evaluate('state.favorites.includes("csip")'), 'Library heart press failed'
            page.get_by_role('button',name='Kedvencek',exact=False).click()
            expect(page.locator('#sheet')).to_contain_text('Hinta, palinta')
            expect(page.locator('#sheet')).to_contain_text('Csip-csip csóka')
            page.evaluate('hideModal()')
            # EVENTS: all three must open program details with time/location/description.
            page.evaluate('go("calendar")')
            rows=page.locator('#content .event')
            assert rows.count()==4, 'Program list missing entries'
            rows.nth(0).get_by_role('button',name='Részletek').click()
            expect(page.locator('#sheet')).to_contain_text('IDŐPONT')
            expect(page.locator('#sheet')).to_contain_text('HELYSZÍN')
            expect(page.locator('#sheet')).to_contain_text('LEÍRÁS')
            expect(page.locator('#sheet')).to_contain_text('Naptárhoz adás')
            page.evaluate('hideModal()')
            rows.nth(2).get_by_role('button',name='Részletek').click()
            expect(page.locator('#sheet')).to_contain_text('Egy családi hely lefoglalása')
            page.evaluate('hideModal()')
            rows.nth(3).get_by_role('button',name='Részletek').click()
            expect(page.locator('#sheet')).to_contain_text('Eseményjegy megvásárlása')
            # QUEUE: add, open and reorder by actual click handlers.
            page.evaluate('hideModal();state.plus=true;state.queue=["hinta","nepdal"];save();go("library")')
            page.get_by_role('button',name='Sor (2)').click()
            expect(page.locator('#sheet')).to_contain_text('Lejátszási sor')
            page.locator('#sheet .queueRow').nth(1).get_by_role('button',name='Fel').click()
            assert page.evaluate('state.queue[0] === "nepdal"'), 'Queue reorder failed'
            page.evaluate('hideModal()')
            page.locator('#mediaList .listrow').nth(1).click()
            expect(page.locator('#sheet')).to_contain_text('Videó')
            expect(page.locator('#sheet')).to_contain_text('Teljes képernyő')
            assert page.locator('#sheet').get_by_text('Képarány váltása').count()==0
            browser.close()
    finally:srv.shutdown()
    assert not failures,'Browser JavaScript runtime errors: '+repr(failures)
    print('PASS: click cards, favorite hearts, library, event details, queue reorder and video')

if __name__=='__main__':test()
