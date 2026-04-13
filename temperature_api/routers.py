from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.models import City
from dependencies import get_db
from temperature_api.crud import create_temperature, get_temperature, update_temperature
from temperature_api.models import Temperature
from temperature_api.schemas import TemperatureCreateResponseSchema, TemperatureCreateSchema, TemperatureUpdateSchema

router = APIRouter()


async def checking_city(data:TemperatureCreateSchema, db: AsyncSession = Depends(get_db)):
    request = await db.execute(select(City).where(City.id == data.city_id))
    city = request.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail=f"City with the ID: {data.city_id} not found")

    return city

@router.post("/temperature", response_model=TemperatureCreateResponseSchema)
async def temperature_create(
        common: Annotated[City, Depends(checking_city)],
        data:TemperatureCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    return await create_temperature(data=data, db=db)


@router.get("/temperatures", response_model=List[TemperatureCreateResponseSchema])
async def get_list_temperatures(db: AsyncSession = Depends(get_db)):
    return await get_temperature(db=db)


@router.get("/temperatures/{city_id}", response_model=TemperatureCreateResponseSchema)
async def get_detail_temperature_by_city_id(city_id: int | None = None, db: AsyncSession = Depends(get_db)):
    request = await db.execute(select(City).where(City.id == city_id))
    city = request.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail=f"City with the ID: {city_id} not found")

    request = await db.execute(select(Temperature).where(Temperature.city_id == city_id))
    temperature = request.scalars().first()

    return temperature


@router.post("/temperatures/update", response_model=TemperatureUpdateSchema)
async def temperature_update(db: AsyncSession = Depends(get_db)):
    await update_temperature(db=db)

    return TemperatureUpdateSchema(message="Updated Successfully!")
