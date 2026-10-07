import math
import time


class MotionAnalyzer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.total_distance = 0.0
        self.frames_tracked = 0

        self.start_position = None
        self.current_position = None

        self.previous_time = None

        self.speed = 0.0
        self.previous_speed = 0.0
        self.acceleration = 0.0

        self.max_speed = 0.0
        self.speed_sum = 0.0

        self.tracking_start_time = None
        self.tracking_duration = 0.0

    def update(self, position):
        current_time = time.time()

        if position is None:
            return {
                "distance": 0.0,
                "total_distance": self.total_distance,
                "frames_tracked": self.frames_tracked,
                "displacement": self._calculate_displacement(),
                "speed": 0.0,
                "average_speed": self._calculate_average_speed(),
                "max_speed": self.max_speed,
                "acceleration": 0.0,
                "tracking_duration": self.tracking_duration
            }

        current = (
            position["center_x"],
            position["center_y"]
        )

        if self.start_position is None:
            self.start_position = current
            self.tracking_start_time = current_time

        distance = 0.0

        if self.current_position is not None:

            dx = (
                current[0]
                - self.current_position[0]
            )

            dy = (
                current[1]
                - self.current_position[1]
            )

            distance = math.sqrt(
                dx ** 2 + dy ** 2
            )

            self.total_distance += distance

            if self.previous_time is not None:

                elapsed = (
                    current_time
                    - self.previous_time
                )

                if elapsed > 0:

                    current_speed = (
                        distance / elapsed
                    )

                    self.previous_speed = self.speed

                    self.speed = current_speed

                    self.acceleration = (
                        self.speed
                        - self.previous_speed
                    ) / elapsed

        self.current_position = current
        self.previous_time = current_time

        self.frames_tracked += 1

        self.speed_sum += self.speed

        if self.speed > self.max_speed:
            self.max_speed = self.speed

        if self.tracking_start_time is not None:
            self.tracking_duration = (
                current_time
                - self.tracking_start_time
            )

        return {
            "distance": distance,
            "total_distance": self.total_distance,
            "frames_tracked": self.frames_tracked,
            "displacement": self._calculate_displacement(),
            "speed": self.speed,
            "average_speed": self._calculate_average_speed(),
            "max_speed": self.max_speed,
            "acceleration": self.acceleration,
            "tracking_duration": self.tracking_duration
        }

    def _calculate_displacement(self):
        if (
            self.start_position is None
            or self.current_position is None
        ):
            return 0.0

        dx = (
            self.current_position[0]
            - self.start_position[0]
        )

        dy = (
            self.current_position[1]
            - self.start_position[1]
        )

        return math.sqrt(
            dx ** 2 + dy ** 2
        )

    def _calculate_average_speed(self):
        if self.tracking_duration <= 0:
            return 0.0

        return (
            self.total_distance
            / self.tracking_duration
        )