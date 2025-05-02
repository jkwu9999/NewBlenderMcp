import bpy
from ._hyper3d_full import (
    create_rodin_job_main_site,
    create_rodin_job_fal_ai,
    poll_rodin_job_status_main_site,
    poll_rodin_job_status_fal_ai,
    import_generated_asset_main_site,
    import_generated_asset_fal_ai,
)

RODIN_FREE_TRIAL_KEY = ""

def get_hyper3d_status():
    scene = bpy.context.scene
    if scene.blendermcp_use_hyper3d:
        if not scene.blendermcp_hyper3d_api_key:
            return {
                "enabled": False,
                "message": "Hyper3D Rodin integration is enabled but API key is missing. Please configure it in the panel."
            }
        mode = scene.blendermcp_hyper3d_mode
        return {
            "enabled": True,
            "message": f"Hyper3D enabled in mode: {mode}, key type: {'private' if scene.blendermcp_hyper3d_api_key != RODIN_FREE_TRIAL_KEY else 'free_trial'}"
        }
    return {
        "enabled": False,
        "message": "Enable Hyper3D from the BlenderMCP panel to use this feature."
    }

def create_rodin_job(*args, **kwargs):
    mode = bpy.context.scene.blendermcp_hyper3d_mode
    if mode == "MAIN_SITE":
        return create_rodin_job_main_site(*args, **kwargs)
    elif mode == "FAL_AI":
        return create_rodin_job_fal_ai(*args, **kwargs)
    return {"error": "Unknown Hyper3D Rodin mode"}

def poll_rodin_job_status(*args, **kwargs):
    mode = bpy.context.scene.blendermcp_hyper3d_mode
    if mode == "MAIN_SITE":
        return poll_rodin_job_status_main_site(*args, **kwargs)
    elif mode == "FAL_AI":
        return poll_rodin_job_status_fal_ai(*args, **kwargs)
    return {"error": "Unknown Hyper3D Rodin mode"}

def import_generated_asset(*args, **kwargs):
    mode = bpy.context.scene.blendermcp_hyper3d_mode
    if mode == "MAIN_SITE":
        return import_generated_asset_main_site(*args, **kwargs)
    elif mode == "FAL_AI":
        return import_generated_asset_fal_ai(*args, **kwargs)
    return {"error": "Unknown Hyper3D Rodin mode"}
