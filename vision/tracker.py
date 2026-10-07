class ObjectTracker:
    def __init__(self):
        self.previous_position = None

    def update(self, position):
        if position is None:
            return {
                "detected": False,
                "dx": 0,
                "dy": 0,
                "distance": 0,
                "direction": "STATIONARY"
            }

        center_x = position["center_x"]
        center_y = position["center_y"]

        if self.previous_position is None:
            self.previous_position = (
                center_x,
                center_y
            )

            return {
                "detected": True,
                "dx": 0,
                "dy": 0,
                "distance": 0,
                "direction": "STATIONARY"
            }

        previous_x, previous_y = self.previous_position

        dx = center_x - previous_x
        dy = center_y - previous_y

        distance = (
            dx ** 2 + dy ** 2
        ) ** 0.5

        direction = self._get_direction(dx, dy)

        self.previous_position = (
            center_x,
            center_y
        )

        return {
            "detected": True,
            "dx": dx,
            "dy": dy,
            "distance": distance,
            "direction": direction
        }

    @staticmethod
    def _get_direction(dx, dy):

        threshold = 3

        horizontal = ""
        vertical = ""

        if dx > threshold:
            horizontal = "RIGHT"
        elif dx < -threshold:
            horizontal = "LEFT"

        if dy > threshold:
            vertical = "DOWN"
        elif dy < -threshold:
            vertical = "UP"

        if horizontal and vertical:
            return f"{vertical}-{horizontal}"

        if horizontal:
            return horizontal

        if vertical:
            return vertical

        return "STATIONARY"