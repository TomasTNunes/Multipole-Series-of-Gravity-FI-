import math
import numpy as np
import sympy as sym
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab
from mpl_toolkits.basemap import Basemap
from tvtk.api import tvtk

# Plot
#################################################################################################################

def matplot_mollweide(X, Y, Values, cmap):
    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(X, Y, Potencial, cmap=cm.RdBu)
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    fig.colorbar(clrbr, orientation='horizontal')
    ax.grid(color='k')

def save_file(Pot,g,st):
    f1 = open(f"P-{st}.txt", "w")
    np.savetxt(f1,Pot)
    f1.close()
    f2 = open(f"A-{st}.txt", "w")
    np.savetxt(f2,g)
    f2.close()

#################################################################################################################

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

def read_file(name, lmax):
    path = 'data/' + name
    with open(path, 'r') as infile:
        lines = infile.readlines()
    line = np.array([lin.split() for lin in lines])
    arr_size = int((4 + lmax) / 2 * (lmax - 1))

    l = line[0:arr_size,0].astype('int64')
    m = line[0:arr_size,1].astype('int64')
    C = line[0:arr_size,2].astype('float64')
    S = line[0:arr_size,3].astype('float64')

    return l, m, C, S

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

def get_pot(l, m, C, S, THETA, PHI, MU, R_T, r):
    arr_size = len(l)
    # Initialize U=1 because of J0 (The sum when l=0,m=0 we have Plm=1 since Cnm=1(I think) what is inside of sum stays 1, in the end its multiplied by MU/r)??????
    U = 1
    for i in range(arr_size):
        U = U + (R_T / r)**l[i] * get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI))
    U = U * MU / r
    return -U

def get_cart(PHI, THETA, r):
    X = r * np.cos(THETA) * np.cos(PHI)
    Y = r * np.cos(THETA) * np.sin(PHI)
    Z = r * np.sin(THETA)

    return X, Y, Z

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


# EARTH EGM96
if __name__ == "__main__":

    # Gravitational parameter of Earth [m^3 s^-2]
    MU = 3.986004405e14 

    # Mean equitorial radius [m]
    R_T = 6.3781363e6

    # Calculate potencial Radius [m]
    r =  R_T + 220e3

    # max ind
    lmax = 5

    # Read File
    l, m, C, S = read_file('earth_egm96_to360.ascii.txt', lmax)
    a = C[0]
    #C[0] = C[16]
    #C[16] = a
    st = 'C20'

    # Define phi & theta
    n = 200
    phi = np.linspace(-np.pi, np.pi, n)
    theta = np.linspace(-np.pi/2, np.pi/2, n)
    [PHI, THETA] = np.meshgrid(phi, theta)

    # Potencial
    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, R_T)

    g = get_accel(l, m, C, S, THETA, PHI, MU, R_T, R_T)
    g[g==np.inf] = np.nan

    save_file(Potencial,g,st)


    """fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(121)
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    ax.pcolormesh(PHI*180/np.pi, THETA*180/np.pi, Potencial, cmap=cm.RdBu)
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Pot')
    ax.grid(color='k')

    ax = plt.subplot(122)
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    ax.pcolormesh(PHI*180/np.pi, THETA*180/np.pi, g, cmap=cm.jet)
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(g)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('accel')
    ax.grid(color='k')
    plt.show()"""