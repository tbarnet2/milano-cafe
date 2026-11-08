from pathlib import Path
import re,base64
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse,unquote
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,os
root=Path(__file__).parent.resolve()
os.chdir(root)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
srv=ThreadingHTTPServer(('127.0.0.1',8765),Quiet)
threading.Thread(target=srv.serve_forever,daemon=True).start()
errs=[]
for page in root.glob('*.html'):
 soup=BeautifulSoup(page.read_text(),'html.parser')
 for img in soup.find_all('img'):
  if not img.get('alt'):errs.append(f'{page.name}: img without alt')
  if not (root/img.get('src','')).exists():errs.append(f'{page.name}: missing img '+img.get('src',''))
 for a in soup.find_all('a'):
  href=a.get('href',''); u=urlparse(href)
  if not u.scheme and not u.netloc and u.path and not u.path.startswith('#') and not (root/u.path).exists():errs.append(f'{page.name}: missing href {href}')
print('STATIC AUDIT ERRORS',errs)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for name,width,height in [('home-desktop',1440,1000),('home-mobile',390,844),('menu-desktop',1440,900),('gallery-mobile',390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  url={'home-desktop':'index.html','home-mobile':'index.html','menu-desktop':'menu.html','gallery-mobile':'gallery.html'}[name]
  html=(root/url).read_text()
  html=html.replace('<link rel="stylesheet" href="assets/css/site.css">','<style>'+ (root/'assets/css/site.css').read_text() +'</style>')
  html=html.replace('<script src="assets/js/site.js" defer></script>','<script>'+ (root/'assets/js/site.js').read_text() +'</script>')
  def data_photo(m):
   raw=(root/m.group(1)).read_bytes()
   return 'src="data:image/webp;base64,'+base64.b64encode(raw).decode()+'"'
  html=re.sub(r'src="(assets/photos/[^"]+)"',data_photo,html)
  page.set_content(html,wait_until='domcontentloaded',timeout=60000)
  resp=None
  page.evaluate('''() => { document.querySelectorAll('img').forEach(el => el.loading = 'eager'); }''')
  page.wait_for_timeout(250)
  total=page.evaluate('document.documentElement.scrollHeight')
  for y in range(0,total,550):
   page.evaluate('(y)=>window.scrollTo(0,y)',y)
   page.wait_for_timeout(80)
  page.evaluate('window.scrollTo(0,0)')
  page.wait_for_timeout(350)
  print(name,'images loaded',page.evaluate('''() => [...document.querySelectorAll('img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,src:i.getAttribute('src').slice(0,30)}))'''))
  path=root.parent/(name+'.png')
  page.screenshot(path=str(path),full_page=True)
  print(name,'status',resp.status if resp else 'file','errors',errors,'horizontal overflow',page.evaluate('document.documentElement.scrollWidth > innerWidth'),'size',path.stat().st_size)
  if name=='menu-desktop':
   page.get_by_role('tab',name='Dinner menu').click()
   print('dinner visible',page.locator('#dinner-panel').is_visible(),'lunch hidden',not page.locator('#lunch-panel').is_visible(),'selected',page.locator('#dinner-tab').get_attribute('aria-selected'))
  if name=='home-mobile':
   page.locator('.menu-toggle').click()
   print('menu open mobile',page.locator('.nav-links').is_visible(),page.locator('.menu-toggle').get_attribute('aria-expanded'))
  page.close()
 browser.close()
srv.shutdown()
