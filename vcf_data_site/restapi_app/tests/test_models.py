from django.test import TestCase
from ..models import VcfRow
from django.contrib.auth.models import User
from ..serializers import VcfRowSerializer, UserSerializer


class TestVcfRowModel(TestCase):

    def setUp(self) -> None:
        self.data1_attributes = {'CHROM': 'chrtest', 'POS': 1000, 'ID': 'rstest', 'REF': 'T', 'ALT': 'T'}
        self.user1_attributes = {'username': 'usertest', 'password': 'temporal'}
        self.data1 = VcfRow.objects.create(**self.data1_attributes)
        self.user1 = User.objects.create(**self.user1_attributes)
        self.data1_serializer = VcfRowSerializer(instance=self.data1)
        self.user1_serializer = UserSerializer(instance=self.user1)

    def test_vcfrow_model_entry(self):
        """
        Test VcfRow model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, VcfRow))

    def test_vcfrow_model_return(self):
        """
        Test VcfRow model return ID
        """
        data = self.data1
        self.assertEqual(str(data), 'rstest')

    def test_vcf_serializer(self):
        """
        Test VcfRowSerializer contains the expected fields.
        """
        data = self.data1_serializer.data
        self.assertEqual(str(data), str(self.data1_attributes))

    # def test_user_serializer(self):
    #     """
    #     Test UserSerializer contains the expected fields and only returns the username and not the password, for safety.
    #     """
    #     user = self.user1_serializer.create(self)
    #     self.assertEqual(str(user), str(self.user1_attributes['username']))
