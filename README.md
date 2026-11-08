# Milano Café & Art Gallery — Website Launch Candidate

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
- Reservation link: https://reserve.spoton.com/restaurant/73694
- Ordering link: https://order.spoton.com/so-milano-cafe-23898/austin-tx/682b85c2b3310a5fadb57869
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
