from vision.tracker import ObjectTracker


def test_tracker_initializes():
    tracker = ObjectTracker()

    assert tracker is not None


def test_tracker_first_position():
    tracker = ObjectTracker()

    result = tracker.update({
        "center_x": 100,
        "center_y": 100
    })

    assert result["detected"] is True
    assert result["dx"] == 0
    assert result["dy"] == 0
    assert result["distance"] == 0
    assert result["direction"] == "STATIONARY"


def test_tracker_calculates_movement():
    tracker = ObjectTracker()

    tracker.update({
        "center_x": 100,
        "center_y": 100
    })

    result = tracker.update({
        "center_x": 130,
        "center_y": 140
    })

    assert result["dx"] == 30
    assert result["dy"] == 40
    assert result["distance"] == 50


def test_tracker_detects_right_movement():
    tracker = ObjectTracker()

    tracker.update({
        "center_x": 100,
        "center_y": 100
    })

    result = tracker.update({
        "center_x": 120,
        "center_y": 100
    })

    assert result["direction"] == "RIGHT"


def test_tracker_detects_up_movement():
    tracker = ObjectTracker()

    tracker.update({
        "center_x": 100,
        "center_y": 100
    })

    result = tracker.update({
        "center_x": 100,
        "center_y": 80
    })

    assert result["direction"] == "UP"


def test_tracker_detects_diagonal_movement():
    tracker = ObjectTracker()

    tracker.update({
        "center_x": 100,
        "center_y": 100
    })

    result = tracker.update({
        "center_x": 120,
        "center_y": 80
    })

    assert result["direction"] == "UP-RIGHT"