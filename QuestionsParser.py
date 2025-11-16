import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass, field
from typing import List, Optional, Set
import random
import pickle
import os

from pprint import pprint as print

@dataclass
class QuestionBlock:
    correctness: str
    question: str
    choices: List[str]
    personal_comment: Optional[str]
    official_explanation: Optional[str]
    correct_answers: Set[str] = field(default_factory=set)
    right: Optional[bool] = None

def parse_file(path: str) -> List[QuestionBlock]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    blocks = [b.strip() for b in raw.split("---") if b.strip()]
    parsed: List[QuestionBlock] = []

    for block in blocks:
        lines = [l.rstrip() for l in block.splitlines()]
        idx = 0
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx >= len(lines):
            continue

        correctness_line = lines[idx].strip().lower()
        if correctness_line.startswith("wrong"):
            correctness = "wrong"
        elif correctness_line.startswith("guessed"):
            correctness = "guessed"
        else:
            continue

        body = lines[idx + 1:]
        while body and not body[0].strip():
            body = body[1:]
        if not body:
            continue

        question = body[0].strip()
        body = body[1:]
        while body and not body[0].strip():
            body = body[1:]
        if not body:
            continue

        explanation = None
        comment = None

        if "```" in body:
            first_fence = body.index("```")
            try:
                second_fence = body.index("```", first_fence + 1)
                explanation_lines = body[first_fence + 1 : second_fence]
                explanation = "\n".join(explanation_lines).strip()
                pre_expl = body[:first_fence]
            except ValueError:
                pre_expl = body
        else:
            pre_expl = body

        while pre_expl and not pre_expl[-1].strip():
            pre_expl = pre_expl[:-1]

        if not pre_expl:
            continue

        if len(pre_expl) >= 2:
            comment = pre_expl[-1].strip()
            choices = [l.strip() for l in pre_expl[:-1]]
        else:
            comment = None
            choices = [l.strip() for l in pre_expl]

        choices = [choice for choice in choices if choice != '']

        parsed.append(
            QuestionBlock(
                correctness=correctness,
                question=question,
                choices=choices,
                personal_comment=comment,
                official_explanation=explanation,
            )
        )

    return parsed

