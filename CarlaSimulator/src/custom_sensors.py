import carla
import roslibpy

class UltrasonicSensor:
    def __init__(self, world: carla.World):
        self.radar_bp = world.get_blueprint_library().find("sensor.other.radar")

        self.parent_name = None
        self.self_name = "ultrasonic"

        self.max_range = 50
        self.radar_bp.set_attribute("range", str(self.max_range))
        self.radar_bp.set_attribute("sensor_tick", "0.05")
        self.radar_bp.set_attribute("horizontal_fov", "15")
        self.radar_bp.set_attribute("vertical_fov", "15")

        self.ros = roslibpy.Ros(host="localhost", port=9080)
        self.ros.run()

    def set_attribute(self, attribute: str, value: str):
        match attribute:
            case "ros_name":
                self.self_name = value
            case "range":
                self.max_range = float(value)
                self.radar_bp.set_attribute(attribute, value)
            case "sensor_tick":
                self.radar_bp.set_attribute(attribute, value)
            case "fov":
                self.radar_bp.set_attribute("horizontal_fov", value)
                self.radar_bp.set_attribute("vertical_fov", value)
            case _:
                raise Exception

    def _on_radar(self, data):
        distance = min(
            (hit.depth for hit in data),
            default=self.max_range
        )
        
        self.distance_pub.publish(
            roslibpy.Message({"data": float(distance)})
        )

    def spawn_actor(self, world: carla.World, transform: carla.Transform, attach_to: carla.Actor):
        self.parent_name = attach_to.attributes.get("role_name")

        self.distance_pub = roslibpy.Topic(
            self.ros,
            f"/carla/{self.parent_name}/{self.self_name}",
            "std_msgs/msg/Float32"
        )

        self.distance_pub.advertise()

        self.radar = world.spawn_actor(
            self.radar_bp,
            transform,
            attach_to
        )
        
        self.radar.listen(lambda data: self._on_radar(data))