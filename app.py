from flask import Flask, Response, jsonify, render_template

from vision.stream import VideoStream


app = Flask(__name__)

video_stream = VideoStream()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        video_stream.generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/api/status")
def status():
    return jsonify({
        "project": "Computer Vision Object Tracker",
        "status": "running"
    })


@app.route("/api/metrics")
def metrics():
    return jsonify(video_stream.latest_data)


@app.route("/api/reset", methods=["POST"])
def reset_tracking():
    video_stream.reset_tracking()

    return jsonify({
        "status": "reset",
        "message": "Tracking session reset successfully"
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )