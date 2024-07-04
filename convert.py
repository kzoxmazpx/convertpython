import subprocess
import tkinter as tk
from tkinter import filedialog
import os

def choose_py_file():
    global py_file_path
    py_file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    py_file_label.config(text=f"Fichier .py sélectionné : {py_file_path}")

def choose_icon_file():
    global icon_file_path
    icon_file_path = filedialog.askopenfilename(filetypes=[("ICO Files", "*.ico")])
    icon_file_label.config(text=f"Fichier .ico sélectionné : {icon_file_path}")

def choose_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory()
    output_folder_label.config(text=f"Dossier de sortie sélectionné : {output_folder_path}")

def convert_to_exe():
    if not py_file_path:
        py_file_label.config(text="Veuillez sélectionner un fichier .py")
        return
    
    command = ['pyinstaller', '--onefile', '--windowed']
    
    if icon_file_path:
        command += ['--icon', icon_file_path]
    
    command += ['--name', 'main.exe', py_file_path]
    
    try:
        # Exécuter la commande avec subprocess
        subprocess.check_call(command, cwd=output_folder_path)
        
        # Supprimer les fichiers inutiles générés par pyinstaller
        cleanup_generated_files(output_folder_path)
        
        result_label.config(text="Conversion en .exe réussie")
    except subprocess.CalledProcessError as e:
        result_label.config(text=f"Erreur lors de la conversion : {e}")

def cleanup_generated_files(output_folder):
    # Liste des extensions de fichiers générés par pyinstaller à supprimer
    extensions_to_remove = ['.spec', '.log', '.zip', '.pyz', '.pyzw']

    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        if os.path.isfile(file_path):
            # Vérifier l'extension du fichier
            _, file_extension = os.path.splitext(file_path)
            if file_extension in extensions_to_remove:
                os.remove(file_path)

# Interface graphique
root = tk.Tk()
root.title("Convertir .py en .exe")

# Frames
frame1 = tk.Frame(root, padx=10, pady=10)
frame1.pack()

frame2 = tk.Frame(root, padx=10, pady=10)
frame2.pack()

# Labels
py_file_label = tk.Label(frame1, text="Aucun fichier .py sélectionné")
py_file_label.pack()

icon_file_label = tk.Label(frame1, text="Aucun fichier .ico sélectionné")
icon_file_label.pack()

output_folder_label = tk.Label(frame1, text="Aucun dossier de sortie sélectionné")
output_folder_label.pack()

result_label = tk.Label(frame2, text="")
result_label.pack()

# Boutons
py_button = tk.Button(frame1, text="Choisir fichier .py", command=choose_py_file)
py_button.pack()

icon_button = tk.Button(frame1, text="Choisir fichier .ico", command=choose_icon_file)
icon_button.pack()

output_button = tk.Button(frame1, text="Choisir dossier de sortie", command=choose_output_folder)
output_button.pack()

convert_button = tk.Button(frame2, text="Convertir en .exe", command=convert_to_exe)
convert_button.pack()

root.mainloop()
