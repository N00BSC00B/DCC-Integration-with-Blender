import bpy
import requests
import threading

# Define FastAPI server URL
SERVER_URL = "http://127.0.0.1:8000"

# Available endpoints
ENDPOINTS = {
    "Full Transform": {
        "path": "/transform",
        "fields": ["position", "rotation", "scale"]
    },
    "Translation": {
        "path": "/translation",
        "fields": ["position"]
    },
    "Rotation": {
        "path": "/rotation",
        "fields": ["rotation"]
    },
    "Scale": {
        "path": "/scale",
        "fields": ["scale"]
    }
}

# Global variable to store server response for UI updates
server_response_message = ""

# Global variable to track the currently selected object
current_selected_object = None

# Global variable to track the last known transform of the selected object
last_known_transform = {"position": None, "rotation": None, "scale": None}


class DCCPluginProperties(bpy.types.PropertyGroup):
    """
    Defines custom properties for the Blender add-on UI, allowing users to
    select transformation options and modify object properties interactively.
    """
    __annotations__ = {
        "endpoint": bpy.props.EnumProperty(
            name="Endpoint",
            items=[(key, key, "") for key in ENDPOINTS.keys()],
            default="Full Transform"
        ),
        "position": bpy.props.FloatVectorProperty(
            name="Position",
            subtype='TRANSLATION',
            default=(0.0, 0.0, 0.0),
            update=lambda self, context: self.update_object_transform(context)
        ),
        "rotation": bpy.props.FloatVectorProperty(
            name="Rotation",
            subtype='EULER',
            default=(0.0, 0.0, 0.0),
            update=lambda self, context: self.update_object_transform(context)
        ),
        "scale": bpy.props.FloatVectorProperty(
            name="Scale",
            subtype='XYZ',
            default=(1.0, 1.0, 1.0),
            update=lambda self, context: self.update_object_transform(context)
        )
    }

    def update_object_transform(self, context):
        """
        Updates the selected object's transform properties in Blender
        when the user modifies them in the UI.
        """
        global current_selected_object
        obj = context.active_object

        # Only update the object if it matches the currently selected object
        if obj and obj == current_selected_object:
            if "position" in ENDPOINTS[self.endpoint]["fields"]:
                obj.location = self.position
            if "rotation" in ENDPOINTS[self.endpoint]["fields"]:
                obj.rotation_euler = self.rotation
            if "scale" in ENDPOINTS[self.endpoint]["fields"]:
                obj.scale = self.scale

            # Update the last known transform
            update_last_known_transform(obj)


class DCCPluginPanel(bpy.types.Panel):
    """
    Creates a UI panel in Blender's sidebar under the "DCC Plugin"
    category, allowing users to modify transformation properties
    and send them to a server.
    """
    bl_label = "DCC Plugin"
    bl_idname = "VIEW3D_PT_dcc_plugin"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DCC Plugin"

    def draw(self, context):
        """
        Renders the UI elements in the panel, including transformation fields
        and a submission button.
        """
        layout = self.layout
        scene = context.scene
        props = scene.dcc_plugin
        endpoint_info = ENDPOINTS[props.endpoint]

        layout.prop(props, "endpoint")

        # Dynamically show only relevant fields
        if "position" in endpoint_info["fields"]:
            layout.prop(props, "position")
        if "rotation" in endpoint_info["fields"]:
            layout.prop(props, "rotation")
        if "scale" in endpoint_info["fields"]:
            layout.prop(props, "scale")

        layout.operator(
            "dcc.send_transform",
            text="Submit to Server",
            icon="EXPORT"
        )

        # Display the last received server response
        global server_response_message
        if server_response_message:
            layout.label(
                text=f"Server: {server_response_message}",
                icon="INFO"
            )


class SendTransformOperator(bpy.types.Operator):
    """
    Operator for sending transformation data of the selected object
    to the FastAPI server.
    """
    bl_idname = "dcc.send_transform"
    bl_label = "Send Transform Data"

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({"WARNING"}, "No object selected!")
            return {"CANCELLED"}

        props = context.scene.dcc_plugin
        endpoint_info = ENDPOINTS[props.endpoint]

        # Prepare transform data dynamically
        transform_data = {"object": obj.name, "transform": {}}
        for field in endpoint_info["fields"]:
            transform_data["transform"][field] = list(getattr(props, field))

        # Start request in a new thread
        thread = threading.Thread(
            target=self.send_request,
            args=(endpoint_info["path"], transform_data)
        )
        thread.start()

        return {"FINISHED"}

    def send_request(self, endpoint, transform_data):
        """
        Sends the transformation data to the FastAPI server
        and updates the UI with the response.
        """
        global server_response_message

        try:
            response = requests.post(
                SERVER_URL + endpoint,
                json=transform_data
            )
            server_response_message = (
                f"{response.status_code}: {response.text}"
            )
            print(f"Server Response: {server_response_message}")

        except requests.exceptions.RequestException as e:
            server_response_message = f"Error: {e}"
            print(f"Request failed: {e}")

        # Update the UI
        bpy.app.timers.register(update_ui, first_interval=0.5)


def update_ui():
    """
    Forces Blender to redraw the UI to display the latest server response.
    """
    bpy.context.area.tag_redraw()
    return None  # Stop the timer after the first execution


def update_last_known_transform(obj):
    """
    Updates the last known transform of the selected object.
    """
    global last_known_transform
    last_known_transform["position"] = obj.location.copy()
    last_known_transform["rotation"] = obj.rotation_euler.copy()
    last_known_transform["scale"] = obj.scale.copy()


def update_plugin_properties_from_object(scene):
    """
    Updates the plugin properties when the user selects a different
    object in Blender.
    """
    global current_selected_object, last_known_transform
    obj = bpy.context.active_object

    if obj:
        # Check if the selected object has changed
        if obj != current_selected_object:
            current_selected_object = obj
            update_last_known_transform(obj)

            # Update the plugin properties
            props = scene.dcc_plugin
            props.position = obj.location
            props.rotation = obj.rotation_euler
            props.scale = obj.scale

        # Check if the object's transform has changed
        elif (
            obj.location != last_known_transform["position"]
            or obj.rotation_euler != last_known_transform["rotation"]
            or obj.scale != last_known_transform["scale"]
        ):
            update_last_known_transform(obj)

            # Update the plugin properties
            props = scene.dcc_plugin
            props.position = obj.location
            props.rotation = obj.rotation_euler
            props.scale = obj.scale


def register():
    """
    Registers the add-on classes and properties with Blender.
    """
    bpy.utils.register_class(DCCPluginProperties)
    bpy.utils.register_class(DCCPluginPanel)
    bpy.utils.register_class(SendTransformOperator)
    bpy.types.Scene.dcc_plugin = bpy.props.PointerProperty(
        type=DCCPluginProperties
    )
    bpy.app.handlers.depsgraph_update_post.append(
        update_plugin_properties_from_object
    )


def unregister():
    """
    Unregisters the add-on classes and properties from Blender.
    """
    bpy.utils.unregister_class(DCCPluginProperties)
    bpy.utils.unregister_class(DCCPluginPanel)
    bpy.utils.unregister_class(SendTransformOperator)
    del bpy.types.Scene.dcc_plugin
    bpy.app.handlers.depsgraph_update_post.remove(
        update_plugin_properties_from_object
    )


if __name__ == "__main__":
    register()
