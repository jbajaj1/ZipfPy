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



def fileFinder(starterDir, jp):
	files = []

	if jp == 'j':
		for src, folders, fileNames in os.walk(starterDir):
			for fileName in fnmatch.filter(fileNames, '*.java'):
				files.append(os.path.join(src, fileName))
	elif jp == 'p':
		for src, folders, fileNames in os.walk(starterDir):
			for fileName in fnmatch.filter(fileNames, '*.py'):
				files.append(os.path.join(src, fileName))
	
	return files


def printSortedZipf(sortedZipf, totalCount):
	i = 0

	while i < len(sortedZipf):
		print str((float(sortedZipf[i][0])/totalCount)) + " : " + str(sortedZipf[i][1])
		i += 1

	print "\n\n"

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


def zipfCounterKWGrade(zipfDic, totalCount, javaKW, year, jp):

	files = fileFinder('./Bill_Code/' + year, jp)

	for file in files:
		f = open(file, 'r')
		f_string = f.read()
		f_words = re.findall(r'([A-Za-z_]+)', f_string)

		if jp == 'j':
			for word in f_words:
				if word in javaKW:
					totalCount += 1
					if word in zipfDic:
						zipfDic[word] = zipfDic[word] + 1
					else:
						zipfDic[word] = 1

		if jp == 'p':
			for word in f_words:
				if keyword.iskeyword(word):
					totalCount += 1
					if word in zipfDic:
						zipfDic[word] = zipfDic[word] + 1
					else:
						zipfDic[word] = 1

		f.close()

	return zipfDic, totalCount


javaKW = createKW()
year = ["Freshman", "Sophmore", "Junior", "Senior"]

for y in year:

	zipfDicJ = {}
	totalCountJ = 0

	zipfDicJ, totalCountJ = zipfCounterKWGrade(zipfDicJ, totalCountJ, javaKW, y, 'j')

	graphScatter(zipfDicJ, totalCountJ)

	zipfDicP = {}
	totalCountP = 0

	zipfDicP, totalCountP = zipfCounterKWGrade(zipfDicP, totalCountP, javaKW, y, 'p')

	graphScatter(zipfDicP, totalCountP)
