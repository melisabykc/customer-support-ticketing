import tempfile,unittest
from pathlib import Path
import app
class Tests(unittest.TestCase):
 def test_ticket_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.sqlite3';app.add('Ada','Login problem','urgent','open','2026-10-27',p);self.assertEqual(app.report(p)['urgent_open'],1)
if __name__=='__main__':unittest.main()
