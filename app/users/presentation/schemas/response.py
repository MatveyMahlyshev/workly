from pydantic import BaseModel


class SuccessfullResponse(BaseModel):
    message: str = "success"
