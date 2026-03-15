ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "shipDate": {
            "type": "string"
        },
        "status": {
            "type": "string",
            "enum": ["approved", "placed", "delivered"]
        },
        "complete": {
            "type": "boolean"
        }
    },
    "required": ["id", "petId", "quantity", "status"],
    "additionalProperties": False
}