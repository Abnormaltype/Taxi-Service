from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "HHH88888",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_license_number(self):
        new_driver = get_user_model().objects.create_user(
            username="username",
            password="password12345",
            first_name="test first",
            last_name="test last",
            license_number="HHH88888"
        )
        new_driver.save()

        form_data = {
            "license_number": "TIT77777"
        }

        self.client.post(reverse("taxi:driver-update-license-number", kwargs={"pk": new_driver.id}), data=form_data)

        upd_driver = get_user_model().objects.get(pk=new_driver.id)

        self.assertEqual(upd_driver.first_name, new_driver.first_name)
        self.assertEqual(upd_driver.last_name, new_driver.last_name)
        self.assertNotEqual(upd_driver.license_number, new_driver.license_number)
        self.assertEqual(upd_driver.license_number, form_data["license_number"])
