from sortedcontainers import SortedList
import datetime


class Cluster:
    def __init__(self, name, elements):
        self.name = name
        self.elements = elements
        self.maxRho = len(elements)
        self.r = -1
        self.rho = -1
        """
        List with the nth element representing the minimum r*r required
        for cluster's points to stick together if density is n
        """
        self.rRho = []
        """
        List with the nth element containing a dictionary of
        the nth points's closest neighbour from each cluster
        """
        self.closestPointFromCluster = []
        for i in range(len(self.elements)):
            self.closestPointFromCluster.append({})
        self.distancesInsideCluster = []
        self.importantPoints = []
        self.finalImportantPoints = []

        self.generateDistancesInCluster()


    """
    Calculates distances from every pair of points in cluster.
    """
    def generateDistancesInCluster(self):
        for i in range(len(self.elements)):
            self.distancesInsideCluster.append([])
        for fr in range(len(self.elements)):
            for to in range(fr, len(self.elements)):
                if fr == to:
                    continue
                distance = self.elements[fr].getSquareDistance(self.elements[to])
                self.distancesInsideCluster[fr].append((distance, to))
                self.distancesInsideCluster[to].append((distance, fr))
            self.distancesInsideCluster[fr].sort(key=lambda x: x[0])

    """
    :returns quality of :param rho and saves important points to self.importantPoints
    """
    def getResult(self, rho):
        #print("Getting result for rho: "+str(rho))
        # building cluster
        self.importantPoints.clear()
        r = -1
        nextR = SortedList(key=lambda x: x[0])
        for i in range(len(self.distancesInsideCluster)):
            #          r                                      name of point with r to given rho
            nextR.add((self.distancesInsideCluster[i][rho][0], i, 0))

        found = [False] * len(self.elements)
        while False in found:
            # get the smallest r that accesses more points
            point = nextR[0]
            # delete it from the list
            del nextR[0]
            # but write back a bigger distance if possible
            if rho+point[2]+1 < self.maxRho-1:
                nextR.add((self.distancesInsideCluster[point[1]][rho+point[2]+1][0], point[1], (point[2]+1)))

            r = point[0]
            if point[2] > 0:
                pointFound = self.distancesInsideCluster[point[1]][rho+point[2]][1]
                found[pointFound] = True
            else:
                self.importantPoints.append(point[1])
                found[point[1]] = True
                for k in range(0, rho):
                    pointFound = self.distancesInsideCluster[point[1]][k][1]
                    found[pointFound] = True

        # testing clusters's connections
        connected = set()
        for important in self.importantPoints:
            for cluster in self.closestPointFromCluster[important].keys():
                if self.closestPointFromCluster[important][cluster] <= r:
                    connected.add(cluster)

        return (1.0 / (1 + len(connected)), r)

    """
    Calculating the best rho and r for the cluster.
    self.calculateDistance must be called for each other cluster before calling this function.
    """
    def processCluster(self):
        start_time = datetime.datetime.now()

        best = -1
        for rho in range(1, self.maxRho-1):
            res = self.getResult(rho)
            if res[0] > best:
                best = res[0]
                self.r = res[1]
                self.rho = rho
                self.finalImportantPoints = self.importantPoints[:]

        print("Cluster named "+str(self.name)+" processed with result r: "+str(self.r)+" and rho: "+str(self.rho+1)+" out of maxRho: "+str(self.maxRho-1))
        print(datetime.datetime.now() - start_time)

    """
    Saves distance of cluster :param otherCluster from every point of this cluster.
    Call this function for every pair of clusters to multithread.
    """
    def calculateDistance(self, otherCluster):
        for p1 in range(len(self.elements)):
            for p2 in range(len(otherCluster.elements)):
                distance = self.elements[p1].getSquareDistance(otherCluster.elements[p2])
                current = self.closestPointFromCluster[p1].get(otherCluster.name)
                if current is None or current > distance:
                    self.closestPointFromCluster[p1][otherCluster.name] = distance
                current = otherCluster.closestPointFromCluster[p2].get(self.name)
                if current is None or current > distance:
                    otherCluster.closestPointFromCluster[p2][otherCluster.name] = distance

    """
    Testing if point is in the cluster.
    :returns number of important points that "see" the point divided by rho to help smaller clusters against bigger ones.
    """
    def testPoint(self, point):
        connections = 0
        for p in self.finalImportantPoints:
            distance = point.getSquareDistance(self.elements[p])
            if distance < self.r:
                connections += 1
        return float(connections)/len(self.finalImportantPoints)