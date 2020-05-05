import mysql.connector 
import re
from shapely.geometry import Polygon
class db_connector:
    def __init__(self, url, username, password):
        self.md_db = mysql.connector.connect(
            host=url,
            user=username,
            passwd=password,
            database = "md_database",
            auth_plugin='mysql_native_password'
        )
        self.county_names = []
        cursor = self.md_db.cursor()
        cursor.execute("SHOW TABLES")
        for table in cursor.fetchall():
            match = re.search("^(.+)county points$", table[0])
            if match != None:
                #print(match.group(1))
                self.county_names.append(match.group(1))
    def load_counties(self):
        print("load_counties")
        county_dicts = []
        mycursor = self.md_db.cursor()
        for table in self.county_names:
            mycursor.execute("SELECT * FROM `" + table + "county points`")
            county_dict = {"poly": mycursor.fetchall()}
            county_dicts.append(county_dict)
        return county_dicts
        
    def load_state_boundary(self):
        print("load_state_boundary")
        mycursor = self.md_db.cursor()
        mycursor.execute("SELECT * FROM `maryland border points`;")
        return mycursor.fetchall()
    

conn = db_connector("localhost", "root", "password")
points = conn.load_state_boundary()
print(type(points))
print(conn.load_counties())

