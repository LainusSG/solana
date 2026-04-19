import cv2
import numpy as np
import yaml
from yaml.loader import SafeLoader


class YOLO_Pred:
    def __init__(self, onnx_model, data_yaml):
        with open(data_yaml, mode="r") as f:
            data_yaml = yaml.load(f, Loader=SafeLoader)
        self.labels = data_yaml["names"]
        self.nc = data_yaml["nc"]

        self.yolo = cv2.dnn.readNetFromONNX(onnx_model)
        cv2.ocl.setUseOpenCL(False)
        self.yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        np.random.seed(10)
        self.colors = np.random.randint(100, 255, size=(self.nc, 3)).tolist()

    def detect(self, image, input_size=640, conf_threshold=0.4, score_threshold=0.25, nms_threshold=0.45):
        row, col, _ = image.shape
        max_rc = max(row, col)
        input_image = np.zeros((max_rc, max_rc, 3), dtype=np.uint8)
        input_image[0:row, 0:col] = image

        blob = cv2.dnn.blobFromImage(
            input_image,
            1 / 255,
            (input_size, input_size),
            swapRB=True,
            crop=False,
        )
        self.yolo.setInput(blob)
        preds = self.yolo.forward()

        detecciones = preds[0]
        boxes = []
        confidences = []
        clases = []

        image_w, image_h = input_image.shape[:2]
        x_factor = image_w / input_size
        y_factor = image_h / input_size

        for detection in detecciones:
            confidence = float(detection[4])
            if confidence <= conf_threshold:
                continue

            class_score = float(detection[5:].max())
            class_id = int(detection[5:].argmax())
            if class_score <= score_threshold:
                continue

            cx, cy, w, h = detection[0:4]
            left = int((cx - 0.5 * w) * x_factor)
            top = int((cy - 0.5 * h) * y_factor)
            width = int(w * x_factor)
            height = int(h * y_factor)

            boxes.append([left, top, width, height])
            confidences.append(confidence)
            clases.append(class_id)

        if not boxes:
            return []

        indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold, nms_threshold)
        if len(indices) == 0:
            return []

        detections_out = []
        for ind in np.array(indices).reshape(-1).tolist():
            x, y, w, h = boxes[ind]
            class_id = clases[ind]
            detections_out.append(
                {
                    "box": [int(x), int(y), int(w), int(h)],
                    "confidence": float(confidences[ind]),
                    "class_id": class_id,
                    "class_name": self.labels[class_id],
                    "color": self.generar_color(class_id),
                }
            )

        return detections_out

    def draw_detections(self, image, detections):
        annotated = image.copy()
        text_scale = max(0.8, annotated.shape[1] / 1200)
        text_thickness = max(2, int(annotated.shape[1] / 500))
        line_thickness = max(2, int(annotated.shape[1] / 400))
        label_height = max(26, int(34 * text_scale))

        for detection in detections:
            x, y, w, h = detection["box"]
            color = detection["color"]
            text = f'{detection["class_name"]}: {int(detection["confidence"] * 100)}%'
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, line_thickness)
            cv2.rectangle(annotated, (x, max(0, y - label_height)), (x + w, y), color, -1)
            cv2.putText(
                annotated,
                text,
                (x, max(20, y - 8)),
                cv2.FONT_HERSHEY_PLAIN,
                text_scale,
                (0, 255, 0),
                text_thickness,
            )
        return annotated

    def predicciones(self, image, input_size=640):
        detections = self.detect(image, input_size=input_size)
        annotated = self.draw_detections(image, detections)
        valorfalla = [f'{item["class_name"]}: {int(item["confidence"] * 100)}%' for item in detections]
        return [annotated, valorfalla]

    def generar_color(self, ID):
        return tuple(self.colors[ID])
