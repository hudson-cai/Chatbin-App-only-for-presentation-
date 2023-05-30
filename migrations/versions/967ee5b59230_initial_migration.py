"""Initial migration

Revision ID: 967ee5b59230
Revises: 6516b4626036
Create Date: 2023-05-15 02:20:35.568241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '967ee5b59230'
down_revision = '6516b4626036'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.alter_column('timestamp',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('timestamp',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###