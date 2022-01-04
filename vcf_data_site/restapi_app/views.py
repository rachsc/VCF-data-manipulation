from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
import io
import gzip
import json
import pandas as pd
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from .models import VcfRow
from .serializers import FileUploadSerializer, VcfRowSerializer, UserSerializer
from django.contrib import messages
from django.utils import timezone


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
    parser_classes = [MultiPartParser]
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        start_time = timezone.now()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vcf_file = serializer.validated_data['file']

        # Check if the file to be uploaded is in fact a VCF file
        if not vcf_file.name.endswith('.vcf.gz') and not vcf_file.name.endswith('.vcf'):
            messages.error(request, 'THIS IS NOT A VCF FILE')
        vcf_reader = read_vcf(vcf_file)
        df = pd.DataFrame(vcf_reader)

        rows = []
        # Save data from VCF file row by row
        for i in range(0, df.shape[0]):
            row = json.loads(df.loc[i].to_json())
            new_row = VcfRow(
                CHROM=row['CHROM'],
                POS=row['POS'],
                ID=row['ID'],
                REF=row['REF'],
                ALT=row['ALT']
            )
            # new_file.save()
            rows.append(new_row)
            if len(rows) > 5000:
                VcfRow.objects.bulk_create(rows)
                rows = []
        if rows:
            VcfRow.objects.bulk_create(rows)

        end_time = timezone.now()
        print(
            f"Loading VCF file took: {(end_time - start_time).total_seconds()} seconds."
        )

        return Response({"status": "success"}, status.HTTP_201_CREATED)


class VcfRowViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, SessionAuthentication,)
    serializer_class = VcfRowSerializer

    def get_permissions(self):
        if self.request.method != 'PUT' and self.request.method != 'POST' and self.request.method != 'DELETE':
            return []
        return super().get_permissions()

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(VcfRow, ID=item)

    def get_queryset(self):
        return VcfRow.objects.all().order_by('CHROM')


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)