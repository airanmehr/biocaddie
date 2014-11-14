import sqlite3;

class dbConnectorMesh():
  def __init__(self, db_name):
    self.conn = sqlite3.connect(db_name);
    self.cur = self.conn.cursor();

  def __enter__(self):
    return self;

  def __exit__(self, type, value, traceback):
    self.conn.close();

  def saveInformation(self, dictionary, table):
    for pmid,header in dictionary.iteritems():
      self.cur.execute('INSERT INTO '+table+'(pmid, header) \
      VALUES (?, ?);', (pmid, str(header)))
    self.conn.commit();

  def upsert(self, dictionary, table):
    for header,entries in dictionary.iteritems():
      self.cur.execute('INSERT INTO '+table+'(header, entry_terms) VALUES (?,?);',(str(header),str(entries)))
  #     # self.cur.execute('INSERT OR REPLACE INTO '+table+'(header, entry_terms) \
  #     # VALUES ('+str(header)+', COALESCE((SELECT entry_terms FROM '+table+' WHERE header = '+str(header)+'), \
  #     # '+str(entries)+'));')
    self.conn.commit();

# CREATE TABLE article_mesh
# (
# pmid INTEGER PRIMARY KEY,
# header TEXT
# );

# CREATE TABLE header_entry
# (
# header TEXT PRIMARY KEY,
# entry_terms TEXT
# );