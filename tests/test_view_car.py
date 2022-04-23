from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        manufacturer2 = Manufacturer.objects.create(name="Audi", country="Germany")

        Car.objects.create(model="e32", manufacturer=manufacturer1)
        Car.objects.create(model="Q8", manufacturer=manufacturer2)

        response = self.client.get(CAR_URL)

        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_delete_car(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        manufacturer2 = Manufacturer.objects.create(name="Audi", country="Germany")

        car1 = Car.objects.create(model="e32", manufacturer=manufacturer1)
        car2 = Car.objects.create(model="RS7", manufacturer=manufacturer2)

        self.assertEqual(Car.objects.count(), 2)

        self.client.post(reverse("taxi:car-delete", kwargs={"pk": car1.id}))
        self.client.post(reverse("taxi:car-delete", kwargs={"pk": car2.id}))

        self.assertEqual(Car.objects.count(), 0)

    def test_search_car(self):
        manufacturer1 = Manufacturer.objects.create(name="BMW", country="Germany")
        manufacturer2 = Manufacturer.objects.create(name="Audi", country="Germany")

        Car.objects.create(model="e32", manufacturer=manufacturer1)
        Car.objects.create(model="Q8", manufacturer=manufacturer2)
        Car.objects.create(model="RS7", manufacturer=manufacturer2)
        Car.objects.create(model="e38", manufacturer=manufacturer1)

        response = self.client.get(CAR_URL + "?model=e")

        car = Car.objects.filter(model__icontains="e")

        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
