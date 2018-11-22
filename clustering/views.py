from clustering.serializers import ClusterSerializer, NodeSerializer, PluginFileSerializer
from clustering.models import Point, Cluster, Node, PluginFile
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
import logging, collections, copy
from sklearn.datasets import make_blobs
from rest_framework.response import Response
from rest_framework import status
import importlib
import os

logger = logging.getLogger(__name__)


class MainView(APIView):
    template_name = 'clustering/index.html'
    serializer_class = NodeSerializer

    def get(self, request):
        queryset = Node.objects.all()

        plugins = [f for f in os.listdir(os.path.abspath('clustering/plugins')) if f.endswith('.py')]
        return render(request, self.template_name, {'plugins': plugins})


class ClusterViewSet(viewsets.ModelViewSet):
    serializer_class = ClusterSerializer
    queryset = Cluster.objects.all()


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = PluginFileSerializer(data=request.data)
        file_serializer.is_valid()
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def assign_cluster(predicted_labels, nodes):
    for i, node in enumerate(nodes):
        node.cluster = predicted_labels[i]
        node.save()


@api_view(['POST'])
def generate_blobs(request):
    n_samples = 100
    random_state = 21
    xdata, ydata = make_blobs(n_samples=n_samples, random_state=random_state, cluster_std=0.99)
    for x1 in xdata:
        point = Point.objects.create(x=x1[0], y=x1[1], z=0)
        node_instance = Node.objects.create(coordinates=point)
        node_instance.save()
    return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)


def import_file(method):
    PLUGIN_NAME = method
    plugin = importlib.import_module('clustering.plugins.' + PLUGIN_NAME, '.')
    plugin_instance = plugin.Plugin()
    return plugin_instance


@api_view(['POST'])
def execute_algorithm(request, method):
    plugin_instance = import_file(method)
    queryset = Node.objects.all()

    dictionary = [obj.as_dict() for obj in queryset]
    history, labels = plugin_instance.execute(request, queryset)

    dict_of_clustered_data = {}

    for key, val in history.items():
        for i, data in enumerate(dictionary):
            data['cluster'] = val[i]
        dict_of_clustered_data[key] = copy.deepcopy(dictionary)

    full_data = {}
    full_data['data'] = dict_of_clustered_data
    full_data['labels'] = labels

    return Response(full_data)


@api_view(['GET'])
def get_params(request, method):
    plugin_instance = import_file(method)
    params = plugin_instance.parameters()
    return Response(params)


@api_view(['GET'])
def get_methods(request):
    plugins = [f.split('.')[0] for f in os.listdir(os.path.abspath('clustering/plugins')) if f.endswith('.py')]
    return Response(plugins)









