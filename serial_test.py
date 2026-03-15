import serial
import time

# 初始化串口，/dev/serial0 是树莓派硬件串口的官方映射名
try:
    boat_serial = serial.Serial('/dev/serial0', 9600, timeout=1)
    print("✅ 成功连接到树莓派硬件串口 /dev/serial0！")
    print("🚢 准备向 STM32 下发指令...")
    print("操作说明：输入 W/A/S/D 控制方向，Q 停止，输入 exit 退出程序。")
except Exception as e:
    print(f"❌ 串口打开失败，请检查连线或底层配置。错误信息: {e}")
    exit()

while True:
    # 获取你在终端里输入的字符，并自动转成大写
    cmd = input("请输入航行指令 (W/A/S/D/Q): ").strip().upper()

    if cmd == 'EXIT':
        print("🔌 正在关闭通信通道...")
        boat_serial.close()
        break
    
    # 确保只发送咱们协议里定义好的单字符
    if cmd in ['W', 'A', 'S', 'D', 'Q']:
        # 将字符串编码为 ASCII 字节流并发送
        boat_serial.write(cmd.encode('ascii'))
        print(f"📡 已发送指令: [ {cmd} ] -> 等待 STM32 差速执行...")
    else:
        print("⚠️ 无效指令！STM32 听不懂，请重新输入 W, A, S, D 或 Q。")
        
    time.sleep(0.1)