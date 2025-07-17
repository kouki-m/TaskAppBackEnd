import os
from typing import Annotated, List
import uuid
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

# from app.cruds.auth import verify_token
import app.cruds.tasks as tasks_cruds
import app.schemas.tasks as tasks_schemas

# .envファイルを読み込む
load_dotenv()
# router = APIRouter(dependencies=[Depends(verify_token)])
router = APIRouter()


# タスク追加API
@router.post("/api/task", response_model=tasks_schemas.TaskCreateResponse)
async def add_task(
    task_request: tasks_schemas.TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    response = await tasks_cruds.add_task(db, task_request)
    return response


@router.get("/api/tasks", response_model=List[tasks_schemas.TaskListResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await tasks_cruds.get_tasks(db)
    return tasks


@router.delete("/api/task/delete/{id}", response_model=tasks_schemas.TaskDeleteResponse)
async def delete_task(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    response = await tasks_cruds.delete_task(db, id)
    return response


@router.put("/api/task/update/{id}", response_model=tasks_schemas.TaskUpdateResponse)
async def update_task(
    id: uuid.UUID,
    task_request: tasks_schemas.TaskUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    response = await tasks_cruds.update_task(db, id, task_request)
    return response
