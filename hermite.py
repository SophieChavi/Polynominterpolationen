import math
from polynomials import Polynomials

class Hermite:

    def __init__(self):
        # Koeffizienten des Hermite Polynom in Newton Form
        self.coefficients = None

        # vollständige Hermite Pyramidenmatrix (z) für spätere Kontrolle
        self.z = []

        # Listen der Eingabewerte
        self.x_values = []
        self.y_values = []

        # Hilfsobjekt zur Extraktion der Werte
        self.ut = Polynomials()

    def get_coefficients(self, xy_list):
        # Extrahiere x Werte, y Werte und Ableitungen 
        self.x_values = self.ut.get_x_values(xy_list)
        self.y_values = self.ut.get_y_values(xy_list)
        self.coeff = self.hermite_divided_differences(xy_list)
        return self.coeff

    def hermite_divided_differences(self, x_values, y_values, xy_list):
        # Anzahl der ursprünglichen Stützstellen
        n = len(x_values)

        # Hermite benötigt für jeden x Wert zwei Einträge
        # z = [x0, x0, x1, x1, x2, x2, ...]
        z = []
        for i in range(n):
            z.append([])
            for j in range(n):
                z[i].append(0.)

        # y-Werten in der erste Spalte der Pyramide
        for i in range(n):
            z[i][0] = float(y_values[i])

        for j in range(1, n): # j ist die aktuelle Spalte der dividierten Differenzen
            
            for i in range(n - j): # i ist die Zeile, pro Spalte werden es weniger

                # Hermite Fall: gleiche x Werte -> Ableitung statt Division
                if(i + j) < len(x_values):
                    if (x_values[i + j] - x_values[i]) == 0:
                        z[i][j] = self.get_derivation_value(
                            xy_list, x_values[i], j) / math.factorial(j)
                    else:
                        z[i][j] = (
                            z[i + 1][j - 1] - z[i][j - 1]) / (x_values[i + j] - x_values[i])
        self.z = z
        return z[0]  # erste Zeile enthält die Newton Koeffizienten

    def get_derivation_value(self, xy_list, x_values, step):
        derivation_value = 0
        for i in range(len(xy_list) - 1):
            if xy_list[i][0] == x_values:
                derivation_value = xy_list[i + step][1]
                break
        return derivation_value

    def build_polynomial(self):
        # Erzeugt das vollständige Polynom in der normalen Potenzform
        # P(x) = c0 + c1*x + c2*x^2 + ...
        P = [0]        # Startpolynom
        basis = [1]    # Startbasis für das Newton Fundamentpolynom
        for i in range(len(xs)):
            term = [c * coeffs[i] for c in basis]
            P = self.util.add_polynoms(P, term)
            basis = self.util.multiply_polynoms(basis, [-xs[i], 1])

        return P # In der Normalform zurückgeben
