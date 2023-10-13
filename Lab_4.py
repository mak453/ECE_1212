import numpy as np


class Lab4:

    # CONSTRAINTS and CONSTANTS
    num = 0
    Rc = 1000.0
    Rl = 1000.0
    Vt = 25e-3
    FREQ = 1000.0
    OMEGA = 2*np.pi*FREQ
    Vout = 5

    # Measured transistor
    Vbe = 0.727
    Vce = 0.016
    Ic = 5e-3
    Ib = 1e-3
    beta = Ic/Ib

    def __init__(self, Vcc=12.0) -> None:
        self.Vcc = Vcc
        Lab4.num += 1
        self.test_num = Lab4.num
        self.calculate()

    def calculate(self):
        self.solve_Veq()
        self.solve_Rac()
        self.solve_step_3()
        self.solve_gain()
        self.solve_step_5()
        self.solve_capacitors()

    def parallel_resistance(self, resistors: list):
        return np.product(resistors)/np.sum(resistors)

    def solve_Veq(self):
        # Given that Veq = 0.2Vcc
        self.Veq = float(.2*self.Vcc)

    def solve_Rac(self):
        resistors = [Lab4.Rc, Lab4.Rl]
        self.Rac = float(self.parallel_resistance(resistors))

    def solve_step_3(self):
        self.Re = float((self.Rac + Lab4.Rc)/4)
        self.Icq = float(self.Veq/(5.0*self.Re))
        Rdc = Lab4.Rc + self.Re
        self.Vceq = float(self.Vcc - self.Icq*Rdc)

    def solve_gain(self):
        Ibq = 2*self.Vceq/Lab4.beta
        self.r_pi = Lab4.Vt/Ibq
        self.Av = -(Lab4.beta*self.Rac)/self.r_pi
        self.Vin = -Lab4.Vout/self.Av

    def solve_step_5(self):
        self.Rbb = 0.1*Lab4.beta*self.Re
        Vbq = self.Veq + Lab4.Vbe
        self.Vbb = 1.1*self.Veq + Lab4.Vbe
        ratio = self.Vbb/self.Vcc
        self.R2 = self.Rbb/ratio
        self.R1 = (ratio*self.R2)/(1-ratio)

    def solve_capacitors(self):
        re = Lab4.Vt/self.Icq
        self.Ce = 1.25/(Lab4.OMEGA*re)
        self.C2 = 10/(Lab4.OMEGA*(Lab4.Rc + Lab4.Rl))
        Rin = self.parallel_resistance([self.Rbb, self.r_pi])
        self.C1 = 10/(Lab4.OMEGA*Rin)

    def display(self):
        print("Test #" + str(Lab4.num))
        print("--------------")
        print("Given and constraints:")
        print("\tRc = " + str(Lab4.Rc) + " , Rl = " +
              str(Lab4.Rl) + " , W low = " + str(Lab4.OMEGA) + " ["+str(Lab4.FREQ) + "Hz]")


def organize(dictionary: dict, test: Lab4):
    voltages = []
    currents = []
    resistors = []
    capacitors = []
    gain = 0

    for name, value in dictionary.items():
        first_letter = name[0]

        value = f"{value:.3e}"
        [num, notation] = value.split("e")

        power = int(notation)
        num = float(num)
        precision = 5

        if power >= 6 and power < 9:
            value = str(np.round(num*(10**(power-6)), precision)) + "M"
        elif power >= 3 and power < 6:
            value = str(np.round(num*(10**(power-3)), precision)) + "K"
        elif power >= 0 and power < 3:
            value = str(np.round(num*(10**(power)), precision))
        elif power >= -3 and power < 0:
            value = str(np.round(num*(10**(power+3)), precision)) + "m"
        elif power >= -6 and power < -3:
            value = str(np.round(num*(10**(power+6)), precision)) + "u"
        elif power >= -9 and power < -6:
            value = str(np.round(num*(10**(power+9)), precision)) + "n"
        elif power >= -12 and power < -9:
            value = str(np.round(num*(10**(power+12)), precision)) + "p"

        if first_letter == "V":
            voltages.append(name + ": " + value)
        elif first_letter == "I":
            currents.append(name + ": " + value)
        elif first_letter in ["R", "r"]:
            resistors.append(name + ": " + value)
        elif first_letter == "C":
            capacitors.append(name + ": " + value)
        elif first_letter == "A":
            gain = value

    print("Test #" + str(test.num)+"\n---------------------")
    print("Gain:\n\t" + gain + "\n")
    print("Voltages:\n\t" + ", ".join(voltages) + "\n")
    print("Currents:\n\t" + ", ".join(currents) + "\n")
    print("Resistors:\n\t" + ", ".join(resistors) + "\n")
    print("Capacitors:\n\t" + ", ".join(capacitors) + "\n")


test_1 = Lab4()
organize(test_1.__dict__, test_1)

answers = ["yes", "y"]
print()
again = input("Calculate another? (y/n) ")

while again in answers:
    Vcc = float(input("Enter Vcc: "))
    new_test = Lab4(Vcc)
    print()
    organize(new_test.__dict__, new_test)
    again = input("Calculate another? (y/n) ")
