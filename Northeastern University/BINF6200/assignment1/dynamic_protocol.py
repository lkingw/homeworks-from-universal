#!/usr/bin/env python3
# dynamic_protocol.py
"""dynamically change the results of the program that already exist."""
# Set stock and final of the NaCl and MgCl2 as inputs
FINAL_VOL = int(input('Please enter the final volume of the solution (ml): '))
NA_CL_STOCK = int(input('Please enter the NaCl stock (mM): '))
NA_CL_FINAL = int(input('Please enter the NaCl final (mM): '))
MG_STOCK = int(input('Please enter the MgCl2 stock (mM): '))
MG_FINAL = float(input('Please enter the MgCl2 final (mM): '))

X = FINAL_VOL * (NA_CL_FINAL / NA_CL_STOCK)
Y = FINAL_VOL * (MG_FINAL / MG_STOCK)
print('Add', X, 'ml', 'NaCl')
print('Add', Y, 'ml', 'MgCl2')
print('Add water to a final volume of', FINAL_VOL, 'ml', 'and mix')
