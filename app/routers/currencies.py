from app.controllers.currencies import currency_controller
from app.database import get_session
from app.schemas.currencies import TimeParams
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


@router.get(
    "/prices/{currency_name}",
    status_code=status.HTTP_200_OK,
    summary="Get price history for currency",
)
async def get_currency_current_price(
    currency_name: str,
    params: TimeParams = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await currency_controller.get_price_history(name=currency_name, session=session, **params.dict())


@router.get("/prices/all", status_code=status.HTTP_200_OK, summary="Get all current prices")
async def get_all_current_prices(session: AsyncSession = Depends(get_session)):
    return await currency_controller.get_current_prices_for_all(session=session)
