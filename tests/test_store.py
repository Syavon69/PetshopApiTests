import allure
import jsonschema
import pytest
import requests

from tests.schemas.order_schema import ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Попытка создания заказа")
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
            assert response.json["petId"] == payload["petId"], "id питомца не совпал с ожидаемым"
            assert response.json["quantity"] == payload["quantity"], "Количество не совпало с ожидаемым"
            assert response.json["status"] == payload["status"], "Статус заказа не совпал с ожидаемым"
            assert response.json["complete"] == payload["complete"], "Выполнение заказа не соответствует ожидаемому"

    @allure.title("Попытка просмотра заказа")
    def test_check_order(self, create_order):
        with allure.step("Подготовка данных заказа"):
            order_id = create_order["id"]
            order_quantity = create_order["quantity"]
            order_status = create_order["status"]
            order_complete = create_order["complete"]
            order_petId = create_order["petId"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == order_id, "id заказа не совпал с ожидаемым"
            assert response.json()["quantity"] == order_quantity, "Количество заказа не соответствует ожидаемому"
            assert response.json()["status"] == order_status, "Статус заказа не соответствует ожидаемому"
            assert response.json()["complete"] == order_complete, "Выполнение заказа не соответствует ожидаемому"
            assert response.json()["petId"] == order_petId, "id питомца не соответствует ожидаемому"

    @allure.title("Попытка удаления заказа")
    def test_delete_order(self, create_order):
        with allure.step("Подготовка данных заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса и текста ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка результата удаления заказа по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ответа не совпал с ожидаемым"

    @allure.title("Попытка просмотра несуществующего заказа")
    def test_get_info_nonexistent_order(self):
        with allure.step("Отправка запроса на просмотр несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка просмотра инвентаря магазина")
    def test_get_info_inventory(self):
        with allure.step("Отправка запроса на просмотр инвентаря"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.json()["approved"] == 57, "Количество не совпало с ожидаемым"
            assert response.json()["delivered"] == 50, "Количество не совпало с ожидаемым"