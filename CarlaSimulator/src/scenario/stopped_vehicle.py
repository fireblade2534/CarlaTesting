
import carla
import time
import math

from src.shared import EgoCar

client = carla.Client("127.0.0.1", 2000)
client.set_timeout(15.0)

world = client.get_world()
bp = world.get_blueprint_library()

ego = None
obstacle = None
camera = None
collision = None
collisions = []

try:
    ego_car = EgoCar(world)

    obstacle_bp = bp.find("vehicle.tesla.model3")

    # Find two available locations in the same lane,
    # approximately 25 metres apart.
    for spawn in world.get_map().get_spawn_points():
        waypoint = world.get_map().get_waypoint(spawn.location)
        ahead = waypoint.next(25.0)

        if not ahead:
            continue

        ego = ego_car.try_spawn(world, spawn)
        if ego is None:
            continue

        target = ahead[0].transform
        target.location.z += 0.3
        obstacle = world.try_spawn_actor(obstacle_bp, target)

        if obstacle is not None:
            break

        ego.destroy()
        ego = None

    if ego is None or obstacle is None:
        raise RuntimeError("Could not find free spawn locations")
    
    obstacle.apply_control(carla.VehicleControl(hand_brake=True))

    ego_car.spawn_sensors(world)

    # Collision detector for pass/fail evaluation
    collision_bp = bp.find("sensor.other.collision")
    collision = world.spawn_actor(
        collision_bp,
        carla.Transform(),
        attach_to=ego,
    )
    collision.listen(lambda event: collisions.append(event))

    start = ego.get_location()
    print("Scenario ready!", flush=True)
    print("ROS camera: /carla/hero/front_camera/image")
    print("ROS control: /carla/hero/vehicle_control_cmd")
    print("Send throttle and brake commands from ROS 2.")

    while True:
        gap = ego.get_location().distance(obstacle.get_location())
        velocity = ego.get_velocity()
        speed = math.sqrt(
            velocity.x**2 + velocity.y**2 + velocity.z**2
        )
        traveled = ego.get_location().distance(start)

        print(
            f"Distance: {gap:.1f} m | Speed: {speed*3.6:.1f} km/h",
            flush=True
        )

        if collisions:
            print("FAIL: collision detected!")
            break

        if traveled > 8 and 5 <= gap <= 12 and speed < 0.5:
            print("PASS: vehicle stopped before obstacle!")
            break

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Scenario interrupted")

finally:
    if collision is not None:
        collision.stop()
        collision.destroy()
    if camera is not None:
        camera.destroy()
    if ego is not None:
        ego.destroy()
    if obstacle is not None:
        obstacle.destroy()
