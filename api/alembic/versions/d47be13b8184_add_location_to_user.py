"""add_location_to_user

Revision ID: d47be13b8184
Revises: bf090c0cdc0f
Create Date: 2022-01-11 07:55:32.627978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd47be13b8184'
down_revision = 'bf090c0cdc0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('location_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'court_location', ['location_id'], ['id'])
    op.drop_column('user', 'location')
    op.execute(
        '''
        DO
        $$
        DECLARE maxid INTEGER;        
        BEGIN         
        SELECT MAX(id) INTO maxid FROM language;       
        EXECUTE 'ALTER SEQUENCE language_id_seq RESTART WITH ' || maxid+1;
        END
        $$
        '''
    )
    op.execute(
        '''
        DO
        $$
        DECLARE maxid INTEGER;        
        BEGIN         
        SELECT MAX(id) INTO maxid FROM interpreter;       
        EXECUTE 'ALTER SEQUENCE interpreter_id_seq RESTART WITH ' || maxid+1;
        END
        $$
        '''
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'location_id')
    # ### end Alembic commands ###
