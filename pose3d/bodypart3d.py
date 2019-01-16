import time


class BodyPart3D:
    def __init__(self, id):
        self.id = id
        self.image_coordinates = (None, None)  # (row, column) in relative coordinates 0.0...1.0 of image size
        self.pixel_coordinates = (None, None)  # (row, column) image_coordinates as integers
        self.camera_coordinates = (0.0, 0.0, 0.0)  # (x, y, z)
        self.timestamp = (0, 0)  # (seconds, nanoseconds) last time image coordinates were set

    def set_pixel_coordinates(self, rows, columns):
        """
        Convenience method to set actual pixel positions from image coordinates and passed image dimensions
        :param rows: Int: Number of rows of the original image
        :param columns: Int: Number of columns of the original image
        """""
        self.pixel_coordinates = (int(self.image_coordinates[0] * rows), int(self.image_coordinates[1] * columns))

    def set_image_coordinates(self, row_rel, col_rel, timestamp):
        self.image_coordinates = (row_rel, col_rel)
        secs, nsecs = divmod(timestamp, 1)
        self.timestamp = (int(secs), int(nsecs * 10**9))
