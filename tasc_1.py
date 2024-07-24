# Создать API для управления списком задач. Приложение должно иметь
# возможность создавать, обновлять, удалять и получать список задач.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Task с полями id, title, description и status.
# Создайте список tasks для хранения задач.
# Создайте маршрут для получения списка задач (метод GET).
# Создайте маршрут для создания новой задачи (метод POST).
# Создайте маршрут для обновления задачи (метод PUT).
# Создайте маршрут для удаления задачи (метод DELETE).
# Реализуйте валидацию данных запроса и ответа.


from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Optional, List
from pydantic import BaseModel
app = FastAPI()


class Task_in(BaseModel):
    title:str
    description : Optional[str] = None 
    status:str
    
class Task(Task_in):
    id:int 

tasks_coll = []


@app.get("/tasks/", response_model=List[Task])
async def root():
    return tasks_coll

@app.get("/tasks/{id}", response_model=Task)
async def task(id:int):
    for tas in tasks_coll:
        if tas.id == id:
            return tas
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks/", response_model=Task)
async def create_tasks(task:Task_in):
    tas = Task(id=len(tasks_coll) + 1, **task.dict())
    tasks_coll.append(tas)
    return tas

@app.put("/tasks/{id}", response_model=Task)
async def update_tasks(id:int, task:Task_in):
    for tas in tasks_coll:
        if tas.id == id:
            tas.title = task.title
            tas.description = task.description
            tas.status = task.status
            return tas
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
async def delete_tasks(id:int):
    for tas in tasks_coll:
        if tas.id == id:
            tasks_coll.remove(tas)
            return {'message':f'task of id={id} is removed'}



if __name__=="__main__":
    uvicorn.run("tasc_1:app", host="127.0.0.1", port=8000, reload=True)
