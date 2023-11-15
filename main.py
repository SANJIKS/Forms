import time
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

client = AsyncIOMotorClient("mongodb://mongo:27017")
db = client["form_templates"]
collection = db["templates"]

def get_field_type(value):
    if any(format in value for format in ['DD.MM.YYYY', 'YYYY-MM-DD']):
        return 'date'
    elif value.startswith('+7') and value[2:].replace(" ", "").isdigit() and len(value) == 16:
        return 'phone'
    elif '@' in value:
        return 'email'
    else:
        return 'text'
    

async def built_data():
    templates = [
        {
            "name": "Order Form",
            "fields": {
                "user_name": "text",
                "order_date": "date",
                "email": "email",
                "phone": "phone"
            }
        },
        {
            "name": "Contact Form",
            "fields": {
                "full_name": "text",
                "email": "email",
                "phone": "phone"
            }
        },
        {
            "name": "Comment Form",
            "fields": {
                "name": "text",
                "email": "email",
                "message": "text"
            }
        }
    ]

    for template in templates:
        await collection.insert_one(template)


@app.on_event("startup")
async def startup_db_client():
    time.sleep(10)
    await client.start_session()
    await built_data()

@app.on_event("shutdown")
async def shutdown_db_client():
    await client.close()

@app.post("/get_form")
async def get_form(request_data: dict):
    form_data = jsonable_encoder(request_data)

    all_templates = await collection.find().to_list(length=None)

    for template in all_templates:
        if set(template['fields'].keys()).issubset(set(form_data.keys())):
            field_types = {}
            for field, value in form_data.items():
                if field in template['fields']:
                    expected_type = template['fields'][field]
                    actual_type = get_field_type(value)
                    if expected_type == actual_type:
                        field_types[field] = expected_type
                    else:
                        break
            else:
                return {"template_name": template['name']}

    field_types = {}
    for field, value in form_data.items():
        actual_type = get_field_type(value)
        field_types[field] = actual_type

    return JSONResponse(field_types)
