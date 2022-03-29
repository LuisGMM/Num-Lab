
import Question1
import Question2
import Question3
import Question4

import numpy as np

from tkinter import *
from tkinter import (
    ttk,
)

from abc import ABC




class FrameCodeQuestion(ABC, Frame):

    def __init__(self, parent, master, question_number):
        Frame.__init__(self, parent)
        
        self.question_number = question_number
        self.filename = f'Question{self.question_number}.py'
        self.code = self.extract_code()

        
        self.init_scroll()
        self.initUI()
        

    def initUI(self):
        self.label_code = Label(self.scrollable_frame, text=self.code, justify="left")
        self.label_code.grid(row = 0, column = 0, sticky ="nsew")
    
    def init_scroll(self):
        self.canvas = Canvas(self)

        self.canvas.grid(sticky=(N,W,S,E))

        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas,borderwidth=2)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox(ALL)
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def extract_code(self) -> str:
        with open(self.filename, 'r') as f:
            return f.read()


class Toolbar(Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):

        self.toolbar = Menu(self.master)
        self.master.config(menu=self.toolbar)

        self.toolbar.add_command(label="Question 1", command=lambda: self.master.show_frame(FrameQuestion1))    
        self.toolbar.add_command(label="Question 2", command=lambda: self.master.show_frame(FrameQuestion2))
        self.toolbar.add_command(label="Question 3", command=lambda: self.master.show_frame(FrameQuestion3))
        self.toolbar.add_command(label="Question 4", command=lambda: self.master.show_frame(FrameQuestion4))

        self.menu_code = Menu(self.toolbar)
        self.toolbar.add_cascade(label="Codes", menu=self.menu_code)

        self.menu_code.add_command(label="Algorithm", command=lambda: self.master.show_frame(FrameCodeAlgorithm))  
        self.menu_code.add_command(label="Question 1", command=lambda: self.master.show_frame(FrameCodeQuestion1))  
        self.menu_code.add_command(label="Question 2", command=lambda: self.master.show_frame(FrameCodeQuestion2))  
        self.menu_code.add_command(label="Question 3", command=lambda: self.master.show_frame(FrameCodeQuestion3))  
        self.menu_code.add_command(label="Question 4", command=lambda: self.master.show_frame(FrameCodeQuestion4))  

        self.toolbar.add_command(label="Exit", underline=0, command=self.onExit)

        self.menu = Menu(self.master, tearoff=0)
        self.menu.add_command(label="Beep", command=self.bell)
        self.menu.add_command(label="Exit", command=self.onExit)

        self.master.bind("<Button-3>", self.showMenu)
        self.pack()

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.quit()


class FrameCodeAlgorithm(FrameCodeQuestion):
    
    def __init__(self, parent, master):
        Frame.__init__(self, parent)
        
        self.code = self.extract_code()
        
        self.init_scroll()
        self.initUI()

    def initUI(self):
        self.label_code = Label(self.scrollable_frame, text=self.code, justify="left")
        self.label_code.grid(row = 0, column = 0, sticky ="nsew")
    
    def init_scroll(self):
        self.canvas = Canvas(self)

        self.canvas.grid(sticky=(N,W,S,E))

        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas,borderwidth=2)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox(ALL)
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    
    def extract_code(self) -> str:
        with open('algorithm.py', 'r') as f:
            return f.read()


class FrameQuestion1(Frame):

    def __init__(self, parent, master):
            Frame.__init__(self, parent)
    
            label = Label(self, text ='Select the $k_0$ of the packet you want to visualize')
            label.grid(row=0, column=0, padx=10, pady=10)
    
            combobox_k0 = ttk.Combobox(self, values=[k0 for k0 in np.arange(0.5,8,0.5)])
            combobox_k0.grid(row=0, column=1, padx=10, pady=10)
            
            button_run = Button(self, text ="Run animation", command=lambda: Question1.run(k0=combobox_k0.get()))
            button_run.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    
            button_last = Button(self, text="Next question", command=lambda: master.show_frame(FrameQuestion2))
            button_last.grid(row=2, column=1, padx=10, pady=10)

