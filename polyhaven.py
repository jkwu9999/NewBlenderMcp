import bpy
import requests

def get_polyhaven_status():
    enabled = bpy.context.scene.blendermcp_use_polyhaven
    if enabled:
        return {"enabled": True, "message": "PolyHaven integration is enabled and ready to use."}
    else:
        return {
            "enabled": False,
            "message": """PolyHaven integration is currently disabled. To enable it:
1. In the 3D Viewport, find the BlenderMCP panel in the sidebar (press N if hidden)
2. Check the 'Use assets from Poly Haven' checkbox
3. Restart the connection to Claude"""
        }

def get_polyhaven_categories(asset_type):
    if asset_type not in ["hdris", "textures", "models", "all"]:
        return {"error": f"Invalid asset type: {asset_type}. Must be one of: hdris, textures, models, all"}

    try:
        response = requests.get(f"https://api.polyhaven.com/categories/{asset_type}")
        response.raise_for_status()
        return {"categories": response.json()}
    except Exception as e:
        return {"error": str(e)}

def search_polyhaven_assets(asset_type=None, categories=None):
    try:
        url = "https://api.polyhaven.com/assets"
        params = {}

        if asset_type and asset_type != "all":
            if asset_type not in ["hdris", "textures", "models"]:
                return {"error": f"Invalid asset type: {asset_type}. Must be one of: hdris, textures, models, all"}
            params["type"] = asset_type

        if categories:
            params["categories"] = categories

        response = requests.get(url, params=params)
        response.raise_for_status()
        assets = response.json()
        limited_assets = dict(list(assets.items())[:20])

        return {
            "assets": limited_assets,
            "total_count": len(assets),
            "returned_count": len(limited_assets)
        }
    except Exception as e:
        return {"error": str(e)}

def download_polyhaven_asset(*args, **kwargs):
    from ._polyhaven_full import download_polyhaven_asset
    return download_polyhaven_asset(*args, **kwargs)

def set_texture(*args, **kwargs):
    from ._polyhaven_full import set_texture
    return set_texture(*args, **kwargs)
