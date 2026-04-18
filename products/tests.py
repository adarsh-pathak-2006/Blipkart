from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from .models import product


class AuthFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com',
            email='user@example.com',
            password='secure-pass',
            first_name='User',
        )

    def test_login_ignores_external_next_url(self):
        response = self.client.post(
            reverse('login'),
            {
                'email': 'user@example.com',
                'password': 'secure-pass',
                'next': 'https://evil.example/steal',
            },
        )

        self.assertRedirects(response, reverse('home'))

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)


class CartFlowTests(TestCase):
    def setUp(self):
        self.item = product.objects.create(
            name='Demo Item',
            description='For testing',
            price=250,
        )

    def test_add_and_remove_cart_require_post(self):
        add_url = reverse('products:add_to_cart', args=[self.item.id])
        remove_url = reverse('products:remove_from_cart', args=[self.item.id])

        self.assertEqual(self.client.get(add_url).status_code, 405)
        self.assertEqual(self.client.get(remove_url).status_code, 405)

        response = self.client.post(add_url)
        self.assertRedirects(response, reverse('home'))

        session = self.client.session
        self.assertIn(self.item.id, session.get('cart', []))

        response = self.client.post(remove_url)
        self.assertRedirects(response, reverse('products:cart'))

        session = self.client.session
        self.assertNotIn(self.item.id, session.get('cart', []))

    def test_cart_view_drops_stale_item_ids(self):
        session = self.client.session
        session['cart'] = [self.item.id, 999999]
        session.save()

        response = self.client.get(reverse('products:cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item_count'], 1)

        session = self.client.session
        self.assertEqual(session.get('cart', []), [self.item.id])


class OrderFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='buyer@example.com',
            email='buyer@example.com',
            password='secure-pass',
            first_name='Buyer',
        )
        self.item = product.objects.create(
            name='Demo Item',
            description='For testing',
            price=250,
        )
        session = self.client.session
        session['cart'] = [self.item.id]
        session.save()

    @patch('products.views.send_mail')
    def test_place_order_clears_cart_on_success(self, mocked_send_mail):
        self.client.force_login(self.user)
        response = self.client.post(reverse('products:place_order'))

        self.assertRedirects(response, reverse('products:cart'))
        mocked_send_mail.assert_called_once()

        session = self.client.session
        self.assertEqual(session.get('cart', []), [])

    @patch('products.views.send_mail', side_effect=TimeoutError('smtp timeout'))
    def test_place_order_handles_network_email_failures(self, mocked_send_mail):
        self.client.force_login(self.user)
        response = self.client.post(reverse('products:place_order'))

        self.assertRedirects(response, reverse('products:cart'))
        mocked_send_mail.assert_called_once()

        session = self.client.session
        self.assertEqual(session.get('cart', []), [self.item.id])