class FrameCodeQuestion1(FrameCodeQuestion):
    
    def __init__(self, parent, master):
        FrameCodeQuestion.__init__(self, parent, master,  question_number=1)


class FrameQuestion2(Frame):

    def __init__(self, parent, master):
            Frame.__init__(self, parent)
    
            label = Label(self, text ='Select the $k_0$ of the packet you want to visualize')
            label.grid(row=0, column=0, padx=10, pady=10)
    
            combobox_k0 = ttk.Combobox(self, values=[k0 for k0 in np.arange(0.5,8,0.5)])
            combobox_k0.grid(row=0, column=1, padx=10, pady=10)
    
            button_run_1 = Button(self, text ="Run animation", command=lambda: Question2.run_graph1(psi_filename=f'psi_{combobox_k0.get()}.npy'))
            button_run_1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            button_run_2 = Button(self, text ="Run plot", command=lambda: Question2.run_graph2(psi_filename=f'psi_{combobox_k0.get()}.npy'))
            button_run_2.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
            
            button_next = Button(self, text="Next question", command=lambda: master.show_frame(FrameQuestion3))
            button_next.grid(row=2, column=1, padx=10, pady=10)
    
            button_last = Button(self, text="Last question", command=lambda: master.show_frame(FrameQuestion1))
            button_last.grid(row=2, column=0, padx=10, pady=10)


class FrameCodeQuestion2(FrameCodeQuestion):
    
    def __init__(self, parent, master):
        FrameCodeQuestion.__init__(self, parent, master, question_number=2)


class FrameQuestion3(Frame):

    def __init__(self, parent, master):
            Frame.__init__(self, parent)
    
            button_run = Button(self, text ="Run plot", command=lambda: Question3.run())
            button_run.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
            button_next = Button(self, text="Next question", command=lambda: master.show_frame(FrameQuestion4))
            button_next.grid(row=2, column=1, padx=10, pady=10)
    
            button_last = Button(self, text="Last question", command=lambda: master.show_frame(FrameQuestion2))
            button_last.grid(row=2, column=0, padx=10, pady=10)


class FrameCodeQuestion3(FrameCodeQuestion):
    
    def __init__(self, parent, master):
        FrameCodeQuestion.__init__(self, parent, master, question_number=3)


class FrameQuestion4(Frame):

    def __init__(self, parent, master):
            Frame.__init__(self, parent)
    
            label = Label(self, text ="Startpage")
            label.grid(row = 0, column = 4, padx = 10, pady = 10)
    
            button_run = Button(self, text ="Run plot", command=lambda: Question4.run())
            button_run.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
    
            button_last = Button(self, text="Last question", command=lambda: master.show_frame(FrameQuestion3))
            button_last.grid(row=2, column=0, padx=10, pady=10)


class FrameCodeQuestion4(FrameCodeQuestion):
    
    def __init__(self, parent, master):
        FrameCodeQuestion.__init__(self, parent, master, question_number=4)


class MainApp(Tk):
     
    def __init__(self, *args, **kwargs):
         
        Tk.__init__(self, *args, **kwargs)
        
        self.title("Quantum Physics numerical lab")
        self.geometry("800x500+300+300")
        
        self.toolbar = Toolbar(master=self)
        self.toolbar.pack(side = "top", fill = "both", expand = True)

        container = Frame(self) 
        container.pack(side = "bottom", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
  
        for F in (FrameQuestion1, FrameQuestion2, FrameQuestion3, FrameQuestion4,
                  FrameCodeQuestion1, FrameCodeQuestion2, FrameCodeQuestion3, FrameCodeQuestion4, FrameCodeAlgorithm):
  
            frame = F(container, self)
            self.frames[F] = frame  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(FrameQuestion1)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()




if __name__ == '__main__':
    
    app = MainApp()
    app.mainloop()