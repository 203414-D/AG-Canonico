import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Logica import GeneticAlgorithm
import numpy as np
from numpy import ma
import matplotlib.pyplot as plt
from tkinter import messagebox

# root window
root = tk.Tk()
w, h = 1000, 780
root.geometry("%dx%d+0+0" % (w, h))
root.title('Algorítmo Genético Canonico - Maximizar o Minimizar')

root.configure(bg="blue")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)

title_label = ttk.Label(root, text="Parámetros del algoritmo", background='#fff',
                        font=('Arial', '12', 'bold'))
title_label.grid(column=0, row=0, )

min_x_label = ttk.Label(root, text="Valor mínimo para X:", background='#fff', font=('Lucida Sands', '10'))
min_x_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
min_x_entry = ttk.Entry(root)
min_x_entry.insert(0, "0")
min_x_entry.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

max_x_label = ttk.Label(root, text="Valor máximo para X:", background='#fff', font=('Lucida Sands', '10'))
max_x_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
max_x_entry = ttk.Entry(root)
max_x_entry.insert(0, "10")
max_x_entry.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

resolution_x_label = ttk.Label(root, text="intervalo de X:", background='#fff', font=('Lucida Sands', '10'))
resolution_x_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
resolution_x_entry = ttk.Entry(root)
resolution_x_entry.insert(0, "0.1")
resolution_x_entry.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

max_generations_label = ttk.Label(root, text="Lim generacion:", background='#fff', font=('Lucida Sands', '10'))
max_generations_label.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
max_generations_entry = ttk.Entry(root)
max_generations_entry.insert(0, "100")
max_generations_entry.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)

initial_population_label = ttk.Label(root, text="Población inicial:", background='#fff', font=('Lucida Sands', '10'))
initial_population_label.grid(column=0, row=9, sticky=tk.W, padx=5, pady=5)
initial_population_entry = ttk.Entry(root)
initial_population_entry.insert(0, "5")
initial_population_entry.grid(column=0, row=10, sticky=tk.W, padx=5, pady=5)

max_population_label = ttk.Label(root, text="Población máxima:", background='#fff', font=('Lucida Sands', '10'))
max_population_label.grid(column=0, row=11, sticky=tk.W, padx=5, pady=5)
max_population_entry = ttk.Entry(root)
max_population_entry.insert(0, "100")
max_population_entry.grid(column=0, row=12, sticky=tk.W, padx=5, pady=5)

individual_mutation_prob_label = ttk.Label(root, text="Pmi:", background='#fff',
                                           font=('Lucida Sands', '10'))
individual_mutation_prob_label.grid(column=0, row=13, sticky=tk.W, padx=5, pady=5)
individual_mutation_prob_entry = ttk.Entry(root)
individual_mutation_prob_entry.insert(0, "0.30")
individual_mutation_prob_entry.grid(column=0, row=14, sticky=tk.W, padx=5, pady=5)

gen_mutation_prob_label = ttk.Label(root, text="Pmg:", background='#fff',
                                    font=('Lucida Sands', '10'))
gen_mutation_prob_label.grid(column=0, row=15, sticky=tk.W, padx=5, pady=5)
gen_mutation_prob_entry = ttk.Entry(root)
gen_mutation_prob_entry.insert(0, "0.30")
gen_mutation_prob_entry.grid(column=0, row=16, sticky=tk.W, padx=5, pady=5)

def run(minimize: bool):
    ga = GeneticAlgorithm(float(resolution_x_entry.get()),
                            (float(min_x_entry.get()), float(max_x_entry.get())),
                            int(max_generations_entry.get()),
                            int(max_population_entry.get()),
                            int(initial_population_entry.get()),
                            float(individual_mutation_prob_entry.get()),
                            float(gen_mutation_prob_entry.get()))
    ga.iniciar(minimize)

    figure2 = plt.figure()


    plt.plot(np.arange(0, ga.limiteGeneraciones), [x[3] for x in ga.best_cases], label="Mejores aptitudes")
    plt.legend()
    plt.title("Evolución de la mejor aptitud")
    plt.xlabel("Generaciones")
    plt.ylabel("Valor de aptitud")
    linear = FigureCanvasTkAgg(figure2, root)
    linear.get_tk_widget().grid(column=1, row=0, rowspan=10, sticky=tk.W, padx=5, pady=5)

    messagebox.showinfo(
        message=f"Gen: {ga.poblacion[0][0]}\nvalor individuo: {ga.poblacion[0][2]},  Aptitud: {ga.poblacion[0][3]}",
        title="Mejor individuo")



login_button = ttk.Button(root, text="Maximizar", command=lambda: run(True))
login_button.grid(column=0, row=17, sticky=tk.W, padx=5, pady=5)
login_button = ttk.Button(root, text="Minimizar", command=lambda: run(False))
login_button.grid(column=0, row=17, sticky=tk.E, padx=5, pady=5)

root.mainloop()