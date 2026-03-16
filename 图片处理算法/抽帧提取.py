# 导入需要的库
# cv2是OpenCV库，用于处理视频和图片
import cv2
# os库用于处理文件和文件夹路径
import os

def extract_frames_from_videos():
    """
    从指定文件夹的视频中每隔0.5秒抽取一帧保存为图片
    """
    # ====================== 配置参数（小白可以修改这里的路径）======================
    # 视频所在文件夹路径（注意路径里的反斜杠用双反斜杠\\，或者用单斜杠/）
    video_folder = r"D:\桌面\shipin"
    # 图片保存的目标文件夹路径
    save_folder = r"D:\数据集"
    # 抽取帧的时间间隔（秒），这里设置为0.5秒
    time_interval = 0.6
    # 图片命名起始序号（DJI_0501对应数字501）
    start_number = 501
    # 图片格式
    img_format = ".JPG"
    # =============================================================================

    # 检查保存文件夹是否存在，如果不存在则创建
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"创建了保存文件夹：{save_folder}")

    # 获取视频文件夹里的所有文件
    video_files = [f for f in os.listdir(video_folder) 
                   if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv'))]
    
    if not video_files:
        print("⚠️ 错误：视频文件夹里没有找到视频文件！")
        return

    # 初始化图片序号
    current_number = start_number

    # 遍历每个视频文件
    for video_file in video_files:
        # 拼接完整的视频路径
        video_path = os.path.join(video_folder, video_file)
        print(f"\n正在处理视频：{video_file}")

        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        # 检查视频是否成功打开
        if not cap.isOpened():
            print(f"❌ 无法打开视频：{video_file}，跳过该视频")
            continue

        # 获取视频的帧率（每秒多少帧）
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 计算每隔0.5秒对应的帧数（帧率 * 时间间隔）
        frame_interval = int(fps * time_interval)
        print(f"视频帧率：{fps}，每隔{time_interval}秒抽取一帧（对应{frame_interval}帧）")

        # 初始化帧计数器
        frame_count = 0

        # 循环读取视频帧
        while True:
            # 读取一帧
            ret, frame = cap.read()
            # ret为False表示已经读到视频末尾，退出循环
            if not ret:
                break

            # 当帧计数器是frame_interval的倍数时，保存该帧
            if frame_count % frame_interval == 0:
                # 生成图片名称：DJI_XXXX + 格式
                img_name = f"DJI_{current_number:04d}{img_format}"
                # 拼接图片保存路径
                img_path = os.path.join(save_folder, img_name)
                
                # 保存图片
                cv2.imwrite(img_path, frame)
                print(f"✅ 保存图片：{img_name}")
                
                # 序号自增1
                current_number += 1

            # 帧计数器自增1
            frame_count += 1

        # 释放视频资源
        cap.release()
        print(f"✅ 视频{video_file}处理完成，共抽取{current_number - start_number}帧（累计序号到{current_number - 1}）")

    print(f"\n🎉 所有视频处理完成！")
    print(f"📁 图片保存路径：{save_folder}")
    print(f"🔢 最后生成的图片名称：DJI_{current_number - 1:04d}{img_format}")

# 程序主入口
if __name__ == "__main__":
    extract_frames_from_videos()