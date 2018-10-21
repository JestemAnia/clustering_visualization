from clustering.serializers import PointSerializer, ClusterSerializer, NodeSerializer
from clustering.models import Point, Cluster, Node
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
import logging
from rest_framework.response import Response
from rest_framework import status
from sklearn import cluster
from django.db.models import Q


class MainView(APIView):
    template_name = 'clustering/index.html'
    serializer_class = NodeSerializer
    logger = logging.getLogger(__name__)

    def get(self, request):
        queryset = Point.objects.all()
        # coordinates = Node.objects.select_related('coordinates').all()

        return render(request, self.template_name, self.scatter_plot(queryset))

    def scatter_plot(self, queryset, labels=1):

        xdata = queryset.values_list('x').distinct()
        ydata = queryset.values_list('y').distinct()

        chartdata = {
            'x': xdata,
            'y': ydata
        }

        charttype = "scatterChart"
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
        }

        return data


class ClusterViewSet(viewsets.ModelViewSet):
    serializer_class = ClusterSerializer
    queryset = Cluster.objects.all()


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()


@api_view(['POST'])
def kmeans(request, n_cluster=2, random_state=0):
    logger = logging.getLogger(__name__)

    queryset = Node.objects.all()
    X = [[node.coordinates.x, node.coordinates.y] for node in queryset]
    y_pred = cluster.KMeans(n_clusters=n_cluster, random_state=random_state).fit_predict(X)
    # labels = y_pred.labels
    # centroids = y_pred.cluster_centers_
    # n_iter = y_pred.n_iter
    assign_cluster(y_pred, queryset)


def assign_cluster(predicted_labels, nodes):
    for i, node in enumerate(nodes):
        node.cluster = predicted_labels[i]
        node.save()





