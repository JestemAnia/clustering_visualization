from sklearn import cluster
from rest_framework.response import Response


class Plugin:
    def __init__(self, *args, **kwargs):
        print('Kmeans algorithm. Args: ', args, '\nkwargs: ', kwargs)

    def execute(self, request, queryset):
        X = [[node.coordinates.x, node.coordinates.y] for node in queryset]
        eps = float(request.POST['eps'])
        y_pred = cluster.DBSCAN(eps=eps).fit_predict(X)
        for i, node in enumerate(queryset):
            node.cluster = y_pred[i]
            node.save()
        dictionary = [obj.as_dict() for obj in queryset]

        return Response(dictionary)