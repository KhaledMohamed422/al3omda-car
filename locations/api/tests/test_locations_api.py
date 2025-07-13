from rest_framework.test import APIClient
from locations.models import Governorate, City



class TestGovernorateAPI:
    client = APIClient()

    def test_create_governorate(self):
        response = self.client.post("/locations/governorates/", {
            "governorate_name_ar": "القاهرة",
            "governorate_name_en": "Cairo"
        })
        assert response.status_code == 201
        assert response.data["governorate_name_ar"] == "القاهرة"

    def test_list_governorates(self):
        Governorate.objects.create(governorate_name_ar="الجيزة", governorate_name_en="Giza")
        response = self.client.get("/locations/governorates/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_retrieve_governorate(self):
        gov = Governorate.objects.create(governorate_name_ar="المنصورة", governorate_name_en="Mansoura")
        response = self.client.get(f"/locations/governorates/{gov.id}/")
        assert response.status_code == 200
        assert response.data["governorate_name_en"] == "Mansoura"

    def test_update_governorate(self):
        gov = Governorate.objects.create(governorate_name_ar="الاسكندرية", governorate_name_en="Alex")
        response = self.client.patch(f"/locations/governorates/{gov.id}/", {
            "governorate_name_en": "Alexandria"
        })
        assert response.status_code == 200
        assert response.data["governorate_name_en"] == "Alexandria"

    def test_delete_governorate(self):
        gov = Governorate.objects.create(governorate_name_ar="بني سويف", governorate_name_en="Beni Suef")
        response = self.client.delete(f"/locations/governorates/{gov.id}/")
        assert response.status_code == 204
        assert not Governorate.objects.filter(id=gov.id).exists()


class TestCityAPI:
    client = APIClient()

    def test_create_city(self):
        gov = Governorate.objects.create(governorate_name_ar="سوهاج", governorate_name_en="Sohag")
        response = self.client.post("/locations/cities/", {
            "city_name_ar": "جرجا",
            "city_name_en": "Girga",
            "governorate": gov.id
        })
        assert response.status_code == 201
        assert response.data["city_name_ar"] == "جرجا"

    def test_list_cities(self):
        gov = Governorate.objects.create(governorate_name_ar="قنا", governorate_name_en="Qena")
        City.objects.create(city_name_ar="نقادة", city_name_en="Naqada", governorate=gov)
        response = self.client.get("/locations/cities/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_retrieve_city(self):
        gov = Governorate.objects.create(governorate_name_ar="الأقصر", governorate_name_en="Luxor")
        city = City.objects.create(city_name_ar="ارمنت", city_name_en="Armant", governorate=gov)
        response = self.client.get(f"/locations/cities/{city.id}/")
        assert response.status_code == 200
        assert response.data["city_name_en"] == "Armant"

    def test_update_city(self):
        gov = Governorate.objects.create(governorate_name_ar="مطروح", governorate_name_en="Matruh")
        city = City.objects.create(city_name_ar="سيوة", city_name_en="Siwa", governorate=gov)
        response = self.client.patch(f"/locations/cities/{city.id}/", {
            "city_name_en": "Siwa Oasis"
        })
        assert response.status_code == 200
        assert response.data["city_name_en"] == "Siwa Oasis"

    def test_delete_city(self):
        gov = Governorate.objects.create(governorate_name_ar="دمياط", governorate_name_en="Damietta")
        city = City.objects.create(city_name_ar="رأس البر", city_name_en="Ras El Bar", governorate=gov)
        response = self.client.delete(f"/locations/cities/{city.id}/")
        assert response.status_code == 204
        assert not City.objects.filter(id=city.id).exists()
