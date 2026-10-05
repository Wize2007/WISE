import math
import random
import tkinter as tk
from datetime import datetime


class WiseStar:
    """Animated Golden Star with a cinematic, smoothly transitioning environment."""

    STATES = {"idle", "listening", "thinking", "speaking", "error", "goodbye"}

    EMOTION_SETTINGS = {
        "neutral": (1.00, 1.00),
        "happy": (1.08, 1.18),
        "sad": (0.92, 0.72),
        "tired": (0.88, 0.62),
        "bored": (0.94, 0.78),
    }

    SCENE_PALETTES = {
        "night": ("#02040b", "#10182c"),
        "evening": ("#130d22", "#50315a"),
        "sunset": ("#3b1830", "#e28a43"),
        "sunrise": ("#8b4c38", "#f7c77a"),
        "day": ("#1685c4", "#bde8ff"),
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
        self._last_scene = "night"
        self._target_scene = "night"
        self._transition_start = None
        self._transition_duration = 2.5

        self.environment = {
            "scene": "night",
            "location": "Nairobi, Kenya",
            "temperature": None,
            "weather": "Weather unavailable",
            "sunrise": None,
            "sunset": None,
            "time": datetime.now(),
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
        if not data:
            return
        old_scene = self.environment.get("scene", "night")
        self.environment.update(data)
        new_scene = self.environment.get("scene", old_scene)
        if new_scene != self._target_scene:
            self._last_scene = self._target_scene
            self._target_scene = new_scene
            self._transition_start = self._clock_seconds()

    def _clock_seconds(self):
        return datetime.now().timestamp()

    def _transition_progress(self):
        if self._transition_start is None:
            return 1.0
        progress = (self._clock_seconds() - self._transition_start) / self._transition_duration
        if progress >= 1.0:
            self._last_scene = self._target_scene
            self._transition_start = None
            return 1.0
        return max(0.0, progress)

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

    def _blend_hex(self, a, b, t):
        a = a.lstrip("#")
        b = b.lstrip("#")
        values = [
            round(int(a[i:i+2], 16) * (1-t) + int(b[i:i+2], 16) * t)
            for i in (0, 2, 4)
        ]
        return "#" + "".join(f"{v:02x}" for v in values)

    def _current_palette(self):
        progress = self._transition_progress()
        a = self.SCENE_PALETTES.get(self._last_scene, self.SCENE_PALETTES["night"])
        b = self.SCENE_PALETTES.get(self._target_scene, self.SCENE_PALETTES["night"])
        return tuple(self._blend_hex(a[i], b[i], progress) for i in range(2)), progress

    def _draw_background(self):
        (top, bottom), transition = self._current_palette()
        scene = self._target_scene
        w, h = self.width, self.height

        bands = 22 if transition >= 0.999 else 12
        for i in range(bands):
            t = i / (bands - 1)
            fill = self._blend_hex(top, bottom, t)
            y0 = h * i / bands
            y1 = h * (i + 1) / bands + 1
            self.canvas.create_rectangle(0, y0, w, y1, fill=fill, outline="")

        if scene in {"night", "evening"}:
            self._draw_space(transition)
        else:
            self._draw_day_world(scene, transition)

        if transition < 1.0:
            old_is_space = self._last_scene in {"night", "evening"}
            new_is_space = scene in {"night", "evening"}
            if old_is_space != new_is_space:
                # The palette crossfade carries the transition; keep both worlds
                # lightweight while they overlap.
                if old_is_space:
                    self._draw_space_overlay(1.0 - transition)
                else:
                    self._draw_day_overlay(1.0 - transition)

    def _draw_space(self, strength=1.0):
        w, h = self.width, self.height
        for p in self.particles:
            p["y"] -= p["speed"] * 0.30
            if p["y"] < 0.03:
                p["y"] = 0.97
            x, y = p["x"] * w, p["y"] * h
            r = p["size"]
            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                    fill="#d8c38d", outline="")

        mx, my = w * 0.79, h * 0.23
        mr = min(w, h) * 0.052
        for factor, fill in (
            (2.4, "#11182a"), (1.8, "#20283d"),
            (1.35, "#5b5d63"), (1.0, "#e4ddc5")
        ):
            r = mr * factor
            self.canvas.create_oval(mx-r, my-r, mx+r, my+r,
                                    fill=fill, outline="")

        cx, cy = w * 0.70, h * 1.08
        r = min(w, h) * 0.48
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                fill="#071522", outline="#2b5368", width=2)
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r,
                               start=198, extent=145,
                               outline="#62889b", width=2)

    def _draw_space_overlay(self, alpha):
        # Lightweight atmospheric veil during a space/day transition.
        w, h = self.width, self.height
        fill = self._blend_hex("#07101c", "#000000", min(1.0, alpha * 0.35))
        self.canvas.create_rectangle(0, 0, w, h, fill=fill, outline="")

    def _draw_day_overlay(self, alpha):
        w, h = self.width, self.height
        fill = self._blend_hex("#bde8ff", "#ffffff", min(1.0, alpha * 0.22))
        self.canvas.create_rectangle(0, 0, w, h, fill=fill, outline="")

    def _draw_day_world(self, scene, transition):
        w, h = self.width, self.height
        horizon = h * 0.62

        now = self.environment.get("time") or datetime.now()
        sun_progress = self._sun_progress(now)
        if scene == "sunrise":
            sun_progress = 0.12
        elif scene == "sunset":
            sun_progress = 0.88
        elif scene in {"day", "sunrise", "sunset"}:
            sun_progress = max(0.0, min(1.0, sun_progress))

        # Sun follows a high arc during the day.
        sun_x = w * (0.10 + 0.80 * sun_progress)
        arc = math.sin(math.pi * sun_progress)
        sun_y = h * (0.57 - 0.38 * arc)
        if scene == "sunrise":
            sun_y = h * 0.56
        elif scene == "sunset":
            sun_y = h * 0.56

        sun_r = min(w, h) * 0.065
        for factor, fill in (
            (3.0, "#d7efff"), (2.3, "#b9e4ff"),
            (1.65, "#fff0ad"), (1.0, "#fff4bf")
        ):
            r = sun_r * factor
            self.canvas.create_oval(
                sun_x-r, sun_y-r, sun_x+r, sun_y+r,
                fill=fill, outline=""
            )

        # Soft cloud banks with darker undersides.
        cloud_specs = [
            (0.08, 0.25, 0.22, 0.055),
            (0.36, 0.17, 0.25, 0.045),
            (0.68, 0.31, 0.20, 0.050),
        ]
        for x, y, cw, ch in cloud_specs:
            px, py = w*x, h*y
            self.canvas.create_oval(px, py, px+w*cw, py+h*ch,
                                    fill="#ffffff", outline="")
            self.canvas.create_oval(px+w*cw*.16, py-h*ch*.45,
                                    px+w*cw*.48, py+h*ch*.55,
                                    fill="#f8fcff", outline="")
            self.canvas.create_oval(px+w*cw*.42, py-h*ch*.25,
                                    px+w*cw*.80, py+h*ch*.65,
                                    fill="#ffffff", outline="")
            self.canvas.create_rectangle(
                px+w*cw*.08, py+h*ch*.42, px+w*cw*.92, py+h*ch*.88,
                fill="#c7d8e2", outline=""
            )

        # Distant blue mountains.
        far = [
            0, horizon+10, w*.10, horizon-95, w*.20, horizon-28,
            w*.32, horizon-118, w*.45, horizon-42, w*.58, horizon-108,
            w*.72, horizon-35, w*.86, horizon-88, w, horizon-20, w, h, 0, h
        ]
        mid = [
            0, horizon+48, w*.13, horizon-15, w*.27, horizon-78,
            w*.39, horizon+2, w*.53, horizon-64, w*.67, horizon-4,
            w*.80, horizon-55, w, horizon+8, w, h, 0, h
        ]
        near = [
            0, horizon+86, w*.17, horizon+28, w*.34, horizon+58,
            w*.50, horizon+5, w*.66, horizon+52, w*.82, horizon+18,
            w, horizon+68, w, h, 0, h
        ]
        self.canvas.create_polygon(far, fill="#6d9fbc", outline="")
        self.canvas.create_polygon(mid, fill="#3d7054", outline="")
        self.canvas.create_polygon(near, fill="#1f4b32", outline="")

        # Green banks.
        bank_y = horizon + 76
        self.canvas.create_polygon(
            0, bank_y, w*.18, bank_y-24, w*.34, bank_y+10,
            w*.50, bank_y-15, w*.67, bank_y+8, w*.83, bank_y-28,
            w, bank_y, w, h, 0, h,
            fill="#163b29", outline=""
        )

        # Lake/valley.
        water_top = horizon + 62
        self.canvas.create_rectangle(0, water_top, w, h,
                                     fill="#2b7892", outline="")
        for i in range(15):
            y = water_top + 8 + i * max(5, h * 0.018)
            width = w * (0.18 + i * 0.025)
            cx = w * 0.50
            self.canvas.create_line(cx-width, y, cx+width, y,
                                    fill="#65b3c5", width=1)

        # Sun reflection and glints.
        reflection = 1.0 - abs(sun_progress - 0.5) * 1.2
        reflection = max(0.25, reflection)
        for i in range(9):
            y = water_top + 10 + i * 8
            half = w * (0.018 + i * 0.006) * reflection
            self.canvas.create_line(
                w*.50-half, y, w*.50+half, y,
                fill="#dff6d2", width=1
            )

        # Horizon haze makes the day scene feel deep rather than flat.
        for i in range(5):
            y = horizon + i * 7
            self.canvas.create_line(w*.04, y, w*.96, y,
                                    fill="#b7d6c6", width=1)

        # Foreground pines.
        for px, scale in ((0.06, 1.0), (0.12, .72), (0.90, .82), (0.96, 1.08)):
            x = w * px
            base = h * 0.90
            height = h * 0.22 * scale
            self._pine(x, base, height)

    def _pine(self, x, base, height):
        trunk = max(2, self.width * 0.004)
        self.canvas.create_rectangle(
            x-trunk, base-height*.10, x+trunk, base,
            fill="#17301e", outline=""
        )
        for i, width in enumerate((0.20, 0.32, 0.44)):
            y = base - height * (0.35 + i*.22)
            hw = height * width
            self.canvas.create_polygon(
                x, y-height*.32, x-hw, y+height*.16,
                x+hw, y+height*.16, fill="#12321f", outline=""
            )

    def _sun_progress(self, now):
        sunrise = self.environment.get("sunrise")
        sunset = self.environment.get("sunset")
        if not sunrise or not sunset:
            hour = now.hour + now.minute / 60.0
            return max(0.0, min(1.0, (hour - 6.0) / 12.0))
        try:
            start = sunrise.replace(tzinfo=None)
            end = sunset.replace(tzinfo=None)
            current = now.replace(tzinfo=None)
            total = (end - start).total_seconds()
            if total <= 0:
                return 0.5
            return max(0.0, min(1.0, (current - start).total_seconds() / total))
        except Exception:
            return 0.5

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
        now = self.environment.get("time") or datetime.now()
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
        energy_pulse = (
            (math.sin(self.phase * 2.3) + 1) * 0.5
            if self.state in {"speaking", "listening", "error"} else 0
        )

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
