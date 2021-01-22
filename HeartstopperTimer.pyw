# Author: John Gresl January 22 2021
# General purpose loop-able timer for farming items in Maplestory
#   - Can have multiple instances
#   - Has "Always-On-Top"
#   - Flashes and beeps when it's time for you to recast summon/loot/whatever 

# Quick and dirty, don't expect too much. I did this in an afternoon.

import os
import sys
import tkinter as tk
import winsound

from PIL import ImageTk, Image

from WidgetTooltips import WidgetToolTip

BG_COLOR = "#00a7b3"

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)


class ToggleButton(tk.Button):
  def __init__(self, master, state0_img_path, state1_img_path, 
               extra_command=None, **config):
    super().__init__(master=master, command = self._on_click, **config)
    self.extra_command = extra_command
    self.state = 0 # Will either be 0 or 1
    self.state0_img = Image.open(resource_path(state0_img_path))
    self.state0_img = self.state0_img.resize((30, 30), Image.ANTIALIAS)
    self.state0_tk = ImageTk.PhotoImage(self.state0_img, master=master)
    self.state1_img = Image.open(resource_path(state1_img_path))
    self.state1_img = self.state1_img.resize((30, 30), Image.ANTIALIAS)
    self.state1_tk = ImageTk.PhotoImage(self.state1_img, master=master)
    self.state_tks = [self.state0_tk, self.state1_tk]
    self.config(image=self.state0_tk)
    return

  def _on_click(self):
    self.state = int(not self.state) # Toggle
    self.config(image=self.state_tks[self.state])
    if self.extra_command:
      self.extra_command()
    return


