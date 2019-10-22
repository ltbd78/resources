import random as rd
import numpy as np
from scipy import linalg as la
import matplotlib.pyplot as p


class MyKmeans:
    data = list()
    centroids = list()

    def __init__(self):
        return

    def readData(self, filename):
        # self.data = pd.read_csv(file, dtype=int, header=None, delimiter=',').transpose()
        file = open(filename, "r")
        for line in file:
            x = [float(i) for i in line.split(",")]
            self.data.append(x)
        file.close()

    def subsetData(self, numbers):
        subset = list()
        for number in numbers:
            for element in self.data:
                if number == element[1]:
                    subset.append(element)
        return subset

    def cluster(self, iterCount, k, centroids=None):
        # list of given centroids priority over given # of centroids k
        if centroids is None:
            data_copy = self.data[:]
            rd.shuffle(data_copy)  # shuffle() is chosen over choice() for selection w/o replacement
            for i in range(0, k):
                self.centroids.append(data_copy[i][2:])
        else:
            for i in range(0, len(centroids)):
                self.centroids.append(self.data[centroids[i]][2:])
            if k != len(centroids):
                print "k and length of centroids list are not equal! " \
                      "Using given centroids list and ignoring k."

        for it in range(0, iterCount):
            dist = list()  # list of distances [[x0-{ci}], [x1-{ci}], ... [xj - {ci}]]
            for i in range(0, len(self.data)):
                dist_i = list()
                for j in range(0, len(self.centroids)):
                    d_i = np.array(self.data[i][2:])
                    d_j = np.array(self.centroids[j])
                    dist_i.append(la.norm(d_i - d_j))
                dist.append(dist_i)
            # print "dist"
            # print dist[0:10]

            small = list()  # list of i s.t. distances [[x0-{ci}], [x1-{ci}] ...] is smallest
            for i in range(0, len(dist)):
                smallest = dist[i][0]
                smallest_index = 0
                for j in range(1, len(dist[i])):
                    if dist[i][j] < smallest:
                        smallest = dist[i][j]
                        smallest_index = j
                small.append(smallest_index)
            # print "small"
            # print small

            cluster_dict = dict()  # which x belongs to which ci {c0: ..., c1: ..., ..., ci: ...}
            for i in range(0, len(dist[0])):
                cluster_dict.update({i: []})
            x = 0
            for i in small:
                cluster_dict[i].append(x)
                x += 1

            # print self.centroids  # old centroids

            nc = list()  # new centroids
            for i in range(0, len(cluster_dict)):
                sum_x = 0
                sum_y = 0
                for j in cluster_dict[i]:
                    sum_x += self.data[j][2]
                    sum_y += self.data[j][3]
                nc.append([sum_x / len(cluster_dict[i]), sum_y / len(cluster_dict[i])])
            self.centroids = nc

            # debugging with 3 centroids
            # y = list()
            # for i in range(0, 100):
            #     y.append(i)
            # print y
            # print "c0", cluster_dict[0]
            # print "c1", cluster_dict[1]
            # print "c2", cluster_dict[2]

        return cluster_dict.values()

    def calculateSC(self, clusters):
        A = list()
        for c in clusters:
            A_i = list()
            for i in c:
                d_i = np.array(self.data[i][2:])
                a = 0
                for j in range(len(c)):
                    d_j = np.array(self.data[c[j]][2:])
                    a += la.norm(d_i - d_j)
                a = a / len(c)
                A_i.append(a)
            A.append(A_i)
        print A

        B = list()
        for c in range(len(clusters)):
            B_i = list()
            for i in clusters[c]:
                d_i = np.array(self.data[i][2:])
                # print "i", i, d_i
                b_small = list()
                temp = clusters[:c] + clusters[c + 1:]
                for i2 in temp:
                    b = 0
                    for j in i2:
                        d_j = np.array(self.data[j][2:])
                        # print "j", j, d_j
                        b += la.norm(d_i - d_j)
                    b = b / len(i2)
                    b_small.append(b)
                B_i.append(min(b_small))
            B.append(B_i)
        print B

        from itertools import chain
        A = list(chain.from_iterable(A))
        B = list(chain.from_iterable(B))

        SC = 0
        for i, j in zip(A, B):
            SC += (j - i) / max(i, j)
        SC = SC / len(self.data)
        print SC

    def visuals(self, clusters=None):
        colors = ["r", "g", "b", "y", "m", "c", "k", "#abcabc", "#7a7a7a", "#aabbcc",
                  "#ff4040", "#ffbfbf", "#73281d", "#e56739", "#402820", "#b39286", "#ffb380", "#b25f00",
                  "#593a16", "#ffaa00", "#7f6600", "#f2e6b6", "#e6f23d", "#717356", "#698c23", "#bfffbf",
                  "#004009", "#40ff59", "#00a658", "#40ffd9", "#238c77", "#3de6f2", "#264a4d", "#39ace6",
                  "#0061f2", "#265499", "#102340", "#80a2ff", "#8c86b3", "#5700d9", "#1f004d", "#4e3366",
                  "#bf73e6", "#f200e2", "#ffbffb", "#660052", "#e63995", "#b3869e", "#7f0033", "#663347",
                  "#33000e", "#b25965"]
        if clusters is not None:
            for i in range(len(clusters)):
                x = list()
                y = list()
                for j in clusters[i]:
                    x.append(self.data[j][2])
                    y.append(self.data[j][3])
                p.plot(x, y, color=colors[i], marker="+", linestyle="None")
            p.show()
        else:
            for i in range(0, 10):
                num = self.subsetData([i])
                x = list()
                y = list()
                for j in num:
                    x.append(j[2])
                    y.append(j[3])
                p.plot(x, y, color=colors[i], marker="+", linestyle="None")
            p.show()

        # temp = np.array(self.data)
        # x = temp[:, 2]
        # y = temp[:, 3]
        # p.plot(x, y, 'ro')
        # p.show()

    def listClusters(self, clusters):
        for c in clusters:
            print c


def main():
    # set km.data = km.subsetData([...]) before calling calculateSC() or visuals()
    km = MyKmeans()
    km.readData("C:\\Users\\Linsu\\Documents\\[PURDUE]\\CS 380\\proj\\digits-embedding.csv")
    # km.data = km.subsetData([2, 4, 6, 7])
    # km.data = km.subsetData([6, 7])
    # vector containing unique points [0, 1, 2, 3, 4, 5, 7, 14, 15, 17]
    # use k = 2, 4, 8, 16, 32
    clusters = km.cluster(50, 2)
    km.listClusters(clusters)
    km.calculateSC(clusters)
    # km.visuals()
    # km.visuals(clusters)


main()
