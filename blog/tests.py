from django.test import TestCase

# Create your tests here.
class IndexTests(TestCase):
	def test_index_view_status_cod(self):
		url = reverse('index')
		response = self.client.get(url)
		self.assertEquals(response.status_code,200)