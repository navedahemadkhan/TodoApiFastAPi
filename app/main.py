from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.middleware import dependency,auth
from .model import models, database
from .validation.schema import TodoCreate, TodoUpdate, Todo,create_user,user_login
from datetime import timedelta
app = FastAPI()

# async def get_db():
#     async with database.SessionLocal() as session:
#         yield session

@app.post("/singup")
async def singup(user:create_user,db: AsyncSession=Depends(dependency.get_db)):
    try:
        user_in_db = await dependency.get_user(db, user.username)
        if user_in_db:
            raise HTTPException(status_code=400,detail="User Already Exixt")
        
        hash_password = auth.get_password_hash(user.password)
        data = models.User(
            username = user.username,
            email = user.email,
            hashpassword = hash_password 
            )
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return data
    except Exception as ex:
        raise HTTPException(status_code=501, detail=str(ex))

@app.post("/login")
async def login(login: user_login, db: AsyncSession=Depends(dependency.get_db)):
    user = await dependency.get_user(db,login.username)
    if not user or not auth.verify_password(login.password, user.hashpassword):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/todos/", response_model=Todo)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(dependency.get_db)):
    # Decode the token and extract the user
    # current_user = dependency.get_current_user(token)

    db_todo = models.Todo(
        title=todo.title, 
        description=todo.description,
        completed=todo.completed,
        owner_id=todo.owner_id 
    )
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[Todo])
async def read_todos(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(dependency.get_db)):
    query = select(models.Todo).offset(skip).limit(limit)
    result = await db.execute(query)
    todos = result.scalars().all()
    return todos

@app.get("/todos/{id}", response_model=Todo)
async def read_todo(id: int, db: AsyncSession = Depends(dependency.get_db)):
    query = select(models.Todo).filter(models.Todo.id == id)
    result = await db.execute(query)
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{id}", response_model=Todo)
async def update_todo(id: int, todo: TodoUpdate, db: AsyncSession = Depends(dependency.get_db)):
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
async def delete_todo(id: int, db: AsyncSession = Depends(dependency.get_db)):
    query = select(models.Todo).filter(models.Todo.id == id)
    result = await db.execute(query)
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(db_todo)
    await db.commit()
    return db_todo
