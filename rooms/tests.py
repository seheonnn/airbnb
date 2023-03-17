from rest_framework.test import APITestCase
from . import models
from users.models import User

class TestAmenities(APITestCase):
    # def test_two_plus_two(self):
    #     self.assertEqual(2+2, 5, "The math is wrong.")
    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self): # 실행할 때마다 test DB가 새로 만들어짐
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_all_amenities(self):
        # API test
        response = self.client.get(self.URL)

        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC)

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."

        response = self.client.post(self.URL, data={"name":new_amenity_name, "description":new_amenity_description})
        data = response.json()

        self.assertEqual(response.status_code, 200, "Not 200 status code")
        self.assertEqual(data["name"], new_amenity_name)
        self.assertEqual(data["description"], new_amenity_description)
        # 예외처리 test
        response = self.client.post(self.URL)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

class TestAmenity(APITestCase):
    NAME = "Test Amenity"
    DESC = "Test Dsc"
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):

        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESC)

    def test_put_amenity(self):
        update_name = "New Amenity"
        update_description = "New Amenity desc."
        response = self.client.put("/api/v1/rooms/amenities/1", data={"name": update_name, "description":update_description})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], update_name)
        self.assertEqual(data["description"], update_description)

        name_validate = 'a' * 200
        name_validate_response = self.client.put("/api/v1/rooms/amenities/1", data={"name": name_validate})
        data = name_validate_response.json()
        print(data)
        self.assertEqual(name_validate_response.status_code, 400)
    # post test
    # create amenity와 비슷
    # serializer가 유효한 경우, 유효하지 않은 경우
    # put 부분은 필수 데이터 없음. but, 조건이 맞지 않는 경우 test

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    # get 부분은 인증 없이 가능
    # post 부분은 로그인 필요
    def setUp(self): # join
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user = user
    def test_create_room(self):
        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403)

        # login
        # self.client.login(username="test", password="123")
        self.client.force_login(self.user)

        response = self.client.post("/api/v1/rooms/")
        print(response.json())


