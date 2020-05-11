from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely import speedups
from shapely.ops import split
from math import isclose
from shapely.strtree import STRtree
import matplotlib.pyplot as plt

import itertools
from shapely import speedups

class stackt_algo:
	def __init__(self, state_polygon, population_polygons):
		self.finished_districts = 0
		speedups.enable()
		self.state_poly = state_polygon
		self.population_polygons = population_polygons
		self.total_pop = 0
		self.county_population_list = [] # keep track of each counties population
		self.county_polygon_list = [] # keep track of each counties polygon
		for i in population_polygons:
			self.county_polygon_list.append(i["poly"])
			self.county_population_list.append(i["population"])
		self.county_tree = STRtree(self.county_polygon_list) # STR trees for faster intersection detection

		
		
	def get_population_in_polygon(self, poly):
		total=0
		for int_poly in self.county_tree.query(poly): # find all county polygons in given polygon
			intersect_area = int_poly.intersection(poly).area # find the amount of the county the polygon intersects
			# here we are assuming that each county has an even distribution of population 			
			total+=(intersect_area/int_poly.area)*self.county_population_list[self.county_polygon_list.index(int_poly)]

		return total

	def closest_k_in_list(self, array, target):
		ratio_array = []
		if len(array) == 0:
			exit(1) # we cannot run this on an empty list
		for i in array:
			ratio_array.append(i["ratio"])
		noramlized_ratios = map(lambda x: abs(x-target),ratio_array) # see how close each candidate is to a given ratio
		noramlized_ratios_2 = map(lambda x: abs(x-target),ratio_array) # map is used up after accessing so have to make 2
		min_value = min(noramlized_ratios) # find closest split 
		found_keys = []
		print("min value: " + str(min_value))
		for i,val in enumerate(noramlized_ratios_2):
			if isclose(val, min_value): # find all splits close to closest split
				found_keys.append(i)
		ret_list = []
		for i in found_keys:
			ret_list.append(array[i])
			print(array[i])
		return ret_list



	def shortest_split_line(self, num_districts, poly):
		if num_districts == 1: #always write base case first
			self.finished_districts+=1
			return [{"district_number": self.finished_districts, "Polygon": list(poly.exterior.coords), "population": self.get_population_in_polygon(poly)}]
		A = num_districts // 2
		B = num_districts - A
		# split lines are made from a combination of exterior points
		combinations = itertools.combinations(list(poly.exterior.coords), 2)
		candidates = []

		#optimization
		count = 0
		N = 2
		skip = (len(poly.exterior.coords)//N)-50
		#this is the slow part
		for combination in combinations: # loop through all possible lines
			if count%(skip) == 0: # skip as many as possible for speed
				point_a = combination[0]
				point_b = combination[1]
				# create line with midpoint from combination
				line_ = LineString([point_a, point_b])
				midpoint = (list(line_.interpolate(line_.length/2).coords)[0])
				line = LineString([point_a, midpoint, point_b])
				# split given polygon by generated line
				polys = split(poly, line)
				if len(polys.geoms) == 2:
					pop_in_a = self.get_population_in_polygon(polys.geoms[0]) #get population in each new polygon
					pop_in_b = self.get_population_in_polygon(polys.geoms[1])
					if pop_in_a != 0 and pop_in_b !=0:
						ratio = pop_in_a/pop_in_b 
						combo_dict = {} # store length of splitline and ratio it creates
						combo_dict["polys"] = (polys.geoms[0], polys.geoms[1])
						combo_dict["ratio"] = ratio
						combo_dict["length"] = line.length
						candidates.append(combo_dict)
							
			count +=1
				
								
		best_candidates = self.closest_k_in_list(candidates, A/B) # find candidates with closest to ideal split
		best_split = min(best_candidates, key=lambda x:x['length']) # of those candidates choose one with shortest length
		print("expected ratio: " + str(A/B))
		print("found ratio:" + str(best_split["ratio"]))
		ret = []
		ret += self.shortest_split_line(A, best_split["polys"][0]) #run algorithm on both new polygons
		ret += self.shortest_split_line(B, best_split["polys"][1])
		return ret
	
	# function to start recursive shortest-splitline algorithm
	def begin(self, num_districts):
		return self.shortest_split_line(num_districts, self.state_poly)
					
def test():
	# simple square test
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

		
		
			
