import re
import matplotlib.pyplot as plt
import math
import pickle
import keyword
import os
import fnmatch


def createKW():
	javaKW = {}

	r = open("javaKW.txt", 'r')

	for line in r:
		javaKW[line.strip('\n')] = 1

	return javaKW



def fileFinder(starterDir):
	files = []
	for src, folders, fileNames in os.walk(starterDir):
		for fileName in fnmatch.filter(fileNames, '*.java'):
			files.append(os.path.join(src, fileName))
	return files


def openPickles():
	try:
	    zipfDic = pickle.load(open("kwJava.p", "rb"))
	except (OSError, IOError) as e:
	    zipfDic = {}

	try:
		filesChecked = pickle.load(open("filesCheckedJKW.p", "rb"))
	except (OSError, IOError) as e:
		filesChecked = {}

	try:
		totalCount = pickle.load(open("totalCountJKW.p", "rb"))
	except (OSError, IOError) as e:
		totalCount = 0

	return zipfDic, filesChecked, totalCount


def savePickle():
	pickle.dump(zipfDic, open("kwJava.p", "wb"))
	pickle.dump(filesChecked, open("filesCheckedJKW.p", "wb"))
	pickle.dump(totalCount, open("totalCountJKW.p", "wb"))

def printSortedZipf(sortedZipf, totalCount):
	i = 0

	while i < len(sortedZipf):
		print str((float(sortedZipf[i][0])/totalCount)) + " : " + str(sortedZipf[i][1])
		i += 1

def createGraphParam(zipfDic, totalCount):
	sortedZipf = sorted( ((v,k) for k,v in zipfDic.iteritems()), reverse=True)

	i = 0
	zipfDis = []
	zipfPosition = []

	printSortedZipf(sortedZipf, totalCount)

	while i < len(sortedZipf):
		zipfDis.append(float(sortedZipf[i][0])/totalCount)
		i += 1
		zipfPosition.append(i)	

	return zipfPosition, zipfDis


def graphScatter(zipfDic, totalCount):
	zipfPosition, zipfDis = createGraphParam(zipfDic, float(totalCount))
	plt.scatter(zipfPosition, zipfDis)
	plt.show()


def zipfCounterJavaKW(zipfDic, filesChecked, totalCount, javaKW):

	files = fileFinder('./githubJavaCode')

	for file in files:
		if file not in filesChecked:
			f = open(file, 'r')
			f_string = f.read()
			f_words = re.findall(r'([A-Za-z_]+)', f_string)

			for word in f_words:
				if word in javaKW:
					totalCount += 1
					if word in zipfDic:
						zipfDic[word] = zipfDic[word] + 1
					else:
						zipfDic[word] = 1

			filesChecked[file] = 1
			f.close()

	return zipfDic, filesChecked, totalCount



zipfDic, filesChecked, totalCount = openPickles()

javaKW = createKW()

zipfDic, filesChecked, totalCount = zipfCounterJavaKW(zipfDic, filesChecked, totalCount, javaKW)

graphScatter(zipfDic, totalCount)

savePickle()
