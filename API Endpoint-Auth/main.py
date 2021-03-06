import json
from fastapi import FastAPI,HTTPException,Depends,status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


with open("menu.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()

@app.get('/')
def root():
    return{'Menu':'Item'}

@app.get('/menu')
async def read_all_menu():
    return data

@app.get('/menu/{item_id}')
async def read_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.post('/menu')
async def post_menu(name: str):
    id = 1
    if (len(data['menu'])>0):
        id = data['menu'][len(data['menu'])-1]['id']+1
        new_data = {'id':id,'name':name}
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data,write_file,indent=4)
    write_file.close()

    return(new_data)
    raise HTTPException(
        status_code=500, detail=f'Internal Server Error'
    )

@app.put('/menu/{item_id}')
async def read_menu(item_id: int, name:str):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name']=name
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()

            return{"message":"Data updated successfully"}
            
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.delete('/menu/{item_id}')
async def delete_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data['menu'].remove(menu_item)
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()

            return{"message":"Data deleted successfully"}
            
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )