from datetime import datetime

from pydantic import BaseModel


class TemperatureBaseSchema(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreateSchema(TemperatureBaseSchema):
    city_id: int


class TemperatureCreateResponseSchema(TemperatureCreateSchema):
    id: int
