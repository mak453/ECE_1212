import numpy as np

def parallel_resistors(resistors:list):
    resistance = 0
    
    for resistor in resistors:
        resistance += 1/resistor
    
    return 1/resistance


Vdd = int(input("Enter Vdd: "))
mode = input("Enter Id mode (high or low): ")

Id = {"high": 2.0e-3, "low": .4e-3}
Vgs = {"high": 3.259,"low": 2.136}
gm = {"high": 1.84e-3, "low":.975e-3}
Rd = (Vdd - Vdd/2)/Id[mode]

Rl, Rg = 1e6, 9e6

Rs = (gm[mode]*parallel_resistors([Rd, Rl])/5 - 1)/gm[mode]
Av = -gm[mode]*parallel_resistors([Rd, Rl])/(1+gm[mode]*Rs)

freq = 1000
omega = 2*np.pi*freq

C1 = 10/(omega*Rg)
C2 = 100/(omega*parallel_resistors([Rd, Rl]))
Cs = 10000/(omega*parallel_resistors([Rd, Rl]))


print("Rd = ", Rd)
print("Rs = ", Rs)

print("C1 >= ", C1, "\tC2 > ", C2, "\tCs > ", Cs)
print("Av = ", Av)