class MCQViewer:
    def __init__(self, root, questions: List[QuestionBlock]):
        self.root = root

        if os.path.exists('QuestionsWithCorrectChoice.pkl'):
            with open('QuestionsWithCorrectChoice.pkl', 'rb') as f:
                self.questions = pickle.load(f)
            self.show_check = True
        else:
            self.questions = questions[:]
            self.show_check = False

        random.shuffle(self.questions)
        self.state = {i: {"vars": [], "revealed": False} for i in range(len(self.questions))}
        self.index = 0

        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill="x")

        self.q_number_label = tk.Label(self.top_frame, text="", font=("Arial", 16))
        self.q_number_label.pack(anchor="nw", padx=10, pady=5)

        self.q_label = tk.Label(root, wraplength=850, font=("Arial", 21), justify="left")
        self.q_label.pack(pady=10)

        self.copy_button = tk.Button(root, text="Copy Question", command=self.copy_question, font=("Arial", 16))
        self.copy_button.pack(pady=5)

        self.choice_frame = tk.Frame(root)
        self.choice_frame.pack(pady=10, fill="both", expand=True)

        self.rev_button = tk.Button(root, text="Reveal Answer", command=self.reveal_answer, font=("Arial", 16))
        self.rev_button.pack(pady=5)

        self.check_button = None
        if self.show_check:
            self.check_button = tk.Button(root, text="Check", command=self.check_answer, font=("Arial", 16))
            self.check_button.pack(pady=5)

        self.explanation_label = tk.Label(root, wraplength=850, font=("Arial", 18), fg="blue", justify="left")
        self.explanation_label.pack(pady=10, fill="x")

        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side="bottom", pady=10)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.prev_question, font=("Arial", 16))
        self.prev_button.grid(row=0, column=0, padx=20)

        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.next_question, font=("Arial", 16))
        self.next_button.grid(row=0, column=1, padx=20)

        self.render_question()

    def copy_question(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.questions[self.index].question)

    def render_question(self):
        q = self.questions[self.index]
        self.q_label.config(text=q.question, bg="SystemButtonFace")
        self.q_number_label.config(text=f"Question {self.index + 1} / {len(self.questions)}")

        for w in self.choice_frame.winfo_children():
            w.destroy()

        if not self.state[self.index]["vars"]:
            shuffled_choices = q.choices[:]
            random.shuffle(shuffled_choices)
            vars_list = []
            for c in shuffled_choices:
                v = tk.BooleanVar()
                chk = tk.Checkbutton(self.choice_frame, text=c, variable=v, font=("Arial", 18), anchor="w")
                chk.pack(anchor="w", pady=5, fill="x")
                vars_list.append((v, c))
            self.state[self.index]["vars"] = vars_list
        else:
            for v, c in self.state[self.index]["vars"]:
                chk = tk.Checkbutton(self.choice_frame, text=c, variable=v, font=("Arial", 18), anchor="w")
                chk.pack(anchor="w", pady=5, fill="x")

        # Retroactively highlight if right/wrong determined
        if q.right is not None:
            self.q_label.config(bg="green" if q.right else "red")
            self.state[self.index]["revealed"] = True
            self.explanation_label.config(text=self.build_explanation(q))
        else:
            if self.state[self.index]["revealed"]:
                self.explanation_label.config(text=self.build_explanation(q))
            else:
                self.explanation_label.config(text="")

        if self.show_check and self.index == len(self.questions)-1:
            self.next_button.config(text="Finish")
        else:
            self.next_button.config(text="Next")

    def build_explanation(self, q):
        parts = []
        if q.personal_comment:
            parts.append("Personal Comment: " + q.personal_comment)
        if q.official_explanation:
            parts.append("Official Explanation: " + q.official_explanation)
        return "\n\n".join(parts)

    def reveal_answer(self):
        self.state[self.index]["revealed"] = True
        self.explanation_label.config(text=self.build_explanation(self.questions[self.index]))

    def check_answer(self):
        q = self.questions[self.index]
        selected = {c for v, c in self.state[self.index]["vars"] if v.get()}
        if q.correct_answers:
            q.right = selected == q.correct_answers
            self.q_label.config(bg="green" if q.right else "red")
            self.state[self.index]["revealed"] = True

    def finish_display(self):
        # Auto-check all unanswered questions
        for q_idx, q in enumerate(self.questions):
            if q.right is None and q.correct_answers:
                selected = {c for v, c in self.state[q_idx]["vars"] if v.get()}
                q.right = selected == q.correct_answers
                self.state[q_idx]["revealed"] = True

        # Retroactively highlight all questions and reveal answers
        for q_idx, q in enumerate(self.questions):
            if q.right is not None:
                self.state[q_idx]["revealed"] = True

        total = len([x for x in self.questions if x.correct_answers])
        correct = len([x for x in self.questions if x.right])
        score = (correct / total) * 100 if total > 0 else 0

        win = tk.Toplevel(self.root)
        win.title(f"Results - {score:.2f}%")

        right_frame = tk.Frame(win)
        right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        wrong_frame = tk.Frame(win)
        wrong_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(right_frame, text=f"Right Questions ({correct})", font=("Arial", 18, "bold")).pack()
        tk.Label(wrong_frame, text=f"Wrong Questions ({total - correct})", font=("Arial", 18, "bold")).pack()

        for q in self.questions:
            if q.right:
                tk.Label(right_frame, text=q.question, wraplength=400, justify="left", font=("Arial", 14)).pack(anchor="w", pady=5)
            elif q.right == False:
                tk.Label(wrong_frame, text=q.question, wraplength=400, justify="left", font=("Arial", 14)).pack(anchor="w", pady=5)

    def next_question(self):
        q = self.questions[self.index]
        selected = {c for v, c in self.state[self.index]["vars"] if v.get()}
        if selected and not q.correct_answers:
            q.correct_answers = selected
            q.right = None
            to_save = [x for x in self.questions if x.correct_answers]
            with open('QuestionsWithCorrectChoice.pkl', 'wb') as f:
                pickle.dump(to_save, f)

        if self.show_check and self.index == len(self.questions)-1:
            self.finish_display()
        else:
            if self.index < len(self.questions)-1:
                self.index += 1
                self.render_question()

    def prev_question(self):
        if self.index > 0:
            self.index -= 1
            self.render_question()

if __name__ == "__main__":
    sample_questions = parse_file("UkTestUnsureQuestions.md")

    root = tk.Tk()
    root.geometry("900x700")
    root.minsize(900,700)
    root.title("MCQ Viewer")
    viewer = MCQViewer(root, sample_questions)
    root.mainloop()
