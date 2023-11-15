import pytest
import httpx
import json

from main import app

@pytest.mark.asyncio
async def test_successful_request_contact_form():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        data = {"full_name": "alwndandian dans iljani dnwa",
                "email": "sanajn@mail.com",
                "phone": "+7 121 321 32 92"}
        json_data = json.dumps(data)
        response = await client.post("/get_form", data=json_data, headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        assert response.json()["template_name"] == "Contact Form"
