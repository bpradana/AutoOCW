import tkinter as tk
from OCW import AutoOCW


class GUIWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('AutoOCW')

        tk.Label(self.root, text='Email').grid(row=0)
        tk.Label(self.root, text='Password').grid(row=1)
        tk.Label(self.root, text='Path').grid(row=2)

        self.email = tk.Entry(self.root, width=35)
        self.password = tk.Entry(self.root, show='*', width=35)
        self.path = tk.Entry(self.root, width=35)
        self.email.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        self.path.grid(row=2, column=1)

        tk.Button(self.root, text='Run', command=self.run).grid(row=3, columnspan=2)

        self.root.mainloop()

    def run(self):
        email = self.email.get()
        password = self.password.get()
        path = self.path.get()
        headless = False

        ocw = AutoOCW(path, email, password, headless=headless)
        ocw.login()
        ocw.buka_matkul()
        ocw.buka_dosen()
        ocw.run(refresh=5, check=2, delay=3)