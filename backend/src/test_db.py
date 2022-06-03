db = MySQLdb.connect('mysql:3306', 'test', 
                     'test', self.schema)
cursor = db.cursor()        
try:
    cursor.execute("SELECT VERSION()")
    results = cursor.fetchone()
    ver = results[0]
    if (ver is None):
        return False
    else:
        return True               
except:
    print "ERROR IN CONNECTION"
    return False
