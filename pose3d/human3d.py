from tf_pose.estimator import Human
from pose3d.bodypart3d import BodyPart3D
import time
import json


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
                self.body_parts[i].set_image_coordinates(bp.y, bp.x, timestamp)
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

    def to_json(self):
        secs, nsecs = divmod(time.time(), 1)
        secs = int(secs)
        nsecs = int(nsecs * 10**9)
        return json.dumps(
            {
                "header": {"stamp": {"secs": secs, "nsecs": nsecs}, "frame_id": "realsense", "seq": 0}, "id": 0,
                "body_part": [
                {"stamp": {"secs": self.body_parts[0].timestamp[0], "nsecs": self.body_parts[0].timestamp[1]}, "id": self.body_parts[0].id,
                 "x": self.body_parts[0].camera_coordinates[0], "y": self.body_parts[0].camera_coordinates[1], "z": self.body_parts[0].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[1].timestamp[0], "nsecs": self.body_parts[1].timestamp[1]}, "id": self.body_parts[1].id,
                 "x": self.body_parts[1].camera_coordinates[0], "y": self.body_parts[1].camera_coordinates[1], "z": self.body_parts[1].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[2].timestamp[0], "nsecs": self.body_parts[2].timestamp[1]}, "id": self.body_parts[2].id,
                 "x": self.body_parts[2].camera_coordinates[0], "y": self.body_parts[2].camera_coordinates[1], "z": self.body_parts[2].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[3].timestamp[0], "nsecs": self.body_parts[3].timestamp[1]}, "id": self.body_parts[3].id,
                 "x": self.body_parts[3].camera_coordinates[0], "y": self.body_parts[3].camera_coordinates[1], "z": self.body_parts[3].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[4].timestamp[0], "nsecs": self.body_parts[4].timestamp[1]}, "id": self.body_parts[4].id,
                 "x": self.body_parts[4].camera_coordinates[0], "y": self.body_parts[4].camera_coordinates[1], "z": self.body_parts[4].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[5].timestamp[0], "nsecs": self.body_parts[5].timestamp[1]}, "id": self.body_parts[5].id,
                 "x": self.body_parts[5].camera_coordinates[0], "y": self.body_parts[5].camera_coordinates[1], "z": self.body_parts[5].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[6].timestamp[0], "nsecs": self.body_parts[6].timestamp[1]}, "id": self.body_parts[6].id,
                 "x": self.body_parts[6].camera_coordinates[0], "y": self.body_parts[6].camera_coordinates[1], "z": self.body_parts[6].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[7].timestamp[0], "nsecs": self.body_parts[7].timestamp[1]}, "id": self.body_parts[7].id,
                 "x": self.body_parts[7].camera_coordinates[0], "y": self.body_parts[7].camera_coordinates[1], "z": self.body_parts[7].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[8].timestamp[0], "nsecs": self.body_parts[8].timestamp[1]}, "id": self.body_parts[8].id,
                 "x": self.body_parts[8].camera_coordinates[0], "y": self.body_parts[8].camera_coordinates[1], "z": self.body_parts[8].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[9].timestamp[0], "nsecs": self.body_parts[9].timestamp[1]}, "id": self.body_parts[9].id,
                 "x": self.body_parts[9].camera_coordinates[0], "y": self.body_parts[9].camera_coordinates[1], "z": self.body_parts[9].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[10].timestamp[0], "nsecs": self.body_parts[10].timestamp[1]}, "id": self.body_parts[10].id,
                 "x": self.body_parts[10].camera_coordinates[0], "y": self.body_parts[10].camera_coordinates[1], "z": self.body_parts[10].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[11].timestamp[0], "nsecs": self.body_parts[11].timestamp[1]}, "id": self.body_parts[11].id,
                 "x": self.body_parts[11].camera_coordinates[0], "y": self.body_parts[11].camera_coordinates[1], "z": self.body_parts[11].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[12].timestamp[0], "nsecs": self.body_parts[12].timestamp[1]}, "id": self.body_parts[12].id,
                 "x": self.body_parts[12].camera_coordinates[0], "y": self.body_parts[12].camera_coordinates[1], "z": self.body_parts[12].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[13].timestamp[0], "nsecs": self.body_parts[13].timestamp[1]}, "id": self.body_parts[13].id,
                 "x": self.body_parts[13].camera_coordinates[0], "y": self.body_parts[13].camera_coordinates[1], "z": self.body_parts[13].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[14].timestamp[0], "nsecs": self.body_parts[14].timestamp[1]}, "id": self.body_parts[14].id,
                 "x": self.body_parts[14].camera_coordinates[0], "y": self.body_parts[14].camera_coordinates[1], "z": self.body_parts[14].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[15].timestamp[0], "nsecs": self.body_parts[15].timestamp[1]}, "id": self.body_parts[15].id,
                 "x": self.body_parts[15].camera_coordinates[0], "y": self.body_parts[15].camera_coordinates[1], "z": self.body_parts[15].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[16].timestamp[0], "nsecs": self.body_parts[16].timestamp[1]}, "id": self.body_parts[16].id,
                 "x": self.body_parts[16].camera_coordinates[0], "y": self.body_parts[16].camera_coordinates[1], "z": self.body_parts[16].camera_coordinates[2]},
                {"stamp": {"secs": self.body_parts[17].timestamp[0], "nsecs": self.body_parts[17].timestamp[1]}, "id": self.body_parts[17].id,
                 "x": self.body_parts[17].camera_coordinates[0], "y": self.body_parts[17].camera_coordinates[1], "z": self.body_parts[17].camera_coordinates[2]}]
            }
        )
