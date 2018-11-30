from sklearn import cluster


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Kmeans algorithm. Args: ', args, '\nkwargs: ', kwargs)

    def execute(self, request, queryset):
        X = [[node.coordinates.x, node.coordinates.y] for node in queryset]
        n_cluster = int(request.POST['n_cluster'])
        max_iter = int(request.POST['max_iter'])
        previous_clusters = []
        history = {}
        for i in range(0, max_iter):
            if i == 0:
                kmeans = cluster.KMeans(init='random', n_clusters=n_cluster, random_state=123, max_iter=1).fit(X)
            else:
                kmeans = cluster.KMeans(init=previous_clusters, n_clusters=n_cluster, random_state=123, max_iter=1).fit(X)

            previous_clusters = kmeans.cluster_centers_
            y_pred = kmeans.predict(X)

            history[str(i+1)] = y_pred
        return history, list(range(n_cluster))

    def parameters(self):
        return {'n_cluster': 'number',
                'max_iter': 'number'}

