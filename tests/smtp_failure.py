"""Run only after coordinator stops the local test SMTP sink and 60s after prior contact."""
from http_regression import Client,sql
import time,json
from pathlib import Path
c=Client();marker='QA-SMTP-FAIL-'+str(int(time.time()))
status,body,_=c.post('contact',{'name':'QA failure','email':'qa@example.test','message':marker+' delivery failure fixture'},'contact')
result={'http':status,'persisted_status':sql("SELECT smtp_status FROM contact_messages WHERE message='"+marker+" delivery failure fixture'"),'expected':'failed','passed':False}
result['passed']=status==200 and result['persisted_status']=='failed'
Path(__file__).with_name('smtp_failure_result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result));raise SystemExit(0 if result['passed'] else 1)
