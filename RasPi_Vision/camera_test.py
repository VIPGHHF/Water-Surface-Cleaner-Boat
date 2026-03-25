import cv2
import time

print("👁️ 正在初始化 IMX219 摄像头通道...")

# 打开视频设备 0 (通常 CSI 摄像头会映射到 video0)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# 设置我们期望的画面分辨率 (1280x720 测试画面足够清晰且不卡)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("❌ 无法打开摄像头！底层节点未能映射。")
    exit()

print("✅ 摄像头连接成功！让传感器适应光线...")
time.sleep(2) # 给传感器 2 秒钟的时间自动调整曝光和白平衡

print("📸 咔嚓！正在捕获当前画面...")
ret, frame = cap.read()

if ret:
    # 将捕获到的画面保存为一张 JPG 图片
    filename = "vision_test_120deg.jpg"
    cv2.imwrite(filename, frame)
    print(f"🎉 照片已成功保存为: {filename}")
    print("👉 请直接在 VS Code 左侧的文件树里双击打开这张图片，查看 120 度广角效果！")
else:
    print("❌ 读取画面失败！")

# 释放摄像头资源
cap.release()