# =========================================
# app.py
# =========================================

import cv2
import os
import csv
import time
import traceback
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    GlobalAveragePooling2D,
    Dense
)

# =========================================
# MOBILE NET V2
# =========================================
from tensorflow.keras.applications import (
    DenseNet121
)

from tensorflow.keras.applications.densenet import (
    preprocess_input
)
# =========================================
# MAIN TRY BLOCK
# =========================================
try:

    # =========================================
    # FIX RANDOMNESS
    # =========================================
    tf.random.set_seed(42)
    np.random.seed(42)

    # =========================================
    # CREATE SESSION FOLDER
    # =========================================
    os.makedirs(
        "sessions",
        exist_ok=True
    )

    # =========================================
    # SESSION CSV
    # =========================================
    session_time = time.strftime(
        "%Y%m%d_%H%M%S"
    )

    CSV_FILE = (
        f"sessions/"
        f"engagement_{session_time}.csv"
    )

    # =========================================
    # SAVE CURRENT SESSION
    # =========================================
    with open(
        "current_session.txt",
        "w"
    ) as f:

        f.write(CSV_FILE)

    # =========================================
    # CREATE CSV
    # =========================================
    with open(
        CSV_FILE,
        'w',
        newline=''
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Timestamp",
            "Student_ID",
            "Status",
            "Probability"
        ])

    # =========================================
    # YOLO MODEL
    # =========================================
    print("Loading YOLO Model...")

    yolo_model = YOLO(
        "yolov5nu.pt"
    )

    print("YOLO Loaded")

    # =========================================
    # DEEPSORT
    # =========================================
    tracker = DeepSort(
        max_age=60,
        n_init=2,
        max_cosine_distance=0.5
    )

    # =========================================
    # FACE DETECTOR
    # =========================================
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        'haarcascade_frontalface_default.xml'
    )

    # =========================================
    # MOBILENET FEATURE EXTRACTOR
    # =========================================
    print("Loading DenseNet121...")

    base_model = DenseNet121(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
    )

    x = GlobalAveragePooling2D()(
        base_model.output
    )

    output = Dense(128)(x)

    feature_model = Model(
        inputs=base_model.input,
        outputs=output
    )

    for layer in base_model.layers:
        layer.trainable = False

    print("DenseNet121 Loaded")

    # =========================================
    # LOAD RF MODEL
    # =========================================
    print("Loading Random Forest Model...")

    rf_model = joblib.load(
        "rf_model_final.pkl"
    )

    engaged_centroid = np.array(joblib.load(
        "engaged_centroid.pkl"
    ))

    disengaged_centroid = np.array(joblib.load(
        "disengaged_centroid.pkl"
    ))

    print("Random Forest Model Loaded")
    print("Centroids Loaded Successfully")

    # =========================================
    # FEATURE EXTRACTION
    # =========================================
    def extract_features(face_img):

        face = cv2.resize(
            face_img,
            (224,224)
        )

        face = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2RGB
        )

        face = preprocess_input(face)

        face = np.expand_dims(
            face,
            axis=0
        )

        features = feature_model.predict(
            face,
            verbose=0
        )

        return features.reshape(1, -1)
    def cosine_refinement(features):

        engaged_sim = cosine_similarity(
            features,
            engaged_centroid.reshape(1, -1)
        )[0][0]

        disengaged_sim = cosine_similarity(
            features,
            disengaged_centroid.reshape(1, -1)
        )[0][0]

        if engaged_sim > disengaged_sim:

            return (
                "Engaged",
                engaged_sim
            )

        return (
            "Disengaged",
            disengaged_sim
        )
    # =========================================
    # TEXT BACKGROUND
    # =========================================
    def draw_text_with_background(
        img,
        text,
        position,
        text_color,
        bg_color=(0,0,0)
    ):

        font = cv2.FONT_HERSHEY_SIMPLEX

        scale = 0.7

        thickness = 2

        (w, h), _ = cv2.getTextSize(
            text,
            font,
            scale,
            thickness
        )

        x, y = position

        cv2.rectangle(
            img,
            (x-5, y-h-10),
            (x+w+5, y+5),
            bg_color,
            -1
        )

        cv2.putText(
            img,
            text,
            (x, y),
            font,
            scale,
            text_color,
            thickness
        )

    # =========================================
    # CAMERA
    # =========================================
    print("Opening Camera...")

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    # CAMERA SETTINGS
    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        640
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        480
    )

    cap.set(
        cv2.CAP_PROP_FPS,
        30
    )

    # =========================================
    # CAMERA CHECK
    # =========================================
    if not cap.isOpened():

        print("Camera failed to open")
        print("Camera not accessible")

        cap.release()

        cv2.destroyAllWindows()

        os._exit(1)

    print("Camera Opened Successfully")

    # =========================================
    # WINDOW
    # =========================================
    window_name = (
        "Optimized Real-Time Monitoring"
    )

    try:

        cv2.namedWindow(
            window_name,
            cv2.WINDOW_NORMAL
        )

    except Exception as e:

        print("Window creation failed")
        print(e)

    cv2.resizeWindow(
        window_name,
        1100,
        650
    )

    print("Press q to quit")

    # =========================================
    # FRAME SKIP
    # =========================================
    frame_skip = 0

    # =========================================
    # PREVIOUS FRAME
    # =========================================
    previous_frame = None

    # =========================================
    # CSV LOGGING TIMER
    # =========================================
    last_logged = {}

    # =========================================
    # FAILED FRAMES
    # =========================================
    failed_frames = 0

    # =========================================
    # MAIN LOOP
    # =========================================
    while True:

        ret, frame = cap.read()

        # =========================================
        # CAMERA FAILURE
        # =========================================
        if not ret:

            failed_frames += 1

            print("Frame not received")

            time.sleep(0.1)

            if failed_frames > 20:

                print("Camera disconnected")

                cap.release()

                cv2.destroyAllWindows()

                os._exit(1)

            continue

        else:

            failed_frames = 0

        # =========================================
        # FRAME SKIP
        # =========================================
        frame_skip += 1

        if frame_skip % 2 != 0:

            if previous_frame is not None:

                cv2.imshow(
                    window_name,
                    previous_frame
                )

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            continue

        # =========================================
        # FRAME RESIZE
        # =========================================
        frame = cv2.resize(
            frame,
            (800, 450)
        )

        detections = []

        # =========================================
        # YOLO DETECTION
        # =========================================
        results = yolo_model(
            frame,
            verbose=False,
            imgsz=192,
            conf=0.5
        )

        for result in results:

            boxes = result.boxes

            for box in boxes:

                cls = int(
                    box.cls[0]
                )

                if cls == 0:

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    conf = float(
                        box.conf[0]
                    )

                    width = x2 - x1
                    height = y2 - y1

                    detections.append([
                        [
                            x1,
                            y1,
                            width,
                            height
                        ],
                        conf,
                        'person'
                    ])

        # =========================================
        # TRACKING
        # =========================================
        tracks = tracker.update_tracks(
            detections,
            frame=frame
        )

        engaged_count = 0
        total_faces = 0

        # =========================================
        # PROCESS TRACKS
        # =========================================
        for track in tracks:

            if not track.is_confirmed():
                continue

            track_id = track.track_id

            ltrb = track.to_ltrb()

            x1, y1, x2, y2 = map(
                int,
                ltrb
            )

            person_roi = frame[
                y1:y2,
                x1:x2
            ]

            if person_roi.size == 0:
                continue

            gray = cv2.cvtColor(
                person_roi,
                cv2.COLOR_BGR2GRAY
            )

            faces = (
                face_detector.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=5,
                    minSize=(30,30)
                )
            )

            draw_text_with_background(
                frame,
                f"ID: {track_id}",
                (x1, y1-15),
                (0,255,255)
            )

            for (
                fx,
                fy,
                fw,
                fh
            ) in faces:

                face = person_roi[
                    fy:fy+fh,
                    fx:fx+fw
                ]

                if face.size == 0:
                    continue

                   

                try:

                    features = extract_features(face)

                    features_df = pd.DataFrame(features)
                    if hasattr(rf_model, "feature_names_in_"):
                        features_df.columns = rf_model.feature_names_in_
                    probs = (
                        rf_model.predict_proba(
                            features_df
                        )[0]
                    )

                    rf_probability = probs[1]
                    prediction = rf_model.predict(features_df)[0]
                    total_faces += 1

                    face_box_color = (
                        0,
                        255,
                        0
                    )

                   
                    if prediction == 1:
                        label = "Engaged"
                    else:
                        label = "Disengaged"

                    probability = rf_probability        

                    if label == "Engaged":

                        text_color = (
                            0,
                            255,
                            255
                        )

                        engaged_count += 1

                    else:

                        text_color = (
                            0,
                            165,
                            255
                        )

                    cv2.rectangle(
                        person_roi,
                        (fx, fy),
                        (fx + fw, fy + fh),
                        face_box_color,
                        2
                    )

                    draw_text_with_background(
                        person_roi,
                        label,
                        (fx, fy - 10),
                        text_color
                    )

                    current_time = time.time()

                    if (
                        track_id not in last_logged
                        or
                        current_time -
                        last_logged[track_id] > 1
                    ):

                        timestamp = time.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                        with open(
                            CSV_FILE,
                            'a',
                            newline=''
                        ) as file:

                            writer = csv.writer(file)

                            writer.writerow([
                                timestamp,
                                track_id,
                                label,
                                round(probability, 2)
                            ])

                        last_logged[
                            track_id
                        ] = current_time

                except Exception as e:
                    print(e)
                    continue

        # =========================================
        # ENGAGEMENT %
        # =========================================
        if total_faces > 0:

            engagement_percentage = (
                engaged_count /
                total_faces
            ) * 100

        else:

            engagement_percentage = 0

        # =========================================
        # DISPLAY TEXT
        # =========================================
        draw_text_with_background(
            frame,
            f"Students: {total_faces}",
            (20,40),
            (255,255,255)
        )

        draw_text_with_background(
            frame,
            f"Engagement: "
            f"{engagement_percentage:.1f}%",
            (20,80),
            (0,255,255)
        )

        draw_text_with_background(
            frame,
            "Real-Time Monitoring",
            (20,120),
            (0,255,0)
        )

        # =========================================
        # SAVE FRAME
        # =========================================
        previous_frame = frame.copy()

        # =========================================
        # SHOW OUTPUT
        # =========================================
        cv2.imshow(
            window_name,
            frame
        )

        # =========================================
        # EXIT
        # =========================================
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # =========================================
    # CLEAN EXIT
    # =========================================
    cap.release()

    cv2.destroyAllWindows()

    print("Monitoring stopped")

    os._exit(0)

# =========================================
# GLOBAL ERROR HANDLING
# =========================================
except Exception as e:

    print("Fatal Error:", e)

    traceback.print_exc()

    try:
        cap.release()
    except:
        pass

    cv2.destroyAllWindows()

    os._exit(1)