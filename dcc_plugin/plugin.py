from maya import cmds
import requests

class DCCPlugin:
    def __init__(self):
        self.selected_object = None
        self.server_url = "http://localhost:8000"  # Change to your server URL

    def select_object(self, object_name):
        if cmds.objExists(object_name):
            self.selected_object = object_name
            self.update_transform_controls()
        else:
            print(f"Object {object_name} does not exist.")

    def update_transform_controls(self):
        if self.selected_object:
            position = cmds.xform(self.selected_object, query=True, translation=True, worldSpace=True)
            rotation = cmds.xform(self.selected_object, query=True, rotation=True, worldSpace=True)
            scale = cmds.xform(self.selected_object, query=True, scale=True)
            # Update UI controls with the current transforms (not implemented here)
            print(f"Updated transforms for {self.selected_object}: Position {position}, Rotation {rotation}, Scale {scale}")

    def submit_transform(self):
        if self.selected_object:
            position = cmds.xform(self.selected_object, query=True, translation=True, worldSpace=True)
            rotation = cmds.xform(self.selected_object, query=True, rotation=True, worldSpace=True)
            scale = cmds.xform(self.selected_object, query=True, scale=True)
            data = {
                "object": self.selected_object,
                "transform": {
                    "position": position,
                    "rotation": rotation,
                    "scale": scale
                }
            }
            response = requests.post(f"{self.server_url}/transform", json=data)
            if response.status_code == 200:
                print("Transform data submitted successfully.")
            else:
                print(f"Failed to submit transform data: {response.status_code}")

# Example usage
plugin = DCCPlugin()
plugin.select_object("pCube1")  # Replace with actual object name
plugin.submit_transform()