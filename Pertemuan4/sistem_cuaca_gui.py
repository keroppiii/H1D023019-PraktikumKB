from pyswip import Prolog  # type: ignore
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

prolog = Prolog()
prolog.consult("sistem_cuaca_gui.pl")  # Pastikan path benar

cuaca_list = list()
gejala_dict = dict()
index_cuaca = 0
index_gejala = 0
current_cuaca = ""
current_gejala = ""

def mulai_diagnosa():
    global cuaca_list, gejala_dict, index_cuaca, index_gejala
    prolog.retractall("gejala_pos(_)")  # Bersihkan sebelumnya
    prolog.retractall("gejala_neg(_)")

    start_btn.configure(state=tk.DISABLED)
    yes_btn.configure(state=tk.NORMAL)
    no_btn.configure(state=tk.NORMAL)

    cuaca_list = [c["Cuaca"].decode() if hasattr(c["Cuaca"], 'decode') else str(c["Cuaca"]) for c in prolog.query("cuaca(Cuaca)")]
    for c in cuaca_list:
        gejala_dict[c] = [g["G"] for g in prolog.query(f'gejala(G, {c})')]
    
    index_cuaca = 0
    index_gejala = -1
    pertanyaan_selanjutnya()

def pertanyaan_selanjutnya(ganti_cuaca=False):
    global current_cuaca, current_gejala, index_cuaca, index_gejala

    if ganti_cuaca:
        index_cuaca += 1
        index_gejala = -1

    if index_cuaca >= len(cuaca_list):
        hasil_diagnosa()
        return

    current_cuaca = cuaca_list[index_cuaca]
    index_gejala += 1

    if index_gejala >= len(gejala_dict[current_cuaca]):
        hasil_diagnosa(current_cuaca)
        return

    current_gejala = gejala_dict[current_cuaca][index_gejala]

    if list(prolog.query(f"gejala_pos({current_gejala})")):
        pertanyaan_selanjutnya()
        return
    elif list(prolog.query(f"gejala_neg({current_gejala})")):
        pertanyaan_selanjutnya(ganti_cuaca=True)
        return

    pertanyaan = list(prolog.query(f"pertanyaan({current_gejala}, Y)"))[0]["Y"].decode()
    tampilkan_pertanyaan(pertanyaan)

def tampilkan_pertanyaan(pertanyaan):
    kotak_pertanyaan.configure(state=tk.NORMAL)
    kotak_pertanyaan.delete(1.0, tk.END)
    kotak_pertanyaan.insert(tk.END, pertanyaan)
    kotak_pertanyaan.configure(state=tk.DISABLED)

def jawaban(jwb):
    if jwb:
        prolog.assertz(f"gejala_pos({current_gejala})")
        pertanyaan_selanjutnya()
    else:
        prolog.assertz(f"gejala_neg({current_gejala})")
        pertanyaan_selanjutnya(ganti_cuaca=True)

def hasil_diagnosa(cuaca=""):
    if cuaca:
        messagebox.showinfo("Hasil Diagnosa", f"Cuaca terdeteksi: {cuaca}.")
    else:
        messagebox.showinfo("Hasil Diagnosa", "Cuaca tidak terdeteksi.")
    
    yes_btn.configure(state=tk.DISABLED)
    no_btn.configure(state=tk.DISABLED)
    start_btn.configure(state=tk.NORMAL)

# GUI
root = tk.Tk()
root.title("Sistem Pakar Prediksi Cuaca")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Sistem Pakar Prediksi Cuaca", font=("Arial", 16)).grid(column=0, row=0, columnspan=3)
ttk.Label(mainframe, text="Pertanyaan:").grid(column=0, row=1)

kotak_pertanyaan = tk.Text(mainframe, height=4, width=40, state=tk.DISABLED)
kotak_pertanyaan.grid(column=0, row=2, columnspan=3)

yes_btn = ttk.Button(mainframe, text="Ya", command=lambda: jawaban(True), state=tk.DISABLED)
yes_btn.grid(column=1, row=3)

no_btn = ttk.Button(mainframe, text="Tidak", command=lambda: jawaban(False), state=tk.DISABLED)
no_btn.grid(column=2, row=3)

start_btn = ttk.Button(mainframe, text="Mulai Diagnosa", command=mulai_diagnosa)
start_btn.grid(column=1, row=4, columnspan=2)

for widget in mainframe.winfo_children():
    widget.grid_configure(padx=5, pady=5)

root.mainloop()
