from scipy.cluster.hierarchy import linkage
import numpy as np
import copy


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Agglomerative Clustering algorithm. Args: ', args, '\nkwargs: ', kwargs)

    def execute(self, request, queryset):
        X = np.array([[node.coordinates.x, node.coordinates.y] for node in queryset])
        n_cluster = int(request.POST['n_cluster'])
        linkage_type = request.POST['linkage']

        linkage_matrix = linkage(X, linkage_type)

        n = len(X)
        labels = list(range(0, n))
        history = {'0': labels}
        cluster_dict = {}
        for i in range(0, n-n_cluster):
            new_cluster_id = i + 1

            previous_it = copy.deepcopy(history[str(i)])
            old_cluster_id_0 = int(linkage_matrix[i, 0])
            old_cluster_id_1 = int(linkage_matrix[i, 1])

            new_linkage = []

            if str(old_cluster_id_0) in cluster_dict.keys():
                cluster = cluster_dict[str(old_cluster_id_0)]
                while not all(x < n for x in cluster):
                    for x in cluster:
                        if x >= n:
                            cluster.extend(cluster_dict[x])
                new_linkage += cluster
            else:
                new_linkage.append(old_cluster_id_0)

            if str(old_cluster_id_1) in cluster_dict.keys():
                cluster = cluster_dict[str(old_cluster_id_1)]
                while any(x >= n for x in cluster):
                    for x in cluster:
                        if x >= n:
                            cluster.extend(cluster_dict[x])
                new_linkage += cluster
            else:
                new_linkage.append(old_cluster_id_1)

            cluster_dict[str(n+i)] = new_linkage

            if int(old_cluster_id_0) >= n:
                valid_cluster_0 = cluster_dict[str(old_cluster_id_0)]
            else:
                valid_cluster_0 = [previous_it[old_cluster_id_0]]

            if int(old_cluster_id_1) >= n:
                valid_cluster_1 = cluster_dict[str(old_cluster_id_1)]
            else:
                valid_cluster_1 = [previous_it[old_cluster_id_1]]

            label_0 = previous_it[valid_cluster_0[0]]
            label_1 = previous_it[valid_cluster_1[0]]
            occurrence_0 = previous_it.count(label_0)
            occurrence_1 = previous_it.count(label_1)

            if occurrence_0 >= occurrence_1:
                for idx in valid_cluster_1:
                    previous_it[idx] = label_0
            else:
                for idx in valid_cluster_0:
                    previous_it[idx] = label_1

            history[str(new_cluster_id)] = previous_it

        return history, labels

    def parameters(self):
        return {'n_cluster': 'number',
                'linkage': 'text'}
