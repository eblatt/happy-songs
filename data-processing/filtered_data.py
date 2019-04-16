from skimage import io
import numpy as np
import random
import numpy.matlib
import math
import csv
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
#import kmeans template

def sk_learn_cluster(X, Y, K):
# """
# TODO: Implement Sci-Kit Learn's kmeans functionality
#
# :param X: 2D np array containing features of the words
# :param Y: 1D np array containing labels
# :param K: number of clusters
# """
	km = KMeans(n_clusters = K)
	km = km.fit(X)
	labels = km.predict(X)
	return labels, km.cluster_centers_


def plot_word_clusters(data, centroids, centroid_indices):
	"""
	DO NOT CHANGE ANYTHING IN THIS FUNCTION

	You can use this function to plot the words and centroids to visualize your code.
	Points with the same color are considered to be in the same cluster.

	:param data - the data set stores as a 2D np array (given in the main function stencil)
	:param centroids - the coordinates that represent the center of the clusters
	:param centroid_indices - the index of the centroid that corresponding data point it closest to

	NOTE: function only works for K <= 5 clusters
	"""
	Y = data[:,0]
	x = data[:,1].astype(np.float)
	y = data[:,2].astype(np.float)
	fig, ax = plt.subplots()
	for c in centroids:
		x = np.append(x,c[0])
		y = np.append(y,c[1])
	try:
		colors = {0: 'red', 1: 'yellow', 2: 'blue', 3: 'green', 4: 'brown'}
		color = [colors[l] for l in centroid_indices]

		for i in range(len(centroids)):
			color.append('black')
	except KeyError:
		print ("Keep to less than 5 clusters")
		return
	for i, txt in enumerate(Y):
		ax.annotate(txt, (x[i], y[i]))
	plt.scatter(x,y,c = color)
	plt.xlabel('Low Loudness --> High Loudness')
	plt.ylabel('Low Happiness --> High Happiness')
	plt.show()


def main():
	"""
	This function loads the data set as a 2D numpy array in the data variable
	"""

# The following codes loads the data set into a 2D np array called data
	with open('complete_data.csv') as features_file:
		csv_reader = csv.DictReader(features_file, delimiter = ',')
		data = []
		counter = 0
		for row in csv_reader:
			print("csv_reader row:", row)
			# if(counter == 20):
			# 	break
			counter+=1
			cleaned_row = []
			cleaned_row.append(row['track'])
			cleaned_row.append(row['loudness'])
			cleaned_row.append(row['score'])
			data.append(np.array(cleaned_row))
		data = random.sample(list(data), 30)
		data = np.array(data)


	X = []
	Y = []
	counter = 0
	for row in data:
		# if(counter == 10):
		# 	break
		# counter+=1
		Y.append(row[0])
		l = [float(i) for i in row[1:]]
		X.append(l)
	X = np.array(X)
	Y = np.array(Y)

	centroid_indices2,centroids2 = sk_learn_cluster(X,Y,3)

	plot_word_clusters(data, centroids2, centroid_indices2 )

if __name__ == '__main__':
	main()
