import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from models.sticker import Sticker
from models.user import User
from schemas.sticker import StickerOut, StickerRegister
from services.user_service import UserService


logger = logging.getLogger(__name__)

class StickerService:
    @staticmethod
    async def get_all_stickers(db):
        stmt = (
            select(Sticker, User.user_name)
            .join(User, Sticker.user_id == User.user_id)
        )
        result = await db.execute(stmt)
        rows = result.all()
        
        return [
            StickerOut.model_validate({
                **dict(sticker.__dict__),
                "userName": user_name
            }, from_attributes=False)
            for sticker, user_name in rows
        ]


    @staticmethod
    async def sticker_exists(db: AsyncSession, sticker_id: int, option_flag: int) -> bool:
        stmt = select(Sticker).where(
            Sticker.sticker_id == sticker_id,
            Sticker.sticker_option_flag == option_flag
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None
    

    @staticmethod
    async def url_exists(db: AsyncSession, sticker_id: int, url: str) -> bool:
        stmt = select(Sticker).where(
            Sticker.sticker_id == sticker_id,   
            Sticker.url == url
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None
    

    @staticmethod
    async def get_sticker_url(db: AsyncSession, sticker_id: int, option_flag: int) -> str | None:
        stmt = select(Sticker.url).where(
            Sticker.sticker_id == sticker_id,
            Sticker.sticker_option_flag == option_flag
        )

        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    

    @staticmethod
    async def register_sticker(db: AsyncSession, dto: StickerRegister) -> bool:
        try:
            # 중복 체크
            exists = await StickerService.sticker_exists(
                db, dto.sticker_id, dto.sticker_option_flag
            )
            if exists:
                return False
                        
            await UserService.update_user(db, dto.user_id, dto.user_name, dto.registed_date_time, skip_commit=True)
            
            # DTO -> ORM 모델 변환
            sticker = Sticker(
                sticker_id=dto.sticker_id,
                sticker_option_flag=dto.sticker_option_flag,
                sticker_title=dto.sticker_title,
                registed_date_time=dto.registed_date_time,
                url=dto.url,
                user_id=dto.user_id,                
            )

            db.add(sticker)
            await db.commit()            

            return True
        
        except Exception as e:
            await db.rollback()
            logger.error(f"스티커 등록 중 예외 발생: {e}")
            return False
        

    @staticmethod
    async def delete_sticker(db: AsyncSession, sticker_id: int, option_flag: int) -> bool:
        try:
            stmt = delete(Sticker).where(
                Sticker.sticker_id == sticker_id,
                Sticker.sticker_option_flag == option_flag
            )
            result = await db.execute(stmt)

            if result.rowcount == 0:
                return False

            await db.commit()
            return True
        
        except Exception as e:
            await db.rollback()
            logger.error(f"스티커 삭제 중 예외 발생: {e}")
            return False