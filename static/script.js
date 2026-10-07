const elements = {
    detected: document.getElementById("detected"),
    direction: document.getElementById("direction"),
    speed: document.getElementById("speed"),
    fps: document.getElementById("fps"),
    totalDistance: document.getElementById("total-distance"),
    displacement: document.getElementById("displacement"),

    averageSpeed: document.getElementById("average-speed"),
    maxSpeed: document.getElementById("max-speed"),
    acceleration: document.getElementById("acceleration"),
    trackingDuration: document.getElementById("tracking-duration"),
    trackedFrames: document.getElementById("tracked-frames"),
    frameSize: document.getElementById("frame-size"),

    centerX: document.getElementById("center-x"),
    centerY: document.getElementById("center-y"),

    cameraStatus: document.getElementById("camera-status"),

    resetTracking:
        document.getElementById("reset-tracking"),

    trajectoryCanvas:
        document.getElementById("trajectoryCanvas"),

    trajectoryEmpty:
        document.getElementById("trajectory-empty")
};


const canvas =
    elements.trajectoryCanvas;

const context =
    canvas.getContext("2d");


let trajectory = [];

let lastKnownDimensions = {
    width: 640,
    height: 480
};


function formatNumber(value, decimals = 1) {

    const number = Number(value);

    if (!Number.isFinite(number)) {
        return "0.0";
    }

    return number.toFixed(decimals);
}


function updateTelemetry(data) {

    if (!data || typeof data !== "object") {
        return;
    }


    const detected =
        Boolean(data.detected);


    elements.detected.textContent =
        detected
            ? "DETECTED"
            : "WAITING";


    elements.detected.style.color =
        detected
            ? "var(--accent)"
            : "var(--text-muted)";


    elements.direction.textContent =
        data.direction || "—";


    elements.speed.textContent =
        formatNumber(data.speed);


    elements.fps.textContent =
        formatNumber(data.fps);


    elements.totalDistance.textContent =
        formatNumber(data.total_distance);


    elements.displacement.textContent =
        formatNumber(data.displacement);


    elements.averageSpeed.textContent =
        formatNumber(data.average_speed);


    elements.maxSpeed.textContent =
        formatNumber(data.max_speed);


    elements.acceleration.textContent =
        formatNumber(data.acceleration);


    elements.trackingDuration.textContent =
        formatNumber(data.tracking_duration);


    elements.trackedFrames.textContent =
        Number.isFinite(Number(data.tracked_frames))
            ? Math.round(Number(data.tracked_frames))
            : "0";


    const frameWidth =
        Number(data.frame_width);

    const frameHeight =
        Number(data.frame_height);


    if (
        Number.isFinite(frameWidth) &&
        Number.isFinite(frameHeight)
    ) {

        lastKnownDimensions.width =
            frameWidth;

        lastKnownDimensions.height =
            frameHeight;


        elements.frameSize.textContent =
            `${Math.round(frameWidth)} × ${Math.round(frameHeight)}`;
    }


    if (
        Number.isFinite(Number(data.center_x)) &&
        Number.isFinite(Number(data.center_y))
    ) {

        elements.centerX.textContent =
            Math.round(Number(data.center_x));

        elements.centerY.textContent =
            Math.round(Number(data.center_y));

    } else {

        elements.centerX.textContent = "—";
        elements.centerY.textContent = "—";
    }


    elements.cameraStatus.textContent =
        detected
            ? "OBJECT LOCK"
            : "SCANNING";


    if (Array.isArray(data.trajectory)) {

        trajectory =
            data.trajectory
                .filter(
                    point =>
                        point &&
                        Number.isFinite(Number(point.x)) &&
                        Number.isFinite(Number(point.y))
                )
                .map(point => ({
                    x: Number(point.x),
                    y: Number(point.y)
                }));
    }


    drawTrajectory();
}


async function fetchMetrics() {

    try {

        const response =
            await fetch(
                "/api/metrics",
                {
                    cache: "no-store"
                }
            );


        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        updateTelemetry(data);

    } catch (error) {

        console.error(
            "Telemetry request failed:",
            error
        );

        elements.cameraStatus.textContent =
            "API OFFLINE";
    }
}


