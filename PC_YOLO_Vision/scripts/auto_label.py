import os
from ultralytics import YOLO


def auto_annotate():
    # 1. 唤醒你刚刚炼好的“初级打工仔”大脑
    # 注意：这里加载的是你刚训练出来的 best.pt，不是官方的 yolo11n.pt 了！
    model = YOLO(r"/PC_YOLO_Vision/runs/seed_model_v1\weights\best.pt")

    # 2. 流水线工位路径（绝对路径最稳）
    image_dir = r"C:\Pycharm_Projects\Water-Surface-Cleaner-Boat\PC_YOLO_Vision\data\unlabeled_images"
    label_dir = r"C:\Pycharm_Projects\Water-Surface-Cleaner-Boat\PC_YOLO_Vision\data\unlabeled_labels"

    # 确保保存标签的文件夹存在
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    # 找出所有图片
    images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"👀 找到 {len(images)} 张未标注图片，打工仔开始疯狂画框...")

    for img_name in images:
        img_path = os.path.join(image_dir, img_name)

        # 让模型去认！(conf=0.4 表示只要它有 40% 的把握，就敢画框)
        results = model(img_path, conf=0.1, verbose=False)

        # 如果模型在图里发现了垃圾，就把结果保存成 .txt
        if len(results[0].boxes) > 0:
            txt_name = os.path.splitext(img_name)[0] + ".txt"
            txt_path = os.path.join(label_dir, txt_name)
            results[0].save_txt(txt_path)
            print(f"✅ 成功标记: {img_name}")
        else:
            print(f"⚠️ 未发现目标: {img_name}")

    print(f"\n🎉 自动标注完成！快去 {label_dir} 看看生成的 txt 文件吧！")


if __name__ == "__main__":
    auto_annotate()