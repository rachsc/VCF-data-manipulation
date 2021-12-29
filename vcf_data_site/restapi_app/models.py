from django.db import models


class File(models.Model):
    chrom = models.CharField(max_length=100)
    pos = models.PositiveIntegerField()
    id = models.CharField(max_length=100, primary_key=True)
    ref = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)

    def __str__(self):
        return self.id


# Function that defines the schema of our model in the database

class VcfDataManager(models.Manager):
    def add_new_data(self, chrom, pos, id, ref, alt):
        new_data = self.create(CHROM=chrom, POS=pos, ID=id, REF=ref, ALT=alt)
        ## AQUI METO LA new_data AL FICHERO VCF !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return new_data


class VcfData(models.Model):
    chrom = models.CharField(max_length=100)
    pos = models.PositiveIntegerField()
    id = models.CharField(max_length=100, primary_key=True)
    ref = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)

    objects = VcfDataManager()

    def __str__(self):
        return self.id
