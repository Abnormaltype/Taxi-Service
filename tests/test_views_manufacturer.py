from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
PAGINATE_BY = 2


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "BMW",
            "country": "Germany",
        }

        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)

        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")

        upd_data = {
            "name": "Mercedes",
            "country": new_manufacturer.country
        }

        self.client.post(reverse("taxi:manufacturer-update", kwargs={"pk": new_manufacturer.id}), data=upd_data)

        upd_manufacturer = Manufacturer.objects.get(pk=new_manufacturer.id)

        self.assertEqual(new_manufacturer.id, upd_manufacturer.id)
        self.assertNotEqual(new_manufacturer.name, upd_manufacturer.name)
        self.assertEqual(upd_manufacturer.name, upd_data["name"])
        self.assertEqual(new_manufacturer.country, upd_manufacturer.country)

    def test_delete_manufacturer(self):
        new_manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        new_manufacturer2 = Manufacturer.objects.create(name="Mercedes", country="Germany")

        self.client.post(reverse("taxi:manufacturer-delete", kwargs={"pk": new_manufacturer1.id}))
        self.client.post(reverse("taxi:manufacturer-delete", kwargs={"pk": new_manufacturer2.id}))

        self.assertEqual(Manufacturer.objects.count(), 0)

    def test_pagination_is_two(self):
        num_manufacturer = 10

        for manufacturer in range(num_manufacturer):
            Manufacturer.objects.create(
                name=f"name {manufacturer}",
                country=f"country {manufacturer}"
            )

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["manufacturer_list"]) == PAGINATE_BY)

    def test_pagination_on_last_page(self):
        num_manufacturer = 11

        for manufacturer in range(num_manufacturer):
            Manufacturer.objects.create(
                name=f"name {manufacturer}",
                country=f"country {manufacturer}"
            )

        response = self.client.get(MANUFACTURER_URL + f"?page={round(num_manufacturer / PAGINATE_BY)}")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["manufacturer_list"]) == 1)
