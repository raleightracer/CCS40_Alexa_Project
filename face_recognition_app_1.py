from deepface import DeepFace
import cv2
import os
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

db_path = "known_faces"

print("Starting webcam... Press Q to quit.")

cap = cv2.VideoCapture(0) # open camera

cap.set(3, 1280) # resolution
cap.set(4, 720)

print("Width:", cap.get(3)) # width and height ng webcam
print("Height:", cap.get(4))

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    try:
        # First, check if a face is actually present
        faces = DeepFace.extract_faces(
            img_path=frame,
            detector_backend='opencv',
            enforce_detection=False
        )

        if len(faces) > 0:
            # Proceed with recognition only if a face is visible
            result = DeepFace.find(
                img_path=frame,
                db_path=db_path,
                detector_backend='opencv',
                enforce_detection=False
            )

            if len(result) > 0: #match
                name = result[0]['identity'][0].split("\\")[-1].split(".")[0]
                cv2.putText(frame, f"Detected: {name}", (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Unknown", (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            # No face detected in frame
            cv2.putText(frame, "No face detected", (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    except Exception as e:
        cv2.putText(frame, "Unknown", (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (50, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    key = cv2.waitKey(10)
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
