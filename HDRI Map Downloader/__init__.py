bl_info = {
    "name": "HDRI Map Downloader",
    "author": "TopL1nk",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > HDRI > Download HDRI Map",
    "description": "Download HDRI maps from Poly Haven",
    "warning": "",
    "doc_url": "https://youtu.be/BGdnM_gWsw8",
    "category": "3D View",
}

import bpy
from . import polyhaven_hdri_downloader

def register():
    bpy.utils.register_class(polyhaven_hdri_downloader.HDRI_OT_download)
    bpy.utils.register_class(polyhaven_hdri_downloader.HDRI_PT_panel)

def unregister():
    bpy.utils.unregister_class(polyhaven_hdri_downloader.HDRI_OT_download)
    bpy.utils.unregister_class(polyhaven_hdri_downloader.HDRI_PT_panel)

if __name__ == "__main__":
    register()
