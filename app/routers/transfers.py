from app.config import jwt_settings
from app.controllers.balance import balance_controller
from app.controllers.users import user_controller
from app.database import get_session
from app.schemas.transactions import Transaction, Transfer
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/transfers",
    tags=["transfers"],
    responses={404: {"description": "Not found"}},
)
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create transfer")
async def transfer_to_user(
    transfer_schema: Transfer,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    user = await user_controller.get_or_404(email=authorize.get_jwt_subject(), session=session)
    recipient = await user_controller.get_or_404(email=transfer_schema.to, session=session)
    await balance_controller.transfer(
        user=user,  # type:ignore
        recipient_id=recipient.guid,
        session=session,
        transaction_schema=Transaction(amount=transfer_schema.amount),
    )
    return {"detail": messages.TRANSFER_SUCCESSFUL}
