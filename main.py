from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return 'staus_code=HTTP_200_OK' 


"""/post Get Post"""


@app.post('/post', summary= 'Get Post')
def post() -> Timestamp:

    new_id = post_db[-1].id + 1
    new_timestamp = int(datetime.now().timestamp())

    post_db.append(Timestamp(id=new_id, timestamp=new_timestamp))
    return post_db[-1]


'''/dog Get Dogs'''


@app.get('/dog', summary='Get Dogs')
def get_dogs() -> List[Dog]:
    return list(dogs_db.values())


'''/dog Create Dog'''


@app.post('/dog', summary='Create Dog')
def create_dog(name: str, kind: DogType) -> Dog:
        
    pk = max([dog.pk for dog in dogs_db.values()], default=-1) + 1
    key = max(dogs_db.keys(), default=-1) + 1

    new_dog = Dog(name=name, pk=pk, kind=kind)
    dogs_db[key] = new_dog

    return new_dog


'''/dog/{pk} Get Dog By Pk'''


@app.get('/dog/{pk}', summary='Get Dog By Pk')
def get_dog_by_pk(pk: int) -> Dog:
    for dog in dogs_db.values():
        if dog.pk == pk:
            return dog


'''/dog/{pk} Update Dog'''


@app.patch("/dog/{pk}", summary='Update Dog')
def update_dog(pk: int, name: str, kind: DogType) -> Dog:
    dog = dogs_db[pk]
    dog.name = name
    dog.kind = kind
    return dog
