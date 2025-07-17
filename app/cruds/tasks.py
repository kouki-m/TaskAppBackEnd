from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.tasks as tasks_schema

from fastapi import HTTPException
from sqlalchemy.future import select

import app.schemas.tasks as tasks_schemas
from app.models.tasks import Task  # 新規追加


async def add_task(
    db: AsyncSession, task_request: tasks_schema.TaskCreateRequest
) -> tasks_schema.TaskCreateResponse:
    # タスクを追加
    try:
        new_task = Task(**task_request.model_dump())
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return tasks_schema.TaskCreateResponse(
            id=new_task.id, message="Task created successfully."
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_tasks(db: AsyncSession) -> list[tasks_schema.TaskListResponse]:
    # タスク一覧を取得
    stmt = select(Task)
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return [tasks_schema.TaskListResponse(**task.__dict__) for task in tasks]


async def delete_task(db: AsyncSession, id: str) -> tasks_schema.TaskDeleteResponse:
    # タスクを削除
    task = await db.get(Task, id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    await db.delete(task)
    await db.commit()
    return tasks_schema.TaskDeleteResponse(
        id=task.id, message="Task deleted successfully."
    )


async def update_task(
    db: AsyncSession, id: str, task_request: tasks_schema.TaskUpdateRequest
) -> tasks_schema.TaskUpdateResponse:
    # タスクを更新
    task = await db.get(Task, id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    for key, value in task_request.model_dump().items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return tasks_schema.TaskUpdateResponse(
        id=task.id, message="Task updated successfully."
    )
