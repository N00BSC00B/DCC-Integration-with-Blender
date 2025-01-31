import unittest
from server.app import app

class TestServerEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_transform_endpoint(self):
        response = self.app.post('/transform', json={
            'position': [1, 2, 3],
            'rotation': [0, 0, 0],
            'scale': [1, 1, 1]
        })
        self.assertEqual(response.status_code, 200)

    def test_translation_endpoint(self):
        response = self.app.post('/translation', json={'position': [1, 2, 3]})
        self.assertEqual(response.status_code, 200)

    def test_rotation_endpoint(self):
        response = self.app.post('/rotation', json={'rotation': [0, 0, 0]})
        self.assertEqual(response.status_code, 200)

    def test_scale_endpoint(self):
        response = self.app.post('/scale', json={'scale': [1, 1, 1]})
        self.assertEqual(response.status_code, 200)

    def test_file_path_endpoint(self):
        response = self.app.get('/file-path')
        self.assertEqual(response.status_code, 200)

    def test_add_item_endpoint(self):
        response = self.app.post('/add-item', json={'name': 'item1', 'quantity': 10})
        self.assertEqual(response.status_code, 200)

    def test_remove_item_endpoint(self):
        response = self.app.post('/remove-item', json={'name': 'item1'})
        self.assertEqual(response.status_code, 200)

    def test_update_quantity_endpoint(self):
        response = self.app.post('/update-quantity', json={'name': 'item1', 'new_quantity': 5})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()