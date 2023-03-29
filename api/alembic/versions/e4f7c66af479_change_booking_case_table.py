"""change_booking_case_table

Revision ID: e4f7c66af479
Revises: 4e967094c2c5
Create Date: 2023-03-11 14:48:34.585850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f7c66af479'
down_revision = '4e967094c2c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking_cases', sa.Column('court_class_other', sa.String(), nullable=True))
    op.add_column('booking_cases', sa.Column('reason_other', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('booking_cases', 'reason_other')
    op.drop_column('booking_cases', 'court_class_other')
    # ### end Alembic commands ###