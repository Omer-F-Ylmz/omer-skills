import json,base64,sys,os
src,w,h=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]);fr=[float(x) for x in sys.argv[4].split(',')];tag=sys.argv[5]
d=os.path.dirname(os.path.abspath(__file__))
html=open(os.path.join(d,src),encoding='utf-8').read()
doc='<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>'
shot='C:/Projeler/omer-skills/sosyal-onizleme/tane-premium/shots/'
js=("async (page) => { await page.setViewportSize({width:%d,height:%d}); const body = Buffer.from(%s,'base64').toString('utf8'); await page.unrouteAll(); const er=[]; page.on('pageerror',e=>er.push(e.message)); "
"await page.route('https://tane.test/**', r => { const u=r.request().url(); if(u.endsWith('/')) return r.fulfill({status:200, contentType:'text/html; charset=utf-8', body}); return r.fulfill({status:404, body:''}); }); "
"await page.goto('https://tane.test/'); await page.waitForTimeout(6000); const fr=%s; for(let i=0;i<fr.length;i++){ await page.evaluate(f=>{window.scrollTo(0,(document.documentElement.scrollHeight-innerHeight)*f)},fr[i]); await page.waitForTimeout(400); await page.evaluate(()=>window.scrollBy(0,2)); await page.waitForTimeout(1800); await page.screenshot({path:'%s%s-'+i+'.jpg',type:'jpeg',quality:70}); } "
"const ow=await page.evaluate(()=>document.documentElement.scrollWidth); return 'SONUC '+JSON.stringify({er,ow}); }")%(w,h,json.dumps(base64.b64encode(doc.encode()).decode()),json.dumps(fr),shot,tag)
open(os.path.join(d,'..','tane-vitrin','pw-ac.js'),'w',encoding='utf-8').write(js);print('ok')
