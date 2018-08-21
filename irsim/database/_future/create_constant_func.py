import os, sys

def show_sorted_vibronic_energy(VIBRONIC_ENERGY_LEVELS):
    order = sorted([v for v in VIBRONIC_ENERGY_LEVELS.values()], reverse = False)
    for v in order:
        for k, vd in VIBRONIC_ENERGY_LEVELS.items():
            if v == vd:
                print(k)
                print(v)
