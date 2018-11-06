#Run to update manufacturer column for all devices

import mysql.connector
from manuf import manuf

p = manuf.MacParser()

cnx = mysql.connector.connect(host="mysql", user="root", passwd="yourpass", database="yourdb", buffered=True)
cur = cnx.cursor(dictionary=True)
cur.execute("SELECT id, MAC FROM devices")
for row in cur:
    manufacturer = p.get_manuf_long(row["MAC"])
    update = cnx.cursor()
    update.execute("UPDATE `devices` SET manufacturer = %s WHERE id = %s", (manufacturer, row["id"]))
cnx.commit()
cnx.close()
