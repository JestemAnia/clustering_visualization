from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from clustering.views import MainView, NodeViewSet, ClusterViewSet, FileView, generate_blobs, execute_algorithm, get_params, get_methods
import importlib
import os


urlpatterns = [
    url(r'^node/$', NodeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='Node_detail'),
    url(r'^cluster/$', ClusterViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='Cluster_detail'),
    url(r'^(?P<method>\w+?)/parameters/$', get_params),
    url(r'^generate/$', generate_blobs, name='generate_data'),
    url(r'^methods/$', get_methods, name='get_methods'),
    url(r'^upload/$', FileView.as_view(), name='file_upload')]

plugins = [f for f in os.listdir(os.path.abspath('clustering/plugins')) if f.endswith('.py')]

for plugin in plugins:
    method_name = plugin[:-3]
    plugin_name = 'clustering.plugins.' + method_name
    plugin_module = importlib.import_module(plugin_name, '.')
    urlpatterns.append(url(r'^(?P<method>\w+?)/$', execute_algorithm, name=method_name))

urlpatterns.append(url(r'^$', MainView.as_view(), name='Point_list'))
urlpatterns = format_suffix_patterns(urlpatterns)
