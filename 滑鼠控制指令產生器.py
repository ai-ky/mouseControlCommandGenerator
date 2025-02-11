import tkinter as tk
from tkinter import ttk, messagebox
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

def on_mouse_move(event):
    # 如果目前焦點在下方的 text_box 時，將焦點移回 root
    if root.focus_get() == text_box:
        root.focus_set()

def add_image_instruction():
    # 將 image_instruction_entry 的內容加入 text_box（並換行）
    content = image_instruction_entry.get()
    text_box.insert(tk.END, content + "\n")

def add_copy_instruction():
    # 將 copy_instruction_entry 的內容加入 text_box（並換行）
    content = copy_instruction_entry.get()
    text_box.insert(tk.END, content + "\n")

def copy_text_to_clipboard():
    # 將 text_box 的內容複製到剪貼簿，並顯示 messagebox
    content = text_box.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(content)
    messagebox.showinfo("複製", "控制指令已複製!")

# 建立主要視窗，並修改視窗標題
root = tk.Tk()
root.title("操作命令產生器")

# ----------------------------
# 新增「安裝指令」區域（置於最開頭）
install_frame = tk.Frame(root)
install_frame.pack(fill=tk.X, padx=10, pady=5)
install_label = tk.Label(install_frame, text="安裝指令：")
install_label.pack(side=tk.LEFT)
install_entry = tk.Entry(install_frame)
install_entry.insert(0, "pip install autobf")
install_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
# ----------------------------

# 建立主框架，左右分欄
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# 左側：操作命令產生區（上半部）
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# 右側：滑鼠即時資訊區
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

# === 左側區域（上半部）===
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

# 新增 copy_instruction_entry 與 "加入" 按鈕，置於同一 frame 中
copy_instruction_frame = tk.Frame(left_frame)
copy_instruction_frame.pack(padx=10, pady=5, fill=tk.X)
copy_instruction_entry = tk.Entry(copy_instruction_frame)
copy_instruction_entry.insert(0, "將'''欲填入的字串'''複製到剪貼簿，再按下 ctrl+v 貼上")
copy_instruction_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
add_copy_button = tk.Button(copy_instruction_frame, text="加入", command=add_copy_instruction)
add_copy_button.pack(side=tk.LEFT, padx=5)

# 在 copy_instruction_frame 底下建立一個 frame，內含 image_instruction_entry 與 "加入" 按鈕
image_instruction_frame = tk.Frame(left_frame)
image_instruction_frame.pack(padx=10, pady=5, fill=tk.X)
image_instruction_entry = tk.Entry(image_instruction_frame)
image_instruction_entry.insert(0, "在螢幕上找到和 1.png 相似度90%以上的圖片並點擊中央")
image_instruction_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
add_image_button = tk.Button(image_instruction_frame, text="加入", command=add_image_instruction)
add_image_button.pack(side=tk.LEFT, padx=5)

# 新增 label "操作程序描述："，置於多列文字區上方
op_label = tk.Label(left_frame, text="操作程序描述：")
op_label.pack(padx=10, pady=5, anchor="w")

# ----------------------------
# 新增 code_frame，放置多列文字區域（text_box），寬度拉滿視窗
code_frame = tk.Frame(root)
code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
text_frame = tk.Frame(code_frame)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

text_box = tk.Text(text_frame, wrap="none")
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_box.insert(tk.END, "寫python程式進行下列動作：\n")

scrollbar_y = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_box.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=scrollbar_y.set)

scrollbar_x = tk.Scrollbar(code_frame, orient=tk.HORIZONTAL, command=text_box.xview)
scrollbar_x.pack(fill=tk.X)
text_box.config(xscrollcommand=scrollbar_x.set)
# ----------------------------

# === 右側區域（滑鼠資訊）===
mouse_info_label = tk.Label(right_frame, text="座標: \nRGB: ", font=("Arial", 12), justify="left")
mouse_info_label.pack(pady=5)
canvas = tk.Canvas(right_frame, width=120, height=120, bd=2, relief="solid")
canvas.pack(pady=5)
color_rect = canvas.create_rectangle(10, 10, 110, 110, fill="white", outline="black")

root.bind("<Key>", on_key_press)
root.bind("<Motion>", on_mouse_move)
update_info()

# ----------------------------
# 在最下方新增一個按鈕，按下時將 text_box 的內容複製到剪貼簿，並顯示 messagebox
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=10, pady=5)
copy_button = tk.Button(button_frame, text="複製控制指令到剪貼簿", command=copy_text_to_clipboard)
copy_button.pack()

root.mainloop()

