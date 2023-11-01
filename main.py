import time
import threading
import tkinter as tk
from tkinter import ttk

class StudyTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x400")
        self.root.title("Study Timer")

        self.s = ttk.Style()
        self.s.configure("TNoteBook.Tab", font=("Ubuntu", 20))
        self.s.configure("TButton.Tab", font=("Ubuntu", 20))
        self.s.configure("TButton")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=False)

        self.tab1 = ttk.Frame(self.tabs, width=400, height=60)
        self.tab2 = ttk.Frame(self.tabs, width=400, height=60)
        self.tab3 = ttk.Frame(self.tabs, width=400, height=60)

        # Tabs Labels
        self.tabs.add(self.tab1, text="Study")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        # Time Labels
        self.study_timer_label = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.study_timer_label.pack(pady=10)
        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.short_break_timer_label.pack(pady=10)
        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.long_break_timer_label.pack(pady=10)

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        # Start Button
        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.root.mainloop()

    def start_timer_thread(self):
        t = threading.Thread(target=self.start_timer)
        t.start()

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
    
    #ToDo: Add skip and reset timer

StudyTimer()