import cv2

print("👁️ 强制使用 V4L2 底层通道直连 /dev/video0 ...")
# 🚨 极客核心：这里的 cv2.CAP_V4L2 就是绕过崩溃区的秘密武器！
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# 设定极低分辨率测试
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("❌ V4L2 通道打开失败！")
    exit()

print("✅ 通道建立！冲刷 5 帧废图唤醒传感器...")
for _ in range(5):
    cap.read()

print("📸 正式抓拍...")
ret, frame = cap.read()

if ret:
    cv2.imwrite("v4l2_victory.jpg", frame)
    print("🎉 抓拍成功！照片已保存为 v4l2_victory.jpg")
else:
    print("❌ 画面读取失败。")

cap.release()