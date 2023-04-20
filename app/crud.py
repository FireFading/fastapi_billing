from collections.abc import Iterable

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUD:
    async def create(self, session: AsyncSession):
        session.add(self)
        await session.flush()
        await session.commit()
        return self

    @classmethod
    async def get_filters(cls, kwargs: dict):
        filters = []
        for field, value in kwargs.items():
            try:
                if field.endswith("__gt"):
                    model_field = getattr(cls, field[:-4])
                    filters.append(model_field > value)
                elif field.endswith("__gte"):
                    model_field = getattr(cls, field[:-5])
                    filters.append(model_field >= value)
                elif field.endswith("__lt"):
                    model_field = getattr(cls, field[:-4])
                    filters.append(model_field < value)
                elif field.endswith("__lte"):
                    model_field = getattr(cls, field[:-5])
                    filters.append(model_field <= value)
                else:
                    model_field = getattr(cls, field)
                    filters.append(model_field == value)
            except AttributeError:
                return None
        return filters

    @classmethod
    async def get_order_by(cls, order_by: str | None = None):
        if order_by:
            if order_by[0] == "-":
                order_by_field = getattr(cls, order_by[1:]).desc()
            else:
                order_by_field = getattr(cls, order_by)
            return order_by_field

    @classmethod
    async def search(cls, session: AsyncSession, kwargs: dict, order_by: str | None = None):
        query = select(cls)
        if filters := await cls.get_filters(kwargs=kwargs):
            query = query.filter(and_(*filters))
        if order_by_field := await cls.get_order_by(order_by=order_by):
            query = query.order_by(order_by_field)
        return await session.execute(query)

    @classmethod
    async def get(cls, session: AsyncSession, **kwargs):
        if result := await cls.search(session=session, kwargs=kwargs):
            return result.scalars().first()

    async def get_or_create(self, session: AsyncSession):
        cls = type(self)
        self_dict = {field: value for field, value in self.__dict__.items() if field != "_sa_instance_state"}
        instance = await cls.get(session=session, **self_dict)
        return instance or await self.create(session=session)

    @classmethod
    async def all(cls, session: AsyncSession):
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def filter(cls, session: AsyncSession, order_by: str | None = None, **kwargs):
        if result := await cls.search(session=session, order_by=order_by, kwargs=kwargs):
            return result.scalars().all()

    async def update(self, session: AsyncSession):
        await session.merge(self)
        await session.commit()

    @classmethod
    async def delete(cls, instances: list | object, session: AsyncSession):
        if isinstance(instances, Iterable):
            for instance in instances:
                await session.delete(instance)
        else:
            await session.delete(instances)
        await session.commit()
