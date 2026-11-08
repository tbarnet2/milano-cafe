#!/usr/bin/env python3
"""Generate six static Milano Café pages. Run: python build_site.py"""
from pathlib import Path
from html import escape
import json, datetime
ROOT=Path(__file__).resolve().parent
DOMAIN='https://www.milanoaustin.com'
ORDER='https://order.spoton.com/so-milano-cafe-23898/austin-tx/682b85c2b3310a5fadb57869'
RESERVE='https://reserve.spoton.com/restaurant/73694'
ADDRESS='4601 Southwest Parkway, Austin, TX 78735'
MAP='https://www.google.com/maps/search/?api=1&query=4601+Southwest+Parkway+Austin+TX+78735'
EMAIL='cafemilanoaustin@gmail.com'
PHONE='(512) 428-6076'
PHOTO='assets/photos/'
# Original image dimensions. Explicit dimensions reduce visual movement while images load.
PHOTO_SIZES = {
    'artwork-detail': (1350, 1800), 'coffee-dessert': (1350, 1013),
    'color-room': (1350, 1800), 'dessert': (1350, 1013),
    'dining-room': (1600, 1200), 'food-spread': (1350, 1800),
    'gallery-portraits': (1350, 1013), 'gallery-wall': (1600, 1200),
    'hero-gallery': (2000, 1500), 'pasta': (1350, 1800),
    'pizza': (1350, 1800), 'quiet-corner': (1350, 1800),
    'table-spread': (1600, 1200), 'window-table': (1350, 1800),
}


def photo(name,alt,**kwargs):
    width, height = PHOTO_SIZES[name]
    attributes={'loading':'lazy','decoding':'async','width':width,'height':height,**kwargs}
    opts=' '.join(f'{k.replace("_","-")}="{escape(str(v),quote=True)}"' for k,v in attributes.items())
    return f'<img src="{PHOTO}{name}.webp" alt="{escape(alt,quote=True)}" {opts}>'

def btn(href,text,style='dark',external=False):
    return f'<a href="{escape(href,quote=True)}" class="btn btn-{style}"'+ (' target="_blank" rel="noopener noreferrer"' if external else '') + f'>{escape(text)} <span aria-hidden="true">↗</span></a>'

def eyebrow(text, tone='copper'):
    return f'<span class="eyebrow {tone}">{escape(text)}</span>'

def header(current):
    links=[('index.html','Home'),('menu.html','Menus'),('story.html','Our story'),('gallery.html','The art'),('catering.html','Catering'),('visit.html','Visit')]
    items=''.join(f'<a href="{u}"'+(' aria-current="page"' if u==current else '')+f'>{label}</a>' for u,label in links)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
 <a href="index.html" class="brand" aria-label="Milano Café & Art Gallery home"><span class="brand-mark" aria-hidden="true">M</span><span class="brand-name"><strong>MILANO</strong><small>Café &amp; Art Gallery</small></span></a>
 <button type="button" class="menu-toggle" aria-controls="main-navigation" aria-expanded="false" aria-label="Open navigation"><span></span><span></span><span></span></button>
 <nav id="main-navigation" aria-label="Main navigation" class="nav-links">{items}<a class="nav-cta" href="{RESERVE}" target="_blank" rel="noopener noreferrer">Reserve a table ↗</a></nav>
