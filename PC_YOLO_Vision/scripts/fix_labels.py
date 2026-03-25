import os


def fix_dataset_labels():
    # 你的 labels 文件夹绝对路径 (根据你的截图填写的)
    label_dir = r"C:\Pycharm_Projects\Water-Surface-Cleaner-Boat\PC_YOLO_Vision\data\boat_trash\labels\train"

    # 【核心魔法】旧序号 -> 新序号 的转换规则
    # 0 (kz) 和 1 (chopsticks) 全都合并变成 0 (chopsticks)
    # 2 (foam) 往前挪变成 1
    # 3 (bottle) 往前挪变成 2
    # 4 (can) 往前挪变成 3
    mapping = {"0": "0", "1": "0", "2": "1", "3": "2", "4": "3"}

    # 1. 遍历所有 txt 标签文件并修改里面的数字
    txt_files = [f for f in os.listdir(label_dir) if f.endswith(".txt") and f != "classes.txt"]

    for filename in txt_files:
        filepath = os.path.join(label_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:  # 确保是标准的 YOLO 格式
                old_id = parts[0]
                if old_id in mapping:
                    parts[0] = mapping[old_id]  # 替换掉开头的序号
                new_lines.append(" ".join(parts) + "\n")

        # 把修改后的内容写回文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    # 2. 安全地重写 classes.txt
    with open(os.path.join(label_dir, "classes.txt"), "w", encoding="utf-8") as f:
        f.write("chopsticks\nfoam\nbottle\ncan\n")

    print(f"🎉 修复完成！成功更新了 {len(txt_files)} 个标签文件！")
    print("现在 classes.txt 已经干干净净，且没有任何错乱。")


if __name__ == "__main__":
    fix_dataset_labels()