import bpy
import requests
import tempfile
import os
import shutil
import json


RODIN_API_MAIN = "https://hyperhuman.deemos.com/api/v2"
RODIN_API_FAL = "https://queue.fal.run/fal-ai/hyper3d"


def create_rodin_job_main_site(text_prompt=None, images=None, bbox_condition=None):
    if images is None:
        images = []
    files = [
        *[("images", (f"{i:04d}{suffix}", img)) for i, (suffix, img) in enumerate(images)],
        ("tier", (None, "Sketch")),
        ("mesh_mode", (None, "Raw")),
    ]
    if text_prompt:
        files.append(("prompt", (None, text_prompt)))
    if bbox_condition:
        files.append(("bbox_condition", (None, json.dumps(bbox_condition))))

    res = requests.post(
        f"{RODIN_API_MAIN}/rodin",
        headers={"Authorization": f"Bearer {bpy.context.scene.blendermcp_hyper3d_api_key}"},
        files=files
    )
    return res.json()


def create_rodin_job_fal_ai(text_prompt=None, images=None, bbox_condition=None):
    req_data = {"tier": "Sketch"}
    if images:
        req_data["input_image_urls"] = images
    if text_prompt:
        req_data["prompt"] = text_prompt
    if bbox_condition:
        req_data["bbox_condition"] = bbox_condition

    res = requests.post(
        f"{RODIN_API_FAL}/rodin",
        headers={
            "Authorization": f"Key {bpy.context.scene.blendermcp_hyper3d_api_key}",
            "Content-Type": "application/json"
        },
        json=req_data
    )
    return res.json()


def poll_rodin_job_status_main_site(subscription_key):
    res = requests.post(
        f"{RODIN_API_MAIN}/status",
        headers={"Authorization": f"Bearer {bpy.context.scene.blendermcp_hyper3d_api_key}"},
        json={"subscription_key": subscription_key}
    )
    data = res.json()
    return {"status_list": [j["status"] for j in data.get("jobs", [])]}


def poll_rodin_job_status_fal_ai(request_id):
    res = requests.get(
        f"{RODIN_API_FAL}/requests/{request_id}/status",
        headers={"Authorization": f"Key {bpy.context.scene.blendermcp_hyper3d_api_key}"}
    )
    return res.json()


def import_generated_asset_main_site(task_uuid, name):
    res = requests.post(
        f"{RODIN_API_MAIN}/download",
        headers={"Authorization": f"Bearer {bpy.context.scene.blendermcp_hyper3d_api_key}"},
        json={"task_uuid": task_uuid}
    )
    data_ = res.json()
    glb_url = next((i["url"] for i in data_["list"] if i["name"].endswith(".glb")), None)
    if not glb_url:
        return {"succeed": False, "error": "No .glb file found in response."}

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".glb")
    try:
        content = requests.get(glb_url).content
        temp_file.write(content)
        temp_file.close()

        return _import_and_format_glb(temp_file.name, name)
    except Exception as e:
        return {"succeed": False, "error": str(e)}


def import_generated_asset_fal_ai(request_id, name):
    res = requests.get(
        f"{RODIN_API_FAL}/requests/{request_id}",
        headers={"Authorization": f"Key {bpy.context.scene.blendermcp_hyper3d_api_key}"}
    )
    glb_url = res.json().get("model_mesh", {}).get("url")
    if not glb_url:
        return {"succeed": False, "error": "No model_mesh URL found."}

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".glb")
    try:
        content = requests.get(glb_url).content
        temp_file.write(content)
        temp_file.close()

        return _import_and_format_glb(temp_file.name, name)
    except Exception as e:
        return {"succeed": False, "error": str(e)}


def _import_and_format_glb(filepath, mesh_name=None):
    existing = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=filepath)
    bpy.context.view_layer.update()
    imported = list(set(bpy.data.objects) - existing)

    mesh_obj = next((obj for obj in imported if obj.type == 'MESH'), None)
    if mesh_obj and mesh_name:
        mesh_obj.name = mesh_name
        mesh_obj.data.name = mesh_name

    if mesh_obj:
        result = {
            "name": mesh_obj.name,
            "type": mesh_obj.type,
            "location": list(mesh_obj.location),
            "rotation": list(mesh_obj.rotation_euler),
            "scale": list(mesh_obj.scale),
        }
        return {"succeed": True, **result}
    else:
        return {"succeed": False, "error": "No mesh object found in import."}