</header>'''

def footer():
    return f'''<footer class="footer"><div class="container">
 <div class="footer-layout"><div>
 <a href="index.html" class="brand" aria-label="Milano Café home"><span class="brand-mark" aria-hidden="true">M</span><span class="brand-name"><strong>MILANO</strong><small>Café &amp; Art Gallery</small></span></a>
 <p>A neighborhood Italian café where food, art, and good company meet. Family-owned in Austin since 2009.</p>
 </div><div><h4>Explore</h4><ul><li><a href="story.html">Our story</a></li><li><a href="menu.html">Lunch &amp; dinner</a></li><li><a href="gallery.html">Artwork</a></li><li><a href="catering.html">Catering</a></li><li><a href="visit.html">Visit</a></li></ul></div>
 <div><h4>Come by</h4><address>4601 Southwest Parkway<br>Austin, TX 78735<br><br>Mon–Sat · 11 AM–9 PM<br>Sunday · Closed</address></div>
 <div><h4>Say hello</h4><ul><li><a href="tel:+15124286076">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li style="margin-top:17px"><a href="{ORDER}" target="_blank" rel="noopener noreferrer">Order online ↗</a></li><li><a href="{RESERVE}" target="_blank" rel="noopener noreferrer">Reserve a table ↗</a></li></ul></div></div>
 <div class="footer-bottom"><span>© {datetime.date.today().year} Milano Café &amp; Art Gallery. All rights reserved.</span><span>Made for the moments worth sharing.</span></div>
 </div></footer><div class="mobile-quick"><a href="{ORDER}" target="_blank" rel="noopener noreferrer">Order online ↗</a><a href="{RESERVE}" target="_blank" rel="noopener noreferrer">Reserve a table ↗</a></div>'''

def ldjson():
    schema={"@context":"https://schema.org","@type":"Restaurant","@id":DOMAIN+'/#restaurant',"name":"Milano Café & Art Gallery","url":DOMAIN+'/',"description":"Family-owned Italian café and art gallery in Southwest Austin since 2009.","image":DOMAIN+'/assets/photos/dining-room.webp',"servesCuisine":"Italian","telephone":"+15124286076","email":EMAIL,"address":{"@type":"PostalAddress","streetAddress":"4601 Southwest Parkway","addressLocality":"Austin","addressRegion":"TX","postalCode":"78735","addressCountry":"US"},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"11:00","closes":"21:00"}],"hasMenu":DOMAIN+'/menu.html',"acceptsReservations":RESERVE,"priceRange":"$$"}
    return json.dumps(schema,ensure_ascii=False,separators=(',',':'))

def render(path,title,description,body,og='hero-gallery',keywords=None):
    canonical=f'{DOMAIN}/{path}' if path!='index.html' else DOMAIN+'/'
    current=path
    content=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}">
<link rel="canonical" href="{canonical}"><link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#1b211d"><meta name="robots" content="index,follow">
<meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta property="og:site_name" content="Milano Café &amp; Art Gallery"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{DOMAIN}/assets/photos/{og}.webp"><meta property="og:image:alt" content="Milano Café &amp; Art Gallery in Austin, Texas">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=Manrope:wght@400;500;600;700&amp;family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&amp;display=swap">
<link rel="preload" as="image" href="assets/photos/{og}.webp">
<link rel="stylesheet" href="assets/css/site.css">
<script type="application/ld+json">{ldjson()}</script>
</head><body>{header(current)}<main id="main">{body}</main>{footer()}<script src="assets/js/site.js" defer></script></body></html>'''
    (ROOT/path).write_text(content,encoding='utf-8')


def page_hero(kicker, heading, desc, image,alt):
    return f'''<section class="page-hero"><div class="page-hero-text">{eyebrow(kicker,'gold')}<h1>{heading}</h1><p class="lede">{desc}</p></div><div class="page-photo">{photo(image,alt,loading='eager',fetchpriority='high')}</div></section>'''

