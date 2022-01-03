from django.db import models


# Function that defines the schema of our model in the database

# class VcfRowManager(models.Manager):
#     def add_new_data(self, CHROM, POS, ID, REF, ALT):
#         new_data = self.create(CHROM=CHROM, POS=POS, ID=ID, REF=REF, ALT=ALT)
#         ## AQUI METO LA new_data AL FICHERO VCF !!!!!!!!!!!!!!!
#         return new_data


class VcfRow(models.Model):
    CHROM = models.CharField(max_length=100)
    POS = models.PositiveIntegerField()
    ID = models.CharField(max_length=100)
    REF = models.CharField(max_length=100)
    ALT = models.CharField(max_length=100)
    my_pk = models.AutoField(primary_key=True)

    objects = models.Manager()

    def __str__(self):
        return self.ID
