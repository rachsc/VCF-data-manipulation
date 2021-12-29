from django.shortcuts import render
from rest_framework import generics, status
import io
import csv
import gzip
import json
import pandas as pd
from rest_framework.response import Response
from .models import File
from .serializers import FileUploadSerializer, SaveFileSerializer
from django.contrib import messages


# Function that reads a VCF file
def read_vcf(vcf_path):
    with gzip.open(vcf_path, "rt") as ifile:
        lines = [l for l in ifile if not l.startswith('##')]

    col_list = ['#CHROM', 'POS', 'ID', 'REF', 'ALT']
    vcf_reader = pd.read_csv(
        io.StringIO(''.join(lines)),
        usecols=col_list,
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})

    return vcf_reader


class UploadFileView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vcf_file = serializer.validated_data['file']

        # Check if the file to be uploaded is in fact a VCF file
        if not vcf_file.name.endswith('.vcf.gz') and not vcf_file.name.endswith('.vcf'):
            messages.error(request, 'THIS IS NOT A VCF FILE')
        vcf_reader = read_vcf(vcf_file)
        df = pd.DataFrame(vcf_reader)

        # Save data from VCF file row by row
        for i in range(0, df.shape[0]):
            row = json.loads(df.loc[i].to_json())
            new_file = File(
                chrom=row['CHROM'],
                pos=row['POS'],
                id=row['ID'],
                ref=row['REF'],
                alt=row['ALT']
            )
            new_file.save()
        return Response({"status": "success"}, status.HTTP_201_CREATED)