home=f'''
<section class="hero">
 <div class="hero-copy">{eyebrow('Austin, Texas · Since 2009','gold')}
 <h1 class="display">An Italian café with an <em>artist’s soul.</em></h1>
 <p class="lede">Italian favorites, original art, and an open seat at the table. Discover a family-owned Austin café where every visit feels a little different.</p>
 <div class="hero-actions">{btn(RESERVE,'Reserve a table','gold',True)}{btn('menu.html','Explore the menus','outline-light')}</div>
 <div class="hero-stat"><b>2009</b><span>Family-owned in<br>Southwest Austin</span></div>
 </div>
 <div class="hero-photo">{photo('hero-gallery','Milano Café dining room with original colorful paintings and inviting tables',loading='eager',fetchpriority='high')}<div class="hero-photo-label">A gathering place for food &amp; art</div></div>
</section>
<section class="section-short intro-section"><div class="container intro-grid">
 <div>{eyebrow('The Milano experience')}<h2 class="section-heading">Something to <em>savor.</em> Somewhere to <em>stay.</em></h2></div>
 <div class="copy"><p>At Milano Café, the art isn’t an afterthought—and neither is the food. Original paintings surround the dining room, adding unexpected color to a familiar ritual: sharing a good meal.</p><p>Come for an unhurried lunch, a comforting dinner, or a special evening around the table. Stay a while.</p></div>
</div></section>
<section class="section"><div class="container"><div class="two-col wide-left">
 <div class="photo-frame wide">{photo('table-spread','A table set with a variety of Milano Café Italian dishes and wine')}<span class="corner-tag">Made to be shared</span></div>
 <div>{eyebrow('From our kitchen')}<h2 class="section-heading">A little more <em>dolce vita.</em></h2><p class="copy">From pasta and pizza to familiar Italian classics, our menus make room for long lunches, date nights, and everything in between.</p><p class="copy">Explore separate lunch and dinner menus, then make your plans.</p>{btn('menu.html','View our menus','dark')}</div>
 </div></div></section>
<section class="section-short" style="background:#eee8dc"><div class="container">
 <div class="feature-heading"><div>{eyebrow('A taste of Milano')}<h2 class="section-heading sm">For the table. <em>For the moment.</em></h2></div><a class="text-link" href="menu.html">Explore the full menu <span aria-hidden="true">↗</span></a></div>
 <div class="feature-grid">
 <a class="feature-card" href="menu.html?service=dinner"><div class="image-wrap">{photo('pasta','Fresh spaghetti pasta served at Milano Café')}</div><div class="meta"><span class="number">01 / PASTA</span><h3>Italian favorites</h3><p>A little comfort in every forkful.</p></div></a>
 <a class="feature-card" href="menu.html?service=lunch"><div class="image-wrap">{photo('pizza','Handmade pizza with cheese and mushrooms at Milano Café')}</div><div class="meta"><span class="number">02 / PIZZA</span><h3>Something to share</h3><p>Gather around a table full of good food.</p></div></a>
 <a class="feature-card" href="visit.html"><div class="image-wrap">{photo('dessert','Coffee and freshly plated cakes at Milano Café')}</div><div class="meta"><span class="number">03 / THE CAFÉ</span><h3>Stay for something sweet</h3><p>The best afternoons don’t need a rush.</p></div></a>
 </div>
 </div></section>
<section class="section dark-section"><div class="container art-editorial">
 <div>{eyebrow('A canvas in every corner','gold')}<h2 class="section-heading">Dinner with <em>a view.</em></h2><p class="copy">The paintings on our walls are original works by the café’s owner. They give Milano its spirit: expressive, personal, and impossible to mistake for anywhere else.</p><p class="copy">See the art while you dine. If a piece catches your eye, ask us about it.</p><a class="text-link" href="gallery.html">Discover the art <span aria-hidden="true">↗</span></a></div>
 <div class="art-image">{photo('gallery-wall','Original colorful artworks hanging over tables at Milano Café')}</div>
 </div></section>
<section class="section-short statement">{eyebrow('More than a meal')}<h2 class="section-heading">Good food brings us together.<br><em>Art gives us something to talk about.</em></h2><p>Our tables are for old friends, new conversations, and the kind of evenings you wish were just a little longer.</p></section>
<section class="section-short visit-band"><div class="container visit-band-grid"><div>{eyebrow('Your table is here','gold')}<h2 class="section-heading">Come as you are.<br><em>Stay a while.</em></h2><p>4601 Southwest Parkway · Austin, Texas 78735<br>Monday–Saturday, 11 AM–9 PM · Closed Sunday</p><div class="links">{btn(RESERVE,'Reserve a table','gold',True)}{btn(MAP,'Get directions','outline-light',True)}</div></div><div>{photo('window-table','A welcoming table beside the window inside Milano Café')}</div></div></section>
'''
render('index.html','Milano Café & Art Gallery | Italian Restaurant in Austin, TX','Italian food, original art, and warm hospitality in Southwest Austin. Visit family-owned Milano Café & Art Gallery, serving Austin since 2009.',home,'hero-gallery')

