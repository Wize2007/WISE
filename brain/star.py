import math
import random
import tkinter as tk


class WiseStar:
    """Animated Golden Star with a living day/night environment."""

    STATES = {
        "idle", "listening", "thinking", "speaking", "error", "goodbye"
    }

    EMOTION_SETTINGS = {
        "neutral": (1.00, 1.00),
        "happy": (1.08, 1.18),
        "sad": (0.92, 0.72),
        "tired": (0.88, 0.62),
        "bored": (0.94, 0.78),
    }

    def __init__(self, parent, width=560, height=500):
        self.parent = parent
        self.width = width
        self.height = height
        self.state = "idle"
        self.emotion = "neutral"
        self.phase = 0.0
        self.rotation = 0.0
        self._after_id = None
        self._closing = False
        self.environment = {
            "scene": "night",
            "location": "Nairobi, Kenya",
            "temperature": None,
            "weather": "Weather unavailable",
            "sunrise": None,
            "sunset": None,
        }

        self.canvas = tk.Canvas(
            parent, width=width, height=height,
            bg="#050505", highlightthickness=0, bd=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.random = random.Random(7319)
        self.particles = [
            {
                "x": self.random.uniform(0.04, 0.96),
                "y": self.random.uniform(0.06, 0.94),
                "speed": self.random.uniform(0.0006, 0.0018),
                "size": self.random.uniform(0.8, 2.2),
                "phase": self.random.uniform(0, math.tau),
            }
            for _ in range(34)
        ]

        self.canvas.bind("<Configure>", self._on_resize)
        self._animate()

    def _on_resize(self, event):
        self.width = max(320, event.width)
        self.height = max(280, event.height)

    def set_state(self, state):
        self.state = state if state in self.STATES else "idle"
        if self.state == "goodbye":
            self._closing = True

    def set_emotion(self, emotion):
        self.emotion = emotion if emotion in self.EMOTION_SETTINGS else "neutral"

    def set_environment(self, data):
        if data:
            self.environment.update(data)

    def _state_motion(self):
        return {
            "idle": (0.006, 0.018, 0.0),
            "listening": (0.014, 0.034, 0.0),
            "thinking": (0.025, 0.022, 0.8),
            "speaking": (0.040, 0.050, 0.0),
            "error": (0.018, 0.040, 2.2),
            "goodbye": (0.020, 0.020, 0.0),
        }.get(self.state, (0.006, 0.018, 0.0))

    def _star_points(self, cx, cy, outer, inner, rotation):
        points = []
        for i in range(20):
            angle = rotation - math.pi / 2 + i * math.pi / 10
            radius = outer if i % 2 == 0 else inner
            points.extend((cx + math.cos(angle) * radius,
                           cy + math.sin(angle) * radius))
        return points

    def _draw_background(self):
        scene = self.environment.get("scene", "night")
        w, h = self.width, self.height

        # Layered bands create a lightweight cinematic gradient without dependencies.
        if scene in {"sunrise", "sunset"}:
            top, bottom = "#100d18", "#8a4b20"
        elif scene in {"day"}:
            top, bottom = "#102033", "#31556a"
        elif scene == "evening":
            top, bottom = "#100d20", "#34244a"
        else:
            top, bottom = "#02030a", "#090b18"

        bands = 18
        for i in range(bands):
            t = i / (bands - 1)
            fill = self._blend_hex(top, bottom, t)
            y0 = h * i / bands
            y1 = h * (i + 1) / bands + 1
            self.canvas.create_rectangle(0, y0, w, y1, fill=fill, outline="")

        if scene in {"night", "evening"}:
            self._draw_space()
        else:
            self._draw_landscape(scene)

    def _blend_hex(self, a, b, t):
        a = a.lstrip("#")
        b = b.lstrip("#")
        values = [
            round(int(a[i:i+2], 16) * (1-t) + int(b[i:i+2], 16) * t)
            for i in (0, 2, 4)
        ]
        return "#" + "".join(f"{v:02x}" for v in values)

    def _draw_space(self):
        for p in self.particles:
            p["y"] -= p["speed"] * 0.35
            if p["y"] < 0.03:
                p["y"] = 0.97
            x = p["x"] * self.width
            y = p["y"] * self.height
            r = p["size"]
            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                    fill="#b99b61", outline="")

        # A subtle distant planet horizon.
        cx = self.width * 0.72
        cy = self.height * 1.05
        r = min(self.width, self.height) * 0.43
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                fill="#0c1722", outline="#1d3342", width=1)

    def _draw_landscape(self, scene):
        w, h = self.width, self.height
        horizon = h * 0.66

        if scene == "sunrise":
            sun_y = h * 0.39
            sun_x = w * 0.72
        elif scene == "sunset":
            sun_y = h * 0.42
            sun_x = w * 0.74
        else:
            sun_y = h * 0.28
            sun_x = w * 0.76

        for radius, fill in [
            (42, "#5f4a2a"), (30, "#896a32"), (20, "#d1a44a"), (12, "#f4d27b")
        ]:
            self.canvas.create_oval(
                sun_x-radius, sun_y-radius, sun_x+radius, sun_y+radius,
                fill=fill, outline=""
            )

        far = [
            0, horizon+28, w*.14, horizon-58, w*.28, horizon+5,
            w*.42, horizon-72, w*.56, horizon+12, w*.72, horizon-48,
            w*.86, horizon+3, w, horizon-62, w, h, 0, h
        ]
        near = [
            0, horizon+58, w*.18, horizon-18, w*.34, horizon+40,
            w*.50, horizon-34, w*.66, horizon+36, w*.82, horizon-24,
            w, horizon+45, w, h, 0, h
        ]
        self.canvas.create_polygon(far, fill="#172a2c", outline="")
        self.canvas.create_polygon(near, fill="#0b1719", outline="")

        # Foreground "vista" floor.
        self.canvas.create_rectangle(0, horizon+75, w, h, fill="#070d0d", outline="")

        # A few thin atmospheric lines.
        for i in range(3):
            y = horizon + 18 + i * 15
            self.canvas.create_line(w*.12, y, w*.88, y,
                                    fill="#243e3b", width=1)

    def _draw_star_particles(self, cx, cy, radius):
        for particle in self.particles[:18]:
            drift = math.sin(self.phase * 1.8 + particle["phase"]) * 6
            x = particle["x"] * self.width + drift
            y = particle["y"] * self.height
            if math.hypot(x-cx, y-cy) < radius * 1.45:
                continue
            size = particle["size"]
            self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                    fill="#8f6a24", outline="")

    def _draw_info(self):
        now = self.environment.get("time")
        if now is None:
            from datetime import datetime
            now = datetime.now()

        time_text = now.strftime("%I:%M %p")
        date_text = now.strftime("%A • %d %B %Y").upper()
        temp = self.environment.get("temperature")
        temp_text = f"{temp:.0f}°C" if isinstance(temp, (int, float)) else "--°C"
        location = self.environment.get("location", "Location unavailable")
        weather = self.environment.get("weather", "")

        self.canvas.create_text(
            self.width * 0.05, self.height * 0.075,
            text=time_text, anchor="w",
            fill="#f2d98c", font=("Arial", 18, "bold")
        )
        self.canvas.create_text(
            self.width * 0.05, self.height * 0.125,
            text=date_text, anchor="w",
            fill="#c0b99f", font=("Arial", 8, "bold")
        )
        self.canvas.create_text(
            self.width * 0.95, self.height * 0.075,
            text=temp_text, anchor="e",
            fill="#f2d98c", font=("Arial", 16, "bold")
        )
        self.canvas.create_text(
            self.width * 0.95, self.height * 0.125,
            text=location.upper(), anchor="e",
            fill="#c0b99f", font=("Arial", 8, "bold")
        )
        self.canvas.create_text(
            self.width * 0.95, self.height * 0.16,
            text=weather.upper(), anchor="e",
            fill="#898777", font=("Arial", 7)
        )

    def _draw_star(self):
        self.canvas.delete("all")
        self._draw_background()
        self._draw_info()

        cx = self.width * 0.47
        cy = self.height * 0.49
        speed, pulse_amount, rotation_speed = self._state_motion()
        emotion_scale, emotion_energy = self.EMOTION_SETTINGS[self.emotion]

        self.phase += speed
        self.rotation += rotation_speed * 0.035
        breathing = math.sin(self.phase) * pulse_amount
        energy_pulse = ((math.sin(self.phase * 2.3) + 1) * 0.5
                        if self.state in {"speaking", "listening", "error"} else 0)

        scale = 1.0
        if self.state == "goodbye":
            scale = max(0.08, 1.0 - (self.phase % 6.0) / 2.0)

        base_radius = min(self.width, self.height) * 0.205
        radius = base_radius * emotion_scale * scale
        radius *= 1 + breathing + energy_pulse * 0.045 * emotion_energy

        self._draw_star_particles(cx, cy, radius)

        for factor, fill in [
            (1.85, "#211b0c"), (1.58, "#3b2c0e"),
            (1.38, "#5d4310"), (1.20, "#8b6416")
        ]:
            self.canvas.create_polygon(
                self._star_points(cx, cy, radius*factor, radius*factor*.42, self.rotation),
                fill=fill, outline=""
            )

        self.canvas.create_polygon(
            self._star_points(cx, cy, radius, radius*.40, self.rotation),
            fill="#d99f20", outline="#f6cf63", width=1
        )
        self.canvas.create_polygon(
            self._star_points(cx, cy, radius*.68, radius*.30, self.rotation),
            fill="#f0bd3e", outline=""
        )

        center = radius * .34
        self.canvas.create_oval(cx-center, cy-center, cx+center, cy+center,
                                fill="#fff1b0", outline="")

        ring = radius * (1.52 + math.sin(self.phase*1.5)*.05)
        self.canvas.create_oval(cx-ring, cy-ring, cx+ring, cy+ring,
                                outline="#6f5015", width=1)

        self.canvas.create_text(
            cx, cy + radius*1.72, text="W I S E",
            fill="#b88a2a", font=("Arial", 10, "bold")
        )

    def _animate(self):
        try:
            if not self.canvas.winfo_exists():
                return
            self._draw_star()
            self._after_id = self.canvas.after(50, self._animate)
        except tk.TclError:
            return

    def stop(self):
        if self._after_id is not None:
            try:
                self.canvas.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None
