import allure
import jsonschema
import pytest
import requests

from tests.schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка просмотреть несуществующего питомца")
    def test_get_info_nonexistent_pet(self):
        with allure.step("Отправка запроса на просмотр несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка добавить нового питомца")
    def test_add_new_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json["id"] == payload["id"], "id питомца не совпал с ожидаемым"
            assert response.json["name"] == payload["name"], "имя питомца не совпало с ожидаемым"
            assert response.json["status"] == payload["status"], "статус питомца не совпал с ожидаемым"

    @allure.title("Попытка добавить нового питомца с полными данными")
    def test_add_new_full_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json["id"] == payload["id"], "id питомца не совпал с ожидаемым"
            assert response.json["name"] == payload["name"], "имя питомца не совпало с ожидаемым"
            assert response.json["category"] == payload["category"], "категория питомца не совпала с ожидаемой"
            assert response.json["photoUrls"] == payload["photoUrls"], "фото питомца не совпало с ожидаемым"
            assert response.json["tags"] == payload["tags"], "тэги питомца не совпали с ожидаемыми"
            assert response.json["status"] == payload["status"], "статус питомца не совпал с ожидаемым"

    @allure.title("Попытка получения информации о питомце по ID")
    def test_pet_by_id(self, create_pet):
        with allure.step("Подготовка ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id, "id питомца не совпал с ожидаемым"

    @allure.title("Попытка получения списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200)
        ]
    )
    def test_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), list)

    @allure.title("Попытка получения списка питомцев по неверному статусу")
    @pytest.mark.parametrize(
        "incorrect_status, expected_status_code",
        [
            ("", 400),
            ("created", 400)
        ]
    )
    def test_pets_by_incorrect_status(self, incorrect_status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по неверному статусу {incorrect_status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": incorrect_status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), dict)

    @allure.title("Попытка обновления информации о питомце")
    def test_update_pet(self, create_pet):
        with allure.step("Подготовка ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление информации о питомце"):
            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа и новых данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id, "id питомца не совпал с ожидаемым"
            assert response.json()["name"] == payload["name"], "имя питомца не совпало с ожидаемым"
            assert response.json()["status"] == payload["status"], "статус питомца не совпал с ожидаемым"

    @allure.title("Попытка удаления питомца")
    def test_delete_pet(self, create_pet):
        with allure.step("Подготовка ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на просмотр удаленного питомца"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
