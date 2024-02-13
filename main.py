import tkinter as tk
import tkinter.ttk as ttk
import pystray
from PIL import Image
import pandas as pd
import os
import webbrowser


def load_data():
    if os.path.isfile("dailies.csv"):
        data = pd.read_csv("dailies.csv")
    else:
        data.to_csv("dailies.csv", sep=',', index=False, encoding="utf-8")



def save_data():
    pass

class MyApp(tk.Tk):
    data = pd.DataFrame()

    def __init__(self):
        super().__init__()


        self.load_data()
        self.title("Daily app manager")
        self.geometry('500x750')
        self.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)

        self.tasks = ttk.Treeview(columns=("Daily"),show='headings',height=25)
        self.tasks.column("Daily", anchor=tk.CENTER, stretch=tk.NO, width=480)
        self.tasks.heading("Daily",text="Daily")
        self.tasks.grid(row=0, column=0, columnspan=3, padx=(10,10), pady=(10,10))

        for index,row in self.data.iterrows():
            self.tasks.insert('',"end",values=(row["Daily"],),tags=(row["complete"]))

        self.tasks.tag_configure("completed", background="green")
        self.tasks.tag_configure("uncompleted", background="red")

        daily_options_frame = tk.LabelFrame(self, text="Daily Options", labelanchor="nw", width=480, height=50)
        daily_options_frame.grid(row=1, column=0, columnspan=3)

        open_selected_button = tk.Button(daily_options_frame,text="Open Selected",command=self.open_selected,width=18)
        open_selected_button.grid(row=0,column=0,padx=(10,10),pady=(0,10))

        complete_selected_button = tk.Button(daily_options_frame,text="Complete Selected",command=self.complete_selected,width=18)
        complete_selected_button.grid(row=0,column=1,padx=(10,10),pady=(0,10))

        delete_selected_button = tk.Button(daily_options_frame,text="Delete Selected",command=self.delete_selected,width=18)
        delete_selected_button.grid(row=0,column=2,padx=(10,10),pady=(0,10))

        new_daily_frame = tk.LabelFrame(self, text="New Daily", labelanchor="nw", width=480, height=100)
        new_daily_frame.grid(row=2, column=0, columnspan=3,sticky="ewns",padx=(10,10))

        new_daily_name_label = tk.Label(new_daily_frame,text="Name",width=20)
        new_daily_name_entry = tk.Entry(new_daily_frame,width=52,selectborderwidth=10)

        new_daily_name_label.grid(row=0,column=0)
        new_daily_name_entry.grid(row=0,column=1,columnspan=2)

        new_daily_type = tk.Menubutton(new_daily_frame,text="Daily Type", relief=tk.RAISED,width=20)
        new_daily_type.grid(row=1,column=0)

        new_daily_type.menu = tk.Menu(new_daily_type, tearoff=0)
        new_daily_type["menu"] = new_daily_type.menu

        self.typeVar = tk.IntVar(self,0)

        new_daily_type.menu.add_radiobutton(label="None",variable=self.typeVar)
        new_daily_type.menu.add_radiobutton(label="Website",variable=self.typeVar)
        new_daily_type.menu.add_radiobutton(label="Application",variable=self.typeVar)
        new_daily_type.grid(row=1,column=0)

        self.shorcutVar = tk.StringVar(self,"Daily Shortcut")

        new_daily_shortcut = tk.Entry(new_daily_frame,width=52,selectborderwidth=10,textvariable=self.shorcutVar)
        new_daily_shortcut.grid(row=1,column=1,columnspan=2)

        self.alertVar = tk.IntVar()
        new_daily_alert_checkbox = tk.Checkbutton(new_daily_frame,text="Alert",variable=self.alertVar)
        new_daily_alert_checkbox.grid(row=2,column=0)

        alert_time_frame = tk.LabelFrame(new_daily_frame,text="Alert Time",width=100,height=40)
        alert_time_frame.grid(row=2,column=1,sticky="w",pady=(10,10),padx=(10,10))

        alert_time_hour = tk.Spinbox(alert_time_frame, from_=0,to=23,width=2)
        alert_time_label = tk.Label(alert_time_frame,text=":",width=1)
        alert_time_min = tk.Spinbox(alert_time_frame, from_=0,to=59,width=2)

        alert_time_hour.grid(row=0,column=0)
        alert_time_label.grid(row=0,column=1)
        alert_time_min.grid(row=0,column=2)

        create_button = tk.Button(new_daily_frame,text="Create New Daily",command=self.create_new_daily,width=18)
        create_button.grid(row=2,column=2)

    def create_new_daily(self):
        print

    def selected_item(self):
        item = self.tasks.focus()
        return self.tasks.item(item)
    
    def delete_selected(self):
        print(self.selected_item()," delete")

    def complete_selected(self):
        print("complete")

    def open_selected(self):
        task = self.selected_item()["values"][0]
        self.open_daily(task)

    def load_data(self):
        if os.path.isfile("dailies.csv"):
            self.data = pd.read_csv("dailies.csv")
        else:
            self.data.to_csv("dailies.csv", sep=',', index=False, encoding="utf-8")



    def save_data(self):
        self.data.to_csv("dailies.csv", sep=',', index=False, encoding="utf-8")

    def create_menu(self):
        out = []
        for index,row in self.data.iterrows():
            if row["complete"] == "uncompleted":
                out.append(pystray.MenuItem(row["Daily"],lambda _, daily=row["Daily"]: self.open_daily(daily),enabled=True))
            else:
                out.append(pystray.MenuItem(row["Daily"],lambda _, daily=row["Daily"]: self.open_daily(daily),enabled=False))

        out.append(pystray.Menu.SEPARATOR)
        out.append(pystray.MenuItem('Open Window',self.show_window))
        out.append(pystray.MenuItem('Quit',  self.quit_window))

        return tuple(out)

    def open_daily(self,task):
        task_to_open = self.data.loc[self.data["Daily"] == str(task)]
        if task_to_open.iloc[0]["type"] == "website":
            webbrowser.open(task_to_open.iloc[0]["shortcut"], new=2)
        elif task_to_open.iloc[0]["type"] == "application":
            os.startfile(task_to_open.iloc[0]["shortcut"])


    def minimize_to_tray(self):
        self.withdraw()
        image = Image.open("app.ico")
        menu = self.create_menu()
        icon = pystray.Icon("name", image, "My App", menu)
        icon.run()

    def quit_window(self, icon):
        icon.stop()
        self.destroy()

    def show_window(self, icon):
        icon.stop()
        self.after(0,self.deiconify)

    def run_daily(self,option):
        print(option)

if __name__ == "__main__":
    app = MyApp()
    app.resizable(False,False)
    app.mainloop()
