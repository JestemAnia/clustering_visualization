from django.db import models


class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    def as_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

    def __str__(self):
        return "(%f, %f, %f)" % (self.x, self.y, self.z)


class Cluster(models.Model):
    centroid = models.OneToOneField(Point, on_delete=models.CASCADE)

    def __str__(self):
        return "(%f, %f, %f)" % (self.centroid.x, self.centroid.y, self.centroid.z)


class Node(models.Model):
    coordinates = models.OneToOneField(Point, on_delete=models.CASCADE)
    cluster = models.IntegerField(blank=True, null=True)

    def as_dict(self):
        return {
            "id": self.id,
            "coordinates": self.coordinates.as_dict(),
            # "cluster": int(self.cluster)
        }

    def __str__(self):
        return "(%f, %f, %f)" % (self.coordinates.x, self.coordinates.y, self.coordinates.z)


class PluginFile(models.Model):
    file = models.FileField(blank=False, null=False)
