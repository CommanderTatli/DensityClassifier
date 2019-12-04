import datetime


class ClusterHolder:
    """
    :param clusters is a list of Clusters
    """
    def __init__(self, clusters):
        self.clusters = clusters
        self.calculateDistances()

    """
    Easy to use cluster processing function.
    If you want to execute this with multithreading, use Cluster.processCluster() for each cluster.
    """
    def processAllClusters(self):
        for i in self.clusters:
            i.processCluster()
        print("Clusters successfully processed!")

    """
    Function for calculating the distances between every points and saving the 
    relevant distances(those that are less than the max range) to Cluster.distances.
    If you want to multithread, call Cluster.calculateDistance to each pair of clusters.
    """
    def calculateDistances(self):
        start_time = datetime.datetime.now()
        for c1 in range(len(self.clusters)):
            for c2 in range(c1+1, len(self.clusters)):
                self.clusters[c1].calculateDistance(self.clusters[c2])
        print("Distances successfully calculated!")
        print(datetime.datetime.now()-start_time)

    """
    :returns the class of :param point
    """
    def classifyPoint(self, point):
        result = 0
        resultName = ""
        for cluster in self.clusters:
            incluster = cluster.testPoint(point)
            if result < incluster:
                result = incluster
                resultName = cluster.name
        return resultName