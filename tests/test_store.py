import allure
import jsonschema
import pytest
import requests

from tests.schemas.order_schema import ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Попытка создания заказа"):
    def test_create_order(self):
        with allure.step("Подготовка данных для создания заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response.json["id"] == payload["id"], "id заказа не совпал с ожидаемым"
            assert response.json["petId"] == payload["peyId"], "id питомца не совпал с ожидаемым"
            assert response.json["quantity"] == payload["quantity"], "Количество не совпало с ожидаемым"
            assert response.json["status"] == payload["status"], "Статус заказа не совпал с ожидаемым"
            assert response.json["complete"] == payload["complete"], "Выполнение заказа не соответствует ожидаемому"