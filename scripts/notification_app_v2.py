"""
定时通知应用 - 带GUI界面 V2
功能：在指定时间发送桌面通知 + 调用API接口
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import threading
import time
from plyer import notification
import requests

class NotificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("定时通知助手 V2")
        self.root.geometry("650x800")
        self.root.resizable(False, False)
        
        # 配置文件路径
        self.config_file = os.path.join(os.path.dirname(__file__), "notification_config.json")
        
        # 默认通知时间
        self.default_times = [
            "09:40", "10:25", "11:10",
            "14:10", "14:55", "15:40", "16:25", "17:10", "17:55"
        ]
        
        # 加载配置
        self.load_config()
        
        # 通知线程运行标志
        self.running = False
        self.notification_thread = None
        
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
        title_frame = tk.Frame(self.root, bg="#4A90E2", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="⏰ 定时通知助手 V2",
            font=("Microsoft YaHei UI", 20, "bold"),
            bg="#4A90E2",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 通知设置区域
        settings_frame = tk.LabelFrame(
            main_frame, 
            text="通知设置",
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
            width=40
        )
        self.title_entry.insert(0, self.notification_title)
        self.title_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
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
            width=40
        )
        self.message_entry.insert(0, self.notification_message)
        self.message_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # API接口设置
        tk.Label(
            settings_frame, 
            text="API接口 (可选)：",
            font=("Microsoft YaHei UI", 10),
            bg="#f5f5f5"
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        self.api_entry = tk.Entry(
            settings_frame, 
            font=("Microsoft YaHei UI", 9),
            width=40
        )
        self.api_entry.insert(0, self.api_url)
        self.api_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # 提示文本
        tip_label = tk.Label(
            settings_frame,
            text="💡 留空则不调用API，支持GET/POST请求",
            font=("Microsoft YaHei UI", 8),
            bg="#f5f5f5",
            fg="#666"
        )
        tip_label.grid(row=3, column=1, sticky="w", padx=(10, 0))
        
        # 按钮容器
        btn_container = tk.Frame(settings_frame, bg="#f5f5f5")
        btn_container.grid(row=4, column=1, pady=10, sticky="e")
        
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
            padx=15,
            pady=5
        )
        test_btn.pack(side=tk.LEFT, padx=(0, 5))
        
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
            padx=15,
            pady=5
        )
        save_btn.pack(side=tk.LEFT)
        
        # 通知时间列表区域
        times_frame = tk.LabelFrame(
            main_frame,
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
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 列表框
        self.times_listbox = tk.Listbox(
            list_container,
            font=("Consolas", 11),
            height=10,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            bg="white",
            relief=tk.FLAT,
            borderwidth=2
        )
        self.times_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.times_listbox.yview)
        
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
            font=("Microsoft YaHei UI", 10),
            bg="#28a745",
            fg="white",
            command=self.add_time,
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # 编辑按钮
        edit_btn = tk.Button(
            btn_frame,
            text="✏️ 编辑选中",
            font=("Microsoft YaHei UI", 10),
            bg="#ffc107",
            fg="black",
            command=self.edit_time,
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        # 删除按钮
        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ 删除选中",
            font=("Microsoft YaHei UI", 10),
            bg="#dc3545",
            fg="white",
            command=self.delete_time,
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        status_frame = tk.Frame(self.root, bg="#34495e", height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="● 通知服务运行中 | 下次通知：计算中...",
            font=("Microsoft YaHei UI", 9),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.status_label.pack(pady=10)
        
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
                    self.api_url = config.get('api_url', '')
            except Exception as e:
                print(f"加载配置失败: {e}")
                self.notification_times = self.default_times.copy()
                self.notification_title = '定时提醒'
                self.notification_message = '该做点什么了！'
                self.api_url = ''
        else:
            self.notification_times = self.default_times.copy()
            self.notification_title = '定时提醒'
            self.notification_message = '该做点什么了！'
            self.api_url = ''
            
    def save_config(self):
        """保存配置文件"""
        config = {
            'times': sorted(self.notification_times),
            'title': self.notification_title,
            'message': self.notification_message,
            'api_url': self.api_url
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
        self.api_url = self.api_entry.get().strip()
        
        if not self.notification_title:
            self.notification_title = '定时提醒'
        if not self.notification_message:
            self.notification_message = '该做点什么了！'
            
        self.save_config()
        messagebox.showinfo("成功", "设置已保存！")
        
    def test_notification(self):
        """测试通知和API调用"""
        self.send_notification()
        messagebox.showinfo("测试", "测试通知已发送！\n请检查右下角是否显示通知。")
        
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
        api_status = "✓ API已配置" if self.api_url else "✗ 无API"
        self.status_label.config(text=f"● 运行中 | 下次通知：{next_time} | {api_status}")
        self.root.after(1000, self.update_status)  # 每秒更新一次
        
    def call_api(self):
        """调用API接口"""
        if not self.api_url:
            return
            
        try:
            # 准备数据
            data = {
                'title': self.notification_title,
                'message': self.notification_message,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 尝试POST请求
            response = requests.post(self.api_url, json=data, timeout=5)
            print(f"API调用成功 (POST): {response.status_code}")
            
        except Exception as e:
            # 如果POST失败，尝试GET
            try:
                response = requests.get(self.api_url, timeout=5)
                print(f"API调用成功 (GET): {response.status_code}")
            except Exception as get_error:
                print(f"API调用失败: {get_error}")
    
    def send_notification(self):
        """发送桌面通知"""
        try:
            # 发送系统通知
            notification.notify(
                title=self.notification_title,
                message=self.notification_message,
                app_name="定时通知助手",
                timeout=10
            )
            
            # 调用API（如果配置了）
            if self.api_url:
                threading.Thread(target=self.call_api, daemon=True).start()
                
        except Exception as e:
            print(f"发送通知失败: {e}")
            
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
            
    def on_closing(self):
        """窗口关闭事件"""
        if messagebox.askokcancel("退出", "确定要退出定时通知助手吗？\n退出后将不再接收通知。"):
            self.running = False
            self.root.destroy()

def main():
    root = tk.Tk()
    app = NotificationApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
