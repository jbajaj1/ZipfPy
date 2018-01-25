import re
import matplotlib.pyplot as plt
import math
import pickle
import os
import fnmatch

def fileFinder(starterDir):
	files = []
	for src, folders, fileNames in os.walk(starterDir):
		for fileName in fnmatch.filter(fileNames, '*.py'):
			files.append(os.path.join(src, fileName))
	return files


def openPickles():
	try:
	    zipfDic = pickle.load(open("allPython.p", "rb"))
	except (OSError, IOError) as e:
	    zipfDic = {}

	try:
		filesChecked = pickle.load(open("filesCheckedAP.p", "rb"))
	except (OSError, IOError) as e:
		filesChecked = {}

	try:
		totalCount = pickle.load(open("totalCountAP.p", "rb"))
	except (OSError, IOError) as e:
		totalCount = 0

	return zipfDic, filesChecked, totalCount


def savePickle():
	pickle.dump(zipfDic, open("allPython.p", "wb"))
	pickle.dump(filesChecked, open("filesCheckedAP.p", "wb"))
	pickle.dump(totalCount, open("totalCountAP.p", "wb"))


def createGraphParam(zipfDic, totalCount):
	sortedZipf = sorted( ((v,k) for k,v in zipfDic.iteritems()), reverse=True)

	i = 0
	zipfDis = []
	zipfPosition = []

	while i < len(sortedZipf):
		zipfDis.append(float(sortedZipf[i][0])/totalCount)
		i += 1
		zipfPosition.append(i)	

	return zipfPosition, zipfDis


def graphScatter(zipfDic, totalCount):
	zipfPosition, zipfDis = createGraphParam(zipfDic, float(totalCount))
	plt.scatter(zipfPosition, map(math.log, zipfDis))
	plt.show()


def zipfCounter(zipfDic, filesChecked, totalCount):

	files = fileFinder('./githubCode')

	for file in files:
		if file not in filesChecked:
			f = open(file, 'r')
			f_string = f.read()
			f_words = re.findall(r'([A-Za-z_]+)', f_string)

			for word in f_words:
				totalCount += 1
				if word in zipfDic:
					zipfDic[word] = zipfDic[word] + 1
				else:
					zipfDic[word] = 1

			filesChecked[file] = 1
			f.close()

	return zipfDic, filesChecked, totalCount




zipfDic, filesChecked, totalCount = openPickles()


zipfDic, filesChecked, totalCount = zipfCounter(zipfDic, filesChecked, totalCount)

graphScatter(zipfDic, totalCount)

savePickle()
