from datetime import date
from django.db import models
from django.test import TestCase
from ..models import Order_days, Order_times, Order, Order_details, Content_text


class ContentTextModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Content_text.objects.create(
            content_kurz='Impressum',
            content_lang='Dies ist das Impressum'
        )

    # check if field exists #######################################################################
    def test_it_has_information_fields(self):
        content_text = Content_text.objects.get(id=1)
        self.assertIsInstance(content_text.content_kurz, str)
        self.assertIsInstance(content_text.content_lang, str)

    # check label #################################################################################
    def test_content_kurz_label(self):
        content_text = Content_text.objects.get(id=1)
        field_label = content_text._meta.get_field('content_kurz').verbose_name
        self.assertEqual(field_label, 'content kurz')

    def test_content_lang_label(self):
        content_text = Content_text.objects.get(id=1)
        field_label = content_text._meta.get_field('content_lang').verbose_name
        self.assertEqual(field_label, 'content lang')

    # check max_length ############################################################################
    def test_content_kurz_max_length(self):
        content_text = Content_text.objects.get(id=1)
        max_length = content_text._meta.get_field('content_kurz').max_length
        self.assertEqual(max_length, 256)

    # check object_name ############################################################################
    def test_Content_text_object_name(self):
        content_text = Content_text.objects.get(id=1)
        expected_object_name = f'{content_text.content_kurz}'
        self.assertEqual(expected_object_name, str(content_text))


class OrderDaysModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Order_days.objects.create(
            order_day='2021-05-21',
            reibekuchen='0',
            spiessbraten='1'
        )

    # check if field exists #######################################################################
    def test_it_has_information_fields(self):
        order_days = Order_days.objects.get(id=1)
        self.assertIsInstance(order_days.order_day, date)
        self.assertIsInstance(order_days.reibekuchen, int)
        self.assertIsInstance(order_days.spiessbraten, int)

    # check object_name ############################################################################
    def test_order_days_object_name(self):
        order_days = Order_days.objects.get(id=1)
        expected_object_name = f'{order_days.order_day}'
        self.assertEqual(expected_object_name, str(order_days))


class OrderTimesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Order_times.objects.create(
            order_time='2021-05-21 20:00:00',
            reserved='0',
            booked='1'
        )

    # check if field exists #######################################################################
    def test_it_has_information_fields(self):
        order_times = Order_times.objects.get(id=1)
        self.assertIsInstance(order_times.order_time, date)
        self.assertIsInstance(order_times.reserved, int)
        self.assertIsInstance(order_times.booked, int)

    # check object_name ############################################################################
    def test_order_times_object_name(self):
        order_times = Order_times.objects.get(id=1)
        expected_object_name = f'{order_times.order_time}'
        self.assertEqual(expected_object_name, str(order_times))


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Order.objects.create(
            name='Mustermann',
            callnumber='123456789'
        )

    # check if field exists #######################################################################
    def test_it_has_information_fields(self):
        order = Order.objects.get(id=1)
        self.assertIsInstance(order.name, str)
        self.assertIsInstance(order.callnumber, str)
        self.assertIsInstance(order.email, str)
        self.assertIsInstance(order.order_day, date)
        self.assertIsInstance(order.order_time, date)
        self.assertIsInstance(order.order_long, str)
        self.assertIsInstance(order.wishes, str)
        self.assertIsInstance(order.price, str)
        self.assertIsInstance(order.session, str)
        self.assertIsInstance(order.session_time, date)

    # check label #################################################################################
    def test_name_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_callnumber_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('callnumber').verbose_name
        self.assertEqual(field_label, 'callnumber')

    def test_email_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_order_day_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('order_day').verbose_name
        self.assertEqual(field_label, 'order day')

    def test_order_time_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('order_time').verbose_name
        self.assertEqual(field_label, 'order time')

    def test_order_long_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('order_long').verbose_name
        self.assertEqual(field_label, 'order long')

    def test_wishes_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('wishes').verbose_name
        self.assertEqual(field_label, 'wishes')

    def test_price_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')

    def test_session_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('session').verbose_name
        self.assertEqual(field_label, 'session')

    def test_session_time_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('session_time').verbose_name
        self.assertEqual(field_label, 'session time')

    # check max_length ############################################################################
    def test_name_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_callnumber_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('callnumber').max_length
        self.assertEqual(max_length, 25)

    def test_email_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('email').max_length
        self.assertEqual(max_length, 75)

    def test_order_long_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('order_long').max_length
        self.assertEqual(max_length, 500)

    def test_price_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('price').max_length
        self.assertEqual(max_length, 10)

    def test_session_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('session').max_length
        self.assertEqual(max_length, 100)

    # check object_name ############################################################################
    def test_Order_object_name(self):
        order = Order.objects.get(id=1)
        expected_object_name = f'{order.name}'
        self.assertEqual(expected_object_name, str(order))


class OrderDetailsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Order.objects.create(
            name='Mustermann',
            callnumber='123456789'
        )
        Order_details.objects.create(
            product='Spießbraten',
            product_count=2,
            order_id=1
        )

    # check if field exists #######################################################################
    def test_it_has_information_fields(self):
        order_details = Order_details.objects.get(id=1)
        self.assertIsInstance(order_details.product, str)
        self.assertIsInstance(order_details.product_count, int)

    # check label #################################################################################
    def test_product_label(self):
        order_details = Order_details.objects.get(id=1)
        field_label = order_details._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'product')

    def test_product_count_label(self):
        order_details = Order_details.objects.get(id=1)
        field_label = order_details._meta.get_field('product_count').verbose_name
        self.assertEqual(field_label, 'product count')

    # check max_length ############################################################################
    def test_product_max_length(self):
        order_details = Order_details.objects.get(id=1)
        max_length = order_details._meta.get_field('product').max_length
        self.assertEqual(max_length, 100)

    # check object_name ############################################################################
    def test_Order_details_object_name(self):
        order_details = Order_details.objects.get(id=1)
        expected_object_name = f'{order_details.product}'
        self.assertEqual(expected_object_name, str(order_details))
