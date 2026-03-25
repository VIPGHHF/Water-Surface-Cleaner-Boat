import cv2
import time

print("👁️ 正在初始化 IMX219 摄像头通道...")

# 打开视频设备 (去掉后端的强制限定，让 OpenCV 自己找最顺手的)
cap = cv2.VideoCapture(0)

# 设置我们期望的画面分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("❌ 无法打开摄像头！底层节点未能映射。")
    exit()

print("✅ 摄像头通道打通！")
print("⏳ 正在冲刷底层图像缓冲帧 (唤醒 ISP)...")

# 🚨 极客核心修复：连续读取并丢弃前 10 帧数据，给传感器充足的曝光计算时间
for i in range(10):
    ret, frame = cap.read()
    # 可以去掉 sleep，让它以最快速度冲刷掉废帧

print("📸 咔嚓！正式捕获...")
# 正式读取有用的那一帧
ret, frame = cap.read()

if ret:
    filename = "vision_test_fixed.jpg"
    cv2.imwrite(filename, frame)
    print(f"🎉 修复成功！照片已成功保存为: {filename}")
else:
    print("❌ 读取画面依然失败！这可能是 Ubuntu 22.04 的 libcamera 驱动冲突。")

# 释放摄像头资源
cap.release()