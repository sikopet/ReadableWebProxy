"""actually Dropping unused columns now

Revision ID: be0687950ece
Revises: d547cd837350
Create Date: 2017-03-01 05:39:20.282931

"""

# revision identifiers, used by Alembic.
revision = 'be0687950ece'
down_revision = 'd547cd837350'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
import sqlalchemy_utils

# Patch in knowledge of the citext type, so it reflects properly.
from sqlalchemy.dialects.postgresql.base import ischema_names
import citext
import queue
import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import TSVECTOR
ischema_names['citext'] = citext.CIText

from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nu_outbound_wrappers')
    op.drop_column('feed_pages', 'srcname')
    op.drop_column('feed_pages', 'feedurl')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feed_pages', sa.Column('feedurl', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('feed_pages', sa.Column('srcname', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_table('nu_outbound_wrappers',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('actual_target', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('client_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('client_key', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('groupinfo', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('outbound_wrapper', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('referrer', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('releaseinfo', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('seriesname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('validated', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('released_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='nu_outbound_wrappers_pkey'),
    sa.UniqueConstraint('client_id', 'client_key', 'seriesname', 'releaseinfo', 'groupinfo', 'actual_target', name='nu_outbound_wrappers_client_id_client_key_seriesname_releas_key')
    )
    ### end Alembic commands ###
