import os.path
import itertools
import codecs
from collections import defaultdict


variations = {}
variations['a'] = set(['a','','ae','i','e','o','u','ea','!','@','#','$','%','^','&','*'])
variations['b']=  set(['b','6','bh' ,'13','!','@','#','$','%','^','&','*'])
variations['c']=set(['c','','s','!','@','#','$','%','^','&','*'])
variations['d'] = set(['d','dh','dh','da','da','di','de','th','!','@','#','$','%','^','&','*'])
variations['e'] = set(['e','ae','a','i','o','u','','ea','!','@','#','$','%','^','&','*'])
variations['f'] = set(['f','ph','!','@','#','$','%','^','&','*'])
variations['g'] =set(['g','j','ga','','ji','je' ,'!','@','#','$','%','^','&','*'])
variations['h'] = set(['h','ha','hai','he','han','hi','','!','@','#','$','%','^','&','*'])
variations['i'] = set(['i','ii','e','ae','a','o','u','','ea','!','@','#','$','%','^','&','*'])
variations['j'] = set(['j','ja','g','z','!','@','#','$','%','^','&','*'])
variations['k']= set(['k','ka','ke','ki','ko','ku','ch','!','@','#','$','%','^','&','*'])
variations['l']= set(['l','la','1','!','@','#','$','%','^','&','*'])
variations['m'] =set(['m','ma','mai','me','am','','!','@','#','$','%','^','&','*','!','@','#','$','%','^','&','*'])
variations['n'] = set(['n','na','ne','!','@','#','$','%','^','&','*'])
variations['o'] = set(['o','oh','u','a','i','e','','oe','oi','oa','oy','!','@','#','$','%','^','&','*'])
variations['p'] = set(['p','pi','pe','pea','pae','!','@','#','$','%','^','&','*'])
variations['q'] = set(['q','qu','k','kyu','!','@','#','$','%','^','&','*'])
variations['r'] = set(['r','re','ri','ra','ro','ru','d','rh','ar','rae','rea','!','@','#','$','%','^','&','*'])
variations['s']= set(['s','c','sh','se','si','sa','so','su','','5','!','@','#','$','%','^','&','*'])
variations['t'] = set(['t','th','the','ta','ti','te','tha','!','@','#','$','%','^','&','*'])
variations['u'] = set(['u','o','v','e','a','i','yu','you','yo','','!','@','#','$','%','^','&','*'])
variations['v']=set(['v','u','we','vi','vhi','bhi','b','bi','be','vh','w','va','vaa','','!','@','#','$','%','^','&','*'])
variations['w'] =set(['w','v','vh','','va','!','@','#','$','%','^','&','*'])
variations['x']=set(['x','aks','ex','ax','oks','','!','@','#','$','%','^','&','*'])
variations['y'] =set(['y','vai','ya','ye','yi','yh','yeh','yo','yu','','j','jhe','je','!','@','#','$','%','^','&','*'])
variations['z'] = set(['z','j','je','ji','az','s','y','!','@','#','$','%','^','&','*'])
variations[' ']=set([' ',''])
variations['0']=set(['0','o'])
variations['1']=set(['1','i','l'])
variations['2']=set(['2'])
variations['3']=set(['3'])
variations['4']=set(['4'])
variations['5']=set(['5','s'])
variations['6']=set(['6'])
variations['7']=set(['7'])
variations['8']=set(['8'])
variations['9']=set(['9'])

