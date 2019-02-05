from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from accounts.models import Churches
# Create your tests here.

class Hometest(SimpleTestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)



class ChurchesPostTest(TestCase):

    def setUp(self):
        Churches.objects.create(name='example name', location='remera', umushumba='gitwaza')
        Churches.objects.create(name='example ', location='gishushu', umushumba='capital pa')


    def test_get_churches(self):
        churches = Churches.objects.all()
        self.assertEquals(len(churches), 2)
