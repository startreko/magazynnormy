
import tkinter as tk
import subprocess
import platform
import os
from pdf_generator import generate_report_pdf

class WarehouseGUI:
    def __init__(self, data_processor, master=None):
        self.data_processor = data_processor
        self.create_temp_directory()
        self.clear_temp_files()
        self.build_ui(master)

    def build_ui(self, master):
        self.main_window = tk.Tk() if master is None else tk.Toplevel(master)
        self.main_window.configure(height=500, width=600)
        self.main_window.resizable(False, False)
        self.main_window.title("Warehouse Report")
        self.main_window.wm_iconbitmap('icon.ico')

        frame1 = tk.Frame(self.main_window)
        frame1.configure(height=200, padx=0, pady=0, width=200)
        frame2 = tk.Frame(frame1)
        frame2.configure(height=200, width=200)

        vcmd = (self.main_window.register(self._validate_input), "%P")
        self.order_entry = tk.Entry(frame2, validate='key', validatecommand=vcmd)
        self.order_entry.configure(
            borderwidth=1,
            font="{Arial} 24 {bold}",
            justify="center",
            relief="groove",
            width=15
        )
        self.order_entry.grid(column=0, ipady=3, padx=10, pady=10, row=0, sticky="nw")

        self.generate_btn = tk.Button(frame2, command=self.generate_report_and_open)
        self.generate_btn.configure(
            anchor="center",
            background="#ffffff",
            borderwidth=2,
            font="{Arial} 12 {}",
            padx=0,
            relief="groove",
            text='Generate\n[Enter]'
        )
        self.generate_btn.grid(column=1, padx=10, pady=10, row=0, sticky="nw")
        self.order_entry.bind('<Return>', self.generate_report_and_open)

        self.summary_only = tk.BooleanVar(value=True)
        checkbox = tk.Checkbutton(frame2, variable=self.summary_only, text='Summary Only')
        checkbox.grid(column=0, ipady=2, row=1)

        frame2.pack(side="top", padx=10, pady=10)
        frame1.pack(side="top")

    def clear_temp_files(self):
        temp_dir = 'temp'
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            os.remove(file_path)

    def _validate_input(self, P):
        return P == '' or (str.isdigit(P) and len(P) <= 7)

    def generate_report_and_open(self, event=None):
        order_number = self.order_entry.get()
        error_msg = self.data_processor.validate_input(order_number)
        if error_msg:
            return

        data = self.data_processor.file_extractor.extract_data(order_number)
        summary_only = self.summary_only.get()
        filepath = generate_report_pdf(data, summary_only)

        try:
            if platform.system() == 'Windows':
                subprocess.Popen(['start', '', filepath], shell=True)
            else:
                raise OSError('Unsupported OS')
        except Exception:
            pass

    def run(self):
        self.main_window.mainloop()

    def create_temp_directory(self):
        temp_directory = 'temp'
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory)

if __name__ == "__main__":
    app = WarehouseGUI(None)
    app.run()
