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
        w, h = self.width, self.height

        # Deep-space star field.
        for p in self.particles:
            p["y"] -= p["speed"] * 0.30
            if p["y"] < 0.03:
                p["y"] = 0.97
            x = p["x"] * w
            y = p["y"] * h
            r = p["size"]
            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                    fill="#d8c38d", outline="")

        # Moon and atmospheric halo.
        mx, my = w * 0.79, h * 0.23
        mr = min(w, h) * 0.052
        for factor, fill in ((2.4, "#121525"), (1.8, "#20243a"),
                             (1.35, "#4a4a4c"), (1.0, "#e4ddc5")):
            r = mr * factor
            self.canvas.create_oval(mx-r, my-r, mx+r, my+r,
                                    fill=fill, outline="")
        self.canvas.create_oval(mx-mr*.35, my-mr*.10,
                                mx-mr*.02, my+mr*.20,
                                fill="#b9b29d", outline="")

        # Distant blue planet rising below the horizon.
        cx, cy = w * 0.70, h * 1.08
        r = min(w, h) * 0.48
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                fill="#071522", outline="#1f4358", width=2)
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                               start=198, extent=145,
                               outline="#5d7c8d", width=2)

    def _draw_landscape(self, scene):
        w, h = self.width, self.height
        horizon = h * 0.64

        if scene == "sunrise":
            sun_x, sun_y = w * 0.76, h * 0.47
        elif scene == "sunset":
            sun_x, sun_y = w * 0.76, h * 0.43
        else:
            sun_x, sun_y = w * 0.78, h * 0.27

        # Large layered sun with rays.
        ray_length = min(w, h) * 0.18
        for i in range(16):
            angle = i * math.tau / 16
            x1 = sun_x + math.cos(angle) * min(w, h) * 0.075
            y1 = sun_y + math.sin(angle) * min(w, h) * 0.075
            x2 = sun_x + math.cos(angle) * ray_length
            y2 = sun_y + math.sin(angle) * ray_length
            self.canvas.create_line(x1, y1, x2, y2,
                                    fill="#9c7130", width=1)

        for radius, fill in (
            (58, "#493a29"), (46, "#77542b"), (34, "#a8732d"),
            (24, "#d39a3b"), (15, "#f3c968")
        ):
            self.canvas.create_oval(
                sun_x-radius, sun_y-radius, sun_x+radius, sun_y+radius,
                fill=fill, outline=""
            )

        # Atmospheric cloud bands.
        cloud_y = h * 0.35
        for offset, scale in ((0, 1.0), (w*.20, .72), (-w*.24, .62)):
            x = w * .20 + offset
            self.canvas.create_oval(x, cloud_y, x+w*.23*scale,
                                    cloud_y+h*.035,
                                    fill="#50646b", outline="")

        # Layered mountain vista.
        far = [
            0, horizon+25, w*.10, horizon-75, w*.20, horizon-30,
            w*.33, horizon-105, w*.46, horizon-38, w*.59, horizon-92,
            w*.72, horizon-35, w*.86, horizon-82, w, horizon-25, w, h, 0, h
        ]
        mid = [
            0, horizon+55, w*.14, horizon-12, w*.27, horizon-68,
            w*.39, horizon+5, w*.53, horizon-58, w*.67, horizon-2,
            w*.80, horizon-48, w, horizon+10, w, h, 0, h
        ]
        near = [
            0, horizon+90, w*.17, horizon+30, w*.34, horizon+62,
            w*.50, horizon+8, w*.66, horizon+55, w*.82, horizon+22,
            w, horizon+70, w, h, 0, h
        ]
        self.canvas.create_polygon(far, fill="#30494b", outline="")
        self.canvas.create_polygon(mid, fill="#172c2e", outline="")
        self.canvas.create_polygon(near, fill="#091719", outline="")

        # Water / valley reflection.
        water_top = horizon + 92
        self.canvas.create_rectangle(0, water_top, w, h,
                                     fill="#071113", outline="")
        for i in range(10):
            y = water_top + 8 + i * 11
            inset = (i % 3) * w * .05
            self.canvas.create_line(w*.16+inset, y, w*.84-inset, y,
                                    fill="#183033", width=1)

        # Small atmospheric haze near the horizon.
        for i in range(3):
            y = horizon + 8 + i * 13
            self.canvas.create_line(w*.08, y, w*.92, y,
                                    fill="#38514f", width=1)
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
