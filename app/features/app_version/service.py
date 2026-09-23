from app.core import config


def version_info() -> dict[str, str]:
    return {
        "app_version": config.settings.app_version,
        "commit_sha": config.settings.commit_sha,
    }