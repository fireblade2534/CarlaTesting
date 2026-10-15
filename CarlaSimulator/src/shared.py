
import carla

from src.custom_sensors import UltrasonicSensor

class EgoCar:

    def __init__(self, world: carla.World):
        bp = world.get_blueprint_library();

        self.ego_bp = bp.find("vehicle.lincoln.mkz_2020")
        self.ego_bp.set_attribute("role_name", "hero")
        self.ego_bp.set_attribute("ros_name", "hero")

        self.ego = None

    def spawn_sensors(self, world: carla.World):
        bp = world.get_blueprint_library();

        self.camera_bp = bp.find("sensor.camera.rgb")
        self.camera_bp.set_attribute("ros_name", "front_camera")
        self.camera_bp.set_attribute("image_size_x", "640")
        self.camera_bp.set_attribute("image_size_y", "480")
    
        self.camera = world.spawn_actor(
            self.camera_bp,
            carla.Transform(carla.Location(x=1.5, z=2.2)),
            attach_to=self.ego,
        )
        self.camera.enable_for_ros()

        self.ultrasonic = UltrasonicSensor(world)
        self.ultrasonic.set_attribute("ros_name", "front_distance")

        self.ultrasonic.spawn_actor(
            world,
            carla.Transform(carla.Location(x=1.5, z=2.2)),
            self.ego,
        )

    def try_spawn(self, world: carla.World, transform: carla.Transform):
        self.ego = world.try_spawn_actor(self.ego_bp, transform)

        if self.ego is None:
            return None

        self.ego.set_autopilot(False)
        self.ego.apply_control(carla.VehicleControl(brake=1.0))

        return self.ego

        
