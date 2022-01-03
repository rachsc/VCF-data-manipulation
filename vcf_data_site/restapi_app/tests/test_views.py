from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ..models import VcfRow
from ..serializers import VcfRowSerializer
from django.urls import reverse
from django.contrib.auth.models import User
import base64


class TestViewResponses(APITestCase):
    api_endpoint = '/api/'

    @classmethod
    def setUp(cls):
        """
        Create a set of data to test with
        """
        cls.rows = [VcfRow.objects.create(CHROM='chrtest1', POS=1000, ID='rstest1', REF='T', ALT='T'),
                    VcfRow.objects.create(CHROM='chrtest2', POS=2000, ID='rstest2', REF='A', ALT='A'),
                    VcfRow.objects.create(CHROM='chrtest3', POS=3000, ID='rstest3', REF='G', ALT='G'),
                    VcfRow.objects.create(CHROM='chrtest4', POS=4000, ID='rstest4', REF='C', ALT='C')]

        cls.row = cls.rows[0]
        cls.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        cls.client = APIClient()
        cls.client.login(username=cls.user.username, password=cls.user.password)
        cls.auth = {'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'admin:admin123').decode("ascii")}

    def test_url_allow_hosts(self):
        """
        Testing allowed hosts
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_list_all_data(self):
        """
        Testing GET request which return all available data
        """
        response = self.client.get(reverse("restapi:vcf-data-list"))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.rows), len(response.data))

        for row in self.rows:
            self.assertIn(VcfRowSerializer(instance=row).data, response.data["results"])

    def test_can_read_a_specific_row(self):
        """
        Testing GET request which return a specific VCF row
        """
        response = self.client.get(reverse("restapi:vcf-data-detail", args=[self.row.ID]))

        self.assertEquals(status.HTTP_200_OK, response.status_code)

        self.assertEquals(VcfRowSerializer(instance=self.row).data, response.data)

    def test_can_add_new_row(self):
        """
        Testing POST request with a payload of new data and Basic Authorization
        """
        payload = {
            "CHROM": "chrtest",
            "POS": 12345,
            "ID": "rstest",
            "REF": "T",
            "ALT": "A"
        }

        response = self.client.post(reverse(
            "restapi:vcf-data-list"), payload, format='json', **self.auth)
        created_row = VcfRow.objects.get(ID=payload["ID"])

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        for k, v in payload.items():
            self.assertEquals(v, response.data[k])
            self.assertEquals(v, getattr(created_row, k))

    def test_can_edit_row(self):
        """
        Testing PUT request editing a row (looking for its ID) with payload.
        PUT needs Basic Authorization
        """

        payload = {
            "CHROM": "chrtestX",
            "POS": 1000,
            "ID": "rstestX",
            "REF": "T",
            "ALT": "T"
        }

        response = self.client.put(reverse("restapi:vcf-data-detail", kwargs={'pk': self.rows[1].ID}), payload,
                                   format='json', **self.auth)
        self.rows[1].refresh_from_db()

        self.assertEquals(status.HTTP_200_OK, response.status_code)

        for k, v in payload.items():
            self.assertEquals(v, response.data[k])
            self.assertEquals(v, getattr(self.rows[1], k))

    def test_can_delete_a_row(self):
        response = self.client.delete(
            reverse("restapi:vcf-data-detail", kwargs={'pk': self.rows[0].ID}), **self.auth
        )

        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(VcfRow.objects.filter(ID=self.rows[0].ID))