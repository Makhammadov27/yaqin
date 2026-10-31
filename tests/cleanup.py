"""Remove only QA-prefixed records made by http_regression/smtp_failure in yaqin_course."""
import subprocess,re,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sql(q):
 r=subprocess.run(['C:/xampp/mysql/bin/mysql.exe','-h','127.0.0.1','-u','root','--default-character-set=utf8mb4','-N','-B','yaqin_course','-e',q],capture_output=True,encoding='utf-8',check=True)
 return r.stdout.strip()
ids=sql("SELECT id FROM listings WHERE title REGEXP 'QA[0-9]+' OR title REGEXP '^QA-expire-[0-9]+'").splitlines()
counts={}
if ids:
 assert all(i.isdigit() for i in ids)
 ids=','.join(ids)
 names=sql('SELECT stored_name FROM attachments WHERE listing_id IN ('+ids+')').splitlines()
 sql('START TRANSACTION; DELETE d FROM moderation_decisions d JOIN complaints c ON c.id=d.complaint_id WHERE c.listing_id IN ('+ids+'); DELETE FROM complaints WHERE listing_id IN ('+ids+'); DELETE FROM attachments WHERE listing_id IN ('+ids+'); DELETE FROM listings WHERE id IN ('+ids+'); COMMIT;')
 base=(ROOT/'storage/uploads').resolve()
 for name in names:
  assert re.fullmatch('[a-f0-9]{64}',name)
  p=(base/name).resolve();assert p.parent==base
  if p.exists():p.unlink()
 counts['listings_removed']=len(ids.split(','));counts['files_removed']=len(names)
sql("DELETE FROM categories WHERE name REGEXP '^QA[0-9]+ category'; DELETE FROM users WHERE name REGEXP '^QA[0-9]+$' AND email LIKE 'qa%@example.test'; DELETE FROM contact_messages WHERE email='qa@example.test' AND (message REGEXP '^QA[0-9]+ local test message$' OR message REGEXP '^QA-SMTP-FAIL-[0-9]+ delivery failure fixture$');")
counts['remaining_seed_counts']=sql('SELECT (SELECT COUNT(*) FROM listings),(SELECT COUNT(*) FROM categories),(SELECT COUNT(*) FROM complaints),(SELECT COUNT(*) FROM moderation_decisions),(SELECT COUNT(*) FROM users),(SELECT COUNT(*) FROM attachments);')
Path(__file__).with_name('cleanup-result.json').write_text(json.dumps(counts,indent=2),encoding='utf-8');print(json.dumps(counts))