class HSTimer(object):
  def __init__(self, seconds):
    self.seconds = seconds
    self.max_time_at_click = seconds
    self.current_time = seconds
    self.timer_active = False
    self.missing_rectangle = None
    self._progress_flag = 0
    self._create_root()
    self._create_header()
    self.header_frame.grid(row=0, column=0, columnspan=2)
    self._create_time_entry()
    self.time_frame.grid(row=1,column=0)
    self._create_control_buttons()
    self.control_frame.grid(row=1, column=1)
    self._create_action_button()
    self.action_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W)
    self.root.after(100, self.update_progress)
    self.root.mainloop()    
    return

  def _create_root(self):
    self.root = tk.Tk()
    self.root.resizable(False, False)
    self.root.configure(background=BG_COLOR)
    self.root.title("Myoni Shark's HS Timer")
    self.root.iconbitmap(resource_path("heartstopper.ico"))
    self.topmost = "true"
    self.root.attributes("-topmost", self.topmost)
    return

  def _create_header(self):
    self.header_frame = tk.Frame(master=self.root, background=BG_COLOR)
    self.stopper_img = Image.open(resource_path("heartstopper.png"))
    self.stopper_tk = ImageTk.PhotoImage(self.stopper_img)
    left = tk.Label(master=self.header_frame, 
                    image=self.stopper_tk,
                    background=BG_COLOR)
    left.image = self.stopper_tk
    left.grid(row=0, column=0)
    header_label = tk.Label(master=self.header_frame,
                            text="HS Timer",
                            background=BG_COLOR,
                            font=("Comic Sans MS", 24, "bold"))
    header_label.grid(row=0, column=1)
    right = tk.Label(master=self.header_frame,
                     image=self.stopper_tk,
                     background=BG_COLOR)
    right.iamge = self.stopper_tk
    right.grid(row=0, column=2)
    return 

  def _create_time_entry(self):
    self.time_frame = tk.Frame(master=self.root, background=BG_COLOR)
    time_label = tk.Label(master=self.time_frame,
                          text="Time:",
                          font=("Comic Sans MS", 14),
                          background=BG_COLOR)
    time_label.grid(row=0, column=0)
    self.time_var = tk.StringVar(master=self.time_frame,value=self.seconds)
    self.time_entry = tk.Entry(master=self.time_frame,
                               background=BG_COLOR,
                               foreground="yellow",
                               font=("Comic Sans MS", 14),
                               text="10",
                               width=9,
                               textvariable=self.time_var)
    self.time_entry.grid(row=0, column=1, padx=[0, 5])
    self.time_entry.bind("<ButtonRelease-1>", 
                         lambda ev, tk_entry=self.time_entry: \
                           self._select_all(tk_entry))
    self.time_entry.bind("<Key>", 
                         lambda ev, 
                                tk_var=self.time_var,
                                tk_entry=self.time_entry: \
                                  self._validate_int_entry(tk_var, 
                                                           tk_entry,
                                                           ev))
    return

  def _validate_int_entry(self, ivar, entry, ev):
    if ev.keysym in ["Tab", "Left", "Right", "BackSpace", "Delete"]:
      return
    if ev.keysym in ("Up", "Home"):
      entry.icursor(0)
      entry.selection_clear()
      return "break"
    if ev.keysym in ("Down", "End"):
      entry.icursor("end")
      entry.selection_clear()
      return "break"
    if ev.keysym not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
      return "break"
    if entry.selection_present():
      entry.delete("sel.first", "sel.last")
    prior_value = ivar.get() or "0"
    entry.insert(tk.INSERT, ev.keysym)
    if int(ivar.get()) > 99999:
      ivar.set(prior_value)
      entry.icursor("end")
    return "break"
  
  def _select_all(self, tk_entry):
    tk_entry.selection_range(0, "end")
    tk_entry.icursor("end")
    return

  def _create_control_buttons(self):
    self.control_frame = tk.Frame(master=self.root, background=BG_COLOR)
    self.play_button = ToggleButton(master=self.control_frame,
                                    state0_img_path="pause.png",
                                    state1_img_path="play.png",
                                    background=BG_COLOR,
                                    activebackground=BG_COLOR)
    self.play_button.grid(row=0, column=0)
    WidgetToolTip(self.play_button, "Start/Stop the timer")

    self.sound_button = ToggleButton(master=self.control_frame,
                                     state0_img_path="sounds_on.png",
                                     state1_img_path="sounds_off.png",
                                     background=BG_COLOR,
                                     activebackground=BG_COLOR)
    self.sound_button.grid(row=0, column=1)
    WidgetToolTip(self.sound_button, "Volume On/Off")

    self.loop_button = ToggleButton(master=self.control_frame,
                                    state0_img_path="loop.png",
                                    state1_img_path="no_loop.png",
                                    background=BG_COLOR,
                                    activebackground=BG_COLOR)
    self.loop_button.grid(row=0, column=2)
    WidgetToolTip(self.loop_button, "Automatically Loop")

    self.pin_button = ToggleButton(master=self.control_frame,
                                   state0_img_path="pin1.png",
                                   state1_img_path="no_pin1.png",
                                   background=BG_COLOR,
                                   activebackground=BG_COLOR,
                                   extra_command = lambda: self._toggle_topmost())    
    self.pin_button.grid(row=0, column=3)                                   
    WidgetToolTip(self.pin_button, "Always On Top")
    return

  def _toggle_topmost(self):
    if self.topmost == "true":
      self.topmost = "false"
    elif self.topmost == "false":
      self.topmost = "true"
    else: # uh ohs
      return
    self.root.attributes("-topmost", self.topmost)
    return

  def _create_action_button(self):
    self.action_frame = tk.Frame(master=self.root, background=BG_COLOR)
    self.action_var = tk.StringVar(master=self.action_frame, 
                                   value=f"{self.seconds} sec.")
    self.action_button = tk.Button(master=self.action_frame,
                                   textvariable=self.action_var,
                                   font=("Comic Sans MS", 20, "bold"),
                                   background=BG_COLOR,
                                   activebackground=BG_COLOR,
                                   height=1, width=14,
                                   bd=10,
                                   relief=tk.RAISED,
                                   command=self._button_click)
    self.action_button.grid(row=0, column=0, sticky=tk.NSEW)
    self.progress_canvas = tk.Canvas(master=self.action_frame, 
                                     width=45,
                                     height=120,
                                     background="#66ff6b", 
                                     highlightthickness=3, 
                                     highlightbackground="brown")
    self.progress_canvas.grid(row=0, column=1)
    return

  def _button_click(self):
    self.max_time_at_click = int(self.time_var.get() or 0)
    self.reset_timer()
    if self.timer_active:
      return
    self.timer_active = True
    self.decrement_timer()
    return

  def decrement_timer(self, ):
    if not self.timer_active:
      return
    if self.play_button.state == 1: # Paused
      self.root.after(100, self.decrement_timer)
      return
    self.current_time -= 1
    self._progress_flag = 0
    if self.current_time < -5:
      if self.loop_button.state == 0: # Do loop
        self.reset_timer()
      else:
        self.timer_active = False
        return
    elif self.current_time == 0:
      self.schedule_beeps(5)
    elif self.current_time < 0:
      self.action_var.set(f"{self.current_time} sec.")
      # if self.sound_button.state == 0: # Sound on
      #   winsound.Beep(frequency=2000, duration=800)
      #   self.root.after(200, self.decrement_timer)
      # else:
      
      self.root.after(1000, self.decrement_timer)
      return
    if self.current_time <=  5:
      self.action_button.config(bg="red")
    elif self.current_time <= 10:
      self.action_button.config(bg="yellow")
    self.action_var.set(f"{self.current_time} sec.")
    self.root.after(1000, self.decrement_timer)
    return

  def schedule_beeps(self, n_beeps):
    for i in range(n_beeps):
      self.root.after(140*i, lambda: self.single_beep(400, 130))
    return

  def single_beep(self, frequency, duration):
    if self.sound_button.state == 0: # Sound on
      winsound.Beep(frequency=frequency, duration=duration)

  def update_progress(self):
    frequency = 20 # 10 Hz
    if self.play_button.state == 1: # Paused
      self.root.after(int(1000./frequency), self.update_progress)
      return
    if not self.timer_active:
      self.root.after(int(1000./frequency), self.update_progress)
      return
    
    if self.max_time_at_click == 0:
      percent = 1
    else:
      percent = (self.current_time-self._progress_flag)/self.max_time_at_click
    progress_width =  self.progress_canvas.winfo_width()
    progress_height = self.progress_canvas.winfo_height()
    
    start = (progress_width, progress_height)
    end = (0, round(progress_height*percent))
    if self.missing_rectangle:
      self.progress_canvas.delete(self.missing_rectangle)
    self.missing_rectangle = self.progress_canvas.create_rectangle(*start, 
                                                                   *end,
                                                                   fill="red")
    self._progress_flag += (1./frequency)
    self.root.after(int(1000./frequency), self.update_progress)
    return

  def reset_timer(self):
    try:
      self.current_time = int(self.time_entry.get())
    except ValueError:
      self.current_time = 0
    self.action_var.set(f"{self.current_time} sec.")
    self.action_button.config(bg=BG_COLOR)
    return


if __name__ == "__main__":
  try:
    timer = HSTimer(150)
  except Exception as e:
    import traceback
    with open("errors.log", "w") as err:
      traceback.print_exc(err)
      err.write("\n\nPlease report this error to Myoni")
    raise e

  