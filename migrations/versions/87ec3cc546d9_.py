"""empty message

Revision ID: 87ec3cc546d9
Revises: 
Create Date: 2018-09-04 15:14:45.862215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87ec3cc546d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line_1', sa.String(length=255), nullable=True),
    sa.Column('line_2', sa.String(length=255), nullable=True),
    sa.Column('line_3', sa.String(length=255), nullable=True),
    sa.Column('line_4', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state_province', sa.String(length=255), nullable=True),
    sa.Column('postal_code', sa.String(length=20), nullable=True),
    sa.Column('county', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=9, scale=6), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=9, scale=6), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('contact_type', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('referral_source', sa.String(length=255), nullable=True),
    sa.Column('investment_strategy', sa.String(length=255), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('list_price', sa.Integer(), nullable=True),
    sa.Column('rehab_amount', sa.Integer(), nullable=True),
    sa.Column('after_repair_value', sa.Integer(), nullable=True),
    sa.Column('equity', sa.Integer(), nullable=True),
    sa.Column('return_on_investment', sa.String(length=255), nullable=True),
    sa.Column('monthly_rent', sa.Integer(), nullable=True),
    sa.Column('taxes', sa.Integer(), nullable=True),
    sa.Column('insurance', sa.Integer(), nullable=True),
    sa.Column('maintenance_percent', sa.Integer(), nullable=True),
    sa.Column('management_percent', sa.Integer(), nullable=True),
    sa.Column('utility_amount', sa.Integer(), nullable=True),
    sa.Column('utility_description', sa.String(length=255), nullable=True),
    sa.Column('capex_reserves', sa.Integer(), nullable=True),
    sa.Column('net_operating_income', sa.Integer(), nullable=True),
    sa.Column('cap_rate', sa.String(length=255), nullable=True),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('investmentcriteria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('property_type', sa.Integer(), nullable=True),
    sa.Column('flip', sa.Integer(), nullable=True),
    sa.Column('rental', sa.Integer(), nullable=True),
    sa.Column('minimum_units', sa.Integer(), nullable=True),
    sa.Column('maximum_units', sa.Integer(), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locationcriteria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('location_type', sa.String(length=255), nullable=True),
    sa.Column('location_code', sa.String(length=255), nullable=True),
    sa.Column('criteria_id', sa.Integer(), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['criteria_id'], ['investmentcriteria.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('property_type', sa.Integer(), nullable=True),
    sa.Column('units', sa.Integer(), nullable=True),
    sa.Column('sq_feet', sa.Integer(), nullable=True),
    sa.Column('bedrooms', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('basement_type', sa.String(length=255), nullable=True),
    sa.Column('garage_type', sa.String(length=255), nullable=True),
    sa.Column('last_sale_date', sa.Date(), nullable=True),
    sa.Column('owner_occupied', sa.Boolean(), nullable=True),
    sa.Column('create_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['create_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=40), nullable=True),
    sa.Column('current_login_ip', sa.String(length=40), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('user_contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_contact_id'], ['usercontact.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('usercontact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usercontact')
    op.drop_table('user')
    op.drop_table('roles_users')
    op.drop_table('role')
    op.drop_table('property')
    op.drop_table('locationcriteria')
    op.drop_table('investmentcriteria')
    op.drop_table('deal')
    op.drop_table('contact')
    op.drop_table('address')
    # ### end Alembic commands ###
