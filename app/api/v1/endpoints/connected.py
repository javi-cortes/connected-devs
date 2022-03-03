from typing import List

from fastapi import APIRouter, Depends, BackgroundTasks

from app import schemas
from app.api.deps import get_db
from app.services.connected import ConnectedService
from app.services.register_calls import RegisterCallsService
from app.utils.service_result import handle_result

router = APIRouter()


@router.post(
    "/{dev1}/{dev2}",
    response_model=schemas.ConnectedResult,
    response_model_exclude_defaults=True,
)
async def connected(
    dev1: str, dev2: str, background_tasks: BackgroundTasks, db: get_db = Depends()
):
    """
    Checks whether two “developers” are fully check_connection_between
        ● They follow each other on Twitter.
        ● They have at least a Github organization in common.
    """
    result = await ConnectedService(db).check_connection_between(dev1, dev2)

    background_tasks.add_task(
        RegisterCallsService(db).register_response, result.value, dev1, dev2
    )

    return handle_result(result)


@router.post(
    "/registered/{dev1}/{dev2}",
    response_model=List[schemas.RequestRegisterResponse],
    response_model_exclude_defaults=True,
)
async def registered_calls(dev1: str, dev2: str, db: get_db = Depends()):
    """
    Check historical all the related information from previous requests to /check_connection_between
    endpoint.
    """
    result = await RegisterCallsService(db).get_historical_calls_of(dev1, dev2)
    return handle_result(result)
