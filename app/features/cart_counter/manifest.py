from flask import session

from app.core.types.features import FeatureManifest, SlotContribution


def cart_counter_menu(**_context) -> str:
    cart = session.get("cart", {})
    total_items = sum(int(quantity) for quantity in cart.values() if int(quantity) > 0)

    if total_items <= 0:
        return ""

    return f"""
        <style>
            nav a[href="/cart"] {{
                position: relative;
                overflow: visible;
            }}
            nav a[href="/cart"] + .cart-count,
            nav a[href="/cart"] ~ .cart-count,
            nav a[href="/cart"] .cart-count {{
                position: absolute;
                top: -10px;
                right: -10px;
                z-index: 10;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 1.5rem;
                height: 1.5rem;
                padding: 0 0.35rem;
                border-radius: 999px;
                background: #0d6efd;
                color: #ffffff;
                font-size: 0.72rem;
                font-weight: 700;
                line-height: 1;
                box-shadow: 0 4px 10px rgba(13, 110, 253, 0.25);
            }}
        </style>
        <script>
            (() => {{
                const cartLink = document.querySelector("nav a[href='/cart']");
                if (!cartLink) return;

                let badge = cartLink.querySelector('.cart-count');
                if (!badge) {{
                    badge = document.createElement('span');
                    badge.className = 'cart-count';
                    cartLink.appendChild(badge);
                }}

                badge.textContent = '{total_items}';
            }})();
        </script>
    """


manifest = FeatureManifest(
    id="cart-counter",
    name="Contador do Carrinho",
    slots=[SlotContribution(slot="MAIN_MENU", renderer=cart_counter_menu)],
)
