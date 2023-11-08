from enum import Enum
from typing import Annotated, List, Union, Any
from uuid import UUID
from datetime import datetime, time, timedelta
from fastapi import FastAPI, Query, Path, Body, Header, status, Form, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    item_id: UUID
    start_datetime: datetime = Field(default_factory=datetime.now)
    end_datetime: datetime = None
    name: str = Field(examples=["Foo"])
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300, examples=["A very nice Item"]
    )
    price: float = Field(gt=0, description="The price must be greater than zero", examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
    tags: set[str] = set()
    images: list[Image] | None = None

fake_items_db = [{"item_name": "Foo", "price": 42}, {"item_name": "Bar", "price": 50}, {"item_name": "Baz", "price": 100, "tax": 10.5}]
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

class Tags(Enum):
    items = "items"
    users = "users"


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/items/")
async def read_items(
        user_agent: Annotated[str | None, Header()] = None,
        q: Annotated[str | None, Query(
            title="Query string", 
            description="Query string for the items to search in the database that have a good match",
            min_length=3, max_length=50
        )] = None
    ):
    results = {"items": fake_items_db}
    if q:
        results.update({"q": q})
    if user_agent:
        results.update({"user_agent": user_agent})
    return results

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: Annotated[int, Path(description="The ID of the user who owns the item", ge=1)],
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1, le=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    short: Annotated[bool, Query(description="Whether to show short or long description")] = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "There goes my error"})
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
    response_description="The created item",
)
async def create_item(item: Item) -> Any:
    """
    Create an item with all the information:
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this attribute
    - **tags**: a set of unique tag strings for this item
    """
    return item

@app.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn) -> Any:
    return user

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.post("/files/")
async def create_file(file: Annotated[Union[bytes, None], File(description="A file read as bytes")] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")] = None,
):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    json_compatible_item_data = jsonable_encoder(item)
    update_item_encoded = jsonable_encoder({"item_id": item_id, **json_compatible_item_data})
    return update_item_encoded


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item