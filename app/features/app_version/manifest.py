from app.core.types.features import FeatureManifest, MenuItem
from app.features.app_version.routes import bp

manifest = FeatureManifest(
    id="app-version",
    name="App Version",
    blueprint=bp,
    menu=MenuItem(label="App Version", endpoint="app_version.page", order=50),
    slots=[],
)
