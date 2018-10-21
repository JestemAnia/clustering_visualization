from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from clustering.views import MainView, NodeViewSet, ClusterViewSet, kmeans


urlpatterns = [
    # handle node object
    url(r'node/$', NodeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='Node_detail'),
    #handle cluster object
    url(r'cluster/$', ClusterViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='Cluster_detail'),
    # kmean
    url(r'kmeans/$', kmeans, name='kmeans'),
    # the main view
    url(r'$', MainView.as_view(), name='Point_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
