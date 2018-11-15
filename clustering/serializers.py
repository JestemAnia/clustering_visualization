from rest_framework import serializers
from clustering.models import Cluster, Point, Node, PluginFile


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('x', 'y', 'z')


class NodeSerializer(serializers.ModelSerializer):
    coordinates = PointSerializer(required=True)

    class Meta:
        model = Node
        fields = ('cluster', 'coordinates')

    def create(self, validated_data):
        coordinates_data = validated_data.pop('coordinates')
        coordinates = PointSerializer.create(PointSerializer(), validated_data=coordinates_data)
        cluster_data = validated_data.pop('cluster')
        node, created = Node.objects.update_or_create(coordinates=coordinates, cluster=cluster_data)
        return node


class ClusterSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True)
    centroid = PointSerializer(required=True)

    class Meta:
        model = Cluster
        fields = ('centroid', 'nodes')

    def create(self, validated_data):
        centroid_data = validated_data.pop('centroid')
        centroid = PointSerializer.create(PointSerializer(), validated_data=centroid_data)
        nodes = validated_data.pop('nodes')
        cluster, created = Cluster.objects.update_or_create(centroid=centroid)
        for node in nodes:
            Node.objects.create(cluster=cluster, **node)
        return cluster


class PluginFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginFile
        fields = ('file',)
