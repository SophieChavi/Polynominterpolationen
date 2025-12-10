from polynomials import Polynomials

class Newton:
    #Konstruktor: Polynomials wird als self.util gespeichert. 
    def __init__(self):
        self.util = Polynomials()
    # Sophie: musste minimale Änderungen machen damit ich Newton in Main verwenden kann: self

    def divided_diff(self,xs,ys):
        # Anzahl der Stützstellen
        n = len(xs)
        # Anfangs ist das einfach die y-Werte (f[x0], f[x1], ...)
        table = list(ys)
        # Der erste Koeffizient a0 ist einfach f[x0]
        coeffs = [table[0]]

    # k ist die Spaltennummer (1. Spalte, 2. Spalte, ...)
        for k in range(1, n):
            new = []  # die neue Spalte speichern

            # für jede Zeile dieser Spalte
            for i in range(n - k):
                v = (table[i + 1] - table[i]) / (xs[i + k] - xs[i])
                new.append(v)

            # die neue Spalte wird zur "aktuellen" Spalte
            table = new

            # oberster Eintrag der Spalte ist der nächste Newton Koeffizient
            coeffs.append(table[0])
        return coeffs

    def build_newton(self,xs, ys): # das Interpolationspolynom aus den Koeffizienten in Normalform aufbauen
        # Newton Koeffizienten mit dividierten Differenzen berechnen
        coeffs = self.divided_diff(xs, ys)
        #n = len(xs)  -> kurz entfernt / S

        P = [0]

        # "basis" ist das aktuelle Basispolynom:
        # Start: 1 -> (x - x0) -> (x - x0)(x - x1) -> (x - x0)(x - x1)(x - x2)
        basis = [1]

        # NEU: baut Polynom direkt in der Normalform, damit ich sie in der main verwenden kann :)
        for i in range(len(xs)):
            term = [c * coeffs[i] for c in basis] #multipliziere das aktuelle Basispolynom mit dem Koeffizienten
            P = self.util.add_polynoms(P, term) #addiere diesen Term zu P
            basis = self.util.multiply_polynoms(basis, [-xs[i], 1]) #erweitere basis um den Faktor (x - x_i) mit multiply_polynoms.
        return P
    
    def get_newton_basis(self, xs):
        basis = [[1]]   # B0(x) = 1
        
        for i in range(1, len(xs)):
            next_basis = self.util.multiply_polynoms(basis[-1], [-xs[i-1], 1])
            basis.append(next_basis)

        return basis

    def printable_newton_basis(self, xs):
        basis = self.get_newton_basis(xs)
        result = []

        for i, poly in enumerate(basis):
            poly = [float(c) for c in poly]
            formatted = self.util.create_string_polynomial(poly.copy())
            result.append(f"B{i}(x) = {formatted}")
        return result