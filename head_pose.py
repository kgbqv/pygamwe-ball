import numpy as np
import cv2
import dlib

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

head_pose = [0,0,0]
#[x,y,z] = [0,0,0]

def get_webcam():
    ret,frame = cap.read()
    fraeme = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #scale down a bit
    fraeme = cv2.resize(fraeme, (0, 0), fx=0.3, fy=0.3)
    return fraeme

def get_head_pose():
    global head_pose
    webcam_frame  = get_webcam()
    faces = detector(webcam_frame)
    for face in faces:
        landmarks = predictor(webcam_frame, face)
        landmarks_points = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmarks_points.append((x, y))
        landmarks_points = np.array(landmarks_points, np.int32)
        image_points = np.array([
            (landmarks.part(30).x, landmarks.part(30).y),  # Nose tip
            (landmarks.part(8).x, landmarks.part(8).y),  # Chin
            (landmarks.part(36).x, landmarks.part(36).y),  # Left eye left corner
            (landmarks.part(45).x, landmarks.part(45).y),  # Right eye right corner
            (landmarks.part(48).x, landmarks.part(48).y),  # Left Mouth corner
            (landmarks.part(54).x, landmarks.part(54).y)  # Right mouth corner
        ], dtype="double")
        model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (-225.0, 170.0, -135.0),  # Left eye left corner
            (225.0, 170.0, -135.0),  # Right eye right corner
            (-150.0, -150.0, -125.0),  # Left Mouth corner
            (150.0, -150.0, -125.0)  # Right mouth corner
        ])
        size = webcam_frame.shape
        focal_length = size[1]
        center = (size[1] // 2, size[0] // 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype="double"
        )
        dist_coeffs = np.zeros((4, 1))
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                      dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                            translation_vector, camera_matrix, dist_coeffs)
        for p in image_points:
            cv2.circle(webcam_frame, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)
        p1 = (int(image_points[0][0]), int(image_points[0][1]))
        p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
        cv2.line(webcam_frame, p1, p2, (255, 0, 0), 2)
    #get head pose
    try:
        rmat, jac = cv2.Rodrigues(rotation_vector)
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
        head_pose = angles
    except:
        pass
    return webcam_frame
def get_face_result():
    return head_pose[1]