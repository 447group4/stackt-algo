from flask import Flask
from flask import jsonify

from db_connector import db_connector
from stackt_algo import stackt_algo
from shapely.geometry import Polygon

md_db = db_connector("localhost", "root", "password")
md_counties = md_db.load_counties("md")
md_state_list = md_db.load_state_boundary("md")

md_polygon = md_db.create_simplified_polygon(md_state_list)
md_algo = stackt_algo(md_polygon, md_counties)
app = Flask(__name__)
print("app is ready")

@app.route('/md')
def md():
    print("md is here")
    district_list = md_algo.begin(8)
    ret_dict = {}
    for i in range(len(district_list)):
        ret_dict[str(i)] = district_list[i]
    print(ret_dict)
    return jsonify({"districts": district_list})
@app.route('/')
def hello():
    print("md is here")
    return "hello"