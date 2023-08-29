from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email:str
    password:str

    class Config:
        json_schema_extra ={
            "example":{
                "email":"example@example.com",
                "password":"password123"
            }
        }


class LoginSchema(BaseModel):
    email:str
    password:str

    class Config:
        json_schema_extra ={
            "example":{
                "email":"example@example.com",
                "password":"password123"
            }
        }


class Todos(BaseModel):
    title:str
    is_done:bool
