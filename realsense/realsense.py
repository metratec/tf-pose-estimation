import numpy as np
import pyrealsense2 as rs


class RealSense:
    def __init__(self, filters=[], laser_power=0.):
        """
        Connect to RealSense and initialize filters
        :param filters: [String, ...], default=[]: 'align_ir'/'align_color', 'decimation', 'spatial', 'temporal', hole_filling', 'colorize'
        :param laser_power: Float, default=0: Power of the laser emitter 0.0...1.0
        """
        # realsense stuff
        self.pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.infrared, 1, 640, 360, rs.format.y8, 30)
        cfg.enable_stream(rs.stream.infrared, 2, 640, 360, rs.format.y8, 30)
        cfg.enable_stream(rs.stream.depth)
        cfg.enable_stream(rs.stream.color)
        profile = self.pipe.start(cfg)
        profile.get_device().first_depth_sensor().set_option(rs.option.laser_power, 360*laser_power)  # get option range via SENSOR.get_option_range(rs.option.laser_power)

        self.intrinsics_color = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
        self.intrinsics_ir = profile.get_stream(rs.stream.infrared, 1).as_video_stream_profile().get_intrinsics()
        # camera parameters
        self.depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

        # filters to apply to depth images
        self.filters = filters
        if 'align_ir' in self.filters or 'align_color' in self.filters:
            stream = rs.stream.infrared if 'align_ir' in self.filters else rs.stream.color
            self.align = rs.align(stream)
        if 'decimation' in self.filters:
            self.decimation = rs.decimation_filter()
            self.decimation.set_option(rs.option.filter_magnitude, 4)
        if 'spatial' in self.filters:
            self.spatial = rs.spatial_filter()
            # self.spatial.set_option(rs.option.holes_fill, 3)
            self.spatial.set_option(rs.option.filter_magnitude, 5)
            self.spatial.set_option(rs.option.filter_smooth_alpha, 1)
            self.spatial.set_option(rs.option.filter_smooth_delta, 50)
        if 'temporal' in self.filters:
            self.temporal = rs.temporal_filter()
        if 'hole_filling' in self.filters:
            self.hole_filling = rs.hole_filling_filter()
        if 'colorize' in self.filters:
            self.colorizer = rs.colorizer()

    def captest(self):
        frameset = self.pipe.wait_for_frames()
        frameset = self.align.process(frameset)
        depth = frameset.get_depth_frame()
        # depth = self.spatial.process(depth)
        depth = self.temporal.process(depth)
        depth = self.hole_filling.process(depth)
        depth = self.colorizer.colorize(depth)
        return np.asanyarray(frameset.get_color_frame().get_data()), np.asanyarray(depth.get_data())

    def cap(self, which, type='rs'):
        """
        Capture an rgb and depth frame, apply filters and return as rs object or np array
        :param which: [String, ...]: Specify which images to return (in given order). 'color', 'depth', 'ir1', ir2'
            Applying the 'colorize' filter will append the colorized depth image at the end for n+1 images
        :param type: String, default='rs': return realsense datatype for images with 'rs' or convert to numpy with 'np'
        :return:
        """
        out = []
        depth_index = None
        # get set of frames from camera
        frameset = self.pipe.wait_for_frames()

        # align color and depth frame
        if 'align_ir' in self.filters or 'align_color' in self.filters:
            frameset = self.align.process(frameset)
        # separate color and depth frame

        for i, w in enumerate(which):
            if w == 'color':
                out.append(frameset.get_color_frame())
            elif w == 'depth':
                out.append(frameset.get_depth_frame())
                depth_index = i
            elif w == 'ir1':
                out.append(frameset.get_infrared_frame(1))
            elif w == 'ir2':
                out.append(frameset.get_infrared_frame(2))

        # filter depth images
        if 'decimation' in self.filters and depth_index is not None:
            out[depth_index] = self.decimation.process(out[depth_index])
        if 'spatial' in self.filters and depth_index is not None:
            out[depth_index] = self.spatial.process(out[depth_index])
        if 'temporal' in self.filters and depth_index is not None:
            out[depth_index] = self.temporal.process(out[depth_index])
        if 'hole_filling' in self.filters and depth_index is not None:
            out[depth_index] = self.hole_filling.process(out[depth_index])
        if 'colorize' in self.filters and depth_index is not None:
            out.append(self.colorizer.colorize(out[depth_index]))

        # return numpy arrays of images
        if type == 'rs':
            return out
        elif type == 'np':
            for i, o in enumerate(out):
                out[i] = np.asanyarray(o.get_data())
            return out
        else:
            return None

    def get_3d(self, depth_frame, pixel, source):
        # pixel in (row, column)
        pixel = [pixel[0], pixel[1]]

        if source == 'ir':
            intrinsics = self.intrinsics_ir
        elif source == 'color':
            intrinsics = self.intrinsics_color

        # get depth image as numpy array
        try:
            depth_frame = np.asanyarray(depth_frame.get_data())
        except AttributeError:
            pass

        # get 3d coordinates given pixel coordinates
        depth_value = depth_frame[pixel[0], pixel[1]]
        out = (rs.rs2_deproject_pixel_to_point(intrinsics, pixel, depth_value * self.depth_scale))

        return out