variation = defaultdict(lambda:"")
variation['a'] = "a!@#$%^&*"
variation['b']= "b!@#$%^&*36"
variation['c'] ="c!@#$%^&*"
variation['d'] ="d!!@#$%^&*"
variation['e']= "e!@#$%^&*"
variation['f']= "f!@#$%^&*"
variation['g']= "g!@#$%^&*9"
variation['h']= "h!@#$%^&*"
variation['i']= "i!@#$%^&*"
variation['j']= "j!@#$%^&*"
variation['k']= "k!@#$%^&*"
variation['l']= "l!@#$%^&*"
variation['m']= "m!@#$%^&*"
variation['n']= "n!@#$%^&*"
variation['o']= "o!@#$%^&*0"
variation['p']= "p!@#$%^&*"
variation['q']= "q!@#$%^&*"
variation['r']= "r!@#$%^&*"
variation['s']= "s!@#$%^&*5"
variation['t']= "t!@#$%^&*+"
variation['u']= "u!@#$%^&*"
variation['v']= "v!@#$%^&*"
variation['w']= "w!@#$%^&*"
variation['x']= "x!@#$%^&*"
variation['y']= "y!@#$%^&*"
variation['z']= "z!@#$%^&*"
variation['0']="0o"
variation['1']="1li"
variation['2']="2"
variation['3']="3"
variation['4']="4"
variation['5']="5s"
variation['6']="6"
variation['7']="7"
variation['8']="8"
variation['9']="9g"

vowel = set(['a','e','i','o','u'])

def check2(s1,s2):
	if ((s1 >= 'a' and s1<='z') or (s1>='0' and s1<='9') or s1 == ' '):
	    if (variations[s1].issuperset(set(s2))):
	        return True
	else:
	    return (s1==s2)    

def check(s1,s2):
	'''
		Return if s1 and s2 are same except for masked charaters
	'''
	if (variation[s1].find(s2) >= 0 ):
		return True
	return False


def edit_distance(s1, s2):
	'''
		Calculate normal edit distance between the words s1 and s2 excdpt for masked characters
	'''
	m=len(s1)+1
	n=len(s2)+1

	tbl = {}
	for i in range(m): tbl[i,0]=i
	for j in range(n): tbl[0,j]=j
	for i in range(1, m):
		for j in range(1, n):
			if(check(s1[i-1],s2[j-1])):
				cost = 0
			else :
				cost =1
			tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

	return tbl[i,j]

def reformed_edit_dist(s1,s2):
	'''
		Calculate edit distance between s1 and s2 using phoetic similarity in Hindi 
	'''
	m=len(s1)+1
	n=len(s2)+1
	nomatchcost = n
	if(m>n):
		nomatchcost = m
	tbl = {}
	for i in range(m): tbl[i,0]=i*nomatchcost
	for j in range(n): tbl[0,j]=j*nomatchcost
	for i in range(1, m):
	    for j in range(1, n):
	        if(s1[i-1] == s2[j-1]):
	            cost = 0
	        elif(check2(s1[i-1],s2[j-1])):
	            cost = 1
	        else :
	            cost = nomatchcost
	        tbl[i,j] = min(tbl[i, j-1]+nomatchcost, tbl[i-1, j]+nomatchcost, tbl[i-1, j-1]+cost)
	        if(i>=1 and j>=2):
	            if(check2(s1[i-1],s2[j-2:j])):
	                cost = 1
	            else :
	                cost = 2*nomatchcost
	            tbl[i,j] = min(tbl[i, j-2]+2*nomatchcost, tbl[i-1, j]+nomatchcost,tbl[i-1,j-2]+cost,tbl[i,j])
	        
	        if(i>=2 and j>=1):
	            if (check2(s2[j-1],s1[i-2:i])):
	                cost = 1
	            else :
	                cost = 2*nomatchcost
	            tbl[i,j] = min(tbl[i, j-1]+nomatchcost, tbl[i-2, j]+2*nomatchcost,tbl[i-2,j-1]+cost,tbl[i,j])
	        if(vowel.issuperset(set(s1[i-1]))):
	            tbl[i,j] = min (tbl[i-1,j]+1,tbl[i,j])
	        if(vowel.issuperset(set(s2[j-1]))):
	            tbl[i,j] = min(tbl[i,j-1]+1,tbl[i,j])
	return tbl[i,j]


