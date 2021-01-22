# John Gresl -- May 2019 -- J.Gresl12@gmail.com

import tkinter as tk

class WidgetToolTip:
    """
    This class allows developers to create a `popup` textbox when the user
    hovers over certain widgets.
    USAGE:
        >>> root = tk.Tk()
        >>> button = tk.Button(master = root, text = "Button", command = None)
        >>> button.pack()
        >>> button_tip = WidgetToolTip(button, "This is the tooltip text!")
        >>> root.mainloop()
    """
    
    def __init__(self, widget, text = "Widget Info", 
                 wait_time = 500, wrap_length = 180):
        """
        Initializes the class. See description above.
        Inputs:
            widget:           Handle to a tkinter widget. Can be a single widget
                              or a list of widgets
            text:        str. Message to be displayed in the tooltip.
            wait_time:   int. # of miliseconds to wait before displaying tooltip
            wrap_length: int. # of pixels to wrap words at inside the tooltip
        """
        self.widgets = [widget] if type(widget) is not list else widget
        self.text = text
        self.wait_time = wait_time
        self.wrap_length = wrap_length
        
        # Create bindings for the widgets
        for idx, widget in enumerate(self.widgets):
            widget.bind("<Enter>",
                        lambda ev, idx = idx: self.enter(idx = idx), add = True)
            widget.bind("<Leave>",
                        lambda ev, idx = idx: self.leave(idx = idx), add = True)
            widget.bind("<ButtonPress>",
                        lambda ev, idx = idx: self.leave(idx = idx), add = True)
        
        # Used for scheduling.
        self.ids = [None] * (idx + 1)
        self.tws = [None] * (idx + 1)
        return

    def enter(self, idx, event = None):
        """ Called when the mouse enters the widget's screen area. """
        self.schedule(idx)

    def leave(self, idx, event = None):
        """ Called when the mouse leaves the widget's screen area. """
        self.unschedule(idx)
        self.hidetip(idx)

    def schedule(self, idx):
        """ Schedules the tooltip to be shown after self._wait_time ms pass. """
        self.unschedule(idx)
        self.ids[idx] = self.widgets[idx].\
                        after(self.wait_time, lambda idx=idx: self.showtip(idx))

    def unschedule(self, idx):
        """ Cancels any currently scheduled tooltips from appearing. """
        for n, tkid in enumerate(self.ids):
            if tkid:
                self.widgets[idx].after_cancel(tkid)
            self.ids[n] = None

    def showtip(self, idx, event=None):
        """ Shows the tooltip on the screen. """
        x = y = 0
        x, y, cx, cy = self.widgets[idx].bbox("insert")
        x += self.widgets[idx].winfo_rootx() + 20
        y += self.widgets[idx].winfo_rooty() + 20
        
        self.tws[idx] = tk.Toplevel(self.widgets[idx])
        self.tws[idx].attributes("-topmost", "true")
        # Leaves only the label and removes the app window
        self.tws[idx].wm_overrideredirect(True)
        self.tws[idx].wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tws[idx], text = self.text, justify='left',
                       background = "#ffffff", relief = 'solid', 
                       borderwidth = 1, wraplength = self.wrap_length)
        label.pack(ipadx = 1)

    def hidetip(self, idx):
        """ Hides the tooltip """
        for n, tw in enumerate(self.tws):
            if tw:
                tw.destroy()
            self.tws[n] = None