story=page_hero('The café & the canvas','Our <em style="color:#d8b990">story.</em>','A family-owned Italian café shaped by the people who gather here—and the artist who fills its walls.','dining-room','Milano Café dining room filled with colorful art and eclectic seating')+f'''
<section class="section"><div class="container two-col wide-left"><div class="image-duo">{photo('color-room','Colorful, art-filled dining room at Milano Café')}{photo('quiet-corner','Quiet corner table with paintings at Milano Café')}</div><div>{eyebrow('Est. April 2009')}<h2 class="section-heading">An Austin original, <em>through and through.</em></h2><p class="copy">Milano Café opened its doors in April 2009 with a simple idea: create a welcoming place for Italian food and shared experiences.</p><p class="copy">Today, the family-owned café is part dining room, part personal gallery. A collection of expressive paintings gives every corner its own character, making each visit feel familiar and full of surprises.</p><p class="copy">It’s a place to come together over good food—and to linger over the details.</p></div></div></section>
<section class="quote-section"><div class="container">{eyebrow('The heart of Milano','gold')}<blockquote>A café can be more than a place to eat. It can be a place to <em>feel at home.</em></blockquote><p style="margin:24px auto 0;color:#c0c1ba;font-size:13px">An invitation to gather</p></div></section>
<section class="section"><div class="container two-col wide-right"><div>{eyebrow('The artist behind the atmosphere')}<h2 class="section-heading">Made with <em>imagination.</em></h2><p class="copy">The café’s owner is also the artist behind most of the paintings you’ll see on our walls. The work adds personality to the space, with pieces available to inquire about while you dine.</p><p class="copy">Occasionally, works by other artists make their way onto the walls as well. The result is a living collection that reflects the people behind this place.</p>{btn('gallery.html','Explore the artwork','dark')}</div><div class="photo-frame tall">{photo('gallery-portraits','Original paintings displayed above seating in Milano Café')}</div></div></section>
<section class="section-short statement">{eyebrow('Join us')}<h2 class="section-heading">A good story is better<br><em>shared around a table.</em></h2><div style="margin-top:32px">{btn(RESERVE,'Find your table','dark',True)}</div></section>
'''
render('story.html','Our Story | Milano Café & Art Gallery','Get to know Milano Café & Art Gallery: a family-owned Austin Italian café since 2009 with original art by its owner displayed throughout the restaurant.',story,'dining-room')

gallery=page_hero('Art at Milano','The art <em style="color:#d8b990">of gathering.</em>','Come for the Italian food. Look a little closer at the walls.','gallery-wall','Original paintings above the tables inside Milano Café')+f'''
<section class="section"><div class="container two-col wide-right"><div>{eyebrow('An artist-owned café')}<h2 class="section-heading">More than <em>decoration.</em></h2><p class="copy">The paintings at Milano are original works by the restaurant’s owner. Bold, expressive, and deeply personal, they give the dining room its one-of-a-kind character.</p><p class="copy">Most of the artwork comes from the owner’s own collection. Select pieces may be available to purchase, and the café occasionally features work by other artists.</p><p class="copy">A formal online catalog is coming later. In the meantime, the best way to discover the work is to experience it in person.</p><a class="text-link" href="mailto:{EMAIL}?subject=Artwork%20inquiry%20at%20Milano%20Cafe">Ask about artwork <span aria-hidden="true">↗</span></a></div><div class="photo-frame tall">{photo('artwork-detail','Original artwork displayed on the wall at Milano Café')}</div></div></section>
<section class="section-short" style="background:#eee8dc"><div class="container"><div class="feature-heading"><div>{eyebrow('The gallery, in place')}<h2 class="section-heading sm">Art that <em>lives here.</em></h2></div></div><div class="art-gallery-grid">
<figure>{photo('gallery-wall','Artist-made original paintings displayed above a café table')}<figcaption>Art at every table</figcaption></figure>
<figure>{photo('gallery-portraits','Colorful portrait paintings inside the café')}<figcaption>A room with a point of view</figcaption></figure>
<figure>{photo('color-room','Original mixed-media paintings and colorful dining room interior')}<figcaption>Color and conversation</figcaption></figure>
</div></div></section>
<section class="section dark-section"><div class="container art-editorial"><div>{eyebrow('See something you love?','gold')}<h2 class="section-heading">Take the <em>conversation</em> home.</h2><p class="copy">If a work catches your eye during your visit, ask our team about its story and availability. You can also contact us ahead of time if you’re interested in a particular piece.</p>{btn(f'mailto:{EMAIL}?subject=Milano%20Cafe%20artwork%20inquiry','Inquire about art','gold')}</div><div class="art-image">{photo('quiet-corner','Intimate art-filled dining nook at Milano Café')}</div></div></section>
'''
render('gallery.html','Art Gallery | Milano Café & Art Gallery','Explore the original paintings that make Milano Café a uniquely artistic Italian dining destination in Austin. Inquire about artwork during your visit.',gallery,'gallery-wall')

