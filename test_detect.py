import pyautogui
import time
import threading
import tkinter as tk
import os

IMAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMAGES", "prochaine_vue.png")
CONFIDENCE = 0.8


_overlay_active = False

def show_overlay(message, duration=2):
    global _overlay_active
    if _overlay_active:
        return
    _overlay_active = True

    def _show():
        global _overlay_active
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.85)
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"{sw}x{sh}+0+0")
        root.configure(bg="#cc0000")
        tk.Label(
            root, text=message, fg="white", bg="#cc0000",
            font=("Arial", 48, "bold"), wraplength=sw - 100
        ).pack(expand=True)
        root.after(duration * 1000, root.quit)
        root.mainloop()
        root.destroy()
        _overlay_active = False

    threading.Thread(target=_show, daemon=True).start()


print("Test de détection - prochaine_vue.png")
print("Ctrl+C pour arrêter\n")

try:
    while True:
        try:
            location = pyautogui.locateOnScreen(IMAGE, confidence=CONFIDENCE)
            if location:
                center = pyautogui.center(location)
                print(f"[TROUVE] position={location} | centre=({center.x}, {center.y})")
                show_overlay("PUB detectee ! Lancement de l'automatisation...")
        except pyautogui.ImageNotFoundException:
            print("[--] non trouvé")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nArrêté.")
