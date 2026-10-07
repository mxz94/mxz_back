"""
定时通知应用 - 带GUI界面 V3
功能：在指定时间发送桌面通知 + 调用多个API接口 + 钉钉机器人支持 + 系统托盘
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import sys
from datetime import datetime
import threading
import time
import random
import re
import html
from plyer import notification
import requests
import hmac
import hashlib
import base64
from urllib.parse import quote_plus
from PIL import Image, ImageDraw, ImageTk
import pystray

# 弹窗强制停留时长（秒）：倒计时结束后才能关闭
REST_SECONDS = 15

# 弹窗对外文案（不出现"休息"字样，外部看只是张普通的卡片）
ALERT_WINDOW_TITLE = "便签"
ALERT_COUNTDOWN_TEXT = "稍等 %ds"
ALERT_UNLOCK_TEXT = "知道了"

# 内置默认题库（未找到 content_library.json 时兜底）
# 格式说明：不需要写 type，程序按内容自动识别
#   纯字符串            → 文本
#   以 .jpg/.png 等结尾 → 图片
#   含 <b> 等标签       → HTML
#   {"title","content"} → 知识点卡片
#   {"q","options","answer","why"} → 答题（点击选项即时判分）
DEFAULT_LIBRARY = [
    {"title": "小笑话", "content": "为什么程序员分不清万圣节和圣诞节？因为 Oct 31 == Dec 25。"},
    {"title": "想一想", "content": "如果让你用一句话向别人解释「沉没成本」，你会怎么说？试着组织下语言，越通俗越好。"},
    "人在注意力高度集中 20 分钟后，眨眼频率会掉到正常状态的三分之一——所以盯屏幕久了会觉得干涩。",
    {"title": "图推·做题总纲", "content": "元素组成相同 → 位置规律（平移、旋转、翻转）\n元素组成相似 → 样式规律（加减同异、黑白运算）\n元素组成不同 → 先属性（对称、曲直、开闭）\n　　　　　　　后数量（面、线、点、素）"},
    {"title": "论证·削弱力度排序", "content": "否定论点 > 拆桥 > 否定论据 > 他因削弱\n因果倒置 > 否定论据 > 他因削弱\n\n加强力度：搭桥 / 必要条件 > 解释原因 > 举例"},
    {"title": "翻译推理·逆否等价", "content": "A → B 等价于 非B → 非A\n口诀：肯前必肯后，否后必否前；\n否前、肯后无必然结论。"},
    {"title": "行测·数量", "q": "1，3，6，10，15，(  )", "options": ["A. 18", "B. 20", "C. 21", "D. 19"], "answer": "C",
     "why": "相邻两项之差为 2、3、4、5，下一差为 6，15+6=21。二级等差数列，也可看作三角形数 n(n+1)/2。"},
    {"title": "行测·言语", "q": "与「坚韧不拔」意思最接近的是：", "options": ["A. 半途而废", "B. 锲而不舍", "C. 知难而退", "D. 浅尝辄止"], "answer": "B",
     "why": "坚韧不拔形容意志坚定、不可动摇，与锲而不舍（不断雕刻，比喻持之以恒）语义最接近。其余三项均为反义或消极表述。"},
]


class NotificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("定时通知助手 V3")
        
        self.root.geometry("700x850")
        self.root.resizable(False, False)
        
        # 配置文件路径 - 修复打包后路径问题
        # 打包后使用 exe 所在目录，开发时使用脚本所在目录
        if getattr(sys, 'frozen', False):
            # 打包后的 exe 运行
            application_path = os.path.dirname(sys.executable)
        else:
            # 开发环境运行
            application_path = os.path.dirname(__file__)
        
        self.application_path = application_path
        self.config_file = os.path.join(application_path, "notification_config.json")
        self.library_path = os.path.join(application_path, "content_library.json")
        self.stats_path = os.path.join(application_path, "quiz_stats.json")
        
        # 默认通知时间
        self.default_times = [
            "09:40", "10:25", "11:10",
            "14:10", "14:55", "15:40", "16:25", "17:10", "17:55"
        ]
        
        # 加载配置
        self.load_config()

        # 加载内容题库（弹窗展示的内容）
        self.library = self.load_library()
        # 加载答题统计（错题优先重抽）
        self.quiz_stats = self.load_stats()
        
        # 通知线程运行标志
        self.running = False
        self.notification_thread = None
        
        # 系统托盘相关
        self.tray_icon = None
        self.is_hidden = False
        self.active_alert_window = None
        
        # 创建UI
        self.create_ui()
        
        # 启动通知检查
        self.start_notification_service()
        
    def create_ui(self):
        """创建用户界面"""
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 标题栏
        title_frame = tk.Frame(self.root, bg="#4A90E2", height=70)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="⏰ 定时通知助手 V3",
            font=("Microsoft YaHei UI", 18, "bold"),
            bg="#4A90E2",
            fg="white"
        )
        title_label.pack(pady=18)
        
        # 主容器 - 使用Canvas和滚动条
        main_canvas = tk.Canvas(self.root, bg="#f5f5f5")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="#f5f5f5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 内容容器
        content_frame = tk.Frame(scrollable_frame, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 通知设置区域
        settings_frame = tk.LabelFrame(
            content_frame, 
            text="基础设置",
            font=("Microsoft YaHei UI", 12, "bold"),
            bg="#f5f5f5",
            padx=15,
            pady=15
        )
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 通知标题
        tk.Label(
            settings_frame, 
            text="通知标题：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.title_entry = tk.Entry(
            settings_frame, 
            font=("Microsoft YaHei UI", 10),
            width=45
        )
        self.title_entry.insert(0, self.notification_title)
        self.title_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="ew")
        
        # 通知内容
        tk.Label(
            settings_frame, 
            text="通知内容：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.message_entry = tk.Entry(
            settings_frame, 
            font=("Microsoft YaHei UI", 10),
            width=45
        )
        self.message_entry.insert(0, self.notification_message)
        self.message_entry.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="ew")

        # 到点桌面弹窗开关
        tk.Label(
            settings_frame,
            text="到点弹窗：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).grid(row=2, column=0, sticky="w", pady=5)

        self.popup_enabled_var = tk.BooleanVar(value=self.show_desktop_popup)
        tk.Checkbutton(
            settings_frame,
            text="到时间弹出桌面通知",
            variable=self.popup_enabled_var,
            command=self.on_popup_toggle,
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5",
            activebackground="#f5f5f5",
            selectcolor="#ffffff"
        ).grid(row=2, column=1, sticky="w", pady=5, padx=(10, 0))

        # 晃动鼠标关闭弹窗开关
        tk.Label(
            settings_frame,
            text="关闭方式：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).grid(row=3, column=0, sticky="w", pady=5)

        self.motion_close_var = tk.BooleanVar(value=self.close_on_mouse_move)
        tk.Checkbutton(
            settings_frame,
            text="晃动鼠标即可关闭弹窗",
            variable=self.motion_close_var,
            command=self.on_motion_close_toggle,
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5",
            activebackground="#f5f5f5",
            selectcolor="#ffffff"
        ).grid(row=3, column=1, sticky="w", pady=5, padx=(10, 0))

        tk.Label(
            settings_frame,
            text="关闭后到点仍会调用 API/钉钉，只是不弹桌面通知。",
            font=("Microsoft YaHei UI", 9),
            fg="#666666",
            bg="#f5f5f5"
        ).grid(row=4, column=1, sticky="w", padx=(10, 0))
        
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # API接口设置区域
        api_frame = tk.LabelFrame(
            content_frame,
            text="API接口设置（可选，支持多个）",
            font=("Microsoft YaHei UI", 12, "bold"),
            bg="#f5f5f5",
            padx=15,
            pady=15
        )
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 钉钉webhook
        tk.Label(
            api_frame,
            text="钉钉机器人：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).grid(row=0, column=0, sticky="nw", pady=5)
        
        self.dingtalk_entry = tk.Entry(
            api_frame,
            font=("Microsoft YaHei UI", 9),
            width=50
        )
        self.dingtalk_entry.insert(0, self.dingtalk_webhook)
        self.dingtalk_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="ew")
        
        tk.Label(
            api_frame,
            text="💡 粘贴钉钉机器人webhook地址",
            font=("Microsoft YaHei UI", 8),
            bg="#f5f5f5",
            fg="#666"
        ).grid(row=1, column=1, sticky="w", padx=(10, 0))
        
        # 其他API接口
        tk.Label(
            api_frame,
            text="其他接口：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).grid(row=2, column=0, sticky="nw", pady=(15, 5))
        
        api_text_frame = tk.Frame(api_frame, bg="#f5f5f5")
        api_text_frame.grid(row=2, column=1, pady=(15, 5), padx=(10, 0), sticky="ew")
        
        self.api_text = tk.Text(
            api_text_frame,
            font=("Consolas", 9),
            width=50,
            height=4,
            wrap=tk.NONE
        )
        self.api_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        api_scrollbar = tk.Scrollbar(api_text_frame, command=self.api_text.yview)
        api_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.api_text.config(yscrollcommand=api_scrollbar.set)
        
        # 加载已有的API列表
        if self.api_urls:
            self.api_text.insert("1.0", "\n".join(self.api_urls))
        
        tk.Label(
            api_frame,
            text="💡 每行一个URL，支持POST/GET请求，可使用 $title 和 $content 变量",
            font=("Microsoft YaHei UI", 8),
            bg="#f5f5f5",
            fg="#666"
        ).grid(row=3, column=1, sticky="w", padx=(10, 0))
        
        api_frame.grid_columnconfigure(1, weight=1)
        
        # 按钮容器
        btn_container = tk.Frame(content_frame, bg="#f5f5f5")
        btn_container.pack(fill=tk.X, pady=(0, 15))
        
        # 测试通知按钮
        test_btn = tk.Button(
            btn_container,
            text="🔔 测试通知",
            font=("Microsoft YaHei UI", 10),
            bg="#17a2b8",
            fg="white",
            command=self.test_notification,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 保存设置按钮
        save_btn = tk.Button(
            btn_container,
            text="💾 保存设置",
            font=("Microsoft YaHei UI", 10),
            bg="#4A90E2",
            fg="white",
            command=self.save_settings,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        save_btn.pack(side=tk.LEFT)
        
        # 通知时间列表区域
        times_frame = tk.LabelFrame(
            content_frame,
            text="通知时间列表（24小时制）",
            font=("Microsoft YaHei UI", 12, "bold"),
            bg="#f5f5f5",
            padx=15,
            pady=15
        )
        times_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 创建时间列表框架
        list_container = tk.Frame(times_frame, bg="#f5f5f5")
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        times_scrollbar = tk.Scrollbar(list_container)
        times_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 列表框
        self.times_listbox = tk.Listbox(
            list_container,
            font=("Consolas", 11),
            height=8,
            yscrollcommand=times_scrollbar.set,
            selectmode=tk.SINGLE,
            bg="white",
            relief=tk.FLAT,
            borderwidth=2
        )
        self.times_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        times_scrollbar.config(command=self.times_listbox.yview)
        
        # 加载时间列表
        self.refresh_times_list()
        
        # 添加/编辑/删除按钮区域
        btn_frame = tk.Frame(times_frame, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 时间输入
        tk.Label(
            btn_frame,
            text="新增时间：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT)
        
        self.new_time_entry = tk.Entry(
            btn_frame,
            font=("Consolas", 11),
            width=10
        )
        self.new_time_entry.insert(0, "HH:MM")
        self.new_time_entry.pack(side=tk.LEFT, padx=10)
        
        # 添加按钮
        add_btn = tk.Button(
            btn_frame,
            text="➕ 添加",
            font=("Microsoft YaHei UI", 9),
            bg="#28a745",
            fg="white",
            command=self.add_time,
            cursor="hand2",
            relief=tk.FLAT,
            padx=12,
            pady=5
        )
        add_btn.pack(side=tk.LEFT, padx=3)
        
        # 编辑按钮
        edit_btn = tk.Button(
            btn_frame,
            text="✏️ 编辑",
            font=("Microsoft YaHei UI", 9),
            bg="#ffc107",
            fg="black",
            command=self.edit_time,
            cursor="hand2",
            relief=tk.FLAT,
            padx=12,
            pady=5
        )
        edit_btn.pack(side=tk.LEFT, padx=3)
        
        # 删除按钮
        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ 删除",
            font=("Microsoft YaHei UI", 9),
            bg="#dc3545",
            fg="white",
            command=self.delete_time,
            cursor="hand2",
            relief=tk.FLAT,
            padx=12,
            pady=5
        )
        delete_btn.pack(side=tk.LEFT, padx=3)
        
        # 状态栏
        status_frame = tk.Frame(self.root, bg="#34495e", height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="● 通知服务运行中 | 下次通知：计算中...",
            font=("Microsoft YaHei UI", 9),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.status_label.pack(pady=8)
        
        # 更新状态
        self.update_status()
        
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.notification_times = config.get('times', self.default_times)
                    self.notification_title = config.get('title', '定时提醒')
                    self.notification_message = config.get('message', '该做点什么了！')
                    self.dingtalk_webhook = config.get('dingtalk_webhook', '')
                    self.api_urls = config.get('api_urls', [])
                    self.show_desktop_popup = config.get('show_desktop_popup', True)
                    self.close_on_mouse_move = config.get('close_on_mouse_move', False)
            except Exception as e:
                print(f"加载配置失败: {e}")
                self.reset_config()
        else:
            self.reset_config()
    
    def reset_config(self):
        """重置为默认配置"""
        self.notification_times = self.default_times.copy()
        self.notification_title = '定时提醒'
        self.notification_message = '该做点什么了！'
        self.dingtalk_webhook = ''
        self.api_urls = []
        self.show_desktop_popup = True
        self.close_on_mouse_move = False
            
    def save_config(self):
        """保存配置文件"""
        config = {
            'times': sorted(self.notification_times),
            'title': self.notification_title,
            'message': self.notification_message,
            'dingtalk_webhook': self.dingtalk_webhook,
            'api_urls': self.api_urls,
            'show_desktop_popup': self.show_desktop_popup,
            'close_on_mouse_move': self.close_on_mouse_move
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
            
    def save_settings(self):
        """保存通知设置"""
        self.notification_title = self.title_entry.get().strip()
        self.notification_message = self.message_entry.get().strip()
        self.dingtalk_webhook = self.dingtalk_entry.get().strip()
        self.show_desktop_popup = bool(self.popup_enabled_var.get())
        self.close_on_mouse_move = bool(self.motion_close_var.get())
        
        # 读取API列表
        api_text_content = self.api_text.get("1.0", tk.END).strip()
        self.api_urls = [url.strip() for url in api_text_content.split('\n') if url.strip()]
        
        if not self.notification_title:
            self.notification_title = '定时提醒'
        if not self.notification_message:
            self.notification_message = '该做点什么了！'
            
        self.save_config()
        
        # 统计配置的接口数
        total_apis = len(self.api_urls) + (1 if self.dingtalk_webhook else 0)
        messagebox.showinfo("成功", f"设置已保存！\n已配置 {total_apis} 个API接口")

    def on_popup_toggle(self):
        """切换到点桌面弹窗开关"""
        self.show_desktop_popup = bool(self.popup_enabled_var.get())
        self.save_config()

    def on_motion_close_toggle(self):
        """切换晃动鼠标关闭弹窗开关"""
        self.close_on_mouse_move = bool(self.motion_close_var.get())
        self.save_config()
        
    def test_notification(self):
        """测试通知和API调用"""
        print("\n" + "="*50)
        print(">>> 开始测试通知...")
        
        notification_sent, errors = self.send_notification()
        
        total_apis = len(self.api_urls) + (1 if self.dingtalk_webhook else 0)
        
        result_msg = f"测试通知已触发！\n\n"
        
        if not self.show_desktop_popup:
            result_msg += "○ 桌面通知：已关闭，未弹窗\n"
        elif notification_sent:
            result_msg += "✓ 桌面通知：成功\n"
        else:
            result_msg += "✗ 桌面通知：失败\n"
            if errors:
                result_msg += f"  错误：{', '.join(errors)}\n"
        
        result_msg += f"✓ API 接口：将调用 {total_apis} 个\n\n"
        result_msg += "请检查：\n"
        result_msg += "1. 桌面右下角是否有通知弹出（开关关闭时不会弹窗）\n"
        result_msg += "2. 控制台是否有 API 调用日志\n"
        
        print("="*50 + "\n")
        
        messagebox.showinfo("测试结果", result_msg)
        
    def refresh_times_list(self):
        """刷新时间列表显示"""
        self.times_listbox.delete(0, tk.END)
        sorted_times = sorted(self.notification_times)
        for i, time_str in enumerate(sorted_times, 1):
            self.times_listbox.insert(tk.END, f"{i:2d}.  {time_str}")
            
    def add_time(self):
        """添加新的通知时间"""
        new_time = self.new_time_entry.get().strip()
        
        # 验证时间格式
        try:
            datetime.strptime(new_time, "%H:%M")
        except ValueError:
            messagebox.showerror("错误", "时间格式不正确！请使用 HH:MM 格式（如 09:30）")
            return
            
        if new_time in self.notification_times:
            messagebox.showwarning("警告", "该时间已存在！")
            return
            
        self.notification_times.append(new_time)
        self.save_config()
        self.refresh_times_list()
        self.new_time_entry.delete(0, tk.END)
        self.new_time_entry.insert(0, "HH:MM")
        messagebox.showinfo("成功", f"已添加通知时间：{new_time}")
        
    def edit_time(self):
        """编辑选中的通知时间"""
        selection = self.times_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要编辑的时间！")
            return
            
        index = selection[0]
        sorted_times = sorted(self.notification_times)
        old_time = sorted_times[index]
        
        # 创建编辑对话框
        edit_dialog = tk.Toplevel(self.root)
        edit_dialog.title("编辑时间")
        edit_dialog.geometry("300x150")
        edit_dialog.resizable(False, False)
        edit_dialog.transient(self.root)
        edit_dialog.grab_set()
        
        # 居中显示
        edit_dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        edit_dialog.geometry(f"+{x}+{y}")
        
        # 内容框架
        content_frame = tk.Frame(edit_dialog, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            content_frame,
            text=f"当前时间：{old_time}",
            font=("Microsoft YaHei UI", 11),
            bg="#f5f5f5"
        ).pack(pady=(0, 10))
        
        tk.Label(
            content_frame,
            text="新的时间：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).pack(pady=(0, 5))
        
        time_entry = tk.Entry(
            content_frame,
            font=("Consolas", 12),
            width=15,
            justify="center"
        )
        time_entry.insert(0, old_time)
        time_entry.pack(pady=(0, 15))
        time_entry.focus_set()
        time_entry.select_range(0, tk.END)
        
        def confirm_edit():
            new_time = time_entry.get().strip()
            
            # 验证时间格式
            try:
                datetime.strptime(new_time, "%H:%M")
            except ValueError:
                messagebox.showerror("错误", "时间格式不正确！请使用 HH:MM 格式（如 09:30）", parent=edit_dialog)
                return
                
            # 检查是否与其他时间重复（排除自己）
            if new_time != old_time and new_time in self.notification_times:
                messagebox.showwarning("警告", "该时间已存在！", parent=edit_dialog)
                return
                
            # 更新时间
            self.notification_times.remove(old_time)
            self.notification_times.append(new_time)
            self.save_config()
            self.refresh_times_list()
            edit_dialog.destroy()
            messagebox.showinfo("成功", f"已将 {old_time} 修改为 {new_time}")
        
        # 按钮框架
        btn_container = tk.Frame(content_frame, bg="#f5f5f5")
        btn_container.pack()
        
        confirm_btn = tk.Button(
            btn_container,
            text="确定",
            font=("Microsoft YaHei UI", 10),
            bg="#4A90E2",
            fg="white",
            command=confirm_edit,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_container,
            text="取消",
            font=("Microsoft YaHei UI", 10),
            bg="#6c757d",
            fg="white",
            command=edit_dialog.destroy,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        time_entry.bind("<Return>", lambda e: confirm_edit())
        edit_dialog.bind("<Escape>", lambda e: edit_dialog.destroy())
        
    def delete_time(self):
        """删除选中的通知时间"""
        selection = self.times_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的时间！")
            return
            
        index = selection[0]
        sorted_times = sorted(self.notification_times)
        time_to_delete = sorted_times[index]
        
        self.notification_times.remove(time_to_delete)
        self.save_config()
        self.refresh_times_list()
        messagebox.showinfo("成功", f"已删除通知时间：{time_to_delete}")
        
    def get_next_notification_time(self):
        """获取下一个通知时间"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        sorted_times = sorted(self.notification_times)
        
        # 查找今天剩余的通知
        for time_str in sorted_times:
            if time_str > current_time:
                return f"今天 {time_str}"
                
        # 如果今天没有了，返回明天第一个
        if sorted_times:
            return f"明天 {sorted_times[0]}"
        else:
            return "无"
            
    def update_status(self):
        """更新状态栏"""
        next_time = self.get_next_notification_time()
        total_apis = len(self.api_urls) + (1 if self.dingtalk_webhook else 0)
        api_status = f"✓ {total_apis}个API" if total_apis > 0 else "✗ 无API"
        popup_status = "弹窗开" if self.show_desktop_popup else "弹窗关"
        self.status_label.config(text=f"● 运行中 | 下次：{next_time} | {api_status} | {popup_status}")
        self.root.after(1000, self.update_status)
        
    def call_dingtalk(self):
        """调用钉钉机器人"""
        if not self.dingtalk_webhook:
            return
            
        try:
            # 钉钉消息格式
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"{self.notification_title}\n{self.notification_message}\n\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }
            
            headers = {'Content-Type': 'application/json'}
            
            # 尝试使用代理
            try:
                response = requests.post(
                    self.dingtalk_webhook,
                    json=data,
                    headers=headers,
                    timeout=5
                )
            except:
                # 如果失败，禁用代理重试
                response = requests.post(
                    self.dingtalk_webhook,
                    json=data,
                    headers=headers,
                    timeout=5,
                    proxies={'http': None, 'https': None}
                )
            
            result = response.json()
            if result.get('errcode') == 0:
                print(f"✓ 钉钉通知发送成功")
            else:
                print(f"✗ 钉钉通知失败: {result}")
                
        except Exception as e:
            print(f"✗ 钉钉API调用失败: {e}")
    
    def call_api(self, url):
        """调用单个API接口 - 支持变量替换 $title, $content"""
        if not url:
            return
            
        try:
            # 替换URL中的变量
            # 使用 $title 和 $content 作为占位符
            processed_url = url.replace('$title', self.notification_title)
            processed_url = processed_url.replace('$content', self.notification_message)
            
            # 准备数据（用于POST请求）
            data = {
                'title': self.notification_title,
                'message': self.notification_message,
                'content': self.notification_message,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 尝试POST请求（先用代理，失败则不用代理）
            try:
                response = requests.post(processed_url, json=data, timeout=5)
                print(f"✓ API调用成功 (POST) [{processed_url[:60]}...]: {response.status_code}")
                return
            except:
                try:
                    response = requests.post(processed_url, json=data, timeout=5, proxies={'http': None, 'https': None})
                    print(f"✓ API调用成功 (POST/无代理) [{processed_url[:60]}...]: {response.status_code}")
                    return
                except:
                    pass
            
            # 如果POST失败，尝试GET
            try:
                response = requests.get(processed_url, timeout=5)
                print(f"✓ API调用成功 (GET) [{processed_url[:60]}...]: {response.status_code}")
            except:
                try:
                    response = requests.get(processed_url, timeout=5, proxies={'http': None, 'https': None})
                    print(f"✓ API调用成功 (GET/无代理) [{processed_url[:60]}...]: {response.status_code}")
                except Exception as get_error:
                    print(f"✗ API调用失败 [{processed_url[:60]}...]: {get_error}")
                
        except Exception as e:
            print(f"✗ API处理失败 [{url[:50]}...]: {e}")
    
    
    def call_all_apis(self):
        """所有API调用都使用异步"""
        # 钉钉机器人异步调用
        if self.dingtalk_webhook:
            threading.Thread(target=self.call_dingtalk, daemon=True).start()
        
        # 其他API异步调用
        for url in self.api_urls:
            threading.Thread(target=self.call_api, args=(url,), daemon=True).start()

    # ---------- 内容题库 ----------
    def load_library(self):
        """加载 content_library.json 题库，返回条目列表；失败则用内置默认题库兜底"""
        items = []
        try:
            if os.path.exists(self.library_path):
                with open(self.library_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for raw in data:
                        it = self._parse_library_item(raw)
                        if it:
                            items.append(it)
        except Exception as e:
            print(f"加载题库失败: {e}")
        if not items:
            items = [dict(x) for x in DEFAULT_LIBRARY]
        return items

    def _parse_library_item(self, raw):
        """把一个题库条目解析为统一 dict，无需 type 字段，按内容自动识别：
        {kind, title, content, src, caption, html, q, options, answer, why}
        kind 取值：quiz（答题）/ image / html / text
        """
        if isinstance(raw, str):
            s = raw.strip()
            if not s:
                return None
            low = s.lower()
            if low.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')):
                return {"kind": "image", "src": s, "caption": ""}
            if re.search(r'<[a-zA-Z/][^>]*>', s):
                return {"kind": "html", "html": s}
            return {"kind": "text", "title": "", "content": s}

        if isinstance(raw, dict):
            # 答题：有题干 + 选项 + 答案
            q = raw.get("q") or raw.get("question") or raw.get("stem") or ""
            opts = raw.get("options") or raw.get("choices") or raw.get("opts") or []
            ans = raw.get("answer") or raw.get("ans") or raw.get("right") or ""
            if q and isinstance(opts, (list, tuple)) and len(opts) >= 2 and str(ans).strip():
                options = [str(o).strip() for o in opts if str(o).strip()]
                if len(options) >= 2:
                    return {"kind": "quiz",
                            "title": raw.get("title", "") or "行测小测",
                            "q": str(q).strip(),
                            "options": options,
                            "answer": str(ans).strip(),
                            "why": raw.get("why") or raw.get("explain") or raw.get("analysis") or ""}

            src = raw.get("src") or raw.get("path") or raw.get("image") or ""
            if src:
                return {"kind": "image",
                        "src": str(src).strip(),
                        "caption": raw.get("caption") or raw.get("text") or ""}

            if raw.get("html"):
                return {"kind": "html", "title": raw.get("title", ""),
                        "html": raw.get("html")}

            content = raw.get("content") or raw.get("text") or raw.get("desc") or ""
            if content or raw.get("title"):
                return {"kind": "text",
                        "title": raw.get("title", ""),
                        "content": str(content)}
        return None

    def pick_random_item(self):
        """从题库随机抽一条；30% 概率从曾答错的题里抽，强化薄弱点"""
        if not self.library:
            self.library = [dict(x) for x in DEFAULT_LIBRARY]
        quizzes = [it for it in self.library if it.get("kind") == "quiz"]
        if quizzes and random.random() < 0.3:
            wrong_pool = [it for it in quizzes
                          if (self.quiz_stats.get(self._quiz_id(it)) or {}).get("wrong", 0) > 0]
            if wrong_pool:
                return random.choice(wrong_pool)
        return random.choice(self.library)

    def _quiz_id(self, item):
        """用题干+首选项算稳定的 12 位 id（题库内容稳定后 id 就不变）"""
        opts = item.get("options") or [""]
        s = (item.get("q") or "") + "|" + str(opts[0])
        return hashlib.md5(s.encode("utf-8")).hexdigest()[:12]

    def load_stats(self):
        """加载 quiz_stats.json，返回 {id: {shown, wrong, last}}"""
        try:
            if os.path.exists(self.stats_path):
                with open(self.stats_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print(f"加载答题统计失败: {e}")
        return {}

    def save_stats(self):
        try:
            with open(self.stats_path, 'w', encoding='utf-8') as f:
                json.dump(self.quiz_stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存答题统计失败: {e}")

    def record_quiz_answer(self, qid, correct):
        """记录一次答题（异步落盘）"""
        s = self.quiz_stats.setdefault(qid, {"shown": 0, "wrong": 0, "last": ""})
        s["shown"] += 1
        if not correct:
            s["wrong"] += 1
        s["last"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        threading.Thread(target=self.save_stats, daemon=True).start()

    def _render_text_body(self, parent, item):
        content = item.get("content") or item.get("text") or ""
        tk.Label(parent, text=content, font=("Microsoft YaHei UI", 12),
                 fg="#1f2937", bg="#ffffff", justify="left",
                 wraplength=380, anchor="nw").pack(fill=tk.BOTH, expand=True)

    def _render_html_body(self, parent, html_str):
        text = tk.Text(parent, font=("Microsoft YaHei UI", 12), bg="#ffffff",
                       fg="#1f2937", wrap="word", borderwidth=0,
                       highlightthickness=0, relief="flat", cursor="arrow")
        text.pack(fill=tk.BOTH, expand=True)
        text.tag_configure("b", font=("Microsoft YaHei UI", 12, "bold"))
        text.tag_configure("i", font=("Microsoft YaHei UI", 12, "italic"))
        self._insert_html(text, html_str or "")
        text.configure(state="disabled")

    def _insert_html(self, text_widget, html_str):
        """把简单 HTML（b/strong/i/em/br/p/font color）渲染进 Text 控件"""
        s = html.unescape(html_str or "")
        s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
        s = re.sub(r'</p\s*>', '\n\n', s, flags=re.I)
        s = re.sub(r'</div\s*>', '\n', s, flags=re.I)
        # 剥离除 b/strong/i/em/font 之外的标签（保留标签内文本）
        s = re.sub(r'<(?!b\b|/b\b|strong\b|/strong\b|i\b|/i\b|em\b|/em\b|font\b|/font\b)[^>]*>',
                   '', s, flags=re.I)
        token_re = re.compile(
            r'(<b\b>|</b\b>|<strong\b>|</strong\b>|<i\b>|</i\b>|<em\b>|</em\b>|<font\b[^>]*>|</font\b>)',
            re.I)
        bold = False
        italic = False
        color = None
        pos = 0
        for m in token_re.finditer(s):
            if m.start() > pos:
                self._insert_styled(text_widget, s[pos:m.start()], bold, italic, color)
            tag = m.group(0).lower()
            if tag in ("<b>", "<strong>"):
                bold = True
            elif tag in ("</b>", "</strong>"):
                bold = False
            elif tag in ("<i>", "<em>"):
                italic = True
            elif tag in ("</i>", "</em>"):
                italic = False
            elif tag.startswith("<font"):
                cm = re.search(r'color\s*=\s*["\']?([^"\'>\s]+)', tag, re.I)
                color = cm.group(1) if cm else None
            elif tag == "</font>":
                color = None
            pos = m.end()
        if pos < len(s):
            self._insert_styled(text_widget, s[pos:], bold, italic, color)

    def _insert_styled(self, text_widget, text, bold, italic, color):
        tags = []
        if bold:
            tags.append("b")
        if italic:
            tags.append("i")
        name = None
        if color:
            name = "c_" + str(color).lstrip("#")
            try:
                text_widget.tag_configure(name, foreground=color)
            except tk.TclError:
                name = None
            if name:
                tags.append(name)
        if text:
            text_widget.insert("end", text, tuple(tags) if tags else ())

    def _render_image_body(self, parent, item):
        src = item.get("src") or ""
        caption = item.get("caption") or ""
        path = src
        if src and not os.path.isabs(src):
            path = os.path.join(self.application_path, src)
        photo = None
        if path and os.path.exists(path):
            try:
                img = Image.open(path)
                img.thumbnail((420, 380))
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"图片加载失败 {path}: {e}")
                photo = None
        if photo:
            parent._photo = photo  # 持有引用，防止被垃圾回收
            tk.Label(parent, image=photo, bg="#ffffff").pack()
        else:
            tk.Label(parent, text="（图片未找到：%s）" % (src or "?"),
                     font=("Microsoft YaHei UI", 11), fg="#94a3b8",
                     bg="#ffffff", wraplength=380, justify="center").pack(pady=40)
        if caption:
            tk.Label(parent, text=caption, font=("Microsoft YaHei UI", 11),
                     fg="#475569", bg="#ffffff", wraplength=380,
                     justify="center").pack(pady=(10, 0))

    def _render_quiz_body(self, parent, item):
        """渲染答题条目：题干 + 选项按钮，点击即时判分并显示解析"""
        # 题干可能含 <b> 等强调标签，Label 不支持，先剥掉
        question = re.sub(r'<br\s*/?>', '\n', str(item.get("q") or ""), flags=re.I)
        question = re.sub(r'<[^>]+>', '', question)
        options = item.get("options") or []
        answer = str(item.get("answer") or "").strip().upper()
        why = item.get("why") or ""

        # 历史统计徽标
        qid = self._quiz_id(item)
        st = self.quiz_stats.get(qid) or {}
        shown = st.get("shown", 0); wrong = st.get("wrong", 0)
        if shown > 0:
            rate = (shown - wrong) * 100 // shown
            if wrong > 0:
                hist_text = "⏪ 上次答错过 · 再做一次 · 历史正确率 %d%%（%d/%d）" % (rate, shown - wrong, shown)
                hist_fg = "#b45309"
            else:
                hist_text = "✅ 历史全对 · 历史正确率 %d%%（%d/%d）" % (rate, shown, shown)
                hist_fg = "#15803d"
            tk.Label(parent, text=hist_text,
                     font=("Microsoft YaHei UI", 9),
                     fg=hist_fg, bg="#fff7ed" if wrong > 0 else "#f0fdf4",
                     justify="left", anchor="w").pack(fill=tk.X, pady=(0, 8))

        tk.Label(parent, text=question, font=("Microsoft YaHei UI", 12),
                 fg="#111827", bg="#ffffff", justify="left",
                 wraplength=400, anchor="nw").pack(fill=tk.X, pady=(0, 10))

        btns = []
        result_label = tk.Label(parent, text="", font=("Microsoft YaHei UI", 11, "bold"),
                                bg="#ffffff", fg="#111827", justify="left",
                                wraplength=400, anchor="nw")
        why_box = tk.Text(parent, font=("Microsoft YaHei UI", 10), bg="#f8fafc",
                          fg="#334155", wrap="word", borderwidth=0,
                          highlightthickness=0, relief="flat", height=4,
                          cursor="arrow", padx=8, pady=8)

        def answer_key(text):
            """从选项文本里取出开头的字母标号 A/B/C/D"""
            m = re.match(r'^\s*([A-Da-d])[\.、\s\)：:]', str(text))
            if m:
                return m.group(1).upper()
            m = re.search(r'([A-Da-d])[\.、\)：:]', str(text)[:12])
            return m.group(1).upper() if m else ""

        def on_pick(idx):
            picked = answer_key(options[idx]) or chr(ord('A') + idx)
            correct = (picked == answer)
            for i, b in enumerate(btns):
                b.configure(state="disabled", cursor="arrow")
                key = answer_key(options[i]) or chr(ord('A') + i)
                if key == answer:
                    b.configure(bg="#dcfce7", fg="#15803d",
                                activebackground="#dcfce7", activeforeground="#15803d")
                elif i == idx:
                    b.configure(bg="#fee2e2", fg="#b91c1c",
                                activebackground="#fee2e2", activeforeground="#b91c1c")
                else:
                    b.configure(bg="#f1f5f9", fg="#94a3b8",
                                activebackground="#f1f5f9", activeforeground="#f1f3b0")
            if correct:
                result_label.configure(text="✅ 答对了！", fg="#15803d")
            else:
                result_label.configure(text="❌ 答错了，正确答案是 %s" % answer, fg="#b91c1c")
            result_label.pack(fill=tk.X, pady=(10, 6))
            if why:
                why_box.configure(state="normal")
                why_box.delete("1.0", "end")
                self._insert_html(why_box, why)
                why_box.configure(state="disabled")
                why_box.pack(fill=tk.X, pady=(0, 4))
            # 记录到统计
            self.record_quiz_answer(qid, correct)

        opt_frame = tk.Frame(parent, bg="#ffffff")
        opt_frame.pack(fill=tk.X)
        for i, opt in enumerate(options):
            b = tk.Button(
                opt_frame, text=str(opt),
                font=("Microsoft YaHei UI", 11),
                bg="#ffffff", fg="#1f2937",
                activebackground="#eff6ff", activeforeground="#1d4ed8",
                relief=tk.GROOVE, bd=1, padx=10, pady=6,
                cursor="hand2", anchor="w", justify="left",
                wraplength=370,
                command=lambda i=i: on_pick(i)
            )
            b.pack(fill=tk.X, pady=3)
            btns.append(b)

    def show_prominent_alert(self):
        """在主线程中显示置顶提醒窗"""
        self.root.after(0, self._show_prominent_alert)

    def _show_prominent_alert(self):
        """右下角小卡片：展示题库随机内容，停留 REST_SECONDS 秒后才能关闭"""
        try:
            if self.active_alert_window and self.active_alert_window.winfo_exists():
                self.active_alert_window.destroy()
        except tk.TclError:
            pass

        # 每次弹窗都重新读取，改完 json 下次提醒立即生效
        self.library = self.load_library()
        item = self.pick_random_item()
        itype = item.get("kind", "text")

        alert = tk.Toplevel(self.root)
        self.active_alert_window = alert
        alert.title(ALERT_WINDOW_TITLE)
        alert.configure(bg="#ffffff")
        alert.resizable(False, False)
        alert.attributes("-topmost", True)

        if itype == "image":
            width, height = 460, 560
        elif itype == "quiz":
            width, height = 450, 460
        else:
            width, height = 440, 320

        screen_w = alert.winfo_screenwidth()
        screen_h = alert.winfo_screenheight()
        x = max(8, screen_w - width - 24)
        y = max(8, screen_h - height - 70)
        alert.geometry(f"{width}x{height}+{x}+{y}")

        state = {"locked": True, "remaining": REST_SECONDS}

        def close_alert():
            if state["locked"]:
                return
            if self.active_alert_window is alert:
                self.active_alert_window = None
            try:
                alert.destroy()
            except tk.TclError:
                pass

        alert.protocol("WM_DELETE_WINDOW", close_alert)
        alert.bind("<Escape>", lambda event: close_alert())

        # 顶部标题栏
        header_title = item.get("title") or (
            "每日一题" if itype == "quiz" else "看看这张图" if itype == "image" else "小知识")
        header = tk.Frame(alert, bg="#4A90E2", height=52)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text=header_title, font=("Microsoft YaHei UI", 14, "bold"),
                 bg="#4A90E2", fg="white").pack(pady=13)

        # 内容区（答题时内容较多，给个可滚动容器）
        if itype == "quiz":
            body_outer = tk.Frame(alert, bg="#ffffff")
            body_outer.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)
            body = tk.Frame(body_outer, bg="#ffffff")
            body.pack(fill=tk.BOTH, expand=True)
        else:
            body = tk.Frame(alert, bg="#ffffff")
            body.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        if itype == "image":
            self._render_image_body(body, item)
        elif itype == "html":
            self._render_html_body(body, item.get("html", ""))
        elif itype == "quiz":
            self._render_quiz_body(body, item)
        else:
            self._render_text_body(body, item)

        # 底部倒计时按钮
        footer = tk.Frame(alert, bg="#ffffff")
        footer.pack(fill=tk.X, padx=20, pady=(0, 18))

        btn = tk.Button(
            footer,
            text=ALERT_COUNTDOWN_TEXT % state['remaining'],
            font=("Microsoft YaHei UI", 12, "bold"),
            bg="#cbd5e1", fg="#64748b",
            activebackground="#cbd5e1", activeforeground="#64748b",
            relief=tk.FLAT, padx=20, pady=8, cursor="arrow",
            state="disabled"
        )
        btn.pack(fill=tk.X)

        def unlock():
            state["locked"] = False
            btn.config(text=ALERT_UNLOCK_TEXT, state="normal",
                       bg="#10b981", fg="white",
                       activebackground="#059669", activeforeground="white",
                       cursor="hand2", command=close_alert)

        def tick():
            try:
                if not alert.winfo_exists():
                    return
            except tk.TclError:
                return
            if state["remaining"] > 0:
                state["remaining"] -= 1
                btn.config(text=ALERT_COUNTDOWN_TEXT % state['remaining'])
                alert.after(1000, tick)
            else:
                unlock()

        alert.after(1000, tick)

        # 晃动鼠标关闭（倒计时结束后才生效）
        if self.close_on_mouse_move:
            motion_state = {"armed": False, "x": None, "y": None}

            def arm_motion_close():
                try:
                    motion_state["x"] = alert.winfo_pointerx()
                    motion_state["y"] = alert.winfo_pointery()
                    motion_state["armed"] = True
                except tk.TclError:
                    pass

            def close_on_motion(event):
                if not motion_state["armed"] or state["locked"]:
                    return
                sx = motion_state["x"]
                sy = motion_state["y"]
                if sx is None or sy is None:
                    close_alert()
                    return
                if abs(event.x_root - sx) >= 30 or abs(event.y_root - sy) >= 30:
                    close_alert()

            alert.bind("<Motion>", close_on_motion)
            alert.after(700, arm_motion_close)

        try:
            alert.lift()
            alert.focus_force()
            self.root.bell()
        except tk.TclError:
            pass
    
    def send_notification(self):
        """发送桌面通知 - 使用 plyer"""
        notification_sent = False
        errors = []
        
        if self.show_desktop_popup:
            self.show_prominent_alert()
            try:
                print(f">>> 准备发送通知: {self.notification_title} - {self.notification_message}")

                # 使用 plyer 发送通知
                notification.notify(
                    title=self.notification_title,
                    message=self.notification_message,
                    app_name="定时通知助手",
                    timeout=10
                )

                notification_sent = True
                print(f"✓ 通知发送成功")

            except Exception as e:
                errors.append(f"通知失败: {e}")
                print(f"✗ 通知发送失败: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(">>> 桌面弹窗已关闭，跳过桌面通知")
        
        try:
            # 调用所有API（钉钉同步，其他异步）
            print(f">>> 开始调用 API...")
            self.call_all_apis()
            print(f">>> API 调用完成")
        except Exception as e:
            errors.append(f"API调用错误: {e}")
            print(f"✗ API调用失败: {e}")
        
        return notification_sent, errors
            
    def notification_service(self):
        """通知服务线程 - 每秒检查一次"""
        last_notified = set()
        
        while self.running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_date = now.strftime("%Y-%m-%d")
            
            # 检查是否需要发送通知
            if current_time in self.notification_times:
                notification_key = f"{current_date}_{current_time}"
                if notification_key not in last_notified:
                    self.send_notification()
                    last_notified.add(notification_key)
                    print(f"✓ 已发送通知：{current_time}")
                    
            # 清理过期的通知记录（保留今天的）
            last_notified = {k for k in last_notified if k.startswith(current_date)}
            
            # 每秒检查一次（提高准确度）
            time.sleep(1)
            
    def start_notification_service(self):
        """启动通知服务"""
        if not self.running:
            self.running = True
            self.notification_thread = threading.Thread(target=self.notification_service, daemon=True)
            self.notification_thread.start()
    
    def create_tray_icon(self):
        """创建系统托盘图标"""
        # 创建一个简单的图标
        icon_image = Image.new('RGB', (64, 64), color=(74, 144, 226))
        draw = ImageDraw.Draw(icon_image)
        draw.ellipse([16, 16, 48, 48], fill='white')
        
        # 创建托盘菜单
        menu = pystray.Menu(
            pystray.MenuItem("显示主窗口", self.show_window, default=True),
            pystray.MenuItem("隐藏窗口", self.hide_window),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", self.quit_app)
        )
        
        # 创建托盘图标
        self.tray_icon = pystray.Icon(
            "notification_helper",
            icon_image,
            "定时通知助手",
            menu
        )
    
    def show_window(self, icon=None, item=None):
        """显示主窗口"""
        self.root.after(0, self._show_window)
    
    def _show_window(self):
        """在主线程中显示窗口"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.is_hidden = False
    
    def hide_window(self, icon=None, item=None):
        """隐藏窗口到托盘"""
        self.root.withdraw()
        self.is_hidden = True
    
    def quit_app(self, icon=None, item=None):
        """退出应用"""
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
    
    def on_closing(self):
        """窗口关闭事件 - 最小化到托盘而不是退出"""
        self.hide_window()
    
    def run_tray_icon(self):
        """在后台线程运行托盘图标"""
        if self.tray_icon:
            self.tray_icon.run()

def main():
    root = tk.Tk()
    app = NotificationApp(root)
    
    # 创建并启动系统托盘
    app.create_tray_icon()
    tray_thread = threading.Thread(target=app.run_tray_icon, daemon=True)
    tray_thread.start()
    
    # 启动时最小化到托盘
    root.withdraw()
    app.is_hidden = True
    
    # 设置窗口关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
