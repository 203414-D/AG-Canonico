import random
from random import choices, choice
import math
from matplotlib import pyplot as plt
import numpy as np
from sympy import lambdify, simplify, var, sin, cos, symbols, sqrt, log, E
from statistics import mean

class GeneticAlgorithm:

    def __init__(self,
                 resolution_x: float,
                 interval_x: tuple,
                 limiteGeneraciones: int,
                 limitePoblacion: int,
                 tamanioPoblacionInicial: int,
                 probabilidadMutIndiv: float,
                 probabilidadMutGen: float
                 ):
        x = symbols('x')
        expr =(sqrt(16*x + pow(x,2) - 28)/sqrt(64 - 16*x + pow(x,2)))
        expr2 = simplify(expr)
        self.f = lambdify((x), expr2)
        self.resolution_x = resolution_x
        self.interval_x = interval_x
        self.limiteGeneraciones = limiteGeneraciones
        self.limitePoblacion = limitePoblacion
        self.tamanioPobInicial = tamanioPoblacionInicial

        self.Rx = self.interval_x[1] - self.interval_x[0]

        self.nPx = math.ceil(self.Rx / self.resolution_x) + 1

        self.nBx = len(bin(self.nPx)) - 2

        self.interval_i = (0, self.nPx - 1)

        self.poblacion = []
        self.best_cases = []
        self.worst_cases = []
        self.avg_cases = []

        self.probabilidadMutIndiv = probabilidadMutIndiv
        self.probabilidadMutGen = probabilidadMutGen

        self.first_generation = []

    def mutacion(self, individual):

        p = random.random()
        if p < self.probabilidadMutIndiv:
            for _ in range(self.nBx):
                index = random.randrange(self.nBx)
                individual[0][index] = individual[0][index] if random.random() > self.probabilidadMutGen else \
                    abs(individual[0][index] - 1)
                individual = self.generarIndividuo(individual[0])
            return individual
        else:
            return individual

    def generarIndividuo(self, genotipo):
        i = int("".join([str(i) for i in genotipo]), 2)
        fenotipo = self.interval_x[0] + (i * self.resolution_x)

        if fenotipo > self.interval_x[-1]:
            fenotipo = self.interval_x[-1]

        aptitud = self.f(fenotipo)
        
        if math.isinf(aptitud) or math.isnan(aptitud):
            if aptitud > 0:
                aptitud = 1e+300
            else:
                aptitud = 1e-300
        return [genotipo, i,fenotipo, aptitud]


    def poda(self):
        self.poblacion = self.poblacion[:self.limitePoblacion]

    def cruza(self, a, b):
        px1, px2 = sorted(random.sample(range(1, self.nBx), 2))
        genotipo_a = a[0][0:px1] + b[0][px1:px2] + a[0][px2:]
        genotipo_b = b[0][0:px1] + a[0][px1:px2] + b[0][px2:]
        offspring_a = self.generarIndividuo(genotipo_a)
        offspring_b = self.generarIndividuo(genotipo_b)
        return offspring_a, offspring_b


    @staticmethod
    def seleccionarPadre(poblacion):
        aptitudes = [individuo[3] for individuo in poblacion]
        total = sum(aptitudes)
        probabilidades = [aptitud/total for aptitud in aptitudes]
        parents = []
        for _ in range(2):
            parents.append(choices(poblacion, weights=probabilidades, k=1)[0])
        return parents

    def generarPoblacionInicial(self):
        for i in range(self.tamanioPobInicial):
            while True:
                genotipo = choices([0, 1], k=self.nBx)
                individual = self.generarIndividuo(genotipo)
                if self.interval_i[0] <= individual[2] <= self.interval_i[1]:
                    self.poblacion.append(individual)
                    break
        

    def iniciar(self, minimize: bool):
        generation = 0

        self.generarPoblacionInicial()
        self.poblacion = sorted(
            self.poblacion,
            key=lambda y: [x[3] for x in self.poblacion],
            reverse=minimize
        )
        for i in range(self.limiteGeneraciones):
            for j in range(int(len(self.poblacion) / 2)):
                parent = self.seleccionarPadre(self.poblacion)
                offspring_a, offspring_b = self.cruza(parent[0], parent[1])
                offspring_a = self.mutacion(offspring_a)
                offspring_b = self.mutacion(offspring_b)
                self.poblacion.append(offspring_a)
                self.poblacion.append(offspring_b)
            self.poblacion = sorted(
                self.poblacion,
                key=lambda y: [y[3] for _ in self.poblacion],
                reverse=minimize
            )
            self.best_cases.append(self.poblacion[0])
            self.avg_cases.append(mean([x[3] for x in self.poblacion]))
            self.worst_cases.append(self.poblacion[-1])

            if len(self.poblacion) > self.limitePoblacion:
                self.poda()
            generation += 1
            x = []
            y = []
            for individual in self.poblacion:  
                x.append(individual[2])
                y.append(individual[3])

            colors = np.random.uniform(15, 80, len(x))
            # # plot
          #  fig, ax = plt.subplots()
          #  ax.scatter(x, y, c=colors, vmin=0, vmax=100)

          #  plt.title(f"Generación {generation}")
          #  plt.xlabel("x")
         #   plt.ylabel("y")
         #   plt.savefig(f"images/generation {generation}.png")
