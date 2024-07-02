#!python db_setup/setup.py
#
# SET THE ENVIRONMENT VARIABLES:
#   $POSTGRES_PASSWD to the restricted user password to be picked up by env
#
# NOTE: A lot of the configuration is picked up config/configuration.py and ultimately config.yaml
#       This was to avoid typos mostly...  Do what you want, this file is just a suggestion.
#       ... or use db.sql and change the password.  (Usual caveats about saving passwords to files apply)

import sys
import os
import asyncpg
import getpass
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.db.models import Base
from config.configuration import env

ADMIN_USER = "admin"
ADMIN_DATABASE = "admin"

PORT = env.postgres['queue']['port']
HOST = env.postgres['queue']['host']

NEW_DATABASE_NAME = 'queue'
RESTRICTED_USER_NAME = env.postgres['queue']['user']
RESTRICTED_USER_PASSWORD = env.postgres['queue']['password']

TABLE_NAMES = Base.metadata.tables.keys()


async def setup_database_and_user(admin_password):

    print(f'Creating database {NEW_DATABASE_NAME} and user {RESTRICTED_USER_NAME}')
    conn = await asyncpg.connect(user=ADMIN_USER,
                                 password=admin_password,
                                 database=ADMIN_DATABASE,
                                 host=HOST,
                                 port=PORT)

    await conn.execute(f'CREATE DATABASE {NEW_DATABASE_NAME}')

    await conn.close()
    conn = await asyncpg.connect(user=ADMIN_USER,
                                 password=admin_password,
                                 database=NEW_DATABASE_NAME,
                                 host=HOST,
                                 port=PORT)

    # Create user and grant permissions
    await conn.execute(f"CREATE USER {RESTRICTED_USER_NAME} WITH PASSWORD '{RESTRICTED_USER_PASSWORD}'")
    await conn.execute(f"GRANT CONNECT ON DATABASE {NEW_DATABASE_NAME} TO {RESTRICTED_USER_NAME}")
    await conn.execute(f"GRANT USAGE ON SCHEMA public TO {RESTRICTED_USER_NAME}")

    await conn.close()


async def create_table(admin_password):
    print(f'Creating table(s): {TABLE_NAMES}')

    database_url = f"postgresql+asyncpg://{ADMIN_USER}:{admin_password}@{HOST}:{PORT}/{NEW_DATABASE_NAME}"
    engine = create_async_engine(database_url, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def set_permissions(admin_password):
    print(f'Granting permissions to {RESTRICTED_USER_NAME}')
    conn = await asyncpg.connect(user=ADMIN_USER,
                                 password=admin_password,
                                 database=NEW_DATABASE_NAME,
                                 host=HOST,
                                 port=PORT)

    for table_name in TABLE_NAMES:
        await conn.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE {table_name} TO {RESTRICTED_USER_NAME}")

    await conn.close()

if __name__ == "__main__":

    print("Setting up database and user...")
    admin_password = getpass.getpass("Enter admin password: ")

    asyncio.run(setup_database_and_user(admin_password))
    asyncio.run(create_table(admin_password))
    asyncio.run(set_permissions(admin_password))


# end
