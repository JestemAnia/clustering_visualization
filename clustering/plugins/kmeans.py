from sklearn import cluster
from rest_framework.response import Response


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Kmeans algorithm. Args: ', args, '\nkwargs: ', kwargs)

    def execute(self, request, queryset):
        X = [[node.coordinates.x, node.coordinates.y] for node in queryset]
        n_cluster = int(request.POST['n_cluster'])
        max_iter = int(request.POST['max_iter'])

        y_pred = cluster.KMeans(n_clusters=n_cluster,
                                max_iter=max_iter,
                                random_state=123).fit_predict(X)
        for i, node in enumerate(queryset):
            node.cluster = y_pred[i]
            node.save()
        dictionary = [obj.as_dict() for obj in queryset]

        return Response(dictionary)