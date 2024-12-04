from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
DARK_BLUE = "#1e1e2f"
CYAN = "#21c8cf"
ORANGE = "#ffa62b"
PURPLE = "#815ac0"
WHITE = "#ffffff"
FONT_NAME = "Courier"
DEFAULT_WORK_MIN = 25
DEFAULT_SHORT_BREAK_MIN = 5
DEFAULT_LONG_BREAK_MIN = 20
reps = 0
timer = None
is_paused = False
remaining_time = 0

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, is_paused, remaining_time
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=WHITE)
    check_marks.config(text="")
    reps = 0
    is_paused = False
    remaining_time = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps, is_paused, remaining_time
    is_paused = False
    reps += 1

    # Get custom durations
    work_sec = int(work_time_input.get()) * 60
    short_break_sec = int(short_break_time_input.get()) * 60
    long_break_sec = int(long_break_time_input.get()) * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Long Break", fg=PURPLE)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Short Break", fg=ORANGE)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=CYAN)

# ---------------------------- PAUSE/RESUME TIMER ------------------------------- #
def pause_timer():
    global is_paused, remaining_time
    if not is_paused:
        is_paused = True
        window.after_cancel(timer)
    else:
        is_paused = False
        count_down(remaining_time)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, remaining_time
    remaining_time = count
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        play_sound()  # Play sound notification
        log_session()
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# ---------------------------- SOUND NOTIFICATION ------------------------------- #
def play_sound():
    window.bell()  # Produces a system beep sound

# ---------------------------- LOG SESSION ------------------------------- #
def log_session():
    session_type = "Work" if reps % 2 == 1 else "Break"
    print(f"Completed: {session_type} session #{math.ceil(reps / 2)}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=DARK_BLUE)

# Title label
title_label = Label(text="Timer", fg=WHITE, bg=DARK_BLUE, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

# Canvas for timer
canvas = Canvas(width=200, height=224, bg=DARK_BLUE, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill=WHITE, font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Start button
start_button = Button(text="Start", highlightthickness=0, command=start_timer, bg=CYAN, fg=WHITE, font=(FONT_NAME, 10, "bold"))
start_button.grid(column=0, row=2)

# Pause/Resume button
pause_button = Button(text="Pause/Resume", highlightthickness=0, command=pause_timer, bg=ORANGE, fg=WHITE, font=(FONT_NAME, 10, "bold"))
pause_button.grid(column=1, row=2)

# Reset button
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer, bg=PURPLE, fg=WHITE, font=(FONT_NAME, 10, "bold"))
reset_button.grid(column=2, row=2)

# Checkmarks
check_marks = Label(fg=CYAN, bg=DARK_BLUE)
check_marks.grid(column=1, row=3)

# Input fields for custom durations
work_time_label = Label(text="Work (min):", fg=WHITE, bg=DARK_BLUE, font=(FONT_NAME, 12))
work_time_label.grid(column=0, row=4)
work_time_input = Entry(width=5)
work_time_input.insert(END, str(DEFAULT_WORK_MIN))
work_time_input.grid(column=1, row=4)

short_break_time_label = Label(text="Short Break (min):", fg=WHITE, bg=DARK_BLUE, font=(FONT_NAME, 12))
short_break_time_label.grid(column=0, row=5)
short_break_time_input = Entry(width=5)
short_break_time_input.insert(END, str(DEFAULT_SHORT_BREAK_MIN))
short_break_time_input.grid(column=1, row=5)

long_break_time_label = Label(text="Long Break (min):", fg=WHITE, bg=DARK_BLUE, font=(FONT_NAME, 12))
long_break_time_label.grid(column=0, row=6)
long_break_time_input = Entry(width=5)
long_break_time_input.insert(END, str(DEFAULT_LONG_BREAK_MIN))
long_break_time_input.grid(column=1, row=6)

window.mainloop()
