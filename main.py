from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app=FastAPI(title = "FIRST TERM EXAM")

class Login(BaseModel):
    correo:str
    password:str

class UserIN(BaseModel):
    correo:str
    usuario:str
    password:str
    activo: Optional[bool]=True

class UserOUT(BaseModel):
    id:int
    correo:str
    usuario:str
    activo:str
    
posibles_usuarios= [
    {"id":1, "correo":"pablo.17@gmail.com", "usuario":"Pablo", "password":"pAbl03", "activo": True },
    {"id":2, "correo":"kate.rine2@gmail.com", "usuario":"Katerine", "password":"kat2lr2", "activo": True}
]

@app.post("/posibles_usuarios", response_model=UserOUT, status_code=201)
def crearusuario(u:UserIN):
    if any(x["correo"] == u.correo for x in posibles_usuarios):
        raise HTTPException(status_code=400, detail="este correo ya existe")
    nuevo_id = max((x["id"] for x in posibles_usuarios), default=0) + 1
    user = {
        "id": nuevo_id,
        "usuario": u.usuario,
        "correo": u.correo,
        "password": u.password,
        "activo": u.activo
    }
    posibles_usuarios.append(user)

    return {"id": user["id"],"correo":user["correo"],"usuario":user["usuario"],"activo":user["activo"]}

@app.get("/usuarios", response_model=List[UserOUT])
def lista_usuarios():
    return [{"id": x["id"], "correo": x["correo"], "usuario": x["usuario"], "activo": x["activo"]} for x in posibles_usuarios]

@app.get("/usuarios/{user_id}", response_model=UserOUT)
def obtener_usuario(user_id: int):
    u = next((x for x in posibles_usuarios if x["id"] == user_id), None)
    if not u:
        raise HTTPException(status_code=404, detail="no se encontro el usuario")
    return {"id": u["id"], "correo": u["correo"], "usuario": u["usuario"], "activo": u["activo"]}

@app.put("/usuarios/{user_id}", response_model=UserOUT)
def actualizar_usuario(user_id: int, data: UserIN):
    u = next((x for x in posibles_usuarios if x["id"] == user_id), None)
    if not u:
        raise HTTPException(status_code=404, detail="no se encontro el usuario")
    
    if any(x["correo"] == data.correo and x["id"] != user_id for x in posibles_usuarios):
        raise HTTPException(status_code=400, detail="correo ya en uso por otro usuario")
    u["correo"] = data.correo
    u["usuario"] = data.usuario
    u["password"] = data.password
    u["activo"] = data.activo if data.activo is not None else u["activo"]
    return {"id": u["id"], "correo": u["correo"], "usuario": u["usuario"], "activo": u["activo"]}


@app.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int):
    global posibles_usuarios
    if not any(x["id"] == user_id for x in posibles_usuarios):
        raise HTTPException(status_code=404, detail="no se encontro el usuario")
    posibles_usuarios = [x for x in posibles_usuarios if x["id"] != user_id]
    return {"message": "se elimino el usuario"}


@app.post("/login")
def login(payload: Login):
    user = next((x for x in posibles_usuarios if x["correo"] == payload.correo and x["password"] == payload.password), None)
    if user:
        return {"message": "login exitoso"}
    return {"message": "no tiene las credenciales necesario"}