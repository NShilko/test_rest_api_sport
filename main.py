from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Database import MyDatabase

app = FastAPI()
db = MyDatabase()


class Pereval(BaseModel):
    user_email: str
    beauty_title: str
    title: str
    other_titles: str
    level_summer: int
    level_autumn: int
    level_winter: int
    level_spring: int
    connect: str
    add_time: str
    coord_id: int

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
