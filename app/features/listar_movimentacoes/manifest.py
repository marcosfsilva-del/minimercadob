from app.core.types.features import FeatureManifest


def toolbar_badge(**_context) -> str:
    return '<span class="badge">Slot de exemplo</span>'


manifest = FeatureManifest(
    id="listar_movimentacoes",
    name="Listar Movimentações",
    blueprint=None,
    menu=None,
    slots=[]
)