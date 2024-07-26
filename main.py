import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.scrolledtext as scrolledtext

class QuizApp:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        self.master.title("CompTIA Security+ SY0-701 Practice Quiz")
        self.master.geometry("800x600")
        self.master.configure(bg='lightblue')

        # Initialize variables
        self.questions_file = ""
        self.answers_file = ""
        self.questions = []
        self.answers = {}
        self.current_question = 0
        self.score = 0
        self.wrong_answers = []

        # Initialize frames
        self.main_frame = None
        self.quiz_frame = None
        self.result_frame = None
        self.wrong_answers_frame = None

        # Create the main screen
        self.create_main_screen()

    def create_main_screen(self):
        # Clear any existing frames
        self.clear_frames()

        # Create and pack the main frame
        self.main_frame = tk.Frame(self.master, bg='lightblue')
        self.main_frame.pack(expand=True, fill="both")

        # Add widgets to the main frame
        tk.Label(self.main_frame, text="CompTIA Security+ SY0-701 Practice Quiz", font=("Arial", 24, "bold"), bg='lightblue').pack(pady=20)

        tk.Button(self.main_frame, text="Select Questions File", command=self.select_questions_file, bg='white').pack(pady=10)
        tk.Button(self.main_frame, text="Select Answers File", command=self.select_answers_file, bg='white').pack(pady=10)
        tk.Button(self.main_frame, text="Start Quiz", command=self.start_quiz, bg='white').pack(pady=20)
        tk.Button(self.main_frame, text="Exit", width=10, height=2, command=self.master.quit, bg='white').pack(side="bottom", pady=20)

    def clear_frames(self):
        # Destroy all frames to clear the window
        for frame in [self.main_frame, self.quiz_frame, self.result_frame, self.wrong_answers_frame]:
            if frame:
                frame.destroy()

    def select_questions_file(self):
        # Open file dialog to select questions file
        self.questions_file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    def select_answers_file(self):
        # Open file dialog to select answers file
        self.answers_file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    def start_quiz(self):
        # Check that both files are selected before starting the quiz
        if not self.questions_file or not self.answers_file:
            messagebox.showerror("Error", "Please select both questions and answers files.")
            return

        # Load questions and answers, clear frames, create quiz screen
        self.load_questions()
        self.load_answers()
        self.clear_frames()
        self.create_quiz_screen()

    def load_questions(self):
        # Load questions from selected file
        with open(self.questions_file, 'r') as file:
            content = file.read().strip().split('\n\n')
            self.questions = [q.strip() for q in content if q.strip()]

    def load_answers(self):
        # Load answers from selected file
        self.answers.clear()
        with open(self.answers_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    question_num, answer = line.split('.', 1)
                    question_num = int(question_num.strip())
                    answer = answer.strip().upper()
                    self.answers[question_num] = answer
                except ValueError:
                    print(f"Warning: Skipping invalid line in answers file: {line}")
        print("Loaded answers:", self.answers)  # Debugging information

    def create_quiz_screen(self):
        # Create and pack the quiz frame
        self.quiz_frame = tk.Frame(self.master, bg='lightblue')
        self.quiz_frame.pack(expand=True, fill="both")

        # Add widgets to the quiz frame
        self.question_label = tk.Label(self.quiz_frame, text="", wraplength=700, justify="left", font=("Arial", 14), bg='lightblue')
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.options = []
        for i in range(4):
            option = tk.Radiobutton(self.quiz_frame, text="", variable=self.var, value=chr(65 + i), font=("Arial", 12), bg='lightblue')
            option.pack(anchor="w", padx=50, pady=5)
            self.options.append(option)

        self.next_button = tk.Button(self.quiz_frame, text="Next", command=self.next_question, bg='white')
        self.next_button.pack(pady=20)

        self.score_label = tk.Label(self.quiz_frame, text="Score: 0", font=("Arial", 14), bg='lightblue')
        self.score_label.pack(pady=10)

        self.show_question()

    def show_question(self):
        # Display current question and options
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            lines = question.split('\n')
            self.question_label.config(text=lines[0])
            for i, option in enumerate(self.options):
                option.config(text=lines[i + 1] if i + 1 < len(lines) else "")

            # Clear the selection
            self.var.set(None)
            for option in self.options:
                option.deselect()
        else:
            self.show_results()

    def next_question(self):
        # Handle the next question logic
        if not self.var.get():
            messagebox.showwarning("Warning", "Please select an answer.")
            return

        question_num = self.current_question + 1
        user_answer = self.var.get().upper()
        correct_answer = self.answers.get(question_num)

        print(f"Question {question_num}: User answered {user_answer}, Correct answer is {correct_answer}")  # Debugging information

        if correct_answer is None:
            messagebox.showerror("Error", f"No answer found for question {question_num}")
            return

        if user_answer == correct_answer:
            self.score += 1
        else:
            self.wrong_answers.append((question_num, user_answer, correct_answer))

        self.current_question += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.show_question()

    def show_results(self):
        # Display the quiz results
        self.clear_frames()
        self.result_frame = tk.Frame(self.master, bg='lightblue')
        self.result_frame.pack(expand=True, fill="both")

        tk.Label(self.result_frame, text="Quiz Completed!", font=("Arial", 24), bg='lightblue').pack(pady=20)
        tk.Label(self.result_frame, text=f"Your Score: {self.score}/{len(self.questions)}", font=("Arial", 18), bg='lightblue').pack(pady=10)
        tk.Label(self.result_frame, text=f"Percentage: {self.score / len(self.questions) * 100:.2f}%", font=("Arial", 18), bg='lightblue').pack(pady=10)

        tk.Button(self.result_frame, text="Show Wrong Answers", command=self.show_wrong_answers, bg='white').pack(pady=10)
        tk.Button(self.result_frame, text="Restart Quiz", command=self.restart_quiz, bg='white').pack(pady=10)
        tk.Button(self.result_frame, text="Exit", command=self.master.quit, bg='white').pack(pady=10)

    def show_wrong_answers(self):
        # Display wrong answers
        self.clear_frames()
        self.wrong_answers_frame = tk.Frame(self.master, bg='lightblue')
        self.wrong_answers_frame.pack(expand=True, fill="both")

        tk.Label(self.wrong_answers_frame, text="Wrong Answers", font=("Arial", 24), bg='lightblue').pack(pady=20)

        wrong_answers_text = scrolledtext.ScrolledText(self.wrong_answers_frame, wrap=tk.WORD, width=70, height=20)
        wrong_answers_text.pack(padx=10, pady=10)

        for q_num, user_answer, correct_answer in self.wrong_answers:
            question = self.questions[q_num - 1]
            lines = question.split('\n')
            question_text = '. '.join(lines[0].split('. ')[1:])
            correct_answer_text = next(
                (line.split(') ', 1)[1] for line in lines if line.lower().startswith(f"{correct_answer.lower()})")),
                "Answer text not found"
            )

            wrong_answers_text.insert(tk.END, f"Question {q_num}: {question_text}\n")
            wrong_answers_text.insert(tk.END, f"Your answer: {user_answer}\n")
            wrong_answers_text.insert(tk.END, f"Correct answer: {correct_answer} - {correct_answer_text}\n")
            wrong_answers_text.insert(tk.END, "\n" + "-" * 62 + "\n\n")

        wrong_answers_text.config(state=tk.DISABLED)

        tk.Button(self.wrong_answers_frame, text="Back to Results", command=self.show_results, bg='white').pack(pady=10)

    def restart_quiz(self):
        # Restart quiz
        self.current_question = 0
        self.score = 0
        self.questions_file = ""
        self.answers_file = ""
        self.questions = []
        self.answers = {}
        self.wrong_answers = []
        self.create_main_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
