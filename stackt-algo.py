from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.ops import split
from math import isclose

import matplotlib.pyplot as plt

import itertools

class stackt_algo:
	def __init__(self, state_boundaries, population_polygons):
		#error checking!
		self.state_poly = Polygon(state_boundaries)
		self.population_polygons = population_polygons
		self.total_pop = 0
		x,y = self.state_poly.exterior.xy
		plt.plot(x,y)
		for i in self.population_polygons:
			x, y = i["poly"].exterior.xy
			plt.plot(x,y)
		plt.show()
		"""for population_point in population_points:
			self.total_pop += population_point["population"]
		xs = [point["point"].x for point in self.population_points]
		ys = [point["point"].y for point in self.population_points]
		plt.scatter(ys, xs)
		x, y = self.state_poly.exterior.xy
		plt.plot(y, x)"""
		
		
	def get_population_in_polygon(self, poly):
		total=0
		for population_poly in self.population_polygons:
			if population_poly["poly"].intersects(poly):
				intersect_area = population_poly["poly"].intersection(poly).area
				total+=(intersect_area/population_poly["poly"].area)*population_poly["population"]

		return total

	def closest_k_in_list(self, array, target):
		print("target = " + str(target))
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
		x,y  = poly.exterior.xy
		plt.plot(y,x)
		plt.show()
		print(num_districts)
		if num_districts == 1:
			
			return [poly]
		A = num_districts // 2
		B = num_districts - A
		permutations = itertools.permutations(list(poly.exterior.coords), 2)
		candidates = []
		for permutation in permutations:
			line_ = LineString(permutation)
			midpoint = (list(line_.interpolate(line_.length/2).coords)[0])
			print(midpoint)
			print((permutation[0], midpoint, permutation[1]))
			line = LineString((permutation[0], midpoint, permutation[1]))
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
		(1,-1),
		(0,-1),
		(-1,-1),
		(-1,0),
		(-1,1),
		(0,1),
		(1,1),
		(1,0),
		

	]	

	pop_polys = [
		{"poly":Polygon([(-1,-1),(-1,0),(0,0),(0,-1)]), "population": 100},
		{"poly":Polygon([(1,1),(1,0),(0,0),(0,1)]), "population": 100},
		{"poly":Polygon([(-1,1),(-1,0),(0,0),(0,1)]), "population": 100},
		{"poly":Polygon([(1,-1),(1,0),(0,0),(0,-1)]), "population": 100},
	]
	

	try:
		s = stackt_algo(sq, pop_polys)
		end_polys = s.begin(4)
		for i in end_polys:
			x,y = i.exterior.xy
			plt.plot(x,y)
		plt.show()
	except:
		import traceback
		traceback.print_exc()
test()
		
		
			
