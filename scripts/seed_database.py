from datetime import datetime, timedelta, timezone

from app.core.database import init_database, session_scope
from app.core.models import InventoryMovement, Product

PRODUCTS = [
    ("Arroz", "Pacote de arroz branco 5kg", "Mercearia", 24.90, 30, True),
    ("Feijão", "Feijão carioca 1kg", "Mercearia", 8.49, 40, False),
    ("Café", "Café torrado e moído 500g", "Bebidas", 15.90, 25, True),
    ("Leite", "Leite integral 1L", "Laticínios", 4.79, 60, False),
    ("Açúcar", "Açúcar refinado 1kg", "Mercearia", 5.29, 35, False),
    ("Macarrão", "Macarrão espaguete 500g", "Massas", 3.99, 50, False),
    ("Sabonete", "Sabonete perfumado 90g", "Higiene", 2.49, 80, True),
    ("Detergente", "Detergente neutro 500ml", "Limpeza", 2.19, 70, False),
    ("Refrigerante", "Refrigerante cola 2L", "Bebidas", 8.99, 22, True),
    ("Biscoito", "Biscoito recheado 130g", "Mercearia", 3.49, 45, False),
]

# (product_id, tipo, quantidade, dias atrás, horas atrás)
MOVEMENTS = [
    (1, "SALE", 3, 0, 0),
    (2, "SALE", 1, 1, 1),
    (3, "SALE", 5, 2, 2),
    (4, "SALE", 2, 3, 3),
    (5, "SALE", 4, 4, 4),
    (1, "SALE", 2, 5, 5),
]


def main() -> None:
    init_database()
    with session_scope() as db:
        for index, (name, description, category, price, stock, promotional) in enumerate(
            PRODUCTS, start=1
        ):
            product = db.get(Product, index)
            if product is None:
                product = Product(id=index)
                db.add(product)

            product.name = name
            product.description = description
            product.category = category
            product.price = price
            product.stock = stock
            product.promotional = promotional

        db.flush()
        now = datetime.now(timezone.utc).replace(tzinfo=None, second=0, microsecond=0)
        for index, (product_id, movement_type, quantity, days, hours) in enumerate(
            MOVEMENTS, start=1
        ):
            movement = db.get(InventoryMovement, index)
            if movement is None:
                movement = InventoryMovement(id=index)
                db.add(movement)

            movement.product_id = product_id
            movement.type = movement_type
            movement.quantity = quantity
            movement.created_at = now - timedelta(days=days, hours=hours)

    print("Seed concluído.")


if __name__ == "__main__":
    main()
