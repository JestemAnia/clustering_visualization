from clustering.serializers import ClusterSerializer, NodeSerializer
from clustering.models import Point, Cluster, Node
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
import logging
from sklearn import cluster
from sklearn.datasets import make_blobs
from rest_framework.response import Response
from rest_framework import status


class MainView(APIView):
    template_name = 'clustering/index.html'
    serializer_class = NodeSerializer
    logger = logging.getLogger(__name__)

    def get(self, request):
        queryset = Node.objects.all()
        return render(request, self.template_name)


class ClusterViewSet(viewsets.ModelViewSet):
    serializer_class = ClusterSerializer
    queryset = Cluster.objects.all()


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()


@api_view(['POST'])
def kmeans(request, random_state=0):
    n_cluster = int(request.POST['n_cluster'])
    max_iter = int(request.POST['max_iter'])
    logger = logging.getLogger(__name__)
    logger.error(max_iter)
    queryset = Node.objects.all()
    X = [[node.coordinates.x, node.coordinates.y] for node in queryset]
    y_pred = cluster.KMeans(n_clusters=n_cluster,
                            max_iter=max_iter,
                            random_state=123).fit_predict(X)
    assign_cluster(y_pred, queryset)
    dictionary = [obj.as_dict() for obj in queryset]

    return Response(dictionary)


@api_view(['POST'])
def dbscan(request):
    eps = float(request.POST['eps'])
    queryset = Node.objects.all()
    X = [[node.coordinates.x, node.coordinates.y] for node in queryset]
    y_pred = cluster.DBSCAN(eps=eps).fit_predict(X)
    assign_cluster(y_pred, queryset)
    dictionary = [obj.as_dict() for obj in queryset]

    return Response(dictionary)


def assign_cluster(predicted_labels, nodes):
    for i, node in enumerate(nodes):
        node.cluster = predicted_labels[i]
        node.save()


@api_view(['POST'])
def generate_blobs(request):
    n_samples = 1500
    random_state = 170
    xdata, ydata = make_blobs(n_samples=n_samples, random_state=random_state)
    for x1 in xdata:
        point = Point.objects.create(x=x1[0], y=x1[1], z=0)
        node_instance = Node.objects.create(coordinates=point)
        node_instance.save()
    return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)







