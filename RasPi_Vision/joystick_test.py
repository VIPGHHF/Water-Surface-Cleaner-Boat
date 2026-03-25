import pygame
import time
import os
import serial  # 👈 核心：引入串口通信引擎

# 骗过 pygame 的假屏幕魔法
os.environ["SDL_VIDEODRIVER"] = "dummy"

# ==========================================
# 🔌 第一步：点亮硬件串口通道 (115200极速模式)
# ==========================================
try:
    # 就在这里！波特率设为极速的 115200
    boat_serial = serial.Serial('/dev/serial0', 115200, timeout=1)
    print("✅ 成功接管树莓派硬件串口 /dev/serial0！波特率: 115200")
except Exception as e:
    print(f"❌ 串口打开失败，请检查连线。错误信息: {e}")
    exit()

# ==========================================
# 🎮 第二步：唤醒游戏手柄引擎
# ==========================================
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ 没有检测到手柄！请检查 2.4G 接收器是否插好。")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"✅ 成功连接手柄: {joystick.get_name()}")
print("🚢 小船动力系统已就绪！推摇杆起航，按 'B' 键熄火退出。")

# 基础参数设定：PWM范围 1100(全速倒退) ~ 1500(停止) ~ 1900(全速前进)
STOP_PWM = 1500
MAX_SPEED_OFFSET = 200 # 最高限制在 1700，最低 1300

# ==========================================
# 🧠 第三步：大脑死循环监控与数据下发
# ==========================================
try:
    while True:
        pygame.event.pump() # 刷新手柄硬件事件

        # 获取左摇杆 X (转向) 和 Y (油门)
        axis_x = joystick.get_axis(0) 
        axis_y = joystick.get_axis(1) 

        # 过滤摇杆物理死区
        if abs(axis_x) < 0.1: axis_x = 0.0
        if abs(axis_y) < 0.1: axis_y = 0.0

        # Y轴反转逻辑（推是正，拉是负）
        forward = -axis_y  
        steer = axis_x     

        # 差速算法：计算左右履带/螺旋桨的受力比例
        left_power = forward + steer
        right_power = forward - steer

        # 暴力限幅，防止计算溢出
        left_power = max(min(left_power, 1.0), -1.0)
        right_power = max(min(right_power, 1.0), -1.0)

        # 转换为 STM32 能听懂的 PWM 数值
        left_pwm = int(STOP_PWM + (left_power * MAX_SPEED_OFFSET))
        right_pwm = int(STOP_PWM + (right_power * MAX_SPEED_OFFSET))

        # 📦 极其关键的封包：<左,右>\n
        # 加上 \n 是为了告诉 STM32 “这句话我说完了”
        data_packet = f"<{left_pwm},{right_pwm}>\n"
        
        # ⚡ 核心动作：将数据包转换为 ASCII 字节流并打入物理串口
        boat_serial.write(data_packet.encode('ascii'))
        
        # 在终端打印个极其装逼的实时监控界面（strip是去掉\n防换行）
        print(f"🕹️ 摇杆 [X:{axis_x:5.2f} Y:{axis_y:5.2f}]  --->  📡 极速下发指令: {data_packet.strip()}      ", end='\r')

        # 紧急退出逻辑
        if joystick.get_button(1):
            print("\n🔌 收到退出指令，正在切断动力与通信通道...")
            boat_serial.close() # 极客好习惯：走之前关掉串口
            break

        time.sleep(0.05) # 20Hz 刷新率，保证手感极其丝滑且不堵塞串口

except KeyboardInterrupt:
    print("\n程序被终端强制中断。")
    boat_serial.close()
finally:
    pygame.quit()