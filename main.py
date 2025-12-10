# Sützpunkte abfrage, Werte prüfen, Eingabe für weitere Punkte und Ausgabe 
print("Polynominterpolationen, hier werden die ST abgefragt")
print("RUNNING main.py FROM:", __file__)
      
from hermite import Hermite
from newton import Newton
from lagrange import Lagrange
from polynomials import Polynomials


# Verschönerte Ausgabe 
def print_header(t1ext):
    print("\n" + "-" * 60)
    print(t1ext.center(60))
    print("-" * 60 + "\n")


def print_stuetzpunkte(xy_values):
    print_header("Stützpunkte")
    print("   x-Wert   |   y-Wert  ")
    print("------------+-----------")
    for x, y in xy_values:
        print(f"{x:10}  | {y:9}")
    print()

def collect_xy_values():
    xy_values = []
    i = 0
    while True:
        if i != 0:
            check_if_wants_to_continue = input("möchten Sie einen " + str(
                i + 1) + "te Stützpunkt eingeben bitte Enter drücken, andernfalls geben sie n ein: ")
            if check_if_wants_to_continue == "n":
                break
        xy_point = (int(input("Bitte Stützstelle des " + str(i + 1) + "ten Punktes eingeben: ")),
                    int(input("Bitte Stützwert des " + str(i + 1) + "ten Punktes eingeben: ")))
        xy_values.append(xy_point)
        i += 1

    return xy_values

def create_polynom(xy_values):
    util = Polynomials()
    xy_len = len(xy_values)
    use_hermite = util.check_for_duplicate_x_values(xy_values)
    x_values = util.get_x_values(xy_values)
    y_values = util.get_y_values(xy_values)

    if use_hermite:
        print_header("Hermite-Interpolation")
        hermite_polynom = Hermite()
        herm_coef = hermite_polynom.hermite_divided_differences(x_values, y_values, xy_values)
        print("Hermite Koeffiziente: ", herm_coef)
        standard_form_polynom_coef = util.generate_polynom_coefficients(
            herm_coef, x_values)
        standard_form_polynom_coef = util.round_list(
            standard_form_polynom_coef, 3)
        pretty_polynom = "Hermite: " + "p(x) = " + util.create_string_polynomial(
            standard_form_polynom_coef) + "\n"

        return [pretty_polynom]

    else:
        print_header("Lagrange- & Newton-Interpolation")

        # Lagrange
        lagrange_polynom = Lagrange()
        li_function = lagrange_polynom.create_li_function(
            x_values)
        Li_function = lagrange_polynom.create_Li_function(
            xy_len, li_function[0], li_function[1])

        polynom = lagrange_polynom.calculate_polynom(
            xy_len, y_values, Li_function)
        norm_poly = lagrange_polynom.normalform_poly(xy_len, polynom)
        norm_poly = util.round_list(norm_poly, 3)
        pretty_polynom = "\nLagrange: p(x) =" + util.create_string_polynomial(norm_poly) + "\n"

        # Newton
        newt = Newton()
        #newt_coeffs = newt.newton_div_diff(x_values, y_values)     -> nicht mehr passend
        #poly_coeffs = util.generate_polynom_coefficients(
        #    newt_coeffs, x_values)
        #poly_coeffs = util.round_list(poly_coeffs, 3)
        #pretty_newt = "Newton: p(x) = " + util.create_string_polynomial(
        #    poly_coeffs)
        poly_coeffs = newt.build_newton(x_values, y_values)
        poly_coeffs = util.round_list(poly_coeffs, 3)

        pretty_newt = "Newton: p(x) = " + util.create_string_polynomial(poly_coeffs)
        basis_strings = newt.printable_newton_basis(x_values)
        print("\nDazugehörige Newton-Basisfunktionen B_i(x):")
        for line in basis_strings:
            print(line)

        return [pretty_polynom, pretty_newt]


if __name__ == '__main__':
    util = Polynomials()
    run: bool = True

    while(run):
        xy_values = collect_xy_values()
        print_stuetzpunkte(xy_values)
        polynom = create_polynom(xy_values)

        for i in polynom:
            print(i)
        
        (user_input) = input("\nNeustart: beliebige Taste. \nProgramm beenden: Schreibe 'exit'.\n")
        if(user_input == "exit"):
            run = False