from ultralytics import YOLO

model = YOLO("yolov8n-pose.pt")

def detect_pose(image):

    results = model(image)

    poses = []

    for r in results:

        if r.keypoints is None:
            continue

        keypoints = r.keypoints.xy.cpu().numpy()

        for kp in keypoints:
            poses.append(kp)

    return poses