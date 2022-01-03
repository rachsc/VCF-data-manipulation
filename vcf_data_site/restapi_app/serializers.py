from abc import ABC

from rest_framework import serializers
from .models import VcfRow


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        model = VcfRow
        fields = ('CHROM', 'POS', 'ID', 'REF', 'ALT')



class VcfRowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VcfRow
        fields = ('CHROM', 'POS', 'ID', 'REF', 'ALT')

