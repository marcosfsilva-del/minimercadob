from html import escape


def _format_brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_cart_item_subtotal(*, item: dict[str, object], **_context: object) -> str:
    product = item["product"]
    price = float(product.price)
    quantity = int(item["quantity"])
    subtotal = price * quantity

    return (
        f'<p class="muted" data-cart-unit-price="{price:.2f}">'
        f'Subtotal: <span data-cart-subtotal>{escape(_format_brl(subtotal))}</span></p>'
    )


def render_cart_summary_script(**_context: object) -> str:
    return """<script>
  (() => {
    const formatCurrency = (value) => new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL"
    }).format(value);

    const updateCartTotals = () => {
      let total = 0;

      document.querySelectorAll(".cart-item").forEach((item) => {
        const priceElement = item.querySelector("[data-cart-unit-price]");
        const quantityInput = item.querySelector('input[name="quantity"]');
        const subtotalElement = item.querySelector("[data-cart-subtotal]");

        if (!priceElement || !quantityInput || !subtotalElement) {
          return;
        }

        const subtotal =
          Number(priceElement.dataset.cartUnitPrice) * Number(quantityInput.value || 0);
        subtotalElement.textContent = formatCurrency(subtotal);
        total += subtotal;
      });

      const totalElement = document.querySelector(".summary .total");
      if (totalElement) {
        totalElement.textContent = formatCurrency(total);
      }
    };

    document.querySelectorAll('input[name="quantity"]').forEach((input) => {
      input.addEventListener("input", updateCartTotals);
    });
  })();
</script>"""
