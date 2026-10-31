"""Authorized local integration regression. Uses only Python standard library.
Run: python tests/http_regression.py http://127.0.0.1:4180
Only dedicated QA records are created in the demo database.
"""
import subprocess, base64, datetime
import urllib.request, urllib.parse, urllib.error, http.cookiejar, re, html, json, sys, time, csv, io
from pathlib import Path
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4180').rstrip('/')+'/index.php'
results=[]
class Client:
 def __init__(self):
  self.jar=http.cookiejar.CookieJar();self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
 def req(self,route='listings',data=None,query=None,files=None):
  url=BASE+'?'+urllib.parse.urlencode({'route':route,**(query or {})}); headers={};body=None
  if files:
   boundary='qa_boundary_871293';parts=[]
   for k,v in (data or {}).items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
   for field,name,mime,content in files:parts.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"; filename="{name}"\r\nContent-Type: {mime}\r\n\r\n'.encode(),content,b'\r\n'])
   parts.append(f'--{boundary}--\r\n'.encode());body=b''.join(parts);headers['Content-Type']='multipart/form-data; boundary='+boundary
  elif data is not None:body=urllib.parse.urlencode(data).encode()
  try:r=self.opener.open(urllib.request.Request(url,body,headers),timeout=20)
  except urllib.error.HTTPError as e:r=e
  return r.code,r.read().decode('utf-8',errors='replace'),r.headers
 def token(self,route='listings',query=None):
  status,text,_=self.req(route,query=query);m=re.search(r'name="csrf"\s+value="([^"]+)"',text)
  if not m:raise RuntimeError(f'CSRF not found {route}: {status}')
  return html.unescape(m.group(1))
 def post(self,route,data,tokenroute='listings',query=None,files=None):return self.req(route,data={'csrf':self.token(tokenroute,query),**data},files=files)
 def login(self,email,password):return self.post('login',{'email':email,'password':password},'login')
def check(name,condition,detail=''):
 results.append({'test':name,'passed':bool(condition),'detail':detail});print(('PASS ' if condition else 'FAIL ')+name,flush=True)
def sql(query):
 proc=subprocess.run(['C:/xampp/mysql/bin/mysql.exe','-h','127.0.0.1','-u','root','--default-character-set=utf8mb4','-N','-B','yaqin_course','-e',query],capture_output=True,encoding='utf-8')
 if proc.returncode:raise RuntimeError(proc.stderr)
 return proc.stdout.strip()
