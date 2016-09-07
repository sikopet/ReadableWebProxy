from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig


# Path hackery
import os.path
import sys
sys.path.append(os.path.abspath(os.getcwd()))

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code

import common.db_engine
import common.database
context.config.set_main_option('sqlalchemy.url', common.db_engine.SQLALCHEMY_DATABASE_URI)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
base = common.database.Base
target_metadata = base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_object(object, name, type_, reflected, compare_to):

	# Ignore a few special things (partial intexes on distance, trigram index, and the
	# autogenerated table from apscheduler).
	ignored = [
		'ix_web_pages_distance_filtered',
		'ix_web_pages_distance_filtered_nowp',
		'ix_web_pages_distance_filtered_wp',
		'ix_web_pages_url_ops',
		'apscheduler',
	]

	# Allow items with null names (it was an issue).
	if not object.name:
		return True

	if any([tmp in object.name for tmp in ignored]):
		print((object.name, object, name, type, reflected, compare_to))
		return False

	return True


def run_migrations_online():
	"""Run migrations in 'online' mode.

	In this scenario we need to create an Engine
	and associate a connection with the context.

	"""
	connectable = engine_from_config(
		config.get_section(config.config_ini_section),
		prefix='sqlalchemy.',
		poolclass=pool.NullPool)

	with connectable.connect() as connection:
		context.configure(
			connection      = connection,
			target_metadata = target_metadata,
			include_object  = include_object,
		)

		with context.begin_transaction():
			context.run_migrations()

run_migrations_online()
