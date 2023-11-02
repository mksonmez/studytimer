import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import sys, os

# Snippet from https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class StudyTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x440")
        # Set the window icon
        self.root.iconbitmap(resource_path("profile.ico"))
        # Set the window title
        self.root.title("Study Timer - Designed by Mehmet")
        # UI options and fonts
        paddings = {'padx': 5, 'pady': 10}
        clock_font = {'font': ('Monospace', 64)}
        study_label = {'font': ('Monospace', 22)}
        note_label = {'font': ('Monospace', 12)}
        # Icons
        start_icon = tk.PhotoImage(file='./start.png')
        skip_icon = tk.PhotoImage(file='./skip.png')
        reset_icon = tk.PhotoImage(file='./reset.png')

        self.style = ttk.Style()
        self.style.configure("Color1.TFrame", background="green")
        self.style.configure("Color2.TFrame", background="blue")
        self.style.configure("Color3.TFrame", background="red")
        self.style.configure("TNoteBook.Tab")
        self.style.configure("TButton.Tab")
        self.style.configure("TButton",
                         background = "blue",
                         relief="raised",
                         borderwidth=1, bd = 10, foreground = "black", focusthickness=3, focuscolor="none")

        # Tabs
        self.tabs = ttk.Notebook(self.root, style="TNoteBook.Tab")
        self.tabs.pack(fill="both", expand=False)

        self.tab1 = ttk.Frame(self.tabs, width=400, height=60, style="Color1.TFrame")
        self.tab2 = ttk.Frame(self.tabs, width=400, height=60, style="Color2.TFrame")
        self.tab3 = ttk.Frame(self.tabs, width=400, height=60, style="Color3.TFrame")

        self.tabs.add(self.tab1, text="Study")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        # Time Labels
        self.study_timer_label = ttk.Label(self.tab1, text="25:00", **clock_font)
        self.study_timer_label.pack()
        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", **clock_font)
        self.short_break_timer_label.pack()
        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", **clock_font)
        self.long_break_timer_label.pack()

        # Grid
        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=20)

        # Start Button
        self.start_button = ttk.Button(self.grid_layout,
                                       image=start_icon,
                                       text="Start",
                                       compound=tk.LEFT,
                                       style="TButton",
                                       command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0, **paddings)

        # Skip Button
        self.skip_button = ttk.Button(self.grid_layout,
                                      image=skip_icon,
                                      text="Skip",
                                      compound=tk.LEFT,
                                      command=self.skip_clock)
        self.skip_button.grid(row=0, column=1, **paddings)

        # Reset Button
        self.reset_button = ttk.Button(self.grid_layout,
                                      image=reset_icon,
                                      text="Reset",
                                      compound=tk.LEFT,
                                      command=self.reset_clock)
        self.reset_button.grid(row=0, column=2, **paddings)

        # Study Point Label
        self.study_counter_label = ttk.Label(self.grid_layout, text="Study Points: 0", **study_label)
        self.study_counter_label.grid(row=1, column=0, columnspan=3, **paddings)

        self.points = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        # Load Button
        self.load_button = ttk.Button(self.grid_layout, text="Load", command=self.load_note)
        self.load_button.grid(row=2, column=1)

        # Save Button
        self.save_button = ttk.Button(self.grid_layout, text="Save", command=self.save_note)
        self.save_button.grid(row=2, column=2)

        # Textbox
        notes = tk.StringVar()
        self.textbox_label = tk.Label(self.grid_layout, text="Notebook", **note_label, justify="left")
        self.textbox_label.grid(row=2, column=0, **paddings)

        self.textbox = tk.Text(self.root, height=6, **note_label)
        self.textbox.pack(**paddings)

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    def save_note(self):
        selected_file = filedialog.asksaveasfile(parent=self.root, defaultextension=".txt", filetypes=[("Text file",".txt"),("All files","*")])
        if selected_file is None:
            return
        filetext = str(self.textbox.get(1.0,6.0))
        selected_file.write(filetext)
        selected_file.close()
    
    def load_note(self):
        selected_file = filedialog.askopenfile(parent=self.root, title="Select a note", filetypes=[("Text file","*.txt"), ("All files","*.*")])
        if selected_file is None:
            return
        # write to console
        print(selected_file.read())

    def start_timer(self):        
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
            
        if timer_id == 1:
            full_seconds = 60 * 25
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.study_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.points += 1
                self.study_counter_label.config(text=f"Study points: {self.points}")
                if self.points % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()

        elif timer_id == 2:
            full_seconds = 60 * 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()

        elif timer_id == 3:
            full_seconds = 60 * 15
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        else:
            print("Invalid timer ID")

    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.running = False
        self.points = 0
        self.study_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.study_counter_label.config(text="Study Points: 0")

    def skip_clock(self):
        current_tab = self.tabs.index(self.tabs.select())
        
        if current_tab == 0:
            self.study_timer_label.config(text="25:00")
        elif current_tab == 1:
            self.short_break_timer_label.config(text="05:00")
        elif current_tab == 2:
            self.long_break_timer_label.config(text="15:00")

        self.stopped = True
        self.skipped = True

    #ToDO: load the saved note to GUI

StudyTimer()