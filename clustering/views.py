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
        queryset = Node.objects.all()
        # coordinates = Node.objects.select_related('coordinates').all()
        coordinates = queryset.coordinates
        self.logger.error(coordinates)

        return render(request, self.template_name, self.scatter_plot(coordinates))

    def scatter_plot(self, queryset, labels=1):
        # self.logger.error(queryset)

        xdata = queryset.values_list('x').distinct()
        ydata = queryset.values_list('y').distinct()
        self.logger.error(ydata)
        self.logger.error(type(xdata[0]))
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
    # request musi mieć w body node'y
    queryset = Node.objects.all()

    y_pred = cluster.KMeans(n_clusters=n_cluster, random_state=random_state).fit(xdata)
    labels = y_pred.labels
    centroids = y_pred.cluster_centers_
    n_iter = y_pred.n_iter
    return Response({"message": y_pred})


