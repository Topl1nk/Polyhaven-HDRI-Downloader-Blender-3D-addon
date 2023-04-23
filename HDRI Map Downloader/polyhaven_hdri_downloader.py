import os
import urllib.request
import tempfile
import bpy
from urllib.parse import urlparse


class HDRI_OT_download(bpy.types.Operator):
    bl_idname = "hdri.download"
    bl_label = "Download HDRI Map"
    bl_description = "Download HDRI map from Poly Haven"
    
    url: bpy.props.StringProperty(name="URL")
    
    def execute(self, context):
        # Set the download URL
        url = self.url

        # Get the last segment of the URL (e.g., "little_paris_eiffel_tower")
        path = urlparse(url).path.split("/")[-1]

        # Create the HDRI download URL
        hdri_url = "https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/4k/{}_4k.exr".format(path)
      
        # Create a temporary file
        temp_dir = tempfile.gettempdir()
        temp_file_name = path + ".exr"
        temp_file_path = os.path.join(temp_dir, temp_file_name)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Referer": "https://example.com/"
        }

        # Download the file using urllib.request and add headers
        req = urllib.request.Request(hdri_url, headers=headers)
        response = urllib.request.urlopen(req)

        # Save the file to a temporary directory
        with open(temp_file_path, "wb") as f:
            f.write(response.read())

        print(f"File {temp_file_path} downloaded to the temporary directory.")

        # Set the map on the scene
        world = bpy.context.scene.world
        world.use_nodes = True
        tree = world.node_tree
        nodes = tree.nodes
        links = tree.links

        # Add an Environment Texture node
        tex_node = nodes.new(type='ShaderNodeTexEnvironment')
        tex_node.image = bpy.data.images.load(temp_file_path)

        # Add a Background node
        bg_node = nodes.new(type='ShaderNodeBackground')

        # Add an Output World node
        out_node = nodes.new(type='ShaderNodeOutputWorld')

        # Connect the nodes
        links.new(tex_node.outputs['Color'], bg_node.inputs['Color'])
        links.new(bg_node.outputs['Background'], out_node.inputs['Surface'])

        # Select the "World Output" node
        for node in nodes:
            if node.name == "World Output":
                out_node.select = True
                tree.nodes.active = out_node  # Set the active node
            else:
                node.select = False

        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class HDRI_PT_panel(bpy.types.Panel):
    bl_idname = "HDRI_PT_panel"
    bl_label = "HDRI Map Downloader"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "HDRI"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("hdri.download", text="Download HDRI Map")


def register():
    bpy.utils.register_class(HDRI_OT_download)
    bpy.utils.register_class(HDRI_PT_panel)


def unregister():
    bpy.utils.unregister_class(HDRI_OT_download)
    bpy.utils.unregister_class(HDRI_PT_panel)


if __name__ == "__main__":
    register()
