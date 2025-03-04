import os
import json
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class QCMApp:
    def __init__(self, root, data_folder="rl"):
        self.root = root
        self.root.title("QCM Interface")
        self.data_folder = data_folder

        # Création et configuration du style pour les Checkbuttons
        self.style = ttk.Style()
        self.style.configure("TCheckbutton", font=("Helvetica", 16))

        self.questions = self.load_questions()
        self.current_question_index = 0
        
        self.setup_ui()
        self.display_question()

    def load_questions(self):
        """Charge toutes les questions des fichiers JSON dans le dossier data et les mélange."""
        questions = []
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".json"):
                filepath = os.path.join(self.data_folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    questions.extend(data.get("qcm", []))
        random.shuffle(questions)
        return questions

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        self.question_label = ttk.Label(self.root, text="", wraplength=600, font=("Helvetica", 18), justify=LEFT)
        self.question_label.pack(pady=20)

        self.options_frame = ttk.Frame(self.root)
        self.options_frame.pack()

        self.validate_button = ttk.Button(self.root, text="Valider", command=self.validate_answer, bootstyle=PRIMARY)
        self.validate_button.pack(pady=10)

        self.result_label = ttk.Label(self.root, text="", font=("Helvetica", 16, "bold"))
        self.result_label.pack()

        self.next_button = ttk.Button(self.root, text="Suivant", command=self.next_question, bootstyle=SUCCESS)
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()

    def display_question(self):
        """Affiche la question actuelle avec ses options."""
        if self.current_question_index >= len(self.questions):
            self.question_label.config(text="QCM terminé !")
            self.validate_button.pack_forget()
            self.next_button.pack_forget()
            return

        # Réinitialisation de la sélection
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        question_data = self.questions[self.current_question_index]
        self.question_label.config(text=question_data["question"])

        self.answer_vars = []
        # Affichage des options sans définir directement la police
        for i, choice in enumerate(question_data["choices"]):
            var = ttk.IntVar(value=0)
            chk = ttk.Checkbutton(self.options_frame, text=choice, variable=var)
            chk.pack(anchor="w", padx=20, pady=5)
            self.answer_vars.append((var, i))

        self.result_label.config(text="")
        self.validate_button.pack()
        self.next_button.pack_forget()

    def validate_answer(self):
        """Vérifie la réponse et affiche le résultat."""
        selected_indices = [i for var, i in self.answer_vars if var.get() == 1]
        correct_answers = self.questions[self.current_question_index]["answer"]

        if sorted(selected_indices) == sorted(correct_answers):
            self.result_label.config(text="Bonne réponse ! ✅", foreground="green")
        else:
            correct_choices = [self.questions[self.current_question_index]["choices"][i] for i in correct_answers]
            self.result_label.config(text=f"Mauvaise réponse ❌\nRéponse correcte : {'\n'.join(correct_choices)}", foreground="red")

        self.validate_button.pack_forget()
        self.next_button.pack()

    def next_question(self):
        """Passe à la question suivante."""
        self.current_question_index += 1
        self.display_question()

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = QCMApp(root)
    root.mainloop()