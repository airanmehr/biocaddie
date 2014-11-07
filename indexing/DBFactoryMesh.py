import sqlite3;

class dbConnectorMesh():
  def __init__(self, db_name):
    self.conn = sqlite3.connect(db_name);
    self.cur = self.conn.cursor();

  def __enter__(self):
    return self;

  def __exit__(self, type, value, traceback):
    self.conn.close();

  def saveInformation(self, values, table):      
    self.cur.execute('INSERT INTO '+table+'(pmid, mesh_tags) \
      VALUES (?, ?)', (values['pmid'], str(values['mesh_tags'])))
    self.conn.commit();