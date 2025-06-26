from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
BLUE = "#1C1678"
PALE_BLUE = "#8576FF"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
tick = ""
time = None

# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    window.after_cancel(time)
    canvas.itemconfig(timer_text, text="00:00")
    timer.config(text="Timer", fg=GREEN, font=(FONT_NAME, 50, "bold"))
    global reps, tick
    reps = 1
    tick = ""
    ticks.config(text=tick)
# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps


    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        countdown(long_break_sec)
        timer.config(text="Long Break", fg=YELLOW, font=(FONT_NAME, 25, "bold"))
    elif reps % 2 == 0:
        countdown(short_break_sec)
        timer.config(text="Short Break", fg=YELLOW, font=(FONT_NAME, 25, "bold"))
    else:
        countdown(work_sec)
        timer.config(text="Work", fg=YELLOW)
    reps += 1
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def countdown(count):
    count_min = count // 60
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global time
        time = window.after(1000, countdown, count - 1)
    else:
        if reps % 2 == 0:
            global tick
            tick += "✔"
            ticks.config(text=tick)
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=BLUE)
window.minsize(width=500, height=500)
window.maxsize(width=500, height=500)

start = Button(text="Start", command=start_timer)
start.grid(column=0, row=2)

timer = Label(text="Timer", fg=PALE_BLUE, bg=BLUE, font=(FONT_NAME, 50, "bold"))
timer.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=BLUE, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

ticks = Label(text=tick, fg=GREEN, bg=BLUE, font=(FONT_NAME, 24, "bold"))
ticks.grid(column=1, row=3)

reset = Button(text="Reset", command=reset_timer)
reset.grid(column=2, row=2)




window.mainloop()
