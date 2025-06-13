import tkinter as tk
from tkinter import ttk, messagebox
import db

def submit_form():
    categorie = categorie_var.get().strip()
    titre = titre_var.get().strip()
    texte = texte_text.get("1.0", tk.END).strip()
    lien = lien_var.get().strip() or None

    if not categorie or not titre or not texte:
        messagebox.showerror("Erreur", "Veuillez remplir les champs obligatoires")
        return

    db.ajouter_modele(categorie, titre, texte, lien)
    messagebox.showinfo("Succès", "Modèle enregistré")
    categorie_var.set("")
    titre_var.set("")
    texte_text.delete("1.0", tk.END)
    lien_var.set("")


def main():
    db.init_db()

    root = tk.Tk()
    root.title("Ajout de réponse")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(main_frame, text="Catégorie:").grid(column=0, row=0, sticky=tk.W)
    categorie_entry = ttk.Entry(main_frame, textvariable=categorie_var, width=40)
    categorie_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

    ttk.Label(main_frame, text="Titre:").grid(column=0, row=1, sticky=tk.W)
    titre_entry = ttk.Entry(main_frame, textvariable=titre_var, width=40)
    titre_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

    ttk.Label(main_frame, text="Texte de réponse:").grid(column=0, row=2, sticky=tk.W)
    texte_text.grid(column=1, row=2, sticky=(tk.W, tk.E))

    ttk.Label(main_frame, text="Lien (facultatif):").grid(column=0, row=3, sticky=tk.W)
    lien_entry = ttk.Entry(main_frame, textvariable=lien_var, width=40)
    lien_entry.grid(column=1, row=3, sticky=(tk.W, tk.E))

    submit_btn = ttk.Button(main_frame, text="Enregistrer", command=submit_form)
    submit_btn.grid(column=0, row=4, columnspan=2, pady=5)

    root.mainloop()


categorie_var = tk.StringVar()
titre_var = tk.StringVar()
texte_text = tk.Text(height=10, width=40)
lien_var = tk.StringVar()

if __name__ == "__main__":
    main()
