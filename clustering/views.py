from clustering.serializers import ClusterSerializer, NodeSerializer, PluginFileSerializer
from clustering.models import Point, Cluster, Node, PluginFile
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
import logging
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
        logger.error(request.data)
        logger.error(request.data['file'])
        file_serializer = PluginFileSerializer(data=request.data)
        logger.error(file_serializer)
        file_serializer.is_valid()
        logger.error(file_serializer.errors)
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
    n_samples = 1500
    random_state = 170
    xdata, ydata = make_blobs(n_samples=n_samples, random_state=random_state)
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
    logger.error(method)
    logger.error(request.POST)
    return plugin_instance.execute(request, queryset)


@api_view(['GET'])
def get_params(request, method):
    plugin_instance = import_file(method)
    params = plugin_instance.parameters()
    logger.error(params)
    return Response(params)


@api_view(['GET'])
def get_methods(request):
    plugins = [f.split('.')[0] for f in os.listdir(os.path.abspath('clustering/plugins')) if f.endswith('.py')]
    return Response(plugins)


# def handle_uploaded_file(files):
#     pass
#
# @api_view(['POST'])
# def upload_file(request):
#     form = UploadFileForm(request.POST, request.FILES)
#     if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})






