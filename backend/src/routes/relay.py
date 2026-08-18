from typing import Annotated

from fastapi import APIRouter, Query, Depends

from src.services.relay_control_service import get_relay_control_service, RelayControlService
from src.schemas.relay_schemas import StatusQuery

router = APIRouter(tags=["Relay"], prefix="/relay")


@router.get("/status")
async def relay_status():
    return {"status": "ok"}


@router.get("/relay/")
async def relay_controller(status_query: Annotated[StatusQuery, Query()],
                           relay_control_service: RelayControlService = Depends(get_relay_control_service)):
    await relay_control_service.request_relay_change_state(status_query.device_id, status_query.relay_id,status_query.state)
    return {"device_id": status_query.device_id,"relay_id": status_query.relay_id, "status": status_query.state}
