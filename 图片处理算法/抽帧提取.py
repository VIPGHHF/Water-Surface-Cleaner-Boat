# 导入需要的库
import cv2  # 处理视频和图片
import os  # 处理文件和文件夹路径
import numpy as np  # 配合 OpenCV 解决中文路径保存报错的“神器”


def extract_frames_from_videos():
    """
    从指定文件夹的视频中每隔 0.4 秒抽取一帧保存为图片
    """
    # ====================== 🌟 小白专属修改区 🌟 ======================

    # 【修改点 1】：你要处理的视频所在的文件夹路径
    # 注意：开头的字母 r 千万别删！
    work_folder = r"C:\boat_work\视频\xuebi"

    # 【修改点 2】：这批视频对应的前缀简称
    # 提示：筷子写 "KZ", 泡沫写 "PM", 易拉罐写 "YLG", 瓶子写 "PZ"
    prefix = "PZ"

    # 抽取帧的时间间隔（秒），已为你设置为 0.4 秒
    time_interval = 0.4

    # ==================================================================

    # 视频来源和保存地址设为同一个，方便你就地剔除废片
    video_folder = work_folder
    save_folder = work_folder

    # 图片命名起始序号和格式
    start_number = 1
    img_format = ".JPG"

    # 获取视频文件夹里的所有视频文件 (忽略大小写，支持多种格式)
    video_files = [f for f in os.listdir(video_folder)
                   if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv'))]

    if not video_files:
        print(f"⚠️ 错误：在 {video_folder} 文件夹里没有找到任何视频！")
        return

    current_number = start_number

    # 开始挨个处理视频
    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        print(f"\n正在处理视频：{video_file}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ 无法打开视频：{video_file}，跳过")
            continue

        # 获取视频的帧率（每秒播放多少张画面）
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 计算：0.4秒对应的是多少帧？
        frame_interval = int(fps * time_interval)
        print(f"视频帧率：{fps}，每隔 {time_interval} 秒抽取一帧（对应每 {frame_interval} 帧抽一张）")

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:  # 视频读完了，退出这个视频的循环
                break

            # 如果到了该抽取的帧数
            if frame_count % frame_interval == 0:
                # 自动生成名字，比如：KZ_0001.JPG
                img_name = f"{prefix}_{current_number:04d}{img_format}"
                img_path = os.path.join(save_folder, img_name)

                # 【防坑神器】使用特殊方法保存图片，完美解决路径中带中文导致保存失败的问题
                cv2.imencode(img_format, frame)[1].tofile(img_path)

                print(f"✅ 成功抽出图片：{img_name}")
                current_number += 1

            frame_count += 1

        cap.release()
        print(f"✅ 视频 [{video_file}] 处理完成！")

    print(f"\n🎉 大功告成！[{prefix}] 类的视频全部抽帧完毕。")
    print(f"📁 图片已保存在：{save_folder}")
    print(f"👉 下一步操作建议：")
    print(f"1. 打开文件夹，手动删掉模糊、完全重复的废片。")
    print(f"2. 修改代码里的文件夹路径和前缀，继续处理下一组视频。")


# 程序主入口
if __name__ == "__main__":
    extract_frames_from_videos()