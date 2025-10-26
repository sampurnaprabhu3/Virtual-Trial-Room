import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image
import PIL.ImageTk
import mediapipe as mp
import os
from pathlib import Path
import numpy as np


class VirtualTrialRoom:
    def __init__(self, window):
        self.window = window
        self.window.title("Mirrorly – Virtual Trial Room")
        self.window.state("zoomed")
        self.window.configure(bg="#121212")

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            model_complexity=2
        )

        self.camera = None
        self.current_cloth_index = 0
        self.clothes = self.load_clothes()
        self.last_landmarks = None
        self.cart = []

        self.cloth_width = 160
        self.cloth_height = 200
        self.cloth_rotation = 0

        self.preview_images = []
        self.debug_label = None

        self.create_homepage()

    def load_clothes(self):
        clothes_dir = Path("assets/clothes")
        clothes = []
        if clothes_dir.exists():
            for file in clothes_dir.glob("*"):
                if file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    clothes.append(str(file))
        return clothes

    def create_homepage(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.window, style="TFrame")
        main_frame.pack(expand=True, fill="both")

        style = ttk.Style()
        style.configure("TFrame", background="#121212")
        style.configure("Title.TLabel", font=("Helvetica Neue", 36, "bold"),
                        foreground="#ffffff", background="#121212")
        style.configure("Subtitle.TLabel", font=("Georgia", 16, "italic"),
                        foreground="#bbbbbb", background="#121212")
        style.configure("Start.TButton", font=("Helvetica Neue", 14),
                        foreground="#000000", background="#1f1f1f")

        title = ttk.Label(
            main_frame, text="Mirrorly – Virtual Trial Room", style="Title.TLabel")
        title.pack(pady=40)

        subtitle = ttk.Label(main_frame, text="Style is a way to say who you are without speaking.",
                             style="Subtitle.TLabel")
        subtitle.pack(pady=10)

        start_button = ttk.Button(
            main_frame, text="Start Try-On", style="Start.TButton", command=self.start_camera)
        start_button.pack(pady=40)

    def start_camera(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.window, style="TFrame")
        main_frame.pack(fill="both", expand=True)

        left_panel = tk.Frame(main_frame, bg="#1f1f1f", width=300)
        left_panel.pack(side="left", fill="y")

        title = tk.Label(left_panel, text="Clothing Preview", font=("Helvetica Neue", 16, "bold"),
                         fg="white", bg="#1f1f1f")
        title.pack(pady=10)

        # Scrollable canvas setup
        canvas = tk.Canvas(left_panel, bg="#1f1f1f", highlightthickness=0)
        scrollbar = tk.Scrollbar(
            left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1f1f1f")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for index, path in enumerate(self.clothes):
            img = cv2.imread(path)
            img = cv2.resize(img, (100, 140))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = PIL.Image.fromarray(img)
            photo = PIL.ImageTk.PhotoImage(img_pil)
            self.preview_images.append(photo)

            thumb_frame = tk.Frame(scrollable_frame, bg="#1f1f1f")
            thumb_frame.grid(row=index // 2, column=index % 2, padx=6, pady=6)

            lbl = tk.Label(thumb_frame, image=photo, bg="#1f1f1f")
            lbl.image = photo
            lbl.pack()

            btn1 = tk.Button(thumb_frame, text="Try This", command=lambda i=index: self.set_outfit(i),
                             bg="#2a2a2a", fg="#dddddd", font=("Arial", 9), relief="flat")
            btn1.pack(pady=(2, 1))

            btn2 = tk.Button(thumb_frame, text="Add to Cart",
                             command=lambda i=index: self.add_to_cart(i),
                             bg="#3a3a3a", fg="#dddddd", font=("Arial", 9), relief="flat")
            btn2.pack()

        right_panel = tk.Frame(main_frame, bg="#121212")
        right_panel.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(right_panel, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        control_frame = tk.Frame(right_panel, bg="#121212")
        control_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("Dark.TButton", background="#000000",
                        foreground="#000000", font=("Arial", 11))

        ttk.Button(control_frame, text="Next Outfit", command=self.next_outfit, style="Dark.TButton").pack(
            side="left", padx=10)
        ttk.Button(control_frame, text="Add to Cart", command=lambda: self.add_to_cart(self.current_cloth_index), style="Dark.TButton").pack(
            side="left", padx=10)
        ttk.Button(control_frame, text="View Cart", command=self.view_cart, style="Dark.TButton").pack(
            side="left", padx=10)
        ttk.Button(control_frame, text="Back to Home", command=self.create_homepage, style="Dark.TButton").pack(
            side="left", padx=10)

        self.debug_label = ttk.Label(
            right_panel, text="", foreground="white", background="#121212", font=("Arial", 12))
        self.debug_label.pack(pady=4)

        self.camera = cv2.VideoCapture(0)
        self.update_camera()

        self.window.bind("<w>", self.increase_height)
        self.window.bind("<s>", self.decrease_height)
        self.window.bind("<a>", self.rotate_left)
        self.window.bind("<d>", self.rotate_right)
        self.window.bind("<q>", self.increase_width)
        self.window.bind("<e>", self.decrease_width)

    def get_size_label(self, width):
        if width < 150:
            return "XS"
        elif width < 170:
            return "S"
        elif width < 200:
            return "M"
        elif width < 230:
            return "L"
        elif width < 260:
            return "XL"
        elif width < 290:
            return "XXL"
        else:
            return "Free"

    def set_outfit(self, index):
        self.current_cloth_index = index

    def add_to_cart(self, index):
        if index not in self.cart:
            self.cart.append(index)

    def view_cart(self):
        cart_window = tk.Toplevel(self.window)
        cart_window.title("Cart")
        cart_window.configure(bg="#1f1f1f")

        if not self.cart:
            label = tk.Label(cart_window, text="Your cart is empty.",
                             fg="white", bg="#1f1f1f", font=("Arial", 14))
            label.pack(pady=20)
        else:
            for idx in self.cart:
                path = self.clothes[idx]
                img = cv2.imread(path)
                img = cv2.resize(img, (120, 160))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = PIL.Image.fromarray(img)
                photo = PIL.ImageTk.PhotoImage(img_pil)

                frame = tk.Frame(cart_window, bg="#1f1f1f")
                frame.pack(pady=10)

                lbl = tk.Label(frame, image=photo, bg="#1f1f1f")
                lbl.image = photo
                lbl.pack(side="left", padx=10)

                name = os.path.basename(path)
                tk.Label(frame, text=name, font=("Arial", 12),
                         fg="white", bg="#1f1f1f").pack(side="left")

    def next_outfit(self):
        if self.clothes:
            self.current_cloth_index = (
                self.current_cloth_index + 1) % len(self.clothes)

    def overlay_clothing(self, frame, landmarks):
        if not self.clothes or landmarks is None:
            return frame

        try:
            cloth_path = self.clothes[self.current_cloth_index]
            cloth_img = cv2.imread(cloth_path, cv2.IMREAD_UNCHANGED)
            if cloth_img is None:
                return frame

            l_shoulder = landmarks.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            r_shoulder = landmarks.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            l_hip = landmarks.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]

            h, w = frame.shape[:2]
            center_x = int((l_shoulder.x + r_shoulder.x) * w / 2)
            center_y = int((l_shoulder.y + l_hip.y) * h / 2)

            cloth = cv2.resize(
                cloth_img, (self.cloth_width, self.cloth_height))
            M = cv2.getRotationMatrix2D(
                (self.cloth_width // 2, self.cloth_height // 2), self.cloth_rotation, 1.0)
            cloth = cv2.warpAffine(
                cloth, M, (self.cloth_width, self.cloth_height))

            y1 = max(center_y - self.cloth_height // 2, 0)
            y2 = min(y1 + self.cloth_height, h)
            x1 = max(center_x - self.cloth_width // 2, 0)
            x2 = min(x1 + self.cloth_width, w)

            if cloth.shape[2] == 4:
                alpha = cloth[:y2 - y1, :x2 - x1, 3] / 255.0
                for c in range(3):
                    frame[y1:y2, x1:x2, c] = (1 - alpha) * frame[y1:y2, x1:x2, c] + \
                        alpha * cloth[:y2 - y1, :x2 - x1, c]
            else:
                frame[y1:y2, x1:x2] = cloth[:y2 - y1, :x2 - x1]

        except Exception as e:
            print(f"Overlay error: {e}")

        return frame

    def update_camera(self):
        if self.camera is None:
            return
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)

            if results.pose_landmarks:
                frame = self.overlay_clothing(frame, results)
            elif self.last_landmarks:
                frame = self.overlay_clothing(frame, self.last_landmarks)

            self.last_landmarks = results.pose_landmarks if results.pose_landmarks else self.last_landmarks

            self.canvas.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 0 and canvas_height > 0:
                frame = cv2.resize(frame, (canvas_width, canvas_height))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = PIL.Image.fromarray(frame)
            photo = PIL.ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.photo = photo

            size_label = self.get_size_label(self.cloth_width)
            self.debug_label.config(text=f"Current Size: {size_label}")

        self.window.after(10, self.update_camera)

    def increase_height(self, _): self.cloth_height += 10
    def decrease_height(self, _): self.cloth_height = max(
        100, self.cloth_height - 10)

    def rotate_left(self, _): self.cloth_rotation -= 10
    def rotate_right(self, _): self.cloth_rotation += 10
    def increase_width(self, _): self.cloth_width += 10

    def decrease_width(self, _): self.cloth_width = max(
        100, self.cloth_width - 10)


if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualTrialRoom(root)
    root.mainloop()
