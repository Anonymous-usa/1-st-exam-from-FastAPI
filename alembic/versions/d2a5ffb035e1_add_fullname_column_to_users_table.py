from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# Revision identifiers, used by Alembic.
revision = 'd2a5ffb035e1'
down_revision = '4e636a3721fc'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Upgrade schema."""
    # Start a batch operation for SQLite
    with op.batch_alter_table('users', schema=None) as batch_op:
        # Inspect the current table
        inspector = inspect(op.get_bind())
        columns = [col['name'] for col in inspector.get_columns('users')]

        # Only add 'fullname' if it doesn't already exist
        if 'fullname' not in columns:
            batch_op.add_column(sa.Column('fullname', sa.String(length=100), nullable=False))

        # Only add 'hashed_password' if it doesn't already exist
        if 'hashed_password' not in columns:
            batch_op.add_column(sa.Column('hashed_password', sa.String(length=100), nullable=False))

        # Ensure unique constraints on 'username' and 'email'
        batch_op.create_unique_constraint('uq_users_username', ['username'])
        batch_op.create_unique_constraint('uq_users_email', ['email'])

def downgrade() -> None:
    """Downgrade schema."""
    # Start a batch operation for SQLite
    with op.batch_alter_table('users', schema=None) as batch_op:
        # Drop unique constraints first
        batch_op.drop_constraint('uq_users_username', type_='unique')
        batch_op.drop_constraint('uq_users_email', type_='unique')

        # Drop the added columns
        batch_op.drop_column('hashed_password')
        batch_op.drop_column('fullname')
