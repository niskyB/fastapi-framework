from pydantic import BaseModel


class Role(BaseModel):
    customer: str
    subcontractor: str
    technician: str
    internal_employee: str
