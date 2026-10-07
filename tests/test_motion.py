from vision.motion import MotionAnalyzer


def test_motion_analyzer_initializes():
    analyzer = MotionAnalyzer()

    assert analyzer.total_distance == 0.0
    assert analyzer.frames_tracked == 0
    assert analyzer.max_speed == 0.0
    assert analyzer.speed == 0.0
    assert analyzer.acceleration == 0.0


def test_first_position_has_zero_distance():
    analyzer = MotionAnalyzer()

    result = analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    assert result["distance"] == 0.0
    assert result["frames_tracked"] == 1


def test_motion_distance_is_calculated():
    analyzer = MotionAnalyzer()

    analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    result = analyzer.update({
        "center_x": 130,
        "center_y": 140
    })

    assert result["distance"] == 50.0
    assert result["frames_tracked"] == 2


def test_displacement_is_calculated():
    analyzer = MotionAnalyzer()

    analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    result = analyzer.update({
        "center_x": 160,
        "center_y": 180
    })

    assert result["displacement"] == 100.0


def test_speed_is_calculated():
    analyzer = MotionAnalyzer()

    analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    analyzer.previous_time -= 0.1

    result = analyzer.update({
        "center_x": 110,
        "center_y": 100
    })

    assert result["speed"] > 0


def test_max_speed_is_recorded():
    analyzer = MotionAnalyzer()

    analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    analyzer.previous_time -= 0.1

    result = analyzer.update({
        "center_x": 120,
        "center_y": 100
    })

    assert result["max_speed"] == result["speed"]


def test_tracking_duration_is_recorded():
    analyzer = MotionAnalyzer()

    analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    analyzer.tracking_start_time -= 2.0

    result = analyzer.update({
        "center_x": 110,
        "center_y": 100
    })

    assert result["tracking_duration"] >= 2.0


def test_average_speed_is_available():
    analyzer = MotionAnalyzer()

    analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    analyzer.previous_time -= 1.0

    result = analyzer.update({
        "center_x": 120,
        "center_y": 100
    })

    assert result["average_speed"] > 0


def test_no_detection_returns_safe_values():
    analyzer = MotionAnalyzer()

    result = analyzer.update(None)

    assert result["distance"] == 0.0
    assert result["speed"] == 0.0
    assert result["acceleration"] == 0.0

def test_motion_analyzer_reset():
    analyzer = MotionAnalyzer()

    analyzer.update({
        "center_x": 100,
        "center_y": 100
    })

    analyzer.update({
        "center_x": 150,
        "center_y": 100
    })

    analyzer.reset()

    assert analyzer.total_distance == 0.0
    assert analyzer.frames_tracked == 0
    assert analyzer.max_speed == 0.0
    assert analyzer.speed == 0.0
    assert analyzer.acceleration == 0.0
    assert analyzer.start_position is None
    assert analyzer.current_position is None