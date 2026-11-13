#!/usr/bin/env python3
"""Builds the static site into ./public from vehicles.json."""
import json, os, html, shutil
BRAND = "Drive With Daniel"
EMAIL = "dannyinhouston@yahoo.com"
PHONE = "832-620-2855"
TEL = "+18326202855"
FORM = "https://formsubmit.co/ajax/" + EMAIL
V = json.load(open("vehicles.json"))
OUT = "public"
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + "/v", exist_ok=True)
shutil.copy("style.css", OUT + "/style.css")
shutil.copy("app.js", OUT + "/app.js")
e = lambda s: html.escape(str(s)) if s is not None else ""
money = lambda n: f"${n:,.0f}" if n else "Call for price"
miles = lambda n: f"{n:,} mi" if n else ""

def head(title, desc, img=None, depth=0):
    r = "../../" if depth else ""
    og = f'<meta property="og:image" content="{e(img)}">' if img else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">{og}
<link rel="stylesheet" href="{r}style.css"></head><body>
<header class="top"><a class="brand" href="{r}index.html">{BRAND}</a>
<a class="call" href="tel:{TEL}">Call/Text {PHONE}</a></header>"""

FOOT = f"""<footer><p><b>{BRAND}</b> · Daniel Quintanilla · <a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p class="fine">Prices shown match the Facebook Marketplace listing and exclude tax, title, license and fees. Availability changes quickly. Every request is confirmed by Daniel personally.</p></footer>"""

# index
cards = []
for v in V:
    img = v["photos"][0] if v["photos"] else ""
    im = f'<img loading="lazy" src="{e(img)}" alt="{e(v["title"])}">' if img else '<div class="noimg">Photos on request</div>'
    cards.append(f'''<a class="card" href="v/{v["slug"]}/" data-q="{e((v["title"]+" "+v["stock"]).lower())}">{im}
<div class="cb"><h3>{e(v["title"])}</h3><p class="pr">{money(v["price"])}</p><p class="mi">{miles(v["miles"])}</p></div></a>''')
idx = head(f"{BRAND} | Vehicles for sale", "Confirm availability or schedule a test drive with Daniel Quintanilla.") + f"""
<main class="wrap"><h1>Vehicles available</h1>
<p class="lead">Tap a vehicle to confirm it's still available or book a test drive. Daniel replies personally.</p>
<input id="q" class="search" type="search" placeholder="Search make, model, year…">
<div class="grid" id="grid">{''.join(cards)}</div></main>{FOOT}
<script>document.getElementById('q').addEventListener('input',function(){{var s=this.value.toLowerCase();document.querySelectorAll('.card').forEach(function(c){{c.style.display=c.dataset.q.indexOf(s)>-1?'':'none'}})}});</script></body></html>"""
open(OUT + "/index.html", "w").write(idx)

for v in V:
    specs = [("Mileage", miles(v["miles"])), ("Exterior", v["ext"]), ("Interior", v["int"]), ("Drivetrain", v["drive"]),
             ("Body", v["body"]), ("Fuel", v["fuel"]), ("MPG city/hwy", v["mpg"]), ("Seats", v["seats"]), ("VIN", v["vin"]), ("Stock #", v["stock"])]
    spec = "".join(f"<tr><th>{k}</th><td>{e(x)}</td></tr>" for k, x in specs if x)
    ph = v["photos"]
    gal = (f'<img id="main" class="main" src="{e(ph[0])}" alt="{e(v["title"])}">' +
           ('<div class="thumbs">' + "".join(f'<img src="{e(u)}" alt="" onclick="document.getElementById(\'main\').src=this.src">' for u in ph) + "</div>" if len(ph) > 1 else "")) if ph else '<div class="noimg big">Photos available on request</div>'
    veh = json.dumps({"title": v["title"], "stock": v["stock"], "price": money(v["price"]), "miles": miles(v["miles"]), "vin": v["vin"] or "", "fb": v["fb"] or ""})
    page = head(f'{v["title"]} | {money(v["price"])}', f'{v["title"]}, {miles(v["miles"])}. Confirm availability or schedule a test drive.', ph[0] if ph else None, 1) + f"""
<main class="wrap veh"><a class="back" href="../../index.html">← All vehicles</a>
<div class="cols"><section>{gal}</section>
<section class="panel"><h1>{e(v["title"])}</h1><p class="mi">{miles(v["miles"])}</p>
<div class="price"><span>Your price</span><b>{money(v["price"])}</b></div>
<button class="btn primary" data-open="avail">Confirm Availability</button>
<button class="btn outline" data-open="drive">Schedule a Test Drive</button>
<a class="btn ghost" href="tel:{TEL}">Call or text Daniel · {PHONE}</a>
<table class="specs">{spec}</table></section></div></main>
<div class="modal" id="modal" hidden><div class="sheet"><button class="x" aria-label="Close">×</button>
<h2 id="mt"></h2><p class="sub">{e(v["title"])} · {money(v["price"])}</p>
<form id="f" novalidate>
<div id="dt" class="row2"><label>Day<select name="day" id="day"></select></label><label>Time<select name="time" id="time"></select></label></div>
<label>Full name<input name="name" required autocomplete="name"></label>
<label>Phone<input name="phone" type="tel" required autocomplete="tel"></label>
<label>Email<input name="email" type="email" required autocomplete="email"></label>
<fieldset><legend>Preferred contact</legend><label class="r"><input type="radio" name="contact" value="Call" checked> Call</label><label class="r"><input type="radio" name="contact" value="Text"> Text</label><label class="r"><input type="radio" name="contact" value="Email"> Email</label></fieldset>
<label>Notes (optional)<textarea name="notes" rows="3" placeholder="Trade-in, financing questions, anything else"></textarea></label>
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
<button class="btn primary" type="submit" id="sb">Send request</button>
<p class="fine">Your info goes only to Daniel Quintanilla and is used to reply about this vehicle.</p></form>
<div id="ok" hidden><h2>Request sent ✔</h2><p>Thanks! Daniel will reach out shortly to confirm. Need it faster? Call or text <a href="tel:{TEL}">{PHONE}</a>.</p></div>
<div id="err" class="err" hidden></div></div></div>
{FOOT}<script>window.VEH={veh};window.FORM="{FORM}";window.PHONE="{PHONE}";window.EMAIL="{EMAIL}";</script><script src="../../app.js"></script></body></html>"""
    os.makedirs(f'{OUT}/v/{v["slug"]}', exist_ok=True)
    open(f'{OUT}/v/{v["slug"]}/index.html', "w").write(page)
open(OUT + "/404.html", "w").write(head("Not found", "") + f'<main class="wrap"><h1>That vehicle is no longer listed</h1><p><a href="/">See all available vehicles</a> or call <a href="tel:{TEL}">{PHONE}</a>.</p></main>{FOOT}</body></html>')
print("built", len(V), "vehicle pages")
