from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 召唤官方基础模型从头开始学（数据量大了，从头学能让它吸收得更全面）
    # 注意把路径换成你电脑里 yolo11n.pt 的绝对路径！
    model = YOLO(r"C:\Pycharm_Projects\Water-Surface-Cleaner-Boat\PC_YOLO_Vision\models\yolo11n.pt")

    print("🚀 所有数据汇合完毕，开始炼制 V2 进阶版水面垃圾模型...")

    # 2. 开始 V2 版本的地狱特训！
    results = model.train(
        # 你的 data.yaml 绝对路径
        data=r"C:\Pycharm_Projects\Water-Surface-Cleaner-Boat\PC_YOLO_Vision\data\data.yaml",
        epochs=100,                # 🌟 数据变多了，这次让它跑 100 轮，学得更扎实！
        imgsz=640,                 # 图像大小保持不变
        batch=8,                   # 每次喂给显卡 8 张图
        device=0,                  # 使用独立显卡
        # 训练结果保存的绝对路径
        project=r"C:\Pycharm_Projects\Water-Surface-Cleaner-Boat\PC_YOLO_Vision\runs",
        name="boat_model_v2"       # 🌟 给新模型起个响亮的名字
    )