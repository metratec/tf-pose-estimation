from tf_pose.estimator import Human
from pose3d.bodypart3d import BodyPart3D
import time


class Human3D:
    def __init__(self):
        self.body_parts = []
        for i in range(18):
            self.body_parts.append(BodyPart3D(i))

    def set2d(self, human, timestamp=None, threshold=0.4, dim=None):
        """Set 2d coordinates of body parts from ildoonet output"""
        # dim = (rows, columns)
        updated_parts = []

        if timestamp is None:
            timestamp = time.time()
        for i in human.body_parts:
            bp = human.body_parts[i]
            if bp.score > threshold:
                # set coordinates and timestamp
                self.body_parts[i].image_coordinates = (bp.y, bp.x)
                self.body_parts[i].timestamp = timestamp
                # also calculate pixel coordinates if dimensions of image are given
                if dim is not None:
                    self.body_parts[i].set_pixel_coordinates(dim[0], dim[1])

                updated_parts.append(i)

        return updated_parts

    def set3d(self, part, point):
        """Set 3d coordinates from realsense output"""
        x = point[1]
        y = point[0]
        z = point[2]
        self.body_parts[part].camera_coordinates = (x, y, z)
