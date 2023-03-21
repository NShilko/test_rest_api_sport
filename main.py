from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.Models import Pereval
from src.Database import MyDatabase


app = FastAPI(
    title="Test REST API for sports data",
    description="Project assignment for implementing a REST API for working with data from a sports application",
    version="0.1.0",
)
db = MyDatabase()

origins = ["*"]  # Which doments will allow to connect

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add pereval
@app.post('/submitData')
async def submit_data(pereval: Pereval) -> dict:
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
        raise HTTPException(status_code=404, detail=str(e))


# Get Pereval info by pereval_id
@app.get("/submitData/{id}")
async def get_pereval(id: int) -> dict:
    pereval = db.get_pereval_by_id(id)
    if pereval is None:
        return {"state": 0, 'message': f"Превелов с id [ {id} ] - не найдено"}
    return pereval


# Get All Perevals by User_email
@app.get("/submitData/")
async def get_user_perevals(user_email: str):
    user_perevals = db.get_user_perevals(user_email)
    if not user_perevals:
        raise HTTPException(status_code=404, detail="Пользователь не публиковал данных о перевалах")
    return user_perevals


# Update Pereval by pereval_id
@app.patch("/submitData/{id}")
async def update_pereval(id: int, data: dict) -> dict:
    # check that pereval with this id exists
    pereval = db.get_pereval_by_id(id)
    if not pereval:
        return {"state": 0, "message": f"Перевал с id [ {id} ] - не найден"}

    # check that post is not new
    elif pereval['status'] != "new":
        return {"state": 0, "message": "Данная запись уже прошла модерацию, ее нельзя изменить"}

    # check bad fields
    elif "user_email" in data or "first_name" in data or "last_name" in data or "phone_number" in data:
        return {"state": 0, "message": "Невозможно редактировать поля с ФИО, адресом почты и номером телефона"}


    # if is everything good, update pereval
    else:
        success = db.update_pereval(id, data)
        if not success:
            return {"state": 0, "message": "Не удалось обновить запись"}

    return {"state": 1, "message": "Запись успешно отредактирована"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)