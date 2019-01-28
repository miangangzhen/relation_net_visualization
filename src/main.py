import seaborn as sns
import matplotlib.pyplot as plt
import json
import random
import numpy as np
import pandas as pd


def prepareGraph(relationDict, threshold=-99):
	"""
	Build a json file to render html.
	:param relationDict:
	:param threshold:
	:return:
	"""
	nodesDict = {}
	toJson = {}

	nodesSet = set()
	weightDict = {}
	for key, value in relationDict.items():
		nodes = key.split("-")
		nodesSet.update(nodes)
		for node in nodes:
			weightDict[node] = weightDict.get(node, 0) + value

	nodesSet = set([x for x in nodesSet if float(weightDict.get(x, -1)) > threshold])
	for id_, node in enumerate(nodesSet):
		nodesDict[node] = id_
	
	toJson["nodes"] = [
	{"name": node + ": {}".format(weightDict.get(node, "-1")), "image": "point{}.png".format(random.randint(0, 1))}
		for node in nodesDict.keys()
	]

	edgesDict = {}
	edgesList = []
	for key in relationDict.keys():
		nodes = key.split("-")
		for i in range(len(nodes) - 1):
			sourceId = nodesDict.get(nodes[i], None)
			targetId = nodesDict.get(nodes[i+1], None)
			if sourceId and targetId:
				if not (edgesDict.get(sourceId, None)):
					edgesDict[sourceId] = []
				edgesDict[sourceId].append(targetId)

	for key, values in edgesDict.items():
		for value in values:
			edgesList.append({"source":key, "target":value})

	if not edgesList:
		raise Exception("Warning：no edge exist，maybe threshold is too high，please try decrease it.")

	toJson["edges"] = edgesList
	jsonString = json.dumps(toJson)
	with open("relation.json", "w", encoding="utf-8") as f:
		f.write(jsonString)


def getRelationDict(percentile_min=0, percentile_max=100):
	"""
	Assume that you can generate or read data and transform them to relation dict.
	For example
	:param percentile_min: threshold of minimum percentile
	:param percentile_max: threshold of maximum percentile
	:return: a relation map
	"""

	relationDict = {}
	for i in range(100):
		source = chr(random.randint(65, 90))
		target = chr(random.randint(65, 90))
		relationDict[source + "-" + target] = random.randint(0, 99)

	# 过滤掉低于95%分位数的
	threshold_min = np.percentile([x for x in relationDict.values()], percentile_min)
	threshold_max = np.percentile([x for x in relationDict.values()], percentile_max)

	draw([x for x in relationDict.values()], "theme_")

	return {key: value for key, value in relationDict.items() if threshold_min <= value <= threshold_max}


def draw(datas, prefix):

	sns.distplot(datas)
	plt.savefig(prefix + "distplot.jpg")
	plt.clf()

	sns.boxplot(datas)
	plt.savefig(prefix + "boxplot.jpg")
	plt.clf()

	sns.violinplot(datas)
	plt.savefig(prefix + "violinpot.jpg")
	plt.clf()

	sns.stripplot(datas)
	plt.savefig(prefix + "stripplot.jpg")
	plt.clf()

if __name__ == "__main__":

	relationDict = getRelationDict(percentile_min=85, percentile_max=100)
	prepareGraph(relationDict, threshold=-99)

	