catering=page_hero('Bring Milano to the table','Gather <em style="color:#d8b990">beautifully.</em>','Italian favorites for gatherings large and small. Let us help make the food the easy part.','table-spread','Italian dishes for sharing at Milano Café')+f'''
<section class="section"><div class="container two-col wide-right"><div>{eyebrow('Catering by Milano')}<h2 class="section-heading">Good food, <em>great company.</em></h2><p class="copy">From birthdays and family celebrations to office gatherings, Milano offers catering trays built for the moments worth sharing.</p><p class="copy">Our current catering menu describes trays designed to serve approximately six guests. Contact the team to confirm availability, portions, timing, and current pricing for your event.</p><div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px">{btn('tel:+15124286076','Call to plan','dark')}{btn(f'mailto:{EMAIL}?subject=Catering%20inquiry%20at%20Milano%20Cafe','Email inquiry','outline')}</div></div><div class="photo-frame tall">{photo('food-spread','An abundant display of freshly prepared Italian food')}</div></div></section>
<section class="section-short" style="background:#ede7dc"><div class="container"><div class="feature-heading"><div>{eyebrow('From the catering menu')}<h2 class="section-heading sm">Favorites, <em>for a crowd.</em></h2></div></div><div class="info-panels"><div class="info-panel"><small>01 / Pasta</small><h3>Fettuccine &amp; pasta</h3><p>Alfredo chicken fettuccine, fettuccine carbonara, and penne bolognese are among the listed catering options.</p></div><div class="info-panel"><small>02 / Italian classics</small><h3>Comforting favorites</h3><p>Chicken Parmesan, Veal Marsala, Eggplant Parmesan, and other familiar favorites.</p></div><div class="info-panel"><small>03 / Special occasions</small><h3>Something for everyone</h3><p>Ask the team about the full catering selection, dietary needs, and planning for your guest count.</p></div></div><p class="copy" style="max-width:100%;font-size:13px;margin-top:25px">Menus and availability are subject to change. Please confirm current offerings and prices directly with the restaurant.</p></div></section>
<section class="section dark-section"><div class="container cta-split"><div>{eyebrow('Let’s plan something good','gold')}<h2 class="section-heading">Have an occasion <em>in mind?</em></h2><p class="copy">Tell us what you’re celebrating and when. We’ll help you find the right menu for your gathering.</p>{btn(f'mailto:{EMAIL}?subject=Catering%20inquiry%20at%20Milano%20Cafe','Start a catering inquiry','gold')}</div>{photo('coffee-dessert','Cakes and coffee served at Milano Café')}</div></section>
'''
render('catering.html','Italian Catering in Austin | Milano Café','Cater your next Austin gathering with Milano Café. Ask about Italian pasta trays, classic dishes, availability, and current pricing.',catering,'table-spread')

visit=page_hero('Find us in Southwest Austin','We saved you <em style="color:#d8b990">a seat.</em>','Whether it’s lunch, dinner, or a look around the gallery, we’d love to see you.','window-table','Table by the sunny window at Milano Café')+f'''
<section class="section-short"><div class="container"><div class="feature-heading"><div>{eyebrow('Visit Milano')}<h2 class="section-heading sm">The details, <em>made easy.</em></h2></div></div>
<div class="info-panels"><div class="info-panel"><small>01 / Find us</small><h3>Southwest Austin</h3><p>4601 Southwest Parkway<br>Austin, TX 78735</p><a href="{MAP}" target="_blank" rel="noopener noreferrer">Get directions ↗</a></div><div class="info-panel"><small>02 / Hours</small><h3>Come by anytime</h3><p>Monday–Saturday<br>11 AM – 9 PM<br>Sunday · Closed</p></div><div class="info-panel"><small>03 / Get in touch</small><h3>We’re here to help</h3><p><a href="tel:+15124286076">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>
<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:32px">{btn(RESERVE,'Reserve a table','dark',True)}{btn(ORDER,'Order online','outline',True)}</div>
</div></section>
<section class="map-wrap" aria-label="Map showing Milano Café's location in Southwest Austin"><iframe title="Map to Milano Café at 4601 Southwest Parkway, Austin Texas" src="https://www.google.com/maps?q=4601%20Southwest%20Parkway%20Austin%20TX%2078735&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>
<section class="section"><div class="container two-col wide-left"><div class="photo-frame wide">{photo('dining-room','The welcoming interior of Milano Café, showing vibrant art and colorful seating')}</div><div>{eyebrow('A little something extra')}<h2 class="section-heading">Make yourself <em>at home.</em></h2><p class="copy">The art is part of the experience here. Give yourself time to look around, share a meal, and enjoy the colorful atmosphere that makes Milano special.</p><a class="text-link" href="gallery.html">Discover the gallery <span aria-hidden="true">↗</span></a></div></div></section>
'''
render('visit.html','Visit Milano Café | Hours, Location & Contact in Austin','Visit Milano Café & Art Gallery at 4601 Southwest Parkway, Austin TX 78735. Open Monday–Saturday, 11 AM–9 PM. Get directions or reserve a table.',visit,'window-table')

