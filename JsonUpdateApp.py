import json
import os
import threading
import time
from tkinter import Tk, Button, Label, filedialog, StringVar, Entry, messagebox, ttk


class JsonUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Updater App")

        # Variables
        self.is_running = False
        self.is_paused = False
        self.processed_count = 0

        # UI Elements
        self.source_file_label = Label(root, text="元のJSONファイル:")
        self.source_file_label.grid(row=0, column=0, padx=5, pady=5)
        self.source_file_path = StringVar()
        self.source_file_entry = Entry(root, textvariable=self.source_file_path, width=40)
        self.source_file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.source_file_button = Button(root, text="選択", command=self.select_source_file)
        self.source_file_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_file_label = Label(root, text="新規JSONファイル:")
        self.output_file_label.grid(row=1, column=0, padx=5, pady=5)
        self.output_file_path = StringVar()
        self.output_file_entry = Entry(root, textvariable=self.output_file_path, width=40)
        self.output_file_entry.grid(row=1, column=1, padx=5, pady=5)
        self.output_file_button = Button(root, text="選択", command=self.select_output_file)
        self.output_file_button.grid(row=1, column=2, padx=5, pady=5)

        self.start_button = Button(root, text="開始", command=self.start_updating)
        self.start_button.grid(row=2, column=0, pady=10)

        self.stop_button = Button(root, text="停止", command=self.stop_updating, state="disabled")
        self.stop_button.grid(row=2, column=1, pady=10)

        self.pause_button = Button(root, text="一時停止", command=self.pause_updating, state="disabled")
        self.pause_button.grid(row=2, column=2, pady=10)

        self.progress_label = Label(root, text="進捗状況:")
        self.progress_label.grid(row=3, column=0, padx=5, pady=5)
        self.progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress_bar.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        self.status_label = Label(root, text="ステータス: -")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def select_source_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.source_file_path.set(file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.output_file_path.set(file_path)

    def start_updating(self):
        source_path = self.source_file_path.get()
        output_path = self.output_file_path.get()

        if not os.path.exists(source_path):
            messagebox.showerror("エラー", "元のJSONファイルが存在しません。")
            return

        if not output_path:
            messagebox.showerror("エラー", "新規JSONファイルを指定してください。")
            return

        self.is_running = True
        self.is_paused = False
        self.processed_count = 0
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.pause_button.config(state="normal")
        self.status_label.config(text="ステータス: 処理中...")

        threading.Thread(target=self.update_json, args=(source_path, output_path), daemon=True).start()

    def stop_updating(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.pause_button.config(state="disabled")
        self.status_label.config(text="ステータス: 停止")

    def pause_updating(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="再開" if self.is_paused else "一時停止")
        self.status_label.config(text="ステータス: 一時停止中..." if self.is_paused else "ステータス: 処理中...")

    def update_json(self, source_path, output_path):
        try:
            with open(source_path, "r", encoding="utf-8") as source_file:
                data = json.load(source_file)

            if not isinstance(data, list):
                messagebox.showerror("エラー", "元のJSONファイルはリスト形式である必要があります。")
                self.stop_updating()
                return

            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write("[]")  # 空リスト作成

            total_items = len(data)
            self.progress_bar["maximum"] = total_items

            for item in data:
                if not self.is_running:
                    break

                while self.is_paused:
                    time.sleep(0.1)

                with open(output_path, "r+", encoding="utf-8") as output_file:
                    existing_data = json.load(output_file)
                    existing_data.append(item)
                    output_file.seek(0)
                    json.dump(existing_data, output_file, indent=4, ensure_ascii=False)

                self.processed_count += 1
                self.progress_bar["value"] = self.processed_count
                self.status_label.config(text=f"ステータス: 処理中 ({self.processed_count}/{total_items})")
                time.sleep(0.3)

            if self.is_running:
                messagebox.showinfo("完了", "データの更新が完了しました。")
            self.stop_updating()
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {e}")
            self.stop_updating()


# アプリの実行
if __name__ == "__main__":
    root = Tk()
    app = JsonUpdaterApp(root)
    root.mainloop()