async function resetTracking() {

    if (!elements.resetTracking) {
        return;
    }


    elements.resetTracking.disabled = true;


    try {

        const response =
            await fetch(
                "/api/reset",
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        trajectory = [];


        updateTelemetry({
            detected: false,
            direction: "STATIONARY",

            speed: 0,
            average_speed: 0,
            max_speed: 0,
            acceleration: 0,

            tracking_duration: 0,
            tracked_frames: 0,

            total_distance: 0,
            displacement: 0,

            center_x: 0,
            center_y: 0,

            frame_width:
                lastKnownDimensions.width,

            frame_height:
                lastKnownDimensions.height,

            trajectory: []
        });


        elements.cameraStatus.textContent =
            "SESSION RESET";


    } catch (error) {

        console.error(
            "Reset request failed:",
            error
        );


        elements.cameraStatus.textContent =
            "RESET FAILED";

    } finally {

        setTimeout(
            () => {

                elements.resetTracking.disabled =
                    false;

            },
            500
        );
    }
}


function resizeCanvas() {

    const rect =
        canvas.getBoundingClientRect();


    const devicePixelRatio =
        window.devicePixelRatio || 1;


    canvas.width =
        Math.max(
            1,
            Math.floor(
                rect.width *
                devicePixelRatio
            )
        );


    canvas.height =
        Math.max(
            1,
            Math.floor(
                rect.height *
                devicePixelRatio
            )
        );


    context.setTransform(
        devicePixelRatio,
        0,
        0,
        devicePixelRatio,
        0,
        0
    );


    drawTrajectory();
}


function drawTrajectory() {

    if (!canvas || !context) {
        return;
    }


    const rect =
        canvas.getBoundingClientRect();


    const width =
        rect.width;

    const height =
        rect.height;


    if (width <= 0 || height <= 0) {
        return;
    }


    context.clearRect(
        0,
        0,
        width,
        height
    );


    context.strokeStyle =
        "rgba(255,255,255,0.035)";

    context.lineWidth = 1;


    const gridSize = 40;


    for (
        let x = 0;
        x <= width;
        x += gridSize
    ) {

        context.beginPath();

        context.moveTo(
            x,
            0
        );

        context.lineTo(
            x,
            height
        );

        context.stroke();
    }


    for (
        let y = 0;
        y <= height;
        y += gridSize
    ) {

        context.beginPath();

        context.moveTo(
            0,
            y
        );

        context.lineTo(
            width,
            y
        );

        context.stroke();
    }


    if (trajectory.length === 0) {

        elements.trajectoryEmpty.style.opacity =
            "1";

        return;
    }


    elements.trajectoryEmpty.style.opacity =
        "0";


    const frameWidth =
        lastKnownDimensions.width || 640;

    const frameHeight =
        lastKnownDimensions.height || 480;


    const scaleX =
        width / frameWidth;

    const scaleY =
        height / frameHeight;


    context.beginPath();


    trajectory.forEach(
        (point, index) => {

            const x =
                point.x * scaleX;

            const y =
                point.y * scaleY;


            if (index === 0) {

                context.moveTo(
                    x,
                    y
                );

            } else {

                context.lineTo(
                    x,
                    y
                );
            }
        }
    );


    context.strokeStyle =
        "rgba(112,225,197,0.85)";

    context.lineWidth = 2;

    context.lineJoin =
        "round";

    context.lineCap =
        "round";

    context.stroke();


    trajectory.forEach(
        (point, index) => {

            const x =
                point.x * scaleX;

            const y =
                point.y * scaleY;


            const progress =
                index /
                Math.max(
                    trajectory.length - 1,
                    1
                );


            const radius =
                index === trajectory.length - 1
                    ? 5
                    : 2;


            context.beginPath();


            context.arc(
                x,
                y,
                radius,
                0,
                Math.PI * 2
            );


            context.fillStyle =
                index === trajectory.length - 1
                    ? "#70e1c5"
                    : `rgba(
                        112,
                        225,
                        197,
                        ${0.15 + progress * 0.45}
                    )`;


            context.fill();
        }
    );


    const latest =
        trajectory[
            trajectory.length - 1
        ];


    if (latest) {

        const x =
            latest.x * scaleX;

        const y =
            latest.y * scaleY;


        context.beginPath();


        context.arc(
            x,
            y,
            10,
            0,
            Math.PI * 2
        );


        context.strokeStyle =
            "rgba(112,225,197,0.25)";

        context.lineWidth = 1;

        context.stroke();
    }
}


if (elements.resetTracking) {

    elements.resetTracking.addEventListener(
        "click",
        resetTracking
    );
}


window.addEventListener(
    "resize",
    resizeCanvas
);


resizeCanvas();

fetchMetrics();


setInterval(
    fetchMetrics,
    250
);