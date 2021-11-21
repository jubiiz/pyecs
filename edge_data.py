from tkinter import *

# code very much adapted from https://www.pythontutorial.net/tkinter/tkinter-frame/#:~:text=The%20size%20of%20a%20frame%20is%20determined%20by,ttk.Frame%20%28container%2C%20height%2C%20width%29%20Code%20language%3A%20Python%20%28python%29

def create_radio_frame(parent):
    frame = Frame(parent)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=2)
        
    t = StringVar(value="resistance")
    # battery radio
    bat_rad = Radiobutton(frame, text="battery", value="battery", justify="left", variable=t)
    bat_rad.grid(column=0, row=0)

    # resistance radio
    res_rad = Radiobutton(frame, text="resistance",value="resistance", justify="left", variable=t)
    res_rad.grid(column=0, row=1)




    return(frame, t)

def create_main_window():
    # root window
    root = Tk()
    root.title("Component Information")
    w = 300 # width for the Tk root
    h = 100 # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = int((ws/2) - (w/2))
    y = int((hs/2) - (h/2))

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry(f'{w}x{h}+{x}+{y}')
    root.resizable(0, 0)

    # layout on the root window
    root.columnconfigure(0, weight=1)
    root.columnconfigure(2, weight=3)

    # radios
    radio_frame, c_type = create_radio_frame(root)
    radio_frame.grid(column=0, row=0)

    # text input
    # TODO
    
    mainloop()
    return((c_type).get(), ))


if __name__ == "__main__":
    create_main_window()