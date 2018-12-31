"""Tests for users app"""
from django.test import TestCase, override_settings
from model_mommy import mommy
from django.conf import settings

from users.utils import get_client_id


@override_settings(APR_CLIENTID_PREFIX="D.")
class TestUtils(TestCase):
    """Test ultils"""

    def test_get_client_id(self):
        """Test get_client_id"""
        user = mommy.make('auth.User')
        customer = mommy.make('customers.Customer', user=user)
        mommy.make(
            'users.Client',
            first_name="A",
            last_name="Keller",
            client_id="{}K18".format(settings.APR_CLIENTID_PREFIX),
            creator=user,
            customer=customer)
        client2 = mommy.make(
            'users.Client',
            first_name="A",
            last_name="Kelly",
            creator=user,
            customer=customer)
        client3 = mommy.make(
            'users.Client',
            first_name="A",
            last_name="",
            creator=user,
            customer=customer)
        client4 = mommy.make(
            'users.Client',
            first_name="A",
            last_name="Z",
            creator=user,
            customer=customer)

        self.assertEqual(
            "D.K 19",
            get_client_id(
                client2,
                prefix=settings.APR_CLIENTID_PREFIX,
                separator=" ",
                use_name=True))

        self.assertEqual(
            "D.A 1",
            get_client_id(
                client3,
                prefix=settings.APR_CLIENTID_PREFIX,
                separator=" ",
                use_name=True))

        self.assertEqual(
            "D.Z 1",
            get_client_id(
                client4,
                prefix=settings.APR_CLIENTID_PREFIX,
                separator=" ",
                use_name=True))
