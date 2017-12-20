from __future__ import print_function
from distance import *
from language_without_processes import *

basepath = ""
# datapath = "/home/bt1/13CS10060/sc_jeenu/socialComputing"


wordlengththreshold = 2
betaforPhonetic = 1
englishmaskthres = 0
commonmaskthres = 0


hindiabuselist = []
englishabuselist = []
englishstocklist = []
hindistocklist = []
# abusefile = codecs.open(basepath+"output/abusiveresult.txt","a","utf-8")
# countfile = codecs.open(basepath+"output/counts.txt","a","utf-8")

def binarySearch(alist, item):
	first = 0
	last = len(alist)-1
	found = False

	while first<=last and not found:
		midpoint = (first + last)//2
		if alist[midpoint] == item:
			found = True
		else:
			if item < alist[midpoint]:
				last = midpoint-1
			else:
				first = midpoint+1
	return found

def getFiles(folder,List,path):
	ppath = path+"/"+folder
	if os.path.isdir(ppath):
		for files in os.listdir(ppath):
			getFiles(files,List,ppath)
	else:
		List.append(ppath)

def readFileIntoList(filename):
	retlist =[]
	filelist = codecs.open(filename,"r","utf-8")
	for lines in filelist:
		retlist.append(lines.strip("\n").split("\t")[0])
	#print(retlist)
	retlist.sort()
	return retlist

hindiabuselist = readFileIntoList(basepath+"corpus/hindiswears.txt")
#print(hindiabuselist)
englishabuselist =  readFileIntoList(basepath+"corpus/englishswears.txt")
#print(englishabuselist)
englishstocklist = readFileIntoList(basepath+"corpus/englishstock.txt")
hindistocklist = readFileIntoList(basepath+"corpus/hindistock.txt")
engstopwordlist = readFileIntoList(basepath+"corpus/englishstopwords.txt")


#habuseFile = basepath + "\hindiabuses.txt"
#hindiAbuseFile = codecs.open(habusefile)
#hindiabuselist = hindiabuselist		

def classifyAsHindi(word):
	result = []
	if(binarySearch(hindistocklist,word)):
		# print("\t",word,":Word Found in hindistocklist",file=logfile)
		return result

	wordlen = len(word)
	if(wordlen <= 0):
		# print("\t",word,":Word Len 0",file=logfile)
		return result

	for abuse in hindiabuselist:
		abuse = abuse.lower()

		#Comparing for a direct match
		if(word == abuse):
			r = (abuse,"DM")
			result.append(r)
			# print("\t",word,": Directly Matched in Hindi",file=logfile)
			return result

	   	## masked words
		count =0

		for i in range(0,wordlen):
			if(word[i]=='!' or word[i]=='@' or word[i]=='#' or word[i]=='$' or word[i]=='%' or word[i]=='^' or word[i]=='&' or word[i]=='*') :
				count = count +1

		#if non zero masking chars, then find masked edit dist
		if((wordlen-count) > 0 and count != 0):
			val = edit_distance(abuse,word)
			if(val == 0):
				r = (abuse,"MEC"+str(count)+"V0")
				result.append(r)
				# print("\t",word,abuse,": Matched with masking",file=logfile)
				continue
				#return result
			else:
				pass
				# print("\t",word,val,": Not Matched with masking",file=logfile)

		##Non Repeated Considerations

		if(count == 0):# if zero masks   ### Why only for zero masks

			temp_word = ''.join(c for c,_ in itertools.groupby(word))
			temp_abuse = ''.join(c for c,_ in itertools.groupby(abuse))
			#compare words without repeated chars
			if(len(word) > len(temp_word) and temp_abuse==temp_word):
				r = (abuse,"RR")
				result.append(r)
				# print("\t",word,abuse,": Mathced with removal of repititions",file=logfile)
				continue
		
		##Phonetic match
		value = reformed_edit_dist(word,abuse)
				   
		if(value <= betaforPhonetic and len(word) > wordlengththreshold):
			r = (abuse,"PM"+str(value))
			result.append(r)
			# print("\t",word,abuse,value,": Mathced with phonetics",file=logfile)
			continue
		else:
			pass
			# print("\t",word,abuse,value,": Not Mathced with phonetics",file=logfile)
	return result		
						 
def classifyAsEnglish(word):
	result = []
	#if(word in englishstocklist):
	#	print("\t",word,":Word Found in englishstocklist",file=logfile)
	#	return result

	wordlen = len(word)
	if(wordlen <= 0):
		# print("\t",word,":Word Len 0",file=logfile)
		return result

	for abuse in englishabuselist:
		abuse = abuse.lower()
		found_a = 0

		#Comparing for a direct match
		if(word == abuse):
			r = (abuse,"DM")
			result.append(r)
			# print("\t",word,": Directly Matched in English",file=logfile)
			return result
		
	   	## masked words
		count =0

		for i in range(0,wordlen):
			if(word[i]=='!' or word[i]=='@' or word[i]=='#' or word[i]=='$' or word[i]=='%' or word[i]=='^' or word[i]=='&' or word[i]=='*') :
				count = count +1

		#if non zero masking chars, then find masked edit dist
		if((wordlen-count) > 0 and count != 0):
			val = edit_distance(abuse,word)
			if(val <= englishmaskthres):
				r = (abuse,"MEC"+str(count)+"V"+str(val))
				result.append(r)
				# print("\t",word,abuse,": Matched with masking",file=logfile)
				continue
				#return result
			else:
				pass
				# print("\t",word,val,": Not Matched with masking",file=logfile)


		##Non Repeated Considerations

		if(count == 0):# if zero masks   ### Why only for zero masks
			temp_word = ''.join(c for c,_ in itertools.groupby(word))
			temp_abuse = ''.join(c for c,_ in itertools.groupby(abuse))
			#compare words without repeated chars
			if(len(word) > len(temp_word) and temp_abuse==temp_word):
				r = (abuse, "RR")
				result.append(r)
				# print("\t",word,abuse,": Mathced with removal of repititions",file=logfile)
				continue
	return result		


