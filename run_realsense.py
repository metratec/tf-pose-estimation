import argparse
import time
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from realsense.realsense import RealSense
from pose3d.human3d import Human3D


parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
parser.add_argument('--camera', type=int, default=0)

parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
args = parser.parse_args()

# TODO
# TODO write human3d into json -> send to ROS via mqtt -> take from mqtt bridge and turn (automatically) into message -> create node that turns human into tf (or just vis. markers) -> show in rviz
# TODO docstrings for all functions to document inputs etc. -> update README
# TODO


def main():
    fps_time = 0
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))

    rs = RealSense(filters=['align_ir', 'colorize', 'spatial', 'temporal', 'hole_filling'], laser_power=0.1)  # 'spatial' with current settings is slow
    h3d = Human3D()
    while True:
        images = rs.cap(['ir1', 'depth'], type='np')
        t = time.time()
        # image = cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB)
        image = np.repeat(images[0].reshape(images[0].shape[0], images[0].shape[1], 1), 3, axis=2)

        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)

        # TODO
        if humans:
            updated_parts = h3d.set2d(humans[0], timestamp=t, threshold=0.1, dim=(360, 640))
            if 5 in updated_parts:
                # print left shoulder coordinates
                pt = rs.get_3d(images[1], h3d.body_parts[5].pixel_coordinates, 'ir')
                h3d.set3d(5, pt)
                print('image: ', h3d.body_parts[5].pixel_coordinates)
                print('3d: ', h3d.body_parts[5].camera_coordinates)
            else:
                print('No left shoulder found')
        # TODO

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('rgb', image)
        cv2.imshow('depth', images[2])
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
