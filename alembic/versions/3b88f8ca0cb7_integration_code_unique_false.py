"""integration_code_unique_false

Revision ID: 3b88f8ca0cb7
Revises: 754632afb373
Create Date: 2021-02-24 22:56:55.068279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b88f8ca0cb7'
down_revision = '754632afb373'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Integration_DataIntegration_Code', table_name='DataIntegration', schema='Integration')
    op.create_index(op.f('ix_Integration_DataIntegration_Code'), 'DataIntegration', ['Code'], unique=False, schema='Integration')
    op.create_index(op.f('ix_Operation_DataOperation_Name'), 'DataOperation', ['Name'], unique=False, schema='Operation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Operation_DataOperation_Name'), table_name='DataOperation', schema='Operation')
    op.drop_index(op.f('ix_Integration_DataIntegration_Code'), table_name='DataIntegration', schema='Integration')
    op.create_index('ix_Integration_DataIntegration_Code', 'DataIntegration', ['Code'], unique=True, schema='Integration')
    # ### end Alembic commands ###