# The lunch and dinner menu data below was transcribed from the restaurant's existing published menus.
# All published prices should be confirmed with the owner before the new site replaces Wix.
M={
 'Antipasti':[
  ('Calamari Fritti','Lightly battered fried calamari with tomato-basil sauce and citronette',17,17),
  ('Caprese','Fresh mozzarella, tomato, basil and aged balsamic vinegar',13,13),
  ('Bruschetta','Tomato, mozzarella and basil on toasted bread',13,14),
  ('Garlic Bread','',7,7),
 ],
 'Insalata':[
  ('Cucumber Salad','Cucumber, tomato, red onion, cranberry, walnut, goat cheese and house Italian dressing',14,15),
  ('Greek Salad','Mixed greens, cucumber, tomato, olive and feta',13,14),
  ('Caesar Salad','Romaine, croutons, parmesan and Caesar dressing',13,13),
  ('Spinach Salad','Baby spinach, red onion, cucumber, tomato and balsamic vinegar',13,13),
  ('Tuna Salad','Tuna salad with mixed greens, tomato and house Italian dressing',14,None),
 ],
 'Pasta & Italian Classics':[
  ('Spinach Ravioli','Spinach ravioli in tomato-basil sauce',18,19),
  ('Italian Flag','Italian sausage, sun-dried tomato, broccoli and penne pasta in garlic and olive oil',18,20),
  ('Fettuccine Ragù','Italian sausage, onion and mushroom in tomato sauce, finished with goat cheese',18,21),
  ('Fettuccine Carbonara','Pancetta, caramelized onion and fettuccine in cream sauce',19,21),
  ('Meat Lasagna','',18,20),
  ('Spaghetti & Meatballs','',18,20),
  ('Penne Bolognese','Ground beef, vegetables, tomato sauce and parmesan',18,20),
  ('Drunken Linguine','Red-wine linguine with chicken, caper, mushroom, pepper and olives in a light cream sauce',19,21),
  ('Tortellini Gorgonzola','Chicken and mushroom in gorgonzola cream sauce',19,21),
  ('Alfredo Chicken Fettuccine','',19,20),
  ('Veal Parmesan','Breaded veal baked in tomato sauce and parmesan, served with spaghetti',28,28),
  ('Veal Piccata','White wine, lemon and capers with roasted vegetables',28,28),
  ('Veal Marsala','Veal in marsala wine and mushroom sauce with roasted vegetables',28,28),
  ('Chicken Parmesan','Breaded chicken in tomato sauce and parmesan, served with spaghetti',20,21),
  ('Chicken Piccata','Chicken in white wine, lemon and capers with roasted vegetables',18,21),
  ('Chicken Marsala','Chicken in marsala wine and mushroom sauce with roasted vegetables',18,21),
  ('Lobster Ravioli','Lobster ravioli in fresh tomato sauce',22,23),
  ('Tortellini Piementosa','Shrimp, capers, berries and cranberries in light cream pesto sauce',22,23),
  ('Linguine Frutto di Mare','Clams, mussels and shrimp in tomato-basil sauce',23,23),
  ('Alfredo Shrimp Fettuccine','',20,21),
  ('Salmon','Salmon with pepper cream sauce and roasted vegetables',27,27),
  ('Butternut Squash Ravioli','Fresh berries, dried cranberries, light cream sauce and walnut garnish',18,20),
  ('Eggplant Parmesan','Baked eggplant, ricotta, mozzarella and parmesan in tomato sauce',18,19),
  ('Pasta Primavera','Fettuccine and seasonal vegetables; choose a sauce (gorgonzola +$2)',18,20),
  ('Eight Meatballs in Tomato Sauce','',18,20),
 ],
 'Pizza':[
  ('Margherita','Tomato, fresh mozzarella and basil',13,14),
  ('Albaneze','Albaneze sausage, mozzarella and feta',15,15),
  ('Spinach','Spinach, mushroom and ricotta sauce',13,14),
  ('Vegetable','Bell pepper, onion, mushroom, olive, feta and pesto',14,14),
  ('Arbreshe','Prosciutto, Albaneze sausage and feta',16,16),
  ('Pepperoni','',14,14),
  ('Cheese','',11,None),
  ('Prosciutto','',16,None),
  ('Italian Sausage','',13,None),
  ('Alfredo Chicken','',14,None),
 ],
 'Panini':[
  ('Tuna Melt','Red onion, celery, capers, light mayo and mozzarella',14,None),
  ('Prosciutto Melt','Prosciutto, mozzarella, pesto and roasted peppers',16,None),
  ('Chicken Melt','Pesto, mozzarella and roasted pepper',13,None),
  ('Caprese Melt','Fresh mozzarella, tomato and basil',12,None),
  ('Meatball Panini','Meatballs, mozzarella and tomato sauce',13,None),
  ('Italian Sausage Panini','Italian sausage, mozzarella and tomato sauce',13,None),
 ]
}

