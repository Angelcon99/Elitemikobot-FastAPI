import logging
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.user import UserBlockRegister
from services.user_service import UserService


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])

@router.patch("/block", status_code=status.HTTP_204_NO_CONTENT)
async def update_block_user(
    dto: UserBlockRegister = Body(..., description="유저 정보"),
    db: AsyncSession = Depends(get_db)
):
    action = "차단" if dto.is_block else "차단 해제"
    logger.info(f"PATCH /users/block - 유저 {action} 요청: user_id={dto.user_id}")

    success = await UserService.update_block_status(db, dto)
    if not success:
        logger.warning(f"유저 {action} 실패: 존재하지 않는 유저 user_id={dto.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"유저 {action} 처리 완료: user_id={dto.user_id}")