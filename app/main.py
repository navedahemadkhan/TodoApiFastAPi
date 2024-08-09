from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .model import models, database
from .validation.schema import TodoCreate, TodoUpdate, Todo

app = FastAPI()

async def get_db():
    async with database.SessionLocal() as session:
        yield session

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    db_todo = models.Todo(
        title=todo.title, 
        description=todo.description,
        completed=todo.completed,
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[Todo])
async def read_todos(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    query = select(models.Todo).offset(skip).limit(limit)
    result = await db.execute(query)
    todos = result.scalars().all()
    return todos

@app.get("/todos/{id}", response_model=Todo)
async def read_todo(id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Todo).filter(models.Todo.id == id)
    result = await db.execute(query)
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{id}", response_model=Todo)
async def update_todo(id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    query = select(models.Todo).filter(models.Todo.id == id)
    result = await db.execute(query)
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo.title is not None:
        db_todo.title = todo.title
    if todo.description is not None:
        db_todo.description = todo.description
    if todo.completed is not None:
        db_todo.completed = todo.completed
    
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{id}", response_model=Todo)
async def delete_todo(id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Todo).filter(models.Todo.id == id)
    result = await db.execute(query)
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(db_todo)
    await db.commit()
    return db_todo
