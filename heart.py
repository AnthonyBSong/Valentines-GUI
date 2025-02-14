import tkinter as tk
import tkinter.messagebox as messagebox

import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Use the TkAgg backend for embedding in Tkinter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------------
# Your heart-curve code
# -----------------------------
def heart_curve(x, a):
    """
    Your custom heart function:
      y = 0.6 * cbrt(x^2) + 0.5 * sqrt(max(5 - x^2, 0)) * sin(2π a x)
    """
    term1 = 0.6 * np.cbrt(x ** 2)
    term2 = 0.5 * np.sqrt(np.maximum(5 - x**2, 0)) * np.sin(2 * a * np.pi * x)
    return term1 + term2

def create_heart_figure():
    """
    Creates the matplotlib Figure and Axes, then sets up the animated line
    using heart_curve(). Returns the figure, line object, and animation instance.
    """
    x = np.linspace(-5, 5, 1000)

    fig, ax = plt.subplots(figsize=(8, 4))
    line, = ax.plot(x, heart_curve(x, 0), color='red', lw=2)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-1.5, 2)
    ax.axis('off')

    def update(a):
        y = heart_curve(x, a)
        line.set_ydata(y)
        return line,

    forward_frames = np.linspace(0, 10, 100)
    reverse_frames = forward_frames[::-1]
    combined_frames = np.concatenate((forward_frames, reverse_frames))

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=combined_frames,
        blit=True,
        interval=10,
        repeat=True
    )

    return fig, line, ani

# -----------------------------
# Popup window for the question
# -----------------------------
class ValentinePopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Question")
        self.parent = parent

        # We track how many times 'No' was clicked
        self.no_count = 0

        # The series of question texts after each 'No'
        self.no_texts = [
            "Are you sure?",
            "Are you REALLY sure?",
            "Will you REALLY not be my valentine? 😭",
            "Last chance 🥺"
        ]
        # The final message if the user presses No again
        self.final_message = "Alright 😔"

        # Initial question
        self.label = tk.Label(self, text="Do you want to be my valentine?")
        self.label.pack(padx=20, pady=10)

        # Buttons
        self.btn_yes = tk.Button(self, text="Yes", command=self.on_yes)
        self.btn_yes.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_no = tk.Button(self, text="No", command=self.on_no)
        self.btn_no.pack(side=tk.RIGHT, padx=10, pady=10)

    def on_yes(self):
        """If user says 'Yes': show 'Yay!!!' and close."""
        messagebox.showinfo("Yay!", "Woohoo!!!")
        self.destroy()

    def on_no(self):
        """
        If user says 'No', change the prompt text in sequence.
        After we've exhausted our list, show final sad message & close.
        """
        self.no_count += 1

        if self.no_count <= len(self.no_texts):
            new_text = self.no_texts[self.no_count - 1]
            self.label.config(text=new_text)
        else:
            messagebox.showinfo("Oh...", self.final_message)
            self.destroy()

# -----------------------------
# Main application (Tk)
# -----------------------------
class ValentineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Valentine Heart Animation")

        # 1) Build the figure that has the animated heart
        fig, line, ani = create_heart_figure()

        # 2) Embed the figure in this Tk window
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 3) The "Start" button at the bottom
        self.start_button = tk.Button(self, text="Start", command=self.show_valentine_popup)
        self.start_button.pack(side=tk.BOTTOM, pady=5)

    def show_valentine_popup(self):
        """Create the popup window asking for Valentine acceptance."""
        ValentinePopup(self)

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    app = ValentineApp()
    app.mainloop()
