import os
from typing import Annotated, List
import uuid
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.cruds.auth import verify_token

# .envファイルを読み込む
load_dotenv()
router = APIRouter(dependencies=[Depends(verify_token)])

# タスク追加API
@router.post("/api/tasks", response_model=List[Annotated[uuid.UUID, "Task ID"]])
