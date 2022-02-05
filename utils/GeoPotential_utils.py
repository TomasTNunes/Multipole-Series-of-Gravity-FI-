import os
import numpy as np
import math
import sympy as sym

# Define paramters of earth
R_T = 6.3781363e6 #m
MU = 3.986004405e14 #m^3 s^-2
# Max Degree (l) to get from files
lmax = 5
# path to the file containing egm96 of the earth
egm96_file_path = './data/GeoPotencial-data/earth_egm96_to360.ascii.txt'


# loads data from a data file
# returns data
def load_txt(path):
    A = np.loadtxt(path)
    return A


# converts value of slider into Coefficient chosen
# retuns coefficient
def get_slider_coeff(value):
    if value == 1:
        coeff = 'C20'
    elif value == 2:
        coeff = 'C21'
    elif value == 3:
        coeff = 'C30'
    elif value == 4:
        coeff = 'C32'
    elif value == 5:
        coeff = 'C40'
    elif value == 6:
        coeff = 'C41'
    elif value == 7:
        coeff = 'C43'
    elif value == 8:
        coeff = 'C50'
    elif value == 9:
        coeff = 'C52'
    elif value == 10:
        coeff = 'C54'
    return coeff


# Loads EGM96 data from file and returns degrees(l), orders(m), and Spherical Harmonic Coefficients (C and S)
def read_egm96_file(path, lmax):
    with open(path, 'r') as infile:
        lines = infile.readlines()
    line = np.array([lin.split() for lin in lines])
    arr_size = int((4 + lmax) / 2 * (lmax - 1))

    l = line[0:arr_size,0].astype('int64')
    m = line[0:arr_size,1].astype('int64')
    C = line[0:arr_size,2].astype('float64')
    S = line[0:arr_size,3].astype('float64')
    return l, m, C, S


# Calculates and returns Associated Legendre polynomial
def get_ass_leg(l, m, THETA): # egm96 norm for a (beacause of coefficients with this norm)
    if m == 0: 
        a = np.sqrt( (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    else: 
        a = np.sqrt( 2 *  (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    s = sym.Symbol('s')
    G = (s ** 2 - 1) ** l
    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = (1 / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)
    P_lm = sym.lambdify(s, P_lm)
    return (a * P_lm(np.sin(THETA)))


# Calculates and returns Differential Associated Legendre polynomial
def get_ass_leg_diff(l, m, THETA): # egm96 norm for a (beacause of coefficients with this norm)
    if m == 0: 
        a = np.sqrt( (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    else: 
        a = np.sqrt( 2 *  (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    s = sym.Symbol('s')
    G = (s ** 2 - 1) ** l
    H = (1 - s ** 2) ** (abs(m) / 2)
    #P_lm = (1 / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)
    #P_lm_diff = sym.diff(P_lm, s, 1)
    P_lm_diff = (1 / (math.factorial(l) * (2 ** l))) * ( (abs(m) / 2) * (1 - s ** 2) ** (abs(m) / 2 - 1) * (-2*s) * sym.diff(G, s, abs(m) + l) + H *  sym.diff(G, s, abs(m) + l + 1))
    P_lm_diff = sym.lambdify(s, P_lm_diff)
    with np.errstate(divide='ignore'):
        P_lm_diff = a * P_lm_diff(np.sin(THETA))
    return P_lm_diff


# Calculates Gravitational Potential caused by earth in a sphere using functions get_ass_leg()
# Return Gravitational Potential Matrix
def get_pot(l, m, C, S, THETA, PHI, MU, R_T, r):
    arr_size = len(l)
    # Initialize U=1 because of J0 (The sum when l=0,m=0 we have Plm=1 since Cnm=1(I think) what is inside of sum stays 1, in the end its multiplied by MU/r)??????
    U = 1
    for i in range(arr_size):
        U = U + (R_T / r)**l[i] * get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI))
    U = U * MU / r
    return -U


# Calculates Gravitational Acceleration caused by earth in a sphere using functions get_ass_leg() and get_ass_leg_diff()
# Return absolute Gravitational Acceleration Matrix
def get_accel(l, m, C, S, THETA, PHI, MU, R_T, r):
    arr_size = len(l)
    gr = -MU/r**2
    gt = 0
    gp = 0
    for i in range(arr_size):
        gr = gr - R_T**l[i] * (l[i]+1) * MU * get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI)) / (r**(l[i]+2))
        with np.errstate(all='ignore'):
            gt = gt + R_T**l[i] * MU * get_ass_leg_diff(l[i], m[i], THETA) * np.cos(THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI)) / (r**(l[i]+2))
        gp = gp + R_T**l[i] * MU * m[i] * get_ass_leg(l[i], m[i], THETA) * (S[i] * np.cos(m[i] * PHI) - C[i] * np.sin(m[i]* PHI)) / (r**(l[i]+2) * np.sin(THETA))
    g = np.sqrt(gr**2 + gt**2 + gp**2)
    return g


########################### No Use ####################################


# # Convert polar coordinates to cartesian coordinates
# Theta -pi/2 to pi/2
def get_cart(PHI, THETA, r):
    X = r * np.cos(THETA) * np.cos(PHI)
    Y = r * np.cos(THETA) * np.sin(PHI)
    Z = r * np.sin(THETA)
    return X, Y, Z


# Calculate and return Undulation using read_file() and get_pot() functions
def get_undulation(THETA, PHI, MU, R_T):
    lmax = 16
    l, m, C, S = read_file('earth_egm96_to360.ascii.txt', lmax)
    Potencial = -get_pot(l, m, C, S, THETA, PHI, MU, R_T, R_T)
    zonal_ind = np.where(m == 0)
    zonal_l = l[zonal_ind]
    zonal_m = m[zonal_ind]
    zonal_C = C[zonal_ind]
    zonal_S = S[zonal_ind]
    zonal_Potencial = -get_pot(zonal_l, zonal_m, zonal_C, zonal_S, THETA, PHI, MU, R_T, R_T)
    T = Potencial - zonal_Potencial
    N = R_T**2 * T / MU # [m]
    return N