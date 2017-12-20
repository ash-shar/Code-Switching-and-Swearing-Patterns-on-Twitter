from __future__ import print_function
import json
import sys
import codecs
import os


def edit_distance(source,dest):
	n = len(source)
	m = len(dest)
	i = 0
	j = 0
	L = []
	for i in range(n+1):
		L.append([])
	for i in range(n+1):
		for j in range(m+1):
			L[i].append(0)
			
	for i in range(n+1):
		L[i][0] = i
	for j in range(m+1):
		L[0][j] = j
	for i in range(1,n+1):
		for j in range(1,m+1):
			if source[i-1] == dest[j-1]:
				L[i][j] = min((L[i-1][j]+1),(L[i][j-1]+1),(L[i-1][j-1]))
			else:
				L[i][j] = min((L[i-1][j]+1),(L[i][j-1]+1),(L[i-1][j-1]+1))
	return L[n][m]

def detect_location(bio):
	cityf = codecs.open("Corpus/city.txt",'r','utf-8')
	statef = codecs.open("Corpus/states.txt",'r','utf-8')
	countryf = codecs.open("Corpus/countries.txt",'r','utf-8')
	locf = codecs.open("Corpus/loc.txt",'r','utf-8')
	worldf = codecs.open("Corpus/worldcitieslist_1.txt",'r','utf-8')
	world_locf = codecs.open("Corpus/worldcitieslist_2.txt",'r','utf-8')

	city = []
	state = []
	country = []
	loc = {}
	world = []
	world_loc = {}

	for row in cityf:
		city.append(row.strip().lower())

	for row in statef:
		state.append(row.strip().lower())

	for row in countryf:
		country.append(row.strip().lower())

	for row in worldf:
		world.append(row.strip().lower())

	for row in locf:
		s = row.split('\t')
		loc[s[0].strip().lower()] = s[2].strip().lower()

	for row in world_locf:
		s = row.split('\t')
		world_loc[s[0].strip().lower()] = s[1].strip().lower()

	dict_loc = {'city':'', 'state': '', 'country':''}


	# Extract Location
	try:
		state_found = False
		city_found = False
		country_found = False
		world_found = False
		location = bio
		comma = location.split(',')
		
		# Search At Comma Level
		
		for elem in comma:
			elem = elem.strip().lower()
			if elem in state:
				dict_loc['state'] = elem
				state_found = True
				found_state = elem

				dict_loc['country'] = 'india'
				country_found = True
				found_country = 'india'
				break

		if state_found:
			# Try For City
			for elem in comma:
				elem = elem.strip().lower()
				if elem in city:
					dict_loc['city'] = elem
					city_found = True
					break
					

		else:
			# State Not Found After Comma Separation -- Search For City
			for elem in comma:
				elem = elem.strip().lower()
				if elem in city:
					dict_loc['city'] = elem
					city_found = True

					dict_loc['state'] = loc[elem]
					
					state_found = True
					found_state = loc[elem]

					dict_loc['country'] = 'india'
					country_found = True
					found_country = 'india'
					break
		# No City Or State Found
		if city_found == False and state_found == False:
			# Check Whether a World City Can be Matched
			for elem in comma:
				elem = elem.strip().lower()
				if elem in world:
					dict_loc['city'] = elem
					world_found = True
					dict_loc['country'] = world_loc[elem]
					
					country_found = True
					break
				
		if country_found == False:
			# Check Whether Country Information has been Provided
			for elem in comma:
				elem = elem.strip().lower()
				if elem in country:
					dict_loc['country'] = elem
					country_found = True
					break

		# Nothing Found So Far -- Let's Try For bracket

		if city_found == False and state_found == False and world_found == False and  country_found == False:
			# Separate by (
			for elems in comma:
				elems = elems.strip().lower()
				bracket = elems.split('(')
				for elem in bracket:
					elem = elem.strip('.')
					elem = elem.strip(')')
					elem = elem.strip().lower()

					if elem in state:
						dict_loc['state'] = elem
						state_found = True
						found_state = elem

						dict_loc['country'] = 'india'
						country_found = True
						found_country = 'india'
						break

				if state_found:
					# Try For City
					for elem in bracket:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip().lower()
						if elem in city:
							dict_loc['city'] = elem
							city_found = True
							break
					

				else:
					# State Not Found After Comma Separation -- Search For City
					for elem in bracket:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip().lower()
						if elem in city:
							dict_loc['city'] = elem
							city_found = True
							dict_loc['state'] = loc[elem]
							state_found = True
							found_state = loc[elem]

							dict_loc['country'] = 'india'
							country_found = True
							found_country = 'india'
							break
				# No City Or State Found
				if city_found == False and state_found == False:
					# Check Whether a World City Can be Matched
					for elem in bracket:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip().lower()
						if elem in world:
							dict_loc['city'] = elem
							#print(loc[elem],end = '\t',file = city_file)
							world_found = True

							dict_loc['country'] = world_loc[elem]
							country_found = True
							break
				
				if country_found == False:
					# Check Whether Country Information has been Provided
					for elem in bracket:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip().lower()
						if elem in country:
							dict_loc['country'] = elem
							country_found = True
							break


		# Nothing Found By Separating By Bracket -- Let's Separate by [

		if city_found == False and state_found == False and world_found == False and  country_found == False:
			for elems in comma:
				elems = elems.strip('.')
				elems = elems.strip(')')
				elems = elems.strip().lower()
				square = elems.split('[')
				for elem in square:
					elem = elem.strip('.')
					elem = elem.strip(')')
					elem = elem.strip(']')
					elem = elem.strip().lower()

					if elem in state:
						dict_loc['state'] = elem
						state_found = True
						found_state = elem

						dict_loc['country'] = 'india'
						country_found = True
						found_country = 'india'
						break

				if state_found:
					# Try For City
					for elem in square:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in city:
							dict_loc['city'] = elem
							city_found = True
							break
					

				else:
					# State Not Found After Comma Separation -- Search For City
					for elem in square:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in city:
							dict_loc['city'] = elem
							city_found = True

							dict_loc['state'] = loc[elem]
							state_found = True
							found_state = loc[elem]

							dict_loc['country'] = 'india'
							country_found = True
							found_country = 'india'
							break
				# No City Or State Found
				if city_found == False and state_found == False:
					# Check Whether a World City Can be Matched
					for elem in square:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in world:
							dict_loc['city'] = elem
							#print(loc[elem],end = '\t',file = city_file)
							world_found = True

							dict_loc['country'] = world_loc[elem]
							country_found = True
							break
				
				if country_found == False:
					# Check Whether Country Information has been Provided
					for elem in square:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in country:
							dict_loc['country'] = elem
							country_found = True
							break

		# Still Nothing Found -- Last Try -- Separating By Spaces
		if city_found == False and state_found == False and world_found == False and  country_found == False:
			for elems in comma:
				elems = elems.strip('.')
				elems = elems.strip(')')
				elems = elems.strip(']')
				elems = elems.strip().lower()
				space = elems.split(' ')
				for elem in space:
					elem = elem.strip('.')
					elem = elem.strip(')')
					elem = elem.strip(']')
					elem = elem.strip().lower()

					if elem in state:
						dict_loc['state'] = elem
						state_found = True
						found_state = elem

						dict_loc['country'] = 'india'
						country_found = True
						found_country = 'india'
						break

				if state_found:
					# Try For City
					for elem in space:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in city:
							dict_loc['city'] = elem
							city_found = True
							break
					

				else:
					# State Not Found After Comma Separation -- Search For City
					for elem in space:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in city:
							dict_loc['city'] = elem
							city_found = True

							dict_loc['state'] = loc[elem]
							state_found = True
							found_state = loc[elem]

							dict_loc['country'] = 'india'
							country_found = True
							found_country = 'india'
							break
				# No City Or State Found
				if city_found == False and state_found == False:
					# Check Whether a World City Can be Matched
					for elem in space:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in world:
							dict_loc['city'] = elem
							#print(loc[elem],end = '\t',file = city_file)
							world_found = True

							dict_loc['country'] = world_loc[elem]
							country_found = True
							break
				
				if country_found == False:
					# Check Whether Country Information has been Provided
					for elem in space:
						elem = elem.strip('.')
						elem = elem.strip(')')
						elem = elem.strip(']')
						elem = elem.strip().lower()
						if elem in country:
							dict_loc['country'] = elem
							country_found = True
							break

		if city_found == False and state_found == False and world_found == False and  country_found == False:
			for elem in comma:
				elem = elem.strip('.')
				elem = elem.strip(')')
				elem = elem.strip(']')
				elem = elem.strip().lower()
				for cities in city:
					n = len(cities)
					m = len(elem)
					if abs(n-m)<=1 and m>6:
						e = edit_distance(cities,elem)
						if e <=1:
							dict_loc['city'] = cities
							dict_loc['state'] = loc[cities]

							city_found = True
							state_found = True
							found_state = loc[cities]

							dict_loc['country'] = 'india'
							country_found = True
							found_country = 'india'
							break

				
				if city_found:
					break
			if city_found == False:
				for elem in comma:
					elem = elem.strip('.')
					elem = elem.strip(')')
					elem = elem.strip(']')
					elem = elem.strip().lower()
					for states in state:
						n = len(states)
						m = len(elem)
						if abs(n-m)<=1 and m>6:
							e = edit_distance(states,elem)
							if e<=1:
								dict_loc['state'] = states
								state_found = True
								#found_state = loc[elem]

								dict_loc['country'] = 'india'
								country_found = True
								found_country = 'india'
								break
					if state_found:
						break
			if state_found == False:
				for elem in comma:
					elem = elem.strip('.')
					elem = elem.strip(')')
					elem = elem.strip(']')
					elem = elem.strip().lower()
					for worlds in world:
						n = len(worlds)
						m = len(elem)
						if abs(n-m)<=1 and m>6:
							e = edit_distance(worlds,elem)
							if e<=1:
								dict_loc['city'] = worlds
								#print(loc[elem],end = '\t',file = city_file)
								world_found = True

								dict_loc['country]'] = world_loc[worlds]
								country_found = True
								break
					if world_found:
						break
			if country_found == False:
				for elem in comma:
					elem = elem.strip('.')
					elem = elem.strip(')')
					elem = elem.strip(']')
					elem = elem.strip().lower()
					for countries in country:
						n = len(countries)
						m = len(elem)
						if abs(n-m)<= 1 and m>6:
							e = edit_distance(countries,elem)
							if e<=1:
								dict_loc['country'] = countries
								country_found = True
								break
					if country_found:
						break

		if city_found == False and state_found == False and world_found == False and  country_found == False:                    
			pass
	except:
		pass

	return dict_loc

print(detect_location('i live in jaipur'))
	
