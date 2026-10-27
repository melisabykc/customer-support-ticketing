import argparse,json,sqlite3
from pathlib import Path
DB=Path(__file__).with_name('data.sqlite3')
def connect(path=DB):
 c=sqlite3.connect(str(path));c.row_factory=sqlite3.Row;c.execute('CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY,customer TEXT NOT NULL,subject TEXT NOT NULL,priority TEXT NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL)');return c
def add(customer,subject,priority,status,created_at,path=DB):
 if priority not in ('low','medium','high','urgent'):raise ValueError('invalid priority')
 if status not in ('open','in_progress','resolved','closed'):raise ValueError('invalid status')
 with connect(path) as c:cur=c.execute('INSERT INTO tickets(customer,subject,priority,status,created_at) VALUES(?,?,?,?,?)',(customer,subject,priority,status,created_at));return cur.lastrowid
def listing(path=DB):
 with connect(path) as c:return [dict(r) for r in c.execute('SELECT * FROM tickets ORDER BY id DESC')]
def report(path=DB):
 rows=listing(path);return {'tickets':len(rows),'by_status':{s:sum(r['status']==s for r in rows) for s in ('open','in_progress','resolved','closed')},'urgent_open':sum(r['priority']=='urgent' and r['status']=='open' for r in rows)}
def main():
 p=argparse.ArgumentParser(description='Customer support ticketing');s=p.add_subparsers(dest='cmd',required=True);a=s.add_parser('add');a.add_argument('--customer',required=True);a.add_argument('--subject',required=True);a.add_argument('--priority',choices=['low','medium','high','urgent'],default='medium');a.add_argument('--status',choices=['open','in_progress','resolved','closed'],default='open');a.add_argument('--created-at',required=True);s.add_parser('list');s.add_parser('report');x=p.parse_args()
 if x.cmd=='add':print(json.dumps({'id':add(x.customer,x.subject,x.priority,x.status,x.created_at)}))
 elif x.cmd=='list':print(json.dumps(listing(),indent=2))
 else:print(json.dumps(report(),indent=2))
if __name__=='__main__':main()
