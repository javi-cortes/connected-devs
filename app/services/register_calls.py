from typing import List

import sqlalchemy
from loguru import logger
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models import RequestRegister
from app.schemas import (
    ConnectedResult,
    RequestRegisterStorePayload,
)
from app.services.main import AppService, AppCRUD
from app.utils.service_result import ServiceResult


class RegisterCallsService(AppService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.register_call_crud = RegisterCallsCRUD(self.db)

    async def get_historical_calls_of(self, dev1: str, dev2: str) -> ServiceResult:
        return ServiceResult(self.register_call_crud.get_registers(dev1, dev2))

    def register_response(self, result: ConnectedResult, dev1, dev2):
        request_register_payload = RequestRegisterStorePayload(
            dev1=dev1,
            dev2=dev2,
            connected=result.connected,
            organizations=result.organizations,
        )
        self.register_call_crud.register_response(request_register_payload)


class RegisterCallsCRUD(AppCRUD):
    def register_response(self, request_payload: RequestRegisterStorePayload):
        request_register = RequestRegister(**request_payload.dict())
        self.db.add(request_register)
        try:
            self.db.commit()
            self.db.refresh(request_register)
        except sqlalchemy.exc.DatabaseError as error:
            logger.error(f"{error}")
            request_register = None
        return request_register

    def get_registers(self, dev1: str, dev2: str) -> List[RequestRegister]:
        """
        Search for registered calls filtering by a given search criteria
        :return: List[RequestRegister]
        """
        return (
            self.db.query(RequestRegister)
            .filter(
                or_(
                    and_(
                        RequestRegister.dev1 == dev1,
                        RequestRegister.dev2 == dev2,
                    ),
                    and_(
                        RequestRegister.dev1 == dev2,
                        RequestRegister.dev2 == dev1,
                    ),
                )
            )
            .all()
        )
