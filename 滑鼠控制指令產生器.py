import tkinter as tk
from tkinter import ttk
import pyautogui

def on_key_press(event):
    # 讀取激活鍵 Entry 中的設定（忽略空白並轉小寫）
    activation_key = activation_key_entry.get().strip().lower()
    # 當按下的鍵符合設定值時執行操作
    if event.char.lower() == activation_key:
        # 取得目前滑鼠位置及該點 RGB 色值
        x, y = pyautogui.position()
        screenshot = pyautogui.screenshot()
        color = screenshot.getpixel((x, y))
        # 根據下拉選單選擇的操作敘述
        move = click_type_var.get()
        code_line = f"滑鼠移到({x},{y})後，不斷檢查顏色是否為{color}，直到條件成立才{move}\n"
        text_box.insert(tk.END, code_line)

def update_info():
    # 取得目前滑鼠位置及該點 RGB 色值，更新右側即時資訊
    x, y = pyautogui.position()
    screenshot = pyautogui.screenshot()
    color = screenshot.getpixel((x, y))
    hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
    mouse_info_label.config(text=f"座標: ({x}, {y})\nRGB: {color}")
    canvas.itemconfig(color_rect, fill=hex_color)
    # 每隔 100 毫秒更新一次
    root.after(100, update_info)

# 建立主要視窗，並修改視窗標題
root = tk.Tk()
root.title("操作命令產生器")

# 建立主框架，左右分欄
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 左側：外掛代碼產生區
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 右側：滑鼠即時資訊區
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

# === 左側區域 ===
# 說明 Label
instruction = (
    "請設定激活鍵，當按下該鍵時會將目前滑鼠的位置及顏色轉換為操作敘述：\n"
    "滑鼠移到目前位置後，檢查顏色是否與取得的 RGB 值一致時，執行指定操作。"
)
label = tk.Label(left_frame, text=instruction, justify="left")
label.pack(padx=10, pady=5, anchor="w")

# 激活鍵設定區：Label 與 Entry
activation_frame = tk.Frame(left_frame)
activation_frame.pack(padx=10, pady=5, anchor="w")
activation_label = tk.Label(activation_frame, text="激活鍵：")
activation_label.pack(side=tk.LEFT)
activation_key_entry = tk.Entry(activation_frame, width=5)
activation_key_entry.insert(0, "r")  # 預設激活鍵為 r
activation_key_entry.pack(side=tk.LEFT)

# 點擊方式選取下拉選單
click_type_var = tk.StringVar()
click_type_combobox = ttk.Combobox(left_frame, textvariable=click_type_var, state="readonly")
click_type_combobox['values'] = ("單擊滑鼠左鍵", "雙擊滑鼠左鍵", "單擊滑鼠右鍵")
click_type_combobox.current(0)
click_type_combobox.pack(padx=10, pady=5, anchor="w")

# 新增單列 textbox，顯示初始字串（複製提示）
copy_instruction_entry = tk.Entry(left_frame)
copy_instruction_entry.insert(0, "將'''欲填入的字串'''複製到剪貼簿，再按下 ctrl+v 貼上")
copy_instruction_entry.pack(padx=10, pady=5, fill=tk.X)

# 放置程式碼顯示的多列文字區域 (含橫向與縱向捲動條)
text_frame = tk.Frame(left_frame)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

text_box = tk.Text(text_frame, wrap="none")
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# 設定初始內容
text_box.insert(tk.END, "寫python程式進行下列動作：\n")

scrollbar_y = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_box.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=scrollbar_y.set)

scrollbar_x = tk.Scrollbar(left_frame, orient=tk.HORIZONTAL, command=text_box.xview)
scrollbar_x.pack(fill=tk.X)
text_box.config(xscrollcommand=scrollbar_x.set)

# === 右側區域 ===
# 顯示目前滑鼠座標及 RGB 的 Label
mouse_info_label = tk.Label(right_frame, text="座標: \nRGB: ", font=("Arial", 12), justify="left")
mouse_info_label.pack(pady=5)

# 顯示顏色方塊的 Canvas，填滿色與目前 RGB 值一致
canvas = tk.Canvas(right_frame, width=120, height=120, bd=2, relief="solid")
canvas.pack(pady=5)
color_rect = canvas.create_rectangle(10, 10, 110, 110, fill="white", outline="black")

# 綁定鍵盤事件：當按下任何鍵時執行 on_key_press
root.bind("<Key>", on_key_press)

# 啟動滑鼠資訊自動更新機制
update_info()

root.mainloop()
