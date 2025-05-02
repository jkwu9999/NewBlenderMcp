import bpy
import mathutils

def get_scene_info():
    """Get information about the current Blender scene"""
    scene = bpy.context.scene
    try:
        info = {
            "name": scene.name,
            "object_count": len(scene.objects),
            "objects": [],
            "materials_count": len(bpy.data.materials),
        }
        for i, obj in enumerate(scene.objects):
            if i >= 10:
                break
            info["objects"].append({
                "name": obj.name,
                "type": obj.type,
                "location": [round(float(obj.location.x), 2),
                             round(float(obj.location.y), 2),
                             round(float(obj.location.z), 2)]
            })
        return info
    except Exception as e:
        return {"error": str(e)}

def get_object_info(name):
    """Get detailed information about a specific object"""
    obj = bpy.data.objects.get(name)
    if not obj:
        raise ValueError(f"Object not found: {name}")

    info = {
        "name": obj.name,
        "type": obj.type,
        "location": [obj.location.x, obj.location.y, obj.location.z],
        "rotation": [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z],
        "scale": [obj.scale.x, obj.scale.y, obj.scale.z],
        "visible": obj.visible_get(),
        "materials": [slot.material.name for slot in obj.material_slots if slot.material],
    }

    if obj.type == "MESH":
        info["world_bounding_box"] = _get_aabb(obj)
        mesh = obj.data
        info["mesh"] = {
            "vertices": len(mesh.vertices),
            "edges": len(mesh.edges),
            "polygons": len(mesh.polygons),
        }

    return info

def _get_aabb(obj):
    """Returns the world-space axis-aligned bounding box (AABB) of an object."""
    if obj.type != 'MESH':
        raise TypeError("Object must be a mesh")
    corners = [mathutils.Vector(corner) for corner in obj.bound_box]
    world_corners = [obj.matrix_world @ corner for corner in corners]
    min_corner = mathutils.Vector(map(min, zip(*world_corners)))
    max_corner = mathutils.Vector(map(max, zip(*world_corners)))
    return [[*min_corner], [*max_corner]]