def menu_panel(service):
    items=''
    for category,rows in M.items():
        parsed=[(name,desc,(dinner if service=='dinner' else lunch)) for name,desc,lunch,dinner in rows]
        parsed=[entry for entry in parsed if entry[2] is not None]
        if not parsed:continue
        cards=''.join('<li class="menu-item"><h3>'+escape(name)+'</h3><span class="price">$'+str(price)+'</span>'+(f'<p>{escape(desc)}</p>' if desc else '')+'</li>' for name,desc,price in parsed)
        items+=f'<section class="menu-category"><h2>{escape(category)}</h2><ul class="menu-list">{cards}</ul></section>'
    added=('<strong>Additional options:</strong> Side house, Greek or Caesar salad +$6; add chicken or Italian sausage +$5, prosciutto +$7, or 3 shrimp +$7.' if service=='lunch' else '<strong>Additional options:</strong> Side house, Greek or Caesar salad +$6; add chicken or Italian sausage +$6, prosciutto +$7, 3 shrimp +$7, or roasted vegetables +$7.')
    return f'''<div id="{service}-panel" role="tabpanel" aria-labelledby="{service}-tab" class="menu-panel" {'hidden' if service=='dinner' else ''}><p class="menu-intro">A collection of Italian favorites, thoughtfully prepared to share with friends and family. {"Lunch" if service=='lunch' else "Dinner"} selections and prices reflect the restaurant’s published menu and are subject to change.</p><div class="menu-content">{items}</div><aside class="menu-notes"><p>{added}</p><p style="margin-top:11px"><strong>Dietary note:</strong> Gluten-free pasta and pizza may be available upon request, but Milano Café is not a gluten-free kitchen. Please notify the staff of allergies and dietary needs before ordering.</p><p style="margin-top:11px"><strong>Prices and availability:</strong> Please confirm current pricing and selections with the restaurant, particularly for special requests.</p></aside></div>'''
menu=page_hero('The menus','Made to <em style="color:#d8b990">share.</em>','Italian comfort, artful details, and something for every kind of gathering.','food-spread','Italian food and pizza served at Milano Café')+f'''
<section class="section-short"><div class="container">{eyebrow('Lunch & dinner')}<h2 class="section-heading sm" style="text-align:center;margin:20px auto 0">Find your next <em>favorite.</em></h2>
<div role="tablist" class="menu-controls" aria-label="Choose menu"><button type="button" role="tab" id="lunch-tab" aria-controls="lunch-panel" aria-selected="true" tabindex="0">Lunch menu</button><button type="button" role="tab" id="dinner-tab" aria-controls="dinner-panel" aria-selected="false" tabindex="-1">Dinner menu</button></div>
{menu_panel('lunch')}{menu_panel('dinner')}</div></section>
<section class="section-short dark-section"><div class="container" style="text-align:center">{eyebrow('Hungry yet?','gold')}<h2 class="section-heading sm" style="margin:20px auto 27px">Save a seat—or bring <em>Milano home.</em></h2><div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">{btn(RESERVE,'Reserve a table','gold',True)}{btn(ORDER,'Order online','outline-light',True)}</div></div></section>
'''
render('menu.html','Lunch & Dinner Menus | Milano Café Austin','Explore the lunch and dinner menus at Milano Café & Art Gallery in Southwest Austin: Italian pastas, pizzas, salads, seafood, and more.',menu,'food-spread')

