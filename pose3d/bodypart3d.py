import time


class BodyPart3D:
    def __init__(self, id):
        self.id = id
        self.image_coordinates = None  # (row, column) in relative coordinates 0.0...1.0 of image size
        self.pixel_coordinates = None  # (row, column) image_coordinates as integers
        self.camera_coordinates = None  # (x, y, z)
        self.timestamp = time.time()

    def set_pixel_coordinates(self, rows, columns):
        self.pixel_coordinates = (int(self.image_coordinates[0] * rows), int(self.image_coordinates[1] * columns))
