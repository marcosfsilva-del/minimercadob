from app.core.types.features import FeatureManifest
from app.features.health_detalhado.routes import health_detalhado_bp

manifest = FeatureManifest(
    id="health-detalhado",
    name="Health Detalhado",
    blueprint=health_detalhado_bp,
)
