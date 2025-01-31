import unittest
from dcc_plugin.plugin import DCCPlugin

class TestDCCPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = DCCPlugin()

    def test_object_selection(self):
        # Simulate object selection
        self.plugin.select_object("Cube")
        self.assertEqual(self.plugin.selected_object, "Cube")

    def test_transform_update(self):
        # Simulate updating transforms
        self.plugin.select_object("Cube")
        self.plugin.update_transform(position=(1, 2, 3), rotation=(0, 0, 0), scale=(1, 1, 1))
        self.assertEqual(self.plugin.get_transform(), {
            "position": (1, 2, 3),
            "rotation": (0, 0, 0),
            "scale": (1, 1, 1)
        })

    def test_submit_transform(self):
        # Simulate submitting transform data to the server
        self.plugin.select_object("Cube")
        self.plugin.update_transform(position=(1, 2, 3), rotation=(0, 0, 0), scale=(1, 1, 1))
        response = self.plugin.submit_transform()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()