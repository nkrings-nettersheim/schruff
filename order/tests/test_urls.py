from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import index, impressum, datenschutz, collectiondate, collectiontime, product, customer, complete, thanks, \
    start_fasttrack, start_order_list, order_list


class TestUrls(SimpleTestCase):

    def test_url_index_is_resolved(self):
        url = reverse('order:index')
        self.assertEqual(resolve(url).func, index)

    def test_url_impressum_is_resolved(self):
        url = reverse('order:impressum')
        self.assertEqual(resolve(url).func, impressum)

    def test_url_datenschutz_is_resolved(self):
        url = reverse('order:datenschutz')
        self.assertEqual(resolve(url).func, datenschutz)

    def test_url_collectiondate_is_resolved(self):
        url = reverse('order:collectiondate')
        self.assertEqual(resolve(url).func, collectiondate)

    def test_url_product_is_resolved(self):
        url = reverse('order:product')
        self.assertEqual(resolve(url).func, product)

    def test_url_collectiontime_is_resolved(self):
        url = reverse('order:collectiontime')
        self.assertEqual(resolve(url).func, collectiontime)

    def test_url_customer_is_resolved(self):
        url = reverse('order:customer')
        self.assertEqual(resolve(url).func, customer)

    def test_url_complete_is_resolved(self):
        url = reverse('order:complete')
        self.assertEqual(resolve(url).func, complete)

    def test_url_thanks_is_resolved(self):
        url = reverse('order:thanks')
        self.assertEqual(resolve(url).func, thanks)

    def test_url_fasttrackstart_is_resolved(self):
        url = reverse('order:fasttrackstart')
        self.assertEqual(resolve(url).func, start_fasttrack)

    def test_url_orderliststart_is_resolved(self):
        url = reverse('order:orderliststart')
        self.assertEqual(resolve(url).func, start_order_list)

    def test_url_orderlist_is_resolved(self):
        url = reverse('order:orderlist')
        self.assertEqual(resolve(url).func, order_list)

