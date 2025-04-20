import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Path, Query, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.sticker import StickerOut, StickerRegister
from services.sticker_service import StickerService


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/stickers", tags=["Stickers"])

@router.get("/", response_model=List[StickerOut])
async def get_all_stickers(
    db: AsyncSession = Depends(get_db)
):
    logger.info("GET /stickers - 전체 스티커 목록 요청")
    return await StickerService.get_all_stickers(db)


@router.get("/{id}/{flag}/exists")
async def sticker_exists(
    id: int = Path(..., description="스티커 ID"),
    flag: int = Path(..., description="옵션 플래그"),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"GET /stickers/{id}/{flag} - 스티커 존재 여부 확인")
    exists = await StickerService.sticker_exists(db, id, flag)
    return {"exists": exists}


@router.get("/{id}/checkurl")
async def check_url_exists(
    id: int = Path(..., description="스티커 ID"),
    url: str = Query(..., description="중복 체크할 URL"),
    db: AsyncSession = Depends(get_db)
):
    
    exists = await StickerService.url_exists(db, id, url)
    return {"exists": exists}


@router.get("/{id}/{flag}/url")
async def get_sticker_url(
    id: int = Path(..., description="스티커 ID"),
    flag: int = Path(..., description="옵션 플래그"),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"GET /stickers/{id}/{flag}/url - 스티커 URL 요청")

    url = await StickerService.get_sticker_url(db, id, flag)
    if url is None:
        logger.warning(f"스티커 URL 없음: id={id}, flag={flag}")
        raise HTTPException(status_code=404, detail="Sticker not found")
    return {"url": url}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_sticker(
    dto: StickerRegister = Body(..., description="등록할 스티커 정보"),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"POST /stickers - 스티커 등록 요청: id={dto.sticker_id}")

    success = await StickerService.register_sticker(db, dto)
    if not success:
        logger.warning(f"스티커 등록 실패: {dto.sticker_id}")
        raise HTTPException(status_code=400, detail="Sticker registration failed")
    
    logger.info(f"스티커 등록 성공: {dto.sticker_id}")
    return {"registered": success}


@router.delete("/{id}/{flag}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sticker(
    id: int = Path(..., description="스티커 ID"),
    flag: int = Path(..., description="옵션 플래그"),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"DELETE /stickers/{id}/{flag} - 스티커 삭제 요청")

    deleted = await StickerService.delete_sticker(db, id, flag)
    if not deleted:
        logger.warning(f"스티커 삭제 실패: id={id}, flag={flag}")
        raise HTTPException(status_code=404, detail="Sticker not found")
    
    logger.info(f"스티커 삭제 성공: id={id}, flag={flag}")