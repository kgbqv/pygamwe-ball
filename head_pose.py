import numpy as np
import cv2
import dlib
import os
import sys
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class HeadPoseDetector:
    
    def __init__(self, webcam_instance=0, shape_predictor_path=resource_path("assets/shape_predictor_68_face_landmarks.dat")):
        self.cap = cv2.VideoCapture(webcam_instance)
        self.instance = webcam_instance
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor_path)
        self.head_pose = [0, 0, 0]

    def get_webcam(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)
        return frame

    def get_head_pose(self):
        webcam_frame = self.get_webcam()
        faces = self.detector(webcam_frame)
        for face in faces:
            landmarks = self.predictor(webcam_frame, face)
            landmarks_points = []
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                landmarks_points.append((x, y))
            landmarks_points = np.array(landmarks_points, np.int32)
            image_points = np.array([
                (landmarks.part(30).x, landmarks.part(30).y), 
                (landmarks.part(8).x, landmarks.part(8).y),
                (landmarks.part(36).x, landmarks.part(36).y),
                (landmarks.part(45).x, landmarks.part(45).y), 
                (landmarks.part(48).x, landmarks.part(48).y),
                (landmarks.part(54).x, landmarks.part(54).y)  
            ], dtype="double")
            model_points = np.array([
                (0.0, 0.0, 0.0), 
                (0.0, -330.0, -65.0), 
                (-225.0, 170.0, -135.0), 
                (225.0, 170.0, -135.0), 
                (-150.0, -150.0, -125.0), 
                (150.0, -150.0, -125.0) 
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
        try:
            rmat, jac = cv2.Rodrigues(rotation_vector)
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
            self.head_pose = angles
        except:
            pass
        return webcam_frame

    def get_face_result(self):
        return self.head_pose[1]
    def change_webcam(self):
        try: 
            self.instance+=1
        except:
            self.instance = 0
        self.cap = cv2.VideoCapture(self.instance)
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()