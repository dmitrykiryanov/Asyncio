import aiohttp
import asyncio
from pprint import pprint
from more_itertools import chunked

from sqlalchemy import  Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import config

URL = 'https://swapi.dev/api/people/'

MAX = 83
PARTITION = 10


async def get_people(people_id, session):
    async with session.get(f'{URL}{people_id}') as response:
        return await response.json()


async def get_person(all_ids, partition, session):
    for chunk_ids in chunked(all_ids, partition):
        tasks = [asyncio.create_task(get_people(people_id, session)) for people_id in chunk_ids]
        for task in tasks:
            task_result = await task
            yield task_result


async def main():
    async with aiohttp.ClientSession() as session:
        person_data = []
        async for person in get_person(range(1, MAX + 1), PARTITION, session):
            person_data.append(person)
        return person_data


# heroes = asyncio.run(main())


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
heroes = loop.run_until_complete(main())
#     pprint(heroes)


# engine = create_async_engine(config.PG_DSN_ALC, echo=True)
# Base = declarative_base()
#
# class Person(Base):
#     __tablename__ = 'Persons'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     birth_year = Column(String)
#     eye_color = Column(String)
#     films = Column(String)
#     gender = Column(String)
#     hair_color = Column(String)
#     height = Column(String)
#     homeworld = Column(String)
#     mass = Column(String)
#     skin_color = Column(String)
#     species = Column(String)
#     starships = Column(String)
#     vehicles = Column(String)