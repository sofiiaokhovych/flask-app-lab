"""Insert data into products table

Revision ID: bac4ec47a714
Revises: be460f589e3f
Create Date: 2026-11-13 18:24:26.888416

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'bac4ec47a714'
down_revision = 'be460f589e3f'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = table('categories', column('id', sa.Integer), column('name', sa.String))

    products_table = table('products',
        column('name', sa.String),
        column('price', sa.Float),
        column('active', sa.Boolean),
        column('category_id', sa.Integer),
    )

    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'},
    ])

    conn = op.get_bind()

    def category_id(name):
        return conn.execute(
            sa.text("SELECT id FROM categories WHERE name = :name"),
            {"name": name},
        ).scalar()

    electronics_id = category_id('Electronics')
    books_id = category_id('Books')
    clothing_id = category_id('Clothing')

    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': electronics_id},
        {'name': 'Smartphone', 'price': 800.0, 'active': True, 'category_id': electronics_id},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': books_id},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': clothing_id},
    ])


def downgrade():
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt');
    """)

    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)