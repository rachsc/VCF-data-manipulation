from django.db import models


class File(models.Model):
    chrom = models.CharField(max_length=100)
    pos = models.PositiveIntegerField()
    id = models.CharField(max_length=100, primary_key=True)
    ref = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)

    def __str__(self):
        return self.id