(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+DOMAIN+'/sitemap.xml\n',encoding='utf-8')
urls=['','menu.html','story.html','gallery.html','catering.html','visit.html']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{DOMAIN}/{u}</loc></url>' for u in urls)+'</urlset>',encoding='utf-8')
(ROOT/'_redirects').write_text('''/about /story.html 301
/copy-of-about /menu.html 301
/copy-of-menu /menu.html?service=lunch 301
/copy-of-lunch-menu /menu.html?service=dinner 301
/copy-of-lunch-menu-2 /menu.html?service=lunch 301
/copy-of-dinner-menu /catering.html 301
/copy-of-catering-menu /visit.html 301
/contact /visit.html 301
/menu /menu.html 301
/reservations /visit.html 301
/ordering /menu.html 301
''',encoding='utf-8')
(ROOT/'_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/assets/photos/*
  Cache-Control: public, max-age=2592000
''',encoding='utf-8')
(ROOT/'README.md').write_text(f'''# Milano Café & Art Gallery — Website Launch Candidate

This is a fully static, original, responsive restaurant website designed for Milano Café in Austin, Texas. No JavaScript framework or paid hosting required.

## Pages
- `index.html` — Home
- `menu.html` — Separate lunch/dinner menus
- `story.html` — Restaurant story
- `gallery.html` — Art showcase and inquiry
- `catering.html` — Catering overview and inquiry
- `visit.html` — Hours, contact and directions

## Preview locally
Open `index.html` in a browser. For more reliable browser testing, run `python -m http.server 8000` in this folder and visit `http://localhost:8000/`.

## Publishing to Cloudflare Pages
Use **Git integration** with the GitHub repository, framework **None**, build command **blank**, output directory **/** (the repository root). Connect the custom domain only after reviewing the preview and taking a backup of existing DNS records.

## Photographs
Optimized WebP originals used with permission. Files are located in `assets/photos/` and sourced from the uploaded ZIP. `prepare_images.py` is included for traceability; it is not needed for deployment. The JPG originals are not modified.

## Restaurant details — VERIFY BEFORE PUBLIC LAUNCH
- 4601 Southwest Parkway, Austin, TX 78735
- (512) 428-6076
- cafemilanoaustin@gmail.com
- Monday–Saturday 11 AM–9 PM; Sunday closed
- Reservation link: {RESERVE}
- Ordering link: {ORDER}
- The owner should verify **all menu prices, descriptions, catering claims and artwork availability**, as restaurant websites are not necessarily updated in real time.

## Outstanding
- Check the published site on a real iPhone and Android browser and run Google PageSpeed Insights after domain launch.
- Confirm legal rights to reuse photographs and owner approval of text.
- Connect Google Search Console and submit sitemap once domain points at this site.
- Test redirects on Cloudflare after deploy; `_redirects` is a Cloudflare Pages feature.
- Do **not** cancel Wix/GoDaddy products or alter MX/TXT email DNS records until all systems are tested.
- Form handling intentionally uses real email/telephone links; no misleading 'message sent' simulation.
- Gallery photography is in-situ only. Add artwork catalog later.
- Set up an owner-friendly CMS after launch; current version is a lightweight static deliverable.

## Updating content
The pages are generated from `build_site.py`, which centralizes header, footer and menu content. Run `python build_site.py` to regenerate all HTML after editing the source. Production hosting serves the generated HTML directly without a build process. A non-coder CMS is a recommended post-launch enhancement.
''',encoding='utf-8')
print('Built',len(list(ROOT.glob('*.html'))),'HTML pages')
