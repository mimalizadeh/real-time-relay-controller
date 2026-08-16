from typing import Annotated

from fastapi import APIRouter, Query

from src.schemas.relay_schemas import StatusQuery

router = APIRouter(tags=["Relay"], prefix="/relay")


@router.get("/status")
async def relay_status():
    return {"status": "ok"}


@router.get("/relay/")
async def relay_controller(status_query: Annotated[StatusQuery, Query()]):
    return {"node_id": status_query.node_id, "status": status_query.status}
