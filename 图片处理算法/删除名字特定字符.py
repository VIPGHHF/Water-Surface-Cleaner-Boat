# 导入os库，用于处理文件和文件夹操作
import os

def rename_files_remove_text():
    """
    批量修改指定文件夹里的JPG文件名称，删除其中的"鏁版嵁闆哱"字符
    """
    # ====================== 配置参数（小白只需改这里）======================
    # 目标文件夹路径（存放需要改名的图片）
    target_folder = r"D:\数据集new"
    # 需要删除的字符（不要修改，就是你要去掉的"鏁版嵁闆哱"）
    text_to_remove = "鏁版嵁闆哱"
    # 要处理的文件格式（只改JPG文件）
    file_extension = ".jpg"
    # =============================================================================

    # 检查目标文件夹是否存在
    if not os.path.exists(target_folder):
        print(f"❌ 错误：找不到文件夹 {target_folder}，请检查路径是否正确！")
        return

    # 统计变量：记录处理的文件数
    renamed_count = 0
    # 遍历文件夹里的所有文件
    for filename in os.listdir(target_folder):
        # 只处理小写/大写的.jpg文件（兼容不同大小写的后缀）
        if filename.lower().endswith(file_extension.lower()):
            # 检查文件名中是否包含要删除的字符
            if text_to_remove in filename:
                # 生成新文件名：替换掉要删除的字符
                new_filename = filename.replace(text_to_remove, "")
                # 拼接原文件的完整路径
                old_path = os.path.join(target_folder, filename)
                # 拼接新文件的完整路径
                new_path = os.path.join(target_folder, new_filename)

                try:
                    # 执行重命名操作
                    os.rename(old_path, new_path)
                    print(f"✅ 重命名成功：{filename} → {new_filename}")
                    renamed_count += 1
                except Exception as e:
                    # 捕获重命名失败的异常（比如文件被占用、权限不足）
                    print(f"❌ 重命名失败：{filename} → {new_filename}，原因：{str(e)}")

    # 处理完成后的总结
    print("\n🎉 批量重命名操作完成！")
    print(f"📁 处理的文件夹：{target_folder}")
    print(f"🔢 成功重命名的文件数量：{renamed_count}")
    if renamed_count == 0:
        print("💡 没有找到包含「鏁版嵁闆哱」字符的JPG文件，无需修改。")

# 程序主入口
if __name__ == "__main__":
    rename_files_remove_text()