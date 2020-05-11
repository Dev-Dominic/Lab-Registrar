"""empty message

Revision ID: ffa7a3c3379b
Revises: 4bdd5579d382
Create Date: 2020-05-10 22:02:07.252224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffa7a3c3379b'
down_revision = '4bdd5579d382'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('swap_request_labtech_confirm_id_fkey', 'swap_request', type_='foreignkey')
    op.drop_constraint('swap_request_labtech_request_id_fkey', 'swap_request', type_='foreignkey')
    op.drop_column('swap_request', 'labtech_request_id')
    op.drop_column('swap_request', 'labtech_confirm_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('swap_request', sa.Column('labtech_confirm_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('swap_request', sa.Column('labtech_request_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('swap_request_labtech_request_id_fkey', 'swap_request', 'labtechs', ['labtech_request_id'], ['uwiIssuedID'])
    op.create_foreign_key('swap_request_labtech_confirm_id_fkey', 'swap_request', 'labtechs', ['labtech_confirm_id'], ['uwiIssuedID'])
    # ### end Alembic commands ###
