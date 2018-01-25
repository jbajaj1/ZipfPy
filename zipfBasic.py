import re
import matplotlib.pyplot as plt
import pylab
import math

TEST_TEXT = './test_text/shakespeare.txt'
TEST_TEXT2 = './test_text/johnstuartmill.txt'
TEST_TEXT3 = './test_text/prideandprejudice.txt'

r = open(TEST_TEXT, 'r')
r2 = open(TEST_TEXT2, 'r')
r3 = open(TEST_TEXT3, 'r')

r_string = r.read().lower() + r2.read().lower() + r3.read().lower()

zipfDisDic = {}

r_words = re.findall(r'([A-Za-z]+)', r_string)

totalCount = 0

for word in r_words:
	totalCount += 1
	if word in zipfDisDic:
		zipfDisDic[word] = zipfDisDic[word] + 1
	else:
		zipfDisDic[word] = 1

sortedZipf = sorted( ((v,k) for k,v in zipfDisDic.iteritems()), reverse=True)

'''
print(sortedZipf[:10])
print(sortedZipf[-100:])
'''
totalCount = float(totalCount)
i = 0
zipfDis = []
zipfPosition = []

while i < len(sortedZipf):
	zipfDis.append(float(sortedZipf[i][0])/totalCount)
	i += 1
	zipfPosition.append(i)


plt.scatter(zipfPosition, map(math.log, zipfDis))
plt.show()


#print totalCount
#print zipfDis[-10:]
