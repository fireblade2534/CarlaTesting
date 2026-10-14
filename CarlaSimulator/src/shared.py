
import carla

class EgoCar:

    def __init__(self, world: carla.World):
        bp = world.get_blueprint_library();

        self.ego_bp = bp.find("vehicle.lincoln.mkz_2020")
        self.ego_bp.set_attribute("role_name", "hero")
        self.ego_bp.set_attribute("ros_name", "hero")

