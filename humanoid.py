from vpython import *
import time
import math


class Humanoid:
    def __init__(self):
        self.head_radius = 0.1
        self.body_length = 0.4
        self.arm_length = 0.3
        self.leg_length = 0.4

        self.head = sphere(pos=vector(0, self.body_length + self.head_radius * 1.5, 0),
                           radius=self.head_radius, color=color.yellow)
        self.body = cylinder(pos=vector(0, self.head.pos.y - self.head_radius, 0),
                             axis=vector(0, -self.body_length, 0),
                             radius=0.05, color=color.blue)

        self.left_arm = cylinder(pos=self.body.pos + vector(0, -self.body_length / 2 + self.head_radius * 0.2, 0),
                                 axis=vector(-self.arm_length, 0, 0),
                                 radius=0.02, color=color.red)
        self.right_arm = cylinder(pos=self.body.pos + vector(0, -self.body_length / 2 + self.head_radius * 0.2, 0),
                                  axis=vector(self.arm_length, 0, 0),
                                  radius=0.02, color=color.red)

        self.left_leg = cylinder(pos=self.body.pos + vector(0, -self.body_length, 0),
                                 axis=vector(0.1, -self.leg_length, 0),
                                 radius=0.02, color=color.green)
        self.right_leg = cylinder(pos=self.body.pos + vector(0, -self.body_length, 0),
                                  axis=vector(-0.1, -self.leg_length, 0),
                                  radius=0.02, color=color.green)

        self.current_angles = {
            'left_arm': 0,
            'right_arm': 0,
            'left_leg': 0,
            'right_leg': 0
        }

    def move_joint(self, joint_name, target_angle, duration):
        start_angle = self.current_angles[joint_name]
        end_angle = start_angle + target_angle

        steps = 50
        step_duration = duration / steps

        for i in range(steps):
            angle = start_angle + (target_angle * (i / steps))
            if joint_name == 'left_arm':
                self.left_arm.axis = vector(-self.arm_length * math.cos(angle), self.arm_length * math.sin(angle), 0)
                self.left_arm.pos = self.body.pos + vector(0, -self.body_length / 2 + self.head_radius * 0.2, 0)
            elif joint_name == 'right_arm':
                self.right_arm.axis = vector(self.arm_length * math.cos(angle), self.arm_length * math.sin(angle), 0)
                self.right_arm.pos = self.body.pos + vector(0, -self.body_length / 2 + self.head_radius * 0.2, 0)
            elif joint_name == 'left_leg':
                self.left_leg.axis = vector(0.1 * math.cos(angle), -self.leg_length * math.cos(angle), self.leg_length * math.sin(angle))
                self.left_leg.pos = self.body.pos + vector(0, -self.body_length, 0)
            elif joint_name == 'right_leg':
                self.right_leg.axis = vector(-0.1 * math.cos(angle), -self.leg_length * math.cos(angle), self.leg_length * math.sin(angle))
                self.right_leg.pos = self.body.pos + vector(0, -self.body_length, 0)
            rate(1 / step_duration) 

        self.current_angles[joint_name] = end_angle


    def reset_position(self):
        self.left_arm.pos = self.body.pos + vector(0, -self.body_length / 2 + self.head_radius * 0.2, 0)
        self.right_arm.pos = self.body.pos + vector(0, -self.body_length / 2 + self.head_radius * 0.2, 0)
        self.left_leg.pos = self.body.pos + vector(0, -self.body_length, 0)
        self.right_leg.pos = self.body.pos + vector(0, -self.body_length, 0)
