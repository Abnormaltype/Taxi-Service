from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name", country="test_country")

        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            first_name="test_FN",
            last_name="test_LN"
        )

        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name", country="test_country")
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)

        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test_password"
        license_number = "TES88888"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

