import uvicorn
import pyrebase
from fastapi import FastAPI
from models import LoginSchema, SignUpSchema, Todos
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request


app = FastAPI(
    description="FastAPI with Firebase authentication",
    title="Firebase authentication",
    docs_url="/",
)


import firebase_admin
from firebase_admin import credentials, auth, firestore


if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)


firebaseConfig = {
    "apiKey": "AIzaSyBhKLNOMXGdLpxzn4qGrtujrKT55dvKW3w",
    "authDomain": "fastapiauth-65d66.firebaseapp.com",
    "projectId": "fastapiauth-65d66",
    "storageBucket": "fastapiauth-65d66.appspot.com",
    "messagingSenderId": "327385738252",
    "appId": "1:327385738252:web:3788fa610d01e4d09f1229",
    "measurementId": "G-DQ3JJRBWGC",
    "databaseURL": "https://FastapiAuth.firebaseio.com",
}


firebase = pyrebase.initialize_app(firebaseConfig)
db = firestore.client()
todo_ref = db.collection('todos')


@app.post("/signup")
async def create_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        auth.create_user(email=email, password=password)

        return JSONResponse(
            content={
                "message": f"User account created successfully for user"
            },
            status_code=201,
        )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400, detail=f"Account already created for the email {email}"
        )


@app.post("/login")
async def create_access_token(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email, password=password
        )

        token = user["idToken"]

        return JSONResponse(content={"token": token}, status_code=200)
    except:
        raise HTTPException(status_code=400, detail="Invalid Credentials")


@app.post("/ping")
async def validate_token(request: Request):
    headers = request.headers
    jwt = headers.get("authorization")

    user = auth.verify_id_token(jwt)

    return user["user_id"]


@app.get('/todos/')
async def get_todos():
    todo = todo_ref.get()
    all_todos = [doc.to_dict() for doc in todo]
    return JSONResponse(all_todos)


@app.post('/todos/')
async def create_todo(todo:Todos):
    todo = todo.__dict__
    db.collection('todos').add(todo)
    return JSONResponse(todo)


@app.get('/todos/{todo_id}')
async def get_todo_by_id(todo_id):
    todo = todo_ref.document(todo_id).get()
    return JSONResponse(todo.to_dict())


@app.put('/todos/{todo_id}')
async def update_todo(todo_id, todo: Todos):
    todo_ref.document(todo_id).update(todo.__dict__)
    return JSONResponse({"message": f"Todo {todo_id} updated"})


@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id):
    todo_ref.document(todo_id).delete()
    return JSONResponse({"message": f"Todo {todo_id} removed"})


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
