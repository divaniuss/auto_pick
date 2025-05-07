import pyautogui
import tkinter as tk
import time

IsWorking = False
log_messages = []

def log(message):
    global log_messages
    if len(log_messages) >= 10:
        log_messages.pop(0)
    log_messages.append(message)
    log_var.set('\n'.join(log_messages))

def choice(location_hero):
    global IsWorking
    log("пикаем")

    pyautogui.moveTo(location_hero)
    pyautogui.click()

    timer = 0
    while True:
        log("ищем кнопку выбор")

        location_choice = None
        try:
            location_choice = pyautogui.locateCenterOnScreen('dota/choice.png', confidence=0.8)
        except pyautogui.ImageNotFoundException:
            pass

        if location_choice is not None:
            log("выбираем")
            pyautogui.moveTo(location_choice)
            pyautogui.click()

            IsWorking = False
            return

        timer += 1
        if timer >= 10:
            break
        time.sleep(5)

def loop():
    global IsWorking
    if not IsWorking:
        return

    location_ready = None
    try:
        location_ready = pyautogui.locateCenterOnScreen('dota/ready.png', confidence=0.8)
    except pyautogui.ImageNotFoundException:
        pass

    if location_ready is not None:
        pyautogui.moveTo(location_ready)
        time.sleep(1)
        pyautogui.click()

        timer = 0
        while True:
            log("ищем")

            location_tekis = None
            location_disruptor = None

            try:
                location_tekis = pyautogui.locateCenterOnScreen('dota/tekis.png', confidence=0.8)
            except pyautogui.ImageNotFoundException:
                pass
            try:
                location_disruptor = pyautogui.locateCenterOnScreen('dota/disruptor.png', confidence=0.8)
            except pyautogui.ImageNotFoundException:
                pass

            if location_tekis is not None:
                log("нашли: Techies")
                choice(location_tekis)
                break
            elif location_disruptor is not None:
                log("нашли: Disruptor")
                choice(location_disruptor)
                break
            else:
                log("hero in ban")

            timer += 1
            if timer >= 10:
                break
            time.sleep(5)

    else:
        log("ready не найдена")

    if IsWorking:
        root.after(5000, loop)

def start():
    global IsWorking
    if not IsWorking:
        IsWorking = True
        loop()

def stop():
    global IsWorking
    log("stop")
    IsWorking = False

def exit_app():
    stop()
    root.destroy()

root = tk.Tk()
root.geometry("400x400")
root.title("Welcome")

button_width = 30
button_pad_y = 10

tk.Button(root, text="Start", width=button_width, command=start).pack(pady=button_pad_y)
tk.Button(root, text="Stop",  width=button_width, command=stop).pack(pady=button_pad_y)
tk.Button(root, text="Выход",  width=button_width, command=exit_app).pack(pady=button_pad_y)

log_var = tk.StringVar()
log_label = tk.Label(root, textvariable=log_var, anchor="nw", justify="left", bg="black", fg="lime", font=("Consolas", 10))
log_label.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()