import time
import os
import threading
import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import ctypes

# ==== 配置区（可自定义）====
TRAIN_TIME = 30   # 训练时间（秒）
REST_TIME = 30    # 休息时间（秒）
TRAIN_SOUND = "launch1.mp3"  # 训练提示音
REST_SOUND = "levelup.mp3"    # 休息提示音
# 把 mp3 文件放在与脚本相同的目录下

# ==== 播放控制 ====
stop_signal = False  # 全局标志位，用于停止音乐

def play_sound_loop(filepath):
    """后台循环播放音乐，直到 stop_signal=True"""
    global stop_signal
    stop_signal = False
    if not os.path.exists(filepath):
        print(f"[警告] 找不到提示音文件：{filepath}")
        return

    def _loop():
        while not stop_signal:
            try:
                playsound(filepath)
            except Exception as e:
                print(f"[警告] 播放失败: {e}")
                break
    threading.Thread(target=_loop, daemon=True).start()

def stop_sound():
    """停止播放音乐（强制停止）"""
    global stop_signal
    stop_signal = True
    # 终止所有 playsound 子进程（Windows）
    try:
        # 在 Windows 下通过终止 mplayer 相关进程实现
        os.system("taskkill /f /im wmplayer.exe >nul 2>&1")
        os.system("taskkill /f /im vlc.exe >nul 2>&1")
        os.system("taskkill /f /im afplay >nul 2>&1")
    except Exception:
        pass

def show_popup(message, sound_file=None):
    """弹窗 + 背景音乐，点击确定后停止音乐"""
    if sound_file:
        play_sound_loop(sound_file)

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("训练提醒", message)
    root.destroy()

    stop_sound()  # 弹窗关闭后立即停止音乐

def countdown(seconds, label):
    """命令行倒计时显示"""
    for remaining in range(seconds, 0, -1):
        print(f"\r{label}倒计时：{remaining:02d} 秒", end="")
        time.sleep(1)
    print("\r" + " " * 40, end="\r")  # 清除行

# ==== 主程序 ====
def main():
    ctypes.windll.kernel32.SetConsoleTitleW("训练节奏计时器 v3")  # 设置窗口标题
    input("按下回车开始训练（30秒训练 + 30秒休息交替循环，关闭窗口即可退出）...")
    print("开始训练循环！")

    cycle = 1
    try:
        while True:
            print(f"\n==== 第 {cycle} 轮训练 ====")
            show_popup(f"第 {cycle} 轮训练开始！加油 💪", TRAIN_SOUND)
            countdown(TRAIN_TIME, "训练")

            print(f"\n==== 第 {cycle} 轮休息 ====")
            show_popup(f"第 {cycle} 轮训练结束！休息一下 😌", REST_SOUND)
            countdown(REST_TIME, "休息")

            cycle += 1

    except KeyboardInterrupt:
        stop_sound()
        print("\n训练计时已终止。")

if __name__ == "__main__":
    main()
