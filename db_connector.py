import mysql.connector 
import re
from shapely.geometry import Polygon
import stackt_algo
import matplotlib.pyplot as plt
from shapely.geometry import LineString, MultiPolygon
from shapely.ops import polygonize, unary_union
from math import isclose

class db_connector:
    def __init__(self, url, username, password):
        # create md database connection
        self.md_db = mysql.connector.connect(
            host=url,
            user=username,
            passwd=password,
            database = "md_database",
            auth_plugin='mysql_native_password'
        )
        # save county names for future use
        self.md_county_names = []
        cursor = self.md_db.cursor()
        cursor.execute("SHOW TABLES")
        for table in cursor.fetchall():
            match = re.search("^(.+)county points$", table[0])
            if match != None:
                self.md_county_names.append(match.group(1))
    def load_counties(self, state):
        if state == "md":
            print("load_counties")
            county_dicts = []
            mycursor = self.md_db.cursor()
            mycursor.execute("SELECT * FROM md_population")
            county_pops = mycursor.fetchall()
            print(county_pops)
            for name in self.md_county_names:
                # go through names and select their polygon tables 
                mycursor.execute("SELECT * FROM `" + name + "county points`")
                #some counties have islands so we need to merge them together into 1 simple polygon
                data = mycursor.fetchall()
                ls = LineString(data)
                lr = LineString(ls.coords[:] + ls.coords[0:1])
                mls = unary_union(lr)
                mp = MultiPolygon(list(polygonize(mls)))
                start_geom = mp.geoms[0]
                for geom in mp.geoms:
                    new_geom = start_geom.union(geom)
                    if new_geom.is_simple:
                        start_geom = new_geom

                # save name and polygon in return dictionary
                county_dict = {"name": name, "poly": new_geom}
                for county_pop in county_pops:
                    # go through all of the counties and get their populations
                    if county_pop[0].lower().rstrip()+ ' ' == (name.lower()):
                        # add the populations to the respective dictionary 
                        county_dict["population"] = county_pop[1]
                        break
                county_dicts.append(county_dict)
            return county_dicts
        
    def load_state_boundary(self, state):
        print("load_state_boundary")
        if state == "md":
            # grab all points defining state boundary
            mycursor = self.md_db.cursor()
            mycursor.execute("SELECT * FROM `maryland border points`;")
            all_points =  mycursor.fetchall()
            return all_points

    # this function is for optimization
    def create_simplified_polygon(self, point_list):
        # simplify polygon by only saving points that have large change in position from previous point
        last_point = point_list[0]
        ret_list = [last_point]
        for point in point_list:
            if not (isclose(point[0], last_point[0], abs_tol=.001) or isclose(point[1], last_point[1], abs_tol=.015)):
                ret_list.append(point)
                last_point = point
        return Polygon(ret_list)
