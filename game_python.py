import tkinter as tk
from tkinter import messagebox
from questions import questions

# 🎨 Color palette
BG_COLOR = "#1e1f2b"
PRIMARY = "#4a90e2"
SECONDARY = "#f5a623"
TEXT_COLOR = "#ffffff"
CORRECT_COLOR = "#4caf50"
WRONG_COLOR = "#e74c3c"

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Quiz Master Game ✨")
        self.root.geometry("600x420")
        self.root.config(bg=BG_COLOR)

        self.score = 0
        self.time_left = 5
        self.question_index = 0
        self.timer_id = None

        # Title
        self.title_label = tk.Label(root, text="🧠 QUIZ MASTER", font=("Comic Sans MS", 22, "bold"),
                                    bg=BG_COLOR, fg=SECONDARY)
        self.title_label.pack(pady=10)

        # Score + Timer
        self.status_frame = tk.Frame(root, bg=BG_COLOR)
        self.status_frame.pack(pady=5)

        self.score_label = tk.Label(self.status_frame, text=f"Score: {self.score}", font=("Arial", 14, "bold"),
                                    bg=BG_COLOR, fg=TEXT_COLOR)
        self.score_label.pack(side="left", padx=20)

        self.timer_label = tk.Label(self.status_frame, text=f"⏱ Time: {self.time_left}s", font=("Arial", 14, "bold"),
                                    bg=BG_COLOR, fg=SECONDARY)
        self.timer_label.pack(side="right", padx=20)

        # Question text
        self.question_label = tk.Label(root, text="", wraplength=520, font=("Arial", 16, "bold"),
                                       bg=BG_COLOR, fg=TEXT_COLOR)
        self.question_label.pack(pady=20)

        # Option buttons
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 14), width=22,
                            bg=PRIMARY, fg="white", relief="raised", bd=3,
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        # Start button
        self.start_button = tk.Button(root, text="🎮 Start Quiz", font=("Arial", 14, "bold"), bg=SECONDARY,
                                      fg="white", width=15, command=self.start_quiz)
        self.start_button.pack(pady=25)

    # -------------------------------
    def start_quiz(self):
        self.score = 0
        self.question_index = 0
        self.update_score()
        self.start_button.pack_forget()
        self.load_question()

    # -------------------------------
    def load_question(self):
        # Stop previous timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if self.question_index >= len(questions):
            messagebox.showinfo("Quiz Finished", f"🎉 Game Over!\nYour final score: {self.score}")
            self.root.destroy()
            return

        q = questions[self.question_index]
        self.question_label.config(text=q["question"])

        # Update options
        for i, opt in enumerate(q["options"]):
            self.option_buttons[i].config(text=opt, bg=PRIMARY, state="normal")

        self.time_left = 5
        self.update_timer_display()
        self.countdown()

    # -------------------------------
    def countdown(self):
        self.timer_label.config(text=f"⏱ Time: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.countdown)
        else:
            self.time_up()

    # -------------------------------
    def time_up(self):
        for btn in self.option_buttons:
            btn.config(state="disabled")
        messagebox.showinfo("⏰ Time's Up", "You ran out of time! 0 point.")
        self.next_round(0)

    # -------------------------------
    def check_answer(self, i):
        q = questions[self.question_index]
        selected = q["options"][i]

        # Stop timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        for btn in self.option_buttons:
            btn.config(state="disabled")

        if selected == q["answer"]:
            self.option_buttons[i].config(bg=CORRECT_COLOR)
            points = 2
        else:
            self.option_buttons[i].config(bg=WRONG_COLOR)
            points = -1

        self.root.after(1000, lambda: self.next_round(points))

    # -------------------------------
    def next_round(self, points):
        self.score += points
        self.update_score()
        self.question_index += 1
        self.load_question()

    # -------------------------------
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_timer_display(self):
        self.timer_label.config(text=f"⏱ Time: {self.time_left}s")


# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()
