"""data_integration_connections

Revision ID: e50ccd73d9c9
Revises: e2bcfbd775cb
Create Date: 2021-03-14 15:50:48.628062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e50ccd73d9c9'
down_revision = 'e2bcfbd775cb'
branch_labels = None
depends_on = None


def insert_data_integration_connection_to_database():
    from models.dao.integration import DataIntegrationConnection,DataIntegrationConnectionDatabase
    bind = op.get_bind()
    from sqlalchemy import orm
    session = orm.Session(bind=bind)
    query = bind.execute('select dic."Id", dic."Schema",dic."TableName",dic."Query" from "Integration"."DataIntegrationConnection"  as dic')
    results = query.fetchall()
    for data_integration_connection_data in results:
        data_integration_connection = session.query(DataIntegrationConnection).filter_by(Id=data_integration_connection_data[0]).first()
        data_integration_connection_database = DataIntegrationConnectionDatabase(DataIntegrationConnection=data_integration_connection,
        Schema=data_integration_connection_data[1],
        TableName=data_integration_connection_data[2],
        Query=data_integration_connection_data[3])
        session.add(data_integration_connection_database)

    session.commit()

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DataIntegrationConnectionDatabase',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('DataIntegrationConnectionId', sa.Integer(), nullable=True),
    sa.Column('Schema', sa.String(length=100), nullable=True),
    sa.Column('TableName', sa.String(length=100), nullable=True),
    sa.Column('Query', sa.Text(), nullable=True),
    sa.Column('CreatedByUserId', sa.Integer(), nullable=False),
    sa.Column('CreationDate', sa.DateTime(), nullable=False),
    sa.Column('LastUpdatedUserId', sa.Integer(), nullable=True),
    sa.Column('LastUpdatedDate', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Integer(), nullable=False),
    sa.Column('Comments', sa.String(length=1000), nullable=True),
    sa.Column('RowVersion', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['DataIntegrationConnectionId'], ['Integration.DataIntegrationConnection.Id'], ),
    sa.PrimaryKeyConstraint('Id'),
    schema='Integration'
    )
    insert_data_integration_connection_to_database()
    op.drop_column('DataIntegrationConnection', 'TableName', schema='Integration')
    op.drop_column('DataIntegrationConnection', 'Schema', schema='Integration')
    op.drop_column('DataIntegrationConnection', 'Query', schema='Integration')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('DataIntegrationConnection', sa.Column('Query', sa.TEXT(), autoincrement=False, nullable=True), schema='Integration')
    op.add_column('DataIntegrationConnection', sa.Column('Schema', sa.VARCHAR(length=100), autoincrement=False, nullable=True), schema='Integration')
    op.add_column('DataIntegrationConnection', sa.Column('TableName', sa.VARCHAR(length=100), autoincrement=False, nullable=True), schema='Integration')
    op.drop_table('DataIntegrationConnectionDatabase', schema='Integration')
    # ### end Alembic commands ###
