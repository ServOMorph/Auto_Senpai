import pyautogui
import time
import sys
import threading
import tkinter as tk
import os

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMAGES")
CONFIDENCE = 0.8


_overlay_active = False

def show_overlay(message, duration=2):
    """Affiche un overlay rouge plein écran non-bloquant pendant `duration` secondes."""
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


def find_and_click_left_half(image_name):
    """Cherche une image dans la moitié gauche de l'écran et clique dessus."""
    screen_width, screen_height = pyautogui.size()
    left_half_width = screen_width // 2

    image_path = f"{IMAGES_DIR}\\{image_name}"
    screenshot = pyautogui.screenshot(region=(0, 0, left_half_width, screen_height))

    try:
        location = pyautogui.locate(image_path, screenshot, confidence=CONFIDENCE)
    except pyautogui.ImageNotFoundException:
        return False

    if location:
        center = pyautogui.center(location)
        # Les coordonnées sont déjà relatives à la moitié gauche (x offset = 0)
        pyautogui.click(center.x, center.y)
        print(f"[OK] Cliqué sur {image_name} à ({center.x}, {center.y})")
        return True
    return False


def find_and_click(image_name):
    """Cherche une image sur tout l'écran et clique dessus."""
    image_path = f"{IMAGES_DIR}\\{image_name}"
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE)
    except pyautogui.ImageNotFoundException:
        print(f"[--] {image_name} non trouvé sur l'écran")
        return False

    if location:
        center = pyautogui.center(location)
        pyautogui.click(center.x, center.y)
        print(f"[OK] Cliqué sur {image_name} à ({center.x}, {center.y})")
        return True
    return False


print("Démarrage du script pub_clicker. Ctrl+C pour arrêter.")
print(f"Résolution écran : {pyautogui.size()}")

try:
    while True:
        # 1. Cherche pub.png dans la moitié gauche de l'écran
        if find_and_click_left_half("pub.png"):
            show_overlay("PUB detectee ! Lancement de l'automatisation...")
            time.sleep(2)

            # 2. Clique sur gagner.png
            find_and_click("gagner.png")
            time.sleep(1)

            # 3. Clique sur valider.png
            find_and_click("valider.png")
            time.sleep(2)

            # 4. Clique sur continuer.png
            find_and_click("continuer.png")
        else:
            # Petite pause avant la prochaine vérification
            time.sleep(0.5)

except KeyboardInterrupt:
    print("\nScript arrêté.")
    sys.exit(0)
