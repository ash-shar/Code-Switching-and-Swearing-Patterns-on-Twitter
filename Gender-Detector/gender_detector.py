from __future__ import print_function
import json
import sys
import codecs
import urllib.request
import binascii
#import requests

def gender_detector(name, geography = "in"):
	try:
		s2 = name.split(' ')
		s2[0] = s2[0].encode('utf-8')

		s3 = binascii.b2a_qp(s2[0])
		s2[0] = s3.decode('utf-8')
		#print(s2[0])

		if len(s2) > 1:
			req = "http://api.namsor.com/onomastics/api/json/gender/"+s2[0]+"/"+s2[1]+"/"+geography
		else:
			req = "http://api.namsor.com/onomastics/api/json/gender/"+s2[0]+"/sharma/"+geography

		ans = urllib.request.urlopen(req).read().decode("utf-8")

		# print(ans)
		d = json.loads(ans)
		gen = d['gender']
		scale = d['scale']		
		return gen
	except:
		pass

	return "Error"


print(gender_detector("Ashish"))
	 
