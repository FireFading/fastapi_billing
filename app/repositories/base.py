from collections.abc import Iterable
from typing import Type, TypeVar

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

TypeModel = TypeVar("TypeModel")


class BaseRepository:
    def __init__(self, model: Type[TypeModel]):
        self.model = model

    async def create(self, instance: TypeModel, session: AsyncSession) -> TypeModel:
        session.add(instance)
        await session.flush()
        await session.commit()
        return instance

    async def bulk_create(self, instances: Iterable[TypeModel], session: AsyncSession) -> Iterable[TypeModel]:
        session.add_all(instances)
        await session.flush()
        await session.commit()
        return instances

    def set_filters(self, query, kwargs: dict[str, str]):
        filters = []
        for field, value in kwargs.items():
            if value:
                try:
                    if field.endswith("__gt"):
                        model_field = getattr(self.model, field[:-4])
                        filters.append(model_field > value)
                    elif field.endswith("__gte"):
                        model_field = getattr(self.model, field[:-5])
                        filters.append(model_field >= value)
                    elif field.endswith("__lt"):
                        model_field = getattr(self.model, field[:-4])
                        filters.append(model_field < value)
                    elif field.endswith("__lte"):
                        model_field = getattr(self.model, field[:-5])
                        filters.append(model_field <= value)
                    else:
                        model_field = getattr(self.model, field)
                        filters.append(model_field == value)
                except AttributeError:
                    return None
        query = query.filter(and_(*filters))
        return query

    def set_order_by(self, query, order_by: str):
        if order_by[0] == "-":
            order_by_field = getattr(self.model, order_by[1:]).desc()
        else:
            order_by_field = getattr(self.model, order_by)
        query = query.order_by(order_by_field)
        return query

    async def get(self, session: AsyncSession, **kwargs) -> TypeModel | None:
        query = select(self.model)
        if kwargs:
            query = self.set_filters(query=query, kwargs=kwargs)
        if result := await session.execute(query):
            return result.scalars().first()
        return None

    async def get_or_create(self, instance: TypeModel, session: AsyncSession) -> TypeModel:
        instance_dict = {field: value for field, value in instance.__dict__.items() if field != "_sa_instance_state"}
        if got_instance := await self.get(**instance_dict, session=session):  # type: ignore
            return got_instance
        return await self.create(instance=instance, session=session)

    async def all(self, session: AsyncSession) -> Iterable[TypeModel] | None:
        query = select(self.model)
        if result := await session.execute(query):
            return result.scalars().all()
        return None

    async def filter(self, session: AsyncSession, order_by: str | None = None, **kwargs) -> Iterable[TypeModel] | None:
        query = select(self.model)
        if kwargs:
            query = self.set_filters(query=query, kwargs=kwargs)
        if order_by:
            query = self.set_order_by(query=query, order_by=order_by)
        if result := await session.execute(query):
            return result.scalars().all()
        return None

    async def update(self, instance: TypeModel, session: AsyncSession) -> TypeModel:
        await session.merge(instance)
        await session.commit()
        return instance

    async def bulk_update(self, instances: Iterable[TypeModel], session: AsyncSession) -> Iterable[TypeModel]:
        for instance in instances:
            await session.merge(instance)
        await session.commit()
        return instances

    async def delete(self, instance, session: AsyncSession) -> None:
        await session.delete(instance)
        await session.commit()

    async def bulk_delete(self, instances: Iterable[TypeModel], session: AsyncSession) -> None:
        for instance in instances:
            await session.delete(instance)
        await session.commit()