def classifyAsCommon(word):
	result = []
	if(binarySearch(englishstocklist,word)):
		#print("\t",word,":Word Found in englishstocklist",file=logfile)
		result = classifyAsEnglish(word)
		return result
		
	   # print(len(hindistocklist))
	if(word in hindistocklist):
		# print("\t",word,":Word Found in hindistocklist",file=logfile)
		return result

	wordlen = len(word)
	if(wordlen <= 0):
		# print("\t",word,":Word Len 0",file=logfile)
		return result
	commonlist = englishabuselist+hindiabuselist
	for abuse in commonlist:
		abuse = abuse.lower()
		found_a = 0

		#Comparing for a direct match
		if(word == abuse):
			r = (abuse,"DM")
			result.append(r)
			# print("\t",word,": Directly Matched in commonlist",file=logfile)
			return result

	   	## masked words
		count =0

		for i in range(0,wordlen):
			if(word[i]=='!' or word[i]=='@' or word[i]=='#' or word[i]=='$' or word[i]=='%' or word[i]=='^' or word[i]=='&' or word[i]=='*') :
				count = count +1

		#if non zero masking chars, then find masked edit dist
		if((wordlen-count) > 0 and count != 0):
			val = edit_distance(abuse,word)
			if(val <= commonmaskthres):
				r = (abuse,"MEC"+str(count)+"V"+str(val))
				result.append(r)
				# print("\t",word,abuse,": Matched with masking",file=logfile)
				continue
			else:
				pass
				# print("\t",word,val,": Not Matched with masking",file=logfile)

		##Non Repeated Considerations

		if(count == 0):# if zero masks   ### Why only for zero masks

			temp_word = ''.join(c for c,_ in itertools.groupby(word))
			temp_abuse = ''.join(c for c,_ in itertools.groupby(abuse))
			#compare words without repeated chars
			if(len(word) > len(temp_word) and temp_abuse==temp_word):
				r = (abuse,"RR")
				result.append(r)
				# print("\t",word,abuse,": Mathced with removal of repititions",file=logfile)
				continue
	return result		

def classifyTweet(tweet,tweetid):
	cnt = 0
	abusedetect = []
	tweet = tweet.strip(' \t\n\r,.!-_?;"')
	tweets = tweet.lower()
	print("Processing tweet : ",tweetid)
	# print("\nProcessing Tweet : ",tweet,tweetid,file=logfile)
	#print(len(hindiabuselist))
	for abuse in hindiabuselist:
		if(len(abuse.split(" ")) < 2):
			continue
		abuse = " "+abuse+" "
		if(abuse in tweets):
			r = [(abuse,"DM")]
			rr = (abuse,"HI",r)
			abusedetect.append(rr)
			# print("\t",abuse,": Directly Matched in Hindi",file=logfile)


	for abuse in englishabuselist:
		if(len(abuse.split(" ")) < 2):
			continue
		abuse = " "+abuse+" "
		if(abuse in tweets):
			r = [(abuse,"DM")]
			rr = (abuse,"EN",r)
			abusedetect.append(rr)
			# print("\t",abuse,": Directly Matched in English",file=logfile)

	tweetwords = tweet.split(' ')
	## Labels : EN, OTHER, NE, HI
	for word in tweetwords:
		lang = getLanguage(tweetid,word)
		word = word.strip("!.%")
		word = word.lower()
		if(word in engstopwordlist):
			continue
		if(len(word)> 0 and word[0] in "#@"):
			continue
		if(lang[0] == "EN"):
			##TODO :Remove this line
			print(word)
			result = classifyAsEnglish(word)
			if(len(result) > 0):
				abusedetect.append((word,"EN",result))
		elif(lang[0] == "HI"):
			print("HI: ",word)
			result = classifyAsHindi(word)
			if(len(result) > 0):
				abusedetect.append((word,"HI",result))
		elif(lang[0] == 0):
			result = classifyAsCommon(word)
			if(len(result) > 0):
				abusedetect.append((word,"CM",result))
	return abusedetect

def processTweetFile(filepath):
	filec = codecs.open(filepath,"r","utf-8")
	filename = os.path.basename(filepath)
	direc = os.path.dirname(filepath).split("/")[-1]
	logfile = codecs.open(basepath+"logs/"+direc+"/"+filename,"w","utf-8")
	resultfile = codecs.open(basepath+"rejresults/"+direc+"/"+filename,"w","utf-8")
	count = 0
	for lines in filec:
		line = lines.strip("\n")
		data = line.split('\t')
		tweetid = data[0]
		text = data[2]
		abusedetect = classifyTweet(text,tweetid,logfile)
		cnt = len(abusedetect)
		if(cnt == 0):
			print(line,file=resultfile)
		else:
			print(line,direc+"/"+filename,cnt,abusedetect,sep="\t",file=abusefile)
			count = count + 1
	print("Completed:"+direc+"/"+filename)
	print(direc+"/"+filename+": "+str(count),file=countfile)

def doForAllFiles():
	fn = processTweetFile
	filelist = []
	getFiles("",filelist,datapath)
	
	for files in filelist:
		'''print("File : ",files,"Continue(y/n)")
		ans = raw_input()
		if(ans == "n"):
			continue'''
		processTweetFile(files)

# def main():
# 		#readFiles()
# 		init()
# 		doForAllFiles()



# if __name__ == "__main__":main()

output = classifyTweet("Saala Uss Waqt se 10.2 K MC chutiya Bna Ra","654680949523791872")
print(output)