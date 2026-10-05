import math
import random
import tkinter as tk


class WiseStar:
    """Lightweight, reusable animated Golden Star visual for WISE."""

    STATES = {
        "idle",
        "listening",
        "thinking",
        "speaking",
        "error",
        "goodbye",
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

        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg="#050505",
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.random = random.Random(7319)
        self.particles = [
            {
                "x": self.random.uniform(0.08, 0.92),
                "y": self.random.uniform(0.10, 0.90),
                "speed": self.random.uniform(0.0008, 0.0020),
                "size": self.random.uniform(1.0, 2.4),
                "phase": self.random.uniform(0, math.tau),
            }
            for _ in range(20)
        ]

        self._bind_resize()
        self._animate()

    def _bind_resize(self):
        self.canvas.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.width = max(320, event.width)
        self.height = max(280, event.height)

    def set_state(self, state):
        if state not in self.STATES:
            state = "idle"
        self.state = state

        if state == "goodbye":
            self._closing = True

    def set_emotion(self, emotion):
        self.emotion = emotion if emotion in self.EMOTION_SETTINGS else "neutral"

    def _state_motion(self):
        if self.state == "idle":
            return 0.006, 0.018, 0.0
        if self.state == "listening":
            return 0.014, 0.034, 0.0
        if self.state == "thinking":
            return 0.025, 0.022, 0.8
        if self.state == "speaking":
            return 0.040, 0.050, 0.0
        if self.state == "error":
            return 0.018, 0.040, 2.2
        if self.state == "goodbye":
            return 0.020, 0.020, 0.0
        return 0.006, 0.018, 0.0

    def _star_points(self, cx, cy, outer, inner, rotation):
        points = []
        point_count = 10

        for i in range(point_count * 2):
            angle = rotation - math.pi / 2 + i * math.pi / point_count
            radius = outer if i % 2 == 0 else inner
            points.extend(
                (
                    cx + math.cos(angle) * radius,
                    cy + math.sin(angle) * radius,
                )
            )

        return points

    def _draw_particles(self, cx, cy, radius):
        for particle in self.particles:
            particle["y"] -= particle["speed"]
            if particle["y"] < 0.06:
                particle["y"] = 0.94
                particle["x"] = self.random.uniform(0.08, 0.92)

            drift = math.sin(self.phase * 1.8 + particle["phase"]) * 7
            x = particle["x"] * self.width + drift
            y = particle["y"] * self.height
            distance = math.hypot(x - cx, y - cy)

            if distance < radius * 1.45:
                continue

            size = particle["size"]
            self.canvas.create_oval(
                x - size,
                y - size,
                x + size,
                y + size,
                fill="#8f6a24",
                outline="",
            )

    def _draw_star(self):
        self.canvas.delete("all")

        cx = self.width * 0.47
        cy = self.height * 0.49

        speed, pulse_amount, rotation_speed = self._state_motion()
        emotion_scale, emotion_energy = self.EMOTION_SETTINGS[self.emotion]

        self.phase += speed
        self.rotation += rotation_speed * 0.035

        breathing = math.sin(self.phase) * pulse_amount
        energy_pulse = (
            (math.sin(self.phase * 2.3) + 1.0) * 0.5
            if self.state in {"speaking", "listening", "error"}
            else 0.0
        )

        if self.state == "goodbye":
            fade = max(0.0, 1.0 - (self.phase % 6.0) / 2.0)
            scale = max(0.08, fade)
        else:
            scale = 1.0

        base_radius = min(self.width, self.height) * 0.205
        radius = base_radius * emotion_scale * scale
        radius *= 1.0 + breathing + energy_pulse * 0.045 * emotion_energy

        self._draw_particles(cx, cy, radius)

        glow_levels = [
            (1.85, "#211b0c"),
            (1.58, "#3b2c0e"),
            (1.38, "#5d4310"),
            (1.20, "#8b6416"),
        ]

        for factor, fill in glow_levels:
            points = self._star_points(
                cx,
                cy,
                radius * factor,
                radius * factor * 0.42,
                self.rotation,
            )
            self.canvas.create_polygon(
                points,
                fill=fill,
                outline="",
            )

        core_points = self._star_points(
            cx,
            cy,
            radius,
            radius * 0.40,
            self.rotation,
        )
        self.canvas.create_polygon(
            core_points,
            fill="#d99f20",
            outline="#f6cf63",
            width=1,
        )

        inner_points = self._star_points(
            cx,
            cy,
            radius * 0.68,
            radius * 0.30,
            self.rotation,
        )
        self.canvas.create_polygon(
            inner_points,
            fill="#f0bd3e",
            outline="",
        )

        center = radius * 0.34
        self.canvas.create_oval(
            cx - center,
            cy - center,
            cx + center,
            cy + center,
            fill="#fff1b0",
            outline="",
        )

        # A small, restrained digital-energy ring.
        ring_radius = radius * (
            1.52 + math.sin(self.phase * 1.5) * 0.05
        )
        self.canvas.create_oval(
            cx - ring_radius,
            cy - ring_radius,
            cx + ring_radius,
            cy + ring_radius,
            outline="#6f5015",
            width=1,
        )

        self.canvas.create_text(
            cx,
            cy + radius * 1.72,
            text="W I S E",
            fill="#b88a2a",
            font=("Arial", 10, "bold"),
        )

    def _animate(self):
        if not self.canvas.winfo_exists():
            return

        self._draw_star()

        if self.state == "goodbye" and self._closing:
            # Continue fading while the interface performs its clean shutdown.
            self.canvas.after(50, self._animate)
            return

        self._after_id = self.canvas.after(50, self._animate)

    def stop(self):
        if self._after_id is not None:
            try:
                self.canvas.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None
