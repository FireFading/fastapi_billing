from app.controllers.currencies import currency_controller
from app.database import get_session
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, summary="Get currencies")
async def get_currencies(
    session: AsyncSession = Depends(get_session),
):
    return await currency_controller.get_all_available(session=session)
