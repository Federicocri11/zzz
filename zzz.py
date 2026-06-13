#!/usr/bin/env python3
"""
Zzz - utility keep-awake cross-platform (Windows & macOS).

Simula la pressione di un tasto innocuo (F15, un "no-op": non scrive nulla
e non sposta il focus) a intervalli randomizzati, per resettare il timer di
inattivita' del sistema ed evitare lo spegnimento dello schermo / lo
screensaver. Gira come icona nella system tray, con toggle on/off e
intervallo configurabile.

Nota macOS: per inviare eventi sintetici l'app deve avere il permesso
"Accessibilita'" (Impostazioni di Sistema > Privacy e sicurezza >
Accessibilita'). Al primo avvio macOS lo richiede.
"""

import random
import threading
import time

import pystray
from PIL import Image, ImageDraw
from pynput.keyboard import Controller, Key
from pystray import Menu, MenuItem as Item

keyboard = Controller()

# Intervalli disponibili (secondi): etichetta -> (min, max)
INTERVALS = {
    "~2 min": (110, 130),
    "~3-4 min": (180, 240),
    "~5 min": (280, 320),
}
DEFAULT_LABEL = "~3-4 min"


class KeepAwake:
    """Motore: in un thread separato invia un F15 a intervalli casuali."""

    def __init__(self):
        self._running = threading.Event()
        self._thread = None
        self.label = DEFAULT_LABEL
        self.lo, self.hi = INTERVALS[DEFAULT_LABEL]

    def _loop(self):
        while self._running.is_set():
            keyboard.press(Key.f15)
            keyboard.release(Key.f15)
            # dormo a piccoli passi cosi' stop() risponde subito
            total = random.uniform(self.lo, self.hi)
            slept = 0.0
            while slept < total and self._running.is_set():
                time.sleep(0.5)
                slept += 0.5

    def start(self):
        if not self._running.is_set():
            self._running.set()
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running.clear()

    def toggle(self):
        self.stop() if self.active else self.start()

    @property
    def active(self):
        return self._running.is_set()

    def set_interval(self, label):
        self.label = label
        self.lo, self.hi = INTERVALS[label]


def make_icon(active):
    """Icona tray: tazzina stilizzata. Verde = attivo, grigio = fermo."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    color = (46, 204, 113) if active else (127, 140, 141)
    # corpo tazza
    d.rounded_rectangle((14, 22, 42, 50), radius=4, fill=color)
    # manico
    d.ellipse((40, 28, 54, 44), outline=color, width=4)
    # vapore (solo quando attivo)
    if active:
        d.line((22, 8, 22, 18), fill=color, width=3)
        d.line((32, 8, 32, 18), fill=color, width=3)
    return img


def build(engine):
    """Costruisce l'icona tray e il menu."""

    def on_toggle(icon, item):
        engine.toggle()
        icon.icon = make_icon(engine.active)
        icon.update_menu()

    def make_interval_handler(label):
        def handler(icon, item):
            engine.set_interval(label)
            icon.update_menu()
        return handler

    def is_selected(label):
        return lambda item: engine.label == label

    def on_quit(icon, item):
        engine.stop()
        icon.stop()

    interval_items = [
        Item(label, make_interval_handler(label),
             checked=is_selected(label), radio=True)
        for label in INTERVALS
    ]

    menu = Menu(
        Item(lambda item: "Attivo  \u2713" if engine.active else "Disattivato",
             on_toggle),
        Menu.SEPARATOR,
        Item("Intervallo", Menu(*interval_items)),
        Menu.SEPARATOR,
        Item("Esci", on_quit),
    )

    return pystray.Icon("Zzz", make_icon(engine.active), "Zzz", menu)


def main():
    engine = KeepAwake()
    engine.start()  # parte attivo: e' lo scopo dell'avvio
    icon = build(engine)
    icon.run()


if __name__ == "__main__":
    main()
