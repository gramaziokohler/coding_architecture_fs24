import math
import threading
import time

from compas.geometry import Frame
from compas_robots import Configuration
from rtde_control import RTDEControlInterface
from rtde_io import RTDEIOInterface
from rtde_receive import RTDEReceiveInterface


def send_commands(commands, ip="127.0.0.1"):
    print("Starting execution thread...")
    print()
    thread = threading.Thread(
        target=_send_commands_thread, args=(commands, ip), daemon=True
    )
    thread.start()


def _send_commands_thread(commands, ip="127.0.0.1"):
    ur_c = _get_rtde_control(ip)
    io = _get_rtde_io_interface(ip)

    try:
        print("Stopping current motions...")
        ur_c.stopJ(0.1)
        print("Stopped")

        grouped = group_commands(commands)
        print("Grouped {} commands in {} groups".format(len(commands), len(grouped)))
        for group in grouped:
            # print("Executing group...")
            # print(group)

            if isinstance(group, list):
                path = []
                for cmd in group:
                    path.append(
                        _get_ur_joint_values_in_order(cmd["configuration"])
                        + [cmd["speed"], cmd["accel"], cmd["blend"]]
                    )

                print(f"Sending path of length={len(path)}")
                for pt in path:
                    print(
                        " - {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(
                            *map(math.degrees, pt[:6])
                        )
                    )

                if len(path):
                    ur_c.moveJ(path)
            else:
                cmd = group
                if cmd["command"] == "wait":
                    print("Waiting {} seconds".format(cmd["wait_time"]))
                    time.sleep(cmd["wait_time"])
                    print("Wait done")
                if cmd["command"] == "set_digital_io":
                    print(
                        "Setting digital IO {} to {}".format(
                            cmd["signal"], cmd["value"]
                        )
                    )
                    io.setStandardDigitalOut(cmd["signal"], cmd["value"])
    except Exception as e:
        print("Error in execution thread: {}".format(e))


def _get_ur_joint_values_in_order(config):
    return [
        config["shoulder_pan_joint"],
        config["shoulder_lift_joint"],
        config["elbow_joint"],
        config["wrist_1_joint"],
        config["wrist_2_joint"],
        config["wrist_3_joint"],
    ]


def group_commands(commands):
    grouped_commands = []
    current_path = []

    for cmd in commands:
        if cmd["command"] == "configuration":
            current_path.append(cmd)
        else:
            if current_path:
                grouped_commands.append(current_path)
                current_path = []
            grouped_commands.append(cmd)

    if current_path:
        grouped_commands.append(current_path)

    return grouped_commands


def stop(ip="127.0.0.1"):
    ur_c = _get_rtde_control(ip)
    ur_c.stopJ(0.1)


def get_config(ip="127.0.0.1"):
    ur_r = _get_rtde_receive(ip)
    robot_joints = ur_r.getActualQ()
    config = Configuration.from_revolute_values(
        robot_joints,
        joint_names=[
            "shoulder_pan_joint",
            "shoulder_lift_joint",
            "elbow_joint",
            "wrist_1_joint",
            "wrist_2_joint",
            "wrist_3_joint",
        ],
    )
    return config


def get_tcp_offset(ip="127.0.0.1"):
    ur_c = _get_rtde_control(ip)
    tcp = ur_c.getTCPOffset()
    return tcp


def move_to_joints(config, speed, accel, nowait, ip="127.0.0.1"):
    # speed rad/s, accel rad/s^2, nowait bool
    ur_c = _get_rtde_control(ip)
    ur_c.moveJ(config.joint_values, speed, accel, nowait)


def movel_to_joints(config, speed, accel, nowait, ip="127.0.0.1"):
    # speed rad/s, accel rad/s^2, nowait bool
    ur_c = _get_rtde_control(ip)
    ur_c.moveL_FK(config.joint_values, speed, accel, nowait)


def get_digital_io(signal, ip="127.0.0.1"):
    ur_r = _get_rtde_receive(ip)
    return ur_r.getDigitalOutState(signal)


def set_digital_io(signal, value, ip="127.0.0.1"):
    io = _get_rtde_io_interface(ip)
    io.setStandardDigitalOut(signal, value)


def set_tool_digital_io(signal, value, ip="127.0.0.1"):
    io = _get_rtde_io_interface(ip)
    io.setToolDigitalOut(signal, value)


def get_tcp_frame(ip="127.0.0.1"):
    ur_r = _get_rtde_receive(ip)
    tcp = ur_r.getActualTCPPose()
    frame = Frame.from_axis_angle_vector(tcp[3:], point=tcp[0:3])
    return frame


def move_trajectory(configurations, speed, accel, blend, ur_c):
    path = []
    for config in configurations:
        path.append(config.joint_values + [speed, accel, blend])

    if len(path):
        ur_c.moveJ(path)


def start_teach_mode(ip="127.0.0.1"):
    ur_c = _get_rtde_control(ip)
    ur_c.teachMode()


def stop_teach_mode(ip="127.0.0.1"):
    ur_c = _get_rtde_control(ip)
    ur_c.endTeachMode()


ACTIVE_CONNECTIONS_CONTROL = {}
ACTIVE_CONNECTIONS_RECEIVE = {}
ACTIVE_CONNECTIONS_IOIFACE = {}


def _get_rtde_control(ip):
    return RTDEControlInterface(ip)
    # if ip not in ACTIVE_CONNECTIONS_CONTROL:
    #     ACTIVE_CONNECTIONS_CONTROL[ip] = RTDEControlInterface(ip)

    # return ACTIVE_CONNECTIONS_CONTROL[ip]


def _get_rtde_receive(ip):
    return RTDEReceiveInterface(ip)
    # if ip not in ACTIVE_CONNECTIONS_RECEIVE:
    #     ACTIVE_CONNECTIONS_RECEIVE[ip] = RTDEReceiveInterface(ip)

    # return ACTIVE_CONNECTIONS_RECEIVE[ip]


def _get_rtde_io_interface(ip):
    return RTDEIOInterface(ip)
    # if ip not in ACTIVE_CONNECTIONS_IOIFACE:
    #     ACTIVE_CONNECTIONS_IOIFACE[ip] = RTDEIOInterface(ip)

    # return ACTIVE_CONNECTIONS_IOIFACE[ip]


if __name__ == "__main__":
    ip = "127.0.0.1"
    frame = get_tcp_frame(ip)
    print(frame)
