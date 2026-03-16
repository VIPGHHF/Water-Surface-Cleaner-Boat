import os

def rename_jpg_to_dji_sequence():
    """
    将指定文件夹中的所有JPG文件，按DJI_0001.jpg、DJI_0002.jpg的格式重新命名
    序号从0001开始递增
    """
    # ====================== 配置参数（小白只需确认这里）======================
    target_folder = r"D:\数据集new"  # 目标文件夹路径
    start_number = 1               # 起始序号（从0001开始）
    file_extension = ".jpg"        # 处理的文件格式
    # =============================================================================

    # 1. 检查目标文件夹是否存在
    if not os.path.exists(target_folder):
        print(f"❌ 错误：找不到文件夹 {target_folder}，请检查路径！")
        return

    # 2. 获取文件夹中所有JPG文件（不区分大小写）
    jpg_files = [
        f for f in os.listdir(target_folder)
        if f.lower().endswith(file_extension.lower())
    ]

    # 3. 检查是否有JPG文件
    if not jpg_files:
        print(f"⚠️ 提示：{target_folder} 中没有找到JPG文件！")
        return

    # 4. 排序文件（按原文件名的默认顺序，也可以按修改时间排序，看注释）
    # （可选）如果想按“文件修改时间”排序，把下面这行注释取消，注释掉上一行
    # jpg_files.sort(key=lambda x: os.path.getmtime(os.path.join(target_folder, x)))

    # 5. 批量重命名
    renamed_count = 0
    for idx, old_filename in enumerate(jpg_files, start=start_number):
        # 生成新文件名：DJI_xxxx + 后缀（xxxx是4位序号，不足补0）
        new_filename = f"DJI_{idx:04d}{file_extension}"
        # 拼接原文件和新文件的完整路径
        old_path = os.path.join(target_folder, old_filename)
        new_path = os.path.join(target_folder, new_filename)

        # 避免新文件名重复（虽然这里不会，但做个保险）
        if os.path.exists(new_path):
            print(f"⚠️ 跳过：新文件名 {new_filename} 已存在，无法重命名 {old_filename}")
            continue

        try:
            os.rename(old_path, new_path)
            print(f"✅ 重命名：{old_filename} → {new_filename}")
            renamed_count += 1
        except Exception as e:
            print(f"❌ 失败：{old_filename} → {new_filename}，原因：{str(e)}")

    # 6. 输出结果总结
    print(f"\n🎉 重命名完成！")
    print(f"📁 处理文件夹：{target_folder}")
    print(f"🔢 成功重命名 {renamed_count} 个JPG文件")
    print(f"🔚 最后一个文件：DJI_{start_number + renamed_count - 1:04d}{file_extension}")

if __name__ == "__main__":
    rename_jpg_to_dji_sequence()