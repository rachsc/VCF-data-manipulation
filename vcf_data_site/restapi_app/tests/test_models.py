from django.test import TestCase
from ..models import VcfRow


class TestVcfRowModel(TestCase):

    def setUp(self) -> None:
        self.data1 = VcfRow.objects.create(CHROM='chrtest', POS=1000, ID='rstest', REF='T', ALT='T')

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
