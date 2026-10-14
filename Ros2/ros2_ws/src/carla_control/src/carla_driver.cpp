
#include <chrono>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "carla_msgs/msg/carla_ego_vehicle_control.hpp"

using namespace std::chrono_literals;

class CarlaDriver : public rclcpp::Node {
    private:
        rclcpp::Publisher<carla_msgs::msg::CarlaEgoVehicleControl>::SharedPtr control_publisher;
        rclcpp::TimerBase::SharedPtr timer;

        void control_loop() {
            if (control_publisher->get_subscription_count() == 0) {
                return;
            }

            carla_msgs::msg::CarlaEgoVehicleControl cmd;

            cmd.header.stamp = this->get_clock()->now();

            cmd.throttle = 1.0f;
            cmd.steer = 0.0f;
            cmd.brake = 0.0f;

            control_publisher->publish(cmd);
        }

    public:
        CarlaDriver() : Node("carla_driver") {
            control_publisher = this->create_publisher<carla_msgs::msg::CarlaEgoVehicleControl>(
                "/carla/hero/vehicle_control_cmd",
                10
            );

            timer = this->create_wall_timer(
                100ms,
                std::bind(&CarlaDriver::control_loop, this)
            );

        }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);

    auto node = std::make_shared<CarlaDriver>();

    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}