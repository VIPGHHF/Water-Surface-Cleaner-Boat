import cv2
from ultralytics import YOLO

# 加载官方最轻量的模型
model = YOLO(r"C:\Pycharm_Projects\Water-Surface-Cleaner-Boat\PC_YOLO_Vision\runs\boat_model_v2\weights\best.pt")


# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        # 推理并实时绘制结果
        results = model(frame)
        annotated_frame = results[0].plot()

        cv2.imshow("Boat Project YOLO Test", annotated_frame)

        # 按 q 退出
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()