def run():
 guest=Client();admin=Client();user=Client();other=Client();mod=Client()
 check('unknown route404',guest.req('qa-missing-route')[0]==404)
 check('anonymous protected users denied',guest.req('users')[0] in (401,403))
 check('CSRF missing rejected',guest.req('login',data={'email':'admin@yaqin.test','password':'Admin123!'})[0]==403)
 for name,c,email,pwd in [('admin',admin,'admin@yaqin.test','Admin123!'),('user',user,'user@yaqin.test','User123!'),('other',other,'user2@yaqin.test','User123!'),('moderator',mod,'moderator@yaqin.test','Moderator123!')]:
  status,text,h=c.login(email,pwd);check('login '+name,status==200,f'HTTP {status}')
 check('session HttpOnly SameSite',all(c.has_nonstandard_attr('HttpOnly') and c.get_nonstandard_attr('SameSite')=='Lax' for c in user.jar))
 check('ordinary user admin route denied',user.req('users')[0]==403)
 check('moderator admin route denied',mod.req('users')[0]==403)
 check('GET mutation rejected',admin.req('category-delete',query={'id':1})[0]==405)
 check('SQL-shaped search safe',guest.req('listings',query={'q':"' OR 1=1 --"})[0]==200)
 check('invalid sort is safe',guest.req('listings',query={'sort':'price;DROP TABLE users'})[0]==200)
 check('private files guest denied',guest.req('files')[0] in (401,403))
 marker='QA'+str(int(time.time()))
 reg=Client()
 check('registration role escalation blocked',reg.post('register',{'name':marker,'email':marker.lower()+'@example.test','password':'QaTest123!','role':'admin'},'register')[0]==200 and sql("SELECT role FROM users WHERE email='"+marker.lower()+"@example.test'")=='user')
 status,csvbody,_=admin.req('export')
 rows=list(csv.reader(io.StringIO(csvbody.lstrip('\ufeff'))))
 check('CSV all pages',status==200 and len(rows)-1==int(sql("SELECT COUNT(*) FROM listings WHERE status<>'archived'")) and len(rows)>9)
 page1=guest.req('listings',query={'page':1})[1];page2=guest.req('listings',query={'page':2})[1]
 check('pagination changes list',page1!=page2 and guest.req('listings',query={'page':2})[0]==200)
 # Database assertions use only application-created dedicated QA records.
 title=marker+' listing'
 fields={'title':title,'description':'QA dedicated listing description long enough','category_id':'1','city':'Toshkent','price':'123456','phone':'+998901234567','expires_at':(datetime.date.today()+datetime.timedelta(days=5)).isoformat()}
 check('listing invalid fields rejected',user.post('listing-save',{'title':''})[0]==422)
 check('listing create',user.post('listing-save',fields)[0]==200)
 lid=sql("SELECT id FROM listings WHERE title='"+title+"'")
 if not lid:raise RuntimeError('Created listing absent in DB')
 check('listing read',title in user.req('listing',query={'id':lid})[1])
 check('listing ownership edit denied',other.post('listing-save',{**fields,'id':lid,'title':marker+' stolen'})[0]==403)
 check('listing ownership archive denied',other.post('listing-delete',{'id':lid,'confirm':'yes'})[0]==403)
 xss='<script>alert(1)</script>'
 fields['title']=marker+' '+xss
 check('listing update',user.post('listing-save',{**fields,'id':lid})[0]==200)
 body=user.req('listing',query={'id':lid})[1]
 check('XSS escaped',xss not in body and '&lt;script&gt;' in body)
 check('listing expire',user.post('listing-expire',{'id':lid,'expected_expires_at':sql('SELECT expires_at FROM listings WHERE id='+lid)})[0]==200 and sql('SELECT status FROM listings WHERE id='+lid)=='expired')
 check('expired listing guest inaccessible',guest.req('listing',query={'id':lid})[0]==403)
 check('repeat expire rejected',user.post('listing-expire',{'id':lid,'expected_expires_at':sql('SELECT expires_at FROM listings WHERE id='+lid)})[0]==409)
 previous_expiry=sql('SELECT expires_at FROM listings WHERE id='+lid)
 check('listing extend',user.post('listing-extend',{'id':lid,'expected_expires_at':previous_expiry})[0]==200 and sql('SELECT status FROM listings WHERE id='+lid)=='active')
 check('repeat stale extension rejected',user.post('listing-extend',{'id':lid,'expected_expires_at':previous_expiry})[0]==409)
 check('complaint created',other.post('complaint-create',{'listing_id':lid,'reason':'QA complaint reason long enough'})[0]==200)
 check('repeat complaint rejected',other.post('complaint-create',{'listing_id':lid,'reason':'QA duplicate complaint reason'})[0]==409)
 cid=sql('SELECT id FROM complaints WHERE listing_id='+lid)
 check('ordinary user moderation denied',user.post('complaint-decide',{'id':cid,'outcome':'approved','note':'QA moderator decision note'})[0]==403)
 check('moderation approval',mod.post('complaint-decide',{'id':cid,'outcome':'approved','note':'QA moderator decision note'})[0]==200 and sql('SELECT status FROM listings WHERE id='+lid)=='blocked')
 check('repeat moderation rejected',mod.post('complaint-decide',{'id':cid,'outcome':'approved','note':'QA moderator decision note'})[0]==409)
 check('blocked extension rejected',user.post('listing-extend',{'id':lid,'expected_expires_at':sql('SELECT expires_at FROM listings WHERE id='+lid)})[0]==409)
 check('fourth section decisions',mod.req('decisions')[0]==200)
 # Category create/read/update/delete with no dependent listings.
 cname=marker+' category'
 check('category user forbidden',user.post('category-save',{'name':cname,'description':'QA category description'})[0]==403)
 check('category create',admin.post('category-save',{'name':cname,'description':'QA category description'})[0]==200)
 catid=sql("SELECT id FROM categories WHERE name='"+cname+"'")
 check('category read',cname in admin.req('category',query={'id':catid})[1])
 check('category update',admin.post('category-save',{'id':catid,'name':cname+' updated','description':'QA updated category description'})[0]==200)
 check('category delete requires confirmation',admin.post('category-delete',{'id':catid})[0] in (409,422))
 check('category delete',admin.post('category-delete',{'id':catid,'confirm':'yes'})[0]==200 and sql('SELECT COUNT(*) FROM categories WHERE id='+catid)=='0')
 check('category FK restrict',admin.post('category-delete',{'id':'1','confirm':'yes'})[0] in (409,422))
 # Authorized filtered CSV: all matching owner rows, no password hashes or tokens.
 fields['title']='=SUM(1,2) '+marker
 check('CSV fixture create',user.post('listing-save',fields)[0]==200)
 fid=sql("SELECT id FROM listings WHERE title LIKE '%"+marker+"' AND title LIKE '=SUM%'")
 status,body,headers=user.req('export',query={'q':marker,'category':1,'city':'Toshkent','sort':'low'})
 check('CSV authorized filtered',status==200 and marker in body and 'password_hash' not in body and 'csrf' not in body)
 check('CSV formula neutralized',"'=SUM" in body)
 # Attachment cases on a still-active owned listing.
 png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jV9sAAAAASUVORK5CYII=')
 pdf=b'%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF'
 mp4=(Path(__file__).parents[1]/'samples/sample.mp4').read_bytes()
 pdf=(Path(__file__).parents[1]/'samples/sample.pdf').read_bytes()
 for name,mime,content in [('test.png','image/png',png),('test.pdf','application/pdf',pdf),('test.mp4','video/mp4',mp4)]:
  status,body,_=user.post('file-upload',{'listing_id':fid,'description':marker+' '+name},files=[('file',name,mime,content)])
  check('upload '+name,status==200,f'HTTP {status}')
 aid=sql('SELECT id FROM attachments WHERE listing_id='+fid+' ORDER BY id LIMIT 1')
 if aid:
  check('private file nonowner denied',other.req('file-download',query={'id':aid})[0]==403)
  check('private file moderator download',mod.req('file-download',query={'id':aid})[0]==200)
  check('private file owner download',user.req('file-download',query={'id':aid})[0]==200)
  check('attachment replace',user.post('file-upload',{'listing_id':fid,'description':marker+' replacement','replace_id':aid},files=[('file','replace.png','image/png',png)])[0]==200)
  aid=sql('SELECT id FROM attachments WHERE listing_id='+fid+' AND description LIKE "%replacement" LIMIT 1')
  check('attachment delete',user.post('file-delete',{'id':aid,'confirm':'yes'})[0]==200 and sql('SELECT COUNT(*) FROM attachments WHERE id='+aid)=='0')
 check('MIME extension mismatch rejected',user.post('file-upload',{'listing_id':fid,'description':'QA mismatch'},files=[('file','bad.png','image/png',pdf)])[0]==422)
 check('oversized image rejected',user.post('file-upload',{'listing_id':fid,'description':'QA oversized'},files=[('file','big.png','image/png',png+b'0'*(2*1024*1024))])[0]==422)
 check('executable upload rejected',user.post('file-upload',{'listing_id':fid,'description':'QA executable'},files=[('file','bad.php','application/octet-stream',b'<?php echo 1;')])[0]==422)
 check('file search',marker in user.req('files',query={'q':marker})[1])
 check('contact invalid email rejected',guest.post('contact',{'name':'QA','email':'invalid','message':'QA message long enough'},'contact')[0]==422)
 check('contact accepted',guest.post('contact',{'name':'QA','email':'qa@example.test','message':marker+' local test message'},'contact')[0]==200)
 check('contact rate limited',guest.post('contact',{'name':'QA','email':'qa@example.test','message':'QA duplicate rate limit message'},'contact')[0]==429)
 check('contact persisted',sql("SELECT COUNT(*) FROM contact_messages WHERE message='"+marker+" local test message'")=='1')
 check('contact SMTP status',sql("SELECT smtp_status FROM contact_messages WHERE message='"+marker+" local test message'")=='sent')
 check('archive owned listing',user.post('listing-delete',{'id':lid,'confirm':'yes'})[0]==200 and sql('SELECT status FROM listings WHERE id='+lid)=='archived')
 check('logout',user.post('logout',{})[0]==200)
 check('post-logout protected denied',user.req('files')[0] in (401,403))
 return {'admin':admin,'user':user,'other':other,'mod':mod,'guest':guest}
if __name__=='__main__':
 try:clients=run()
 except Exception as e:check('test execution',False,str(e))
 Path(__file__).with_name('results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'{sum(r["passed"] for r in results)}/{len(results)} passed')
 sys.exit(0 if all(r['passed'] for r in results) else 1)
