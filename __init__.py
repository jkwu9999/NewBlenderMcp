bl_info = {
    "name": "Blender MCP",
    "author": "BlenderMCP",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > BlenderMCP",
    "description": "Connect Blender to Claude via MCP",
    "category": "Interface",
}

RODIN_FREE_TRIAL_KEY = "k9TcfFoEhNd9cCPP2guHAHHHkctZHIRhZDywZ1euGUXwihbYLpOjQhofby80NJez"

import bpy
from . import server
from .ui import panel
from .handlers import dispatcher

def register():
    server.register_server()
    panel.register()

def unregister():
    server.unregister_server()
    panel.unregister()

if __name__ == "__main__":
    register()