from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Database import MyDatabase
from typing import Optional

app = FastAPI()
db = MyDatabase()


class Pereval(BaseModel):
    user_email: str
    beauty_title: Optional[str]
    title: Optional[str]
    other_titles: Optional[str]
    level_summer: Optional[int]
    level_autumn: Optional[int]
    level_winter: Optional[int]
    level_spring: Optional[int]
    connect: Optional[str]
    add_time: Optional[str]
    coord_id: Optional[int]

@app.post('/submitData')
async def submit_data(pereval: Pereval):
    try:
        data = pereval.dict()
        db.add_pereval(data)
        response = {
            'status': 'success',
            'message': 'Информация о превале успешно добавлена!',
            'data': data,
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/submitData/{id}")
async def get_pereval(id: int):
    pereval = db.get_pereval_by_id(id)
    if pereval is None:
        return {"Ошибка": f"Превелов с id [ {id} ] - не наййдено"}
    return pereval


@app.get("/submitData/")
async def get_user_perevals(user_email: str):
    user_perevals = db.get_user_perevals(user_email)
    if not user_perevals:
        raise HTTPException(status_code=404, detail="Пользователь не публиковал данных о перевалах")
    return user_perevals