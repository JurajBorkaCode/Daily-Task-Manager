import tkinter as tk
import tkinter.ttk as ttk
import pystray
from PIL import Image
import pandas as pd
import os
import webbrowser
from datetime import date
import sys


def load_data():
    if os.path.isfile("dailies.csv"):
        data = pd.read_csv("dailies.csv")
    else:
        data.to_csv("dailies.csv", sep=',', index=False, encoding="utf-8")



def save_data():
    pass

class MyApp(tk.Tk):
    data = pd.DataFrame(columns=["Daily","type","shortcut","date"])

    def __init__(self):
        super().__init__()


        self.load_data()
        self.title("Daily app manager")
        self.geometry('500x725')
        self.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)

        self.tasks = ttk.Treeview(columns=("Daily"),show='headings',height=25)
        self.tasks.column("Daily", anchor=tk.CENTER, stretch=tk.NO, width=480)
        self.tasks.heading("Daily",text="Daily")
        self.tasks.grid(row=0, column=0, columnspan=3, padx=(10,10), pady=(10,10))

        for index,row in self.data.iterrows():
            if str(row["date"]) == str(date.today()):
                self.tasks.insert('',"end",values=(row["Daily"],),tags=("completed"))
            else:
                self.tasks.insert('',"end",values=(row["Daily"],),tags=("uncompleted"))

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
        self.new_daily_name_entry = tk.Entry(new_daily_frame,width=52,selectborderwidth=10)

        new_daily_name_label.grid(row=0,column=0)
        self.new_daily_name_entry.grid(row=0,column=1,columnspan=2)

        new_daily_type = tk.Menubutton(new_daily_frame,text="Daily Type", relief=tk.RAISED,width=20)
        new_daily_type.grid(row=1,column=0)

        new_daily_type.menu = tk.Menu(new_daily_type, tearoff=0)
        new_daily_type["menu"] = new_daily_type.menu

        self.typeVar = tk.StringVar(self,"None")

        new_daily_type.menu.add_radiobutton(label="None",variable=self.typeVar)
        new_daily_type.menu.add_radiobutton(label="Website",variable=self.typeVar)
        new_daily_type.menu.add_radiobutton(label="Application",variable=self.typeVar)
        new_daily_type.grid(row=1,column=0)

        self.shorcutVar = tk.StringVar(self,"Daily Shortcut")

        new_daily_shortcut = tk.Entry(new_daily_frame,width=52,selectborderwidth=10,textvariable=self.shorcutVar)
        new_daily_shortcut.grid(row=1,column=1,columnspan=2)


        create_button = tk.Button(new_daily_frame,text="Create New Daily",command=self.create_new_daily,width=18)
        create_button.grid(row=2,column=0,columnspan=3, padx=(10,10),pady=(10,10))

    def create_new_daily(self):
        #new_daily = {"Daily":self.new_daily_name_entry.get(),"type":self.typeVar.get(),"shortcut":self.shorcutVar.get(),"date":1,"alert":self.alertVar.get(),"time":f"{self.alert_time_hour.get()}:{self.alert_time_min.get()}"}
        self.data.loc[len(self.data), ["Daily","type","shortcut","date"]] = self.new_daily_name_entry.get(),self.typeVar.get(),self.shorcutVar.get(),1
        self.save_data()
        self.reload_dailies()



    def selected_item(self):
        item = self.tasks.focus()
        return self.tasks.item(item)
    
    def delete_selected(self):
        daily = self.selected_item()["values"][0]
        daily_index = self.data.loc[self.data["Daily"] == daily].index[0]
        self.data = self.data.drop(self.data.index[[daily_index]])
        self.save_data()
        self.reload_dailies()



    def complete_selected(self):
        daily = self.selected_item()["values"][0]
        daily_index = self.data.loc[self.data["Daily"] == daily].index[0]
        self.data.loc[daily_index, "date"] = date.today()
        self.save_data()
        self.reload_dailies()






    def open_selected(self):
        task = self.selected_item()["values"][0]
        self.open_daily(task)

    def load_data(self):
        if os.path.isfile("dailies.csv"):
            self.data = pd.read_csv("dailies.csv")
        else:
            self.data.to_csv("dailies.csv", sep=',', index=False, encoding="utf-8")

    def reload_dailies(self):
        self.tasks.delete(*self.tasks.get_children())

        for index,row in self.data.iterrows():
            if str(row["date"]) == str(date.today()):
                self.tasks.insert('',"end",values=(row["Daily"],),tags=("completed"))
            else:
                self.tasks.insert('',"end",values=(row["Daily"],),tags=("uncompleted"))

    def save_data(self):
        self.data.to_csv("dailies.csv", sep=',', index=False, encoding="utf-8")

    def create_menu(self):
        out = []
        for index,row in self.data.iterrows():
            if str(row["date"]) != str(date.today()):
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


    def create_icon(self):
        try:
            count = self.data["date"].value_counts()[str(date.today())]
        except:
            count = 0
        data_size = len(self.data.index)
        if count != 0:
            image1_size = int((count/data_size)*64)
        else:
            image1_size = 0
        image1 = Image.new('RGB', (image1_size, 64), (0, 255, 0))
        image2 = Image.new('RGB', (64-image1_size, 64), (255, 0, 0))
        image = Image.new('RGB',(64, 64), (250,250,250))
        image.paste(image1,(0,0))
        image.paste(image2,(image1.size[0],0))
        return image

    def minimize_to_tray(self):
        self.withdraw()
        image = self.create_icon()
        menu = self.create_menu()
        icon = pystray.Icon("name", image, "My App", menu)
        icon.icon = image
        icon.run()

    def quit_window(self, icon):
        icon.stop()
        self.destroy()

    def show_window(self, icon):
        icon.stop()
        self.after(0,self.deiconify)

    def run_daily(self,option):
        print(option)

    def set_alerts(self):
        pass

if __name__ == "__main__":
    app = MyApp()
    app.resizable(False,False)
    app.mainloop()


