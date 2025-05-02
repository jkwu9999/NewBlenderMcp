import bpy
from . import scene, polyhaven, hyper3d, execute

def handle_command(command):
    cmd_type = command.get("type")
    params = command.get("params", {})
    handlers = {
        "get_scene_info": scene.get_scene_info,
        "get_object_info": scene.get_object_info,
        "execute_code": execute.execute_code,
        "get_polyhaven_status": polyhaven.get_polyhaven_status,
        "get_hyper3d_status": hyper3d.get_hyper3d_status,
    }

    if bpy.context.scene.blendermcp_use_polyhaven:
        handlers.update({
            "get_polyhaven_categories": polyhaven.get_polyhaven_categories,
            "search_polyhaven_assets": polyhaven.search_polyhaven_assets,
            "download_polyhaven_asset": polyhaven.download_polyhaven_asset,
            "set_texture": polyhaven.set_texture,
        })

    if bpy.context.scene.blendermcp_use_hyper3d:
        handlers.update({
            "create_rodin_job": hyper3d.create_rodin_job,
            "poll_rodin_job_status": hyper3d.poll_rodin_job_status,
            "import_generated_asset": hyper3d.import_generated_asset,
        })

    if cmd_type not in handlers:
        return {"status": "error", "message": f"Unknown command type: {cmd_type}"}

    try:
        result = handlers[cmd_type](**params)
        return {"status": "success", "result": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
