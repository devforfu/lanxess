"""Many-to-many tables to support timeslots allocation.

Revision ID: 3443a69e4ad4
Revises: f2bfea05fe49
Create Date: 2018-06-11 05:57:26.542474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3443a69e4ad4'
down_revision = 'f2bfea05fe49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate_timeslots',
    sa.Column('candidate_id', sa.Integer(), nullable=True),
    sa.Column('timeslots_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.ForeignKeyConstraint(['timeslots_id'], ['timeslots.id'], )
    )
    op.create_table('employee_timeslots',
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('timeslots_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['timeslots_id'], ['timeslots.id'], )
    )
    op.drop_table('candidates_timeslots')
    op.drop_table('employees_timeslots')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees_timeslots',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('timeslot_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name='employees_timeslots_employee_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['timeslot_id'], ['timeslots.id'], name='employees_timeslots_timeslot_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='employees_timeslots_pkey')
    )
    op.create_table('candidates_timeslots',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('candidate_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('timeslot_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], name='candidates_timeslots_candidate_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['timeslot_id'], ['timeslots.id'], name='candidates_timeslots_timeslot_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='candidates_timeslots_pkey')
    )
    op.drop_table('employee_timeslots')
    op.drop_table('candidate_timeslots')
    # ### end Alembic commands ###
