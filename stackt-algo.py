from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.ops import split
from math import isclose

import matplotlib.pyplot as plt

import itertools

class stackt_algo:
	def __init__(self, state_boundaries, population_points):
		#error checking!
		self.state_poly = Polygon(state_boundaries)
		self.population_points = population_points
		self.total_pop = 0
		for population_point in population_points:
			self.total_pop += population_point["population"]
		xs = [point["point"].x for point in self.population_points]
		ys = [point["point"].y for point in self.population_points]
		plt.scatter(ys, xs)
		x, y = self.state_poly.exterior.xy
		plt.plot(y, x)
		
	def get_population_in_polygon(self, poly):
		total=0
		for population_point in self.population_points:
			if population_point["point"].within(poly):
				total+=population_point["population"]

		return total

	def closest_k_in_list(self, array, target):
		epsilon = 0.00
		ratio_array = []
		if len(array) == 0:
			print("oh no")
		for i in array:
			ratio_array.append(i["ratio"])
		noramlized_ratios = map(lambda x: abs(x-target),ratio_array)
		noramlized_ratios_2 = map(lambda x: abs(x-target),ratio_array)
		min_value=min(noramlized_ratios)
		found_keys = []

		for i,val in enumerate(noramlized_ratios_2):
			if isclose(val, min_value):
				found_keys.append(i)
		ret_list = []
		for i in found_keys:
			ret_list.append(array[i])
		return ret_list



	def shortest_split_line(self, num_districts, poly):
		print(num_districts)
		if num_districts == 1:
			x,y  = poly.exterior.xy
			plt.plot(y,x)
			plt.show()
			

			return [poly]
		A = num_districts // 2
		B = num_districts - A
		permutations = itertools.permutations(list(poly.exterior.coords), 2)
		candidates = []
		for permutation in permutations:
			line = LineString(permutation)
			polys = split(poly, line)
			if len(polys.geoms) == 2:
				poly_a = polys.geoms[0]
				poly_b = polys.geoms[1]
				pop_in_a = self.get_population_in_polygon(poly_a)
				pop_in_b = self.get_population_in_polygon(poly_b)
				if pop_in_a != 0 and pop_in_b !=0:
					ratio = pop_in_a/pop_in_b
					combo_dict = {}
					combo_dict["polys"] = (poly_a, poly_b)
					combo_dict["ratio"] = ratio
					combo_dict["length"] = line.length
					candidates.append(combo_dict)
		best_candidates = self.closest_k_in_list(candidates, A/B)
		best_split = min(best_candidates, key=lambda x:x['length'])
		ret = []
		ret += self.shortest_split_line(A, best_split["polys"][0])
		ret += self.shortest_split_line(B, best_split["polys"][1])
		return ret
		
				



	
	
	def begin(self,num_districts):
		return self.shortest_split_line(num_districts, self.state_poly)
					
def test():
	sq = [
		(39.233528,-79.478559),
		(39.716904,-79.462079),
		(39.712679,-75.792646),
		(38.459179,-75.704755),
		(38.450576,-75.073041),
		(38.027755,-75.171918),
		(37.932499,-75.776166),
		(38.33433,-76.204633),
		(38.652484,-76.232099),
		(38.930783,-76.215619),
		(39.229273,-76.232099),
		(39.38229,-76.105756),
		(39.352563,-76.330976),
		(39.276064,-76.42436),
		(39.088714,-76.51225),
		(38.952146,-76.517743),
		(38.789629,-76.539716),
		(38.484983,-76.446332),
		(38.360179,-76.429853),
		(38.252415,-76.396894),
		(38.096955,-76.325483),
		(38.075337,-76.358442),
		(38.342708,-76.987369),
		(38.362093,-77.29224),
		(38.51054,-77.305973),
		(38.630793,-77.135684),
		(38.720851,-77.080753),
		(38.755129,-77.05054),
		(38.896352,-76.907718),
		(39.001018,-77.045047),
		(38.934819,-77.121952),
		(38.97967,-77.201602),
		(39.040018,-77.314402),
		(39.133821,-77.525889),
		(39.318926,-77.649485),
		(39.127153,-77.830228),
		(39.45875,-78.343839)
	]	

	pop_points = [
		{"point":Point((38.5, -77)), "population": 620961},
		{"point":Point((39.595,-77.647)), "population": 63374},
		{"point":Point((39.245,-77.244)), "population": 65239},
		{"point":Point((38.5823,-76.)), "population": 38394},
	]
	

	try:
		s = stackt_algo(sq, pop_points)
		print(s.begin(4))
		plt.show()
	except:
		import traceback
		traceback.print_exc()
test()
		
		
			
