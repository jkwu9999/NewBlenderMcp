import bpy
import requests
import tempfile
import os
import shutil

def download_polyhaven_asset(asset_id, asset_type, resolution="1k", file_format=None):
    from .utils import setup_hdri, setup_texture_material, import_polyhaven_model

    files_response = requests.get(f"https://api.polyhaven.com/files/{asset_id}")
    if files_response.status_code != 200:
        return {"error": f"Failed to get asset files: {files_response.status_code}"}

    files_data = files_response.json()

    try:
        if asset_type == "hdris":
            return setup_hdri(asset_id, files_data, resolution, file_format)
        elif asset_type == "textures":
            return setup_texture_material(asset_id, files_data, resolution, file_format)
        elif asset_type == "models":
            return import_polyhaven_model(asset_id, files_data, resolution, file_format)
        else:
            return {"error": f"Unsupported asset type: {asset_type}"}
    except Exception as e:
        return {"error": f"Failed to download asset: {str(e)}"}

def set_texture(object_name, texture_id):
    from .utils import apply_texture_to_object
    try:
        return apply_texture_to_object(object_name, texture_id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"Failed to apply texture: {str(e)}"}
