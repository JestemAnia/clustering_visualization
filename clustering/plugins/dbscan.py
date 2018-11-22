from sklearn import cluster
from rest_framework.response import Response
import numpy as np
import logging, copy
logger = logging.getLogger(__name__)
import math


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Kmeans algorithm. Args: ', args, '\nkwargs: ', kwargs)

    def execute(self, request, queryset):
        X = np.array([[node.coordinates.x, node.coordinates.y] for node in queryset])
        eps = float(request.POST['eps'])
        min_pts = float(request.POST['minPts'])
        history = {}
        iteration = 1
        c = 0
        labels = np.zeros(X.shape[0])
        set_of_labels = [0]

        for i, p in enumerate(X):
            if labels[i] != 0:
                continue
            N = self.RangeQuery(X, self.distFunc, p, eps)
            if len(N) < min_pts:
                labels[i] = -1
                if labels[i] not in set_of_labels:
                    set_of_labels.append(labels[i])
                history[str(iteration)] = copy.deepcopy(labels)
                iteration += 1
                continue

            c = c + 1
            labels[i] = c
            if labels[i] not in set_of_labels:
                set_of_labels.append(labels[i])
            history[str(iteration)] = copy.deepcopy(labels)
            iteration += 1

            S = ([[x, y] for x, y in N if x != p[0] and y != p[1]])

            for q in S:
                j = np.where(X == q)[0][0]
                if labels[j] == -1 or labels[j] == 0:
                    labels[j] = c
                    if labels[i] not in set_of_labels:
                        set_of_labels.append(labels[i])
                    history[str(iteration)] = copy.deepcopy(labels)
                    iteration += 1
                    N = self.RangeQuery(X, self.distFunc, q, eps)
                    if len(N) >= min_pts:
                        S += ([[x, y] for x, y in N if [x, y] not in S])
                else:
                    continue
        return history, sorted(set_of_labels)

    def parameters(self):
        return {'eps': 'float',
                'minPts': 'number'}

    def RangeQuery(self, X, distFunc, q, eps):
        neighbors = []
        for p in X:
            if distFunc(q, p) <= eps:
                neighbors.append(p)

        return neighbors

    def distFunc(self, q, p):
        return math.sqrt(np.power(p - q, 2).sum())
