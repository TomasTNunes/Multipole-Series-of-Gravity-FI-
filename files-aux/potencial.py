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


def save_file(X,Y,Z,N):
    f1 = open(f"X.txt", "w")
    np.savetxt(f1,X)
    f1.close()
    f2 = open(f"Y.txt", "w")
    np.savetxt(f2,Y)
    f2.close()
    f3 = open(f"Z.txt", "w")
    np.savetxt(f3,Z)
    f3.close()
    f4 = open(f"N.txt", "w")
    np.savetxt(f4,N)
    f4.close()

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

    # Define phi & theta
    n = 200
    phi = np.linspace(-np.pi, np.pi, n)
    theta = np.linspace(-np.pi/2, np.pi/2, n)
    [PHI, THETA] = np.meshgrid(phi, theta)

    # Potencial
    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, r)

    # Potencial mollweide 
    """fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, Potencial, cmap=cm.RdBu)
    ax.set_title(f'h = {(r-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    #gravitational acceleration
    """g = get_accel(l, m, C, S, THETA, PHI, MU, R_T, r)
    g[g==np.inf] = np.nan

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, g, cmap=cm.jet)
    ax.set_title(f'h = {(r-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(g)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('g [m/s^2]')
    ax.grid(color='k')
    plt.show()"""

    # Potencial 3D (X)
    """X, Y, Z = get_cart(PHI, THETA, r)
    norm = colors.Normalize()
    ax = plt.subplot(111, projection = '3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=cm.RdBu(norm(Potencial)))
    plt.show()"""

    # Potencial for 2 different r
    """r2 =  R_T + 230e3
    Potencial2 = get_pot(l, m, C, S, THETA, PHI, MU, R_T, r2)

    if Potencial.min() < Potencial2.min():
        vmin = Potencial.min()
    else:
        vmin = Potencial2.min()

    if Potencial.max() > Potencial2.max():
        vmax = Potencial.max()
    else:
        vmax = Potencial2.max()
    
    print(vmin)
    print(vmax)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, Potencial, cmap=cm.RdBu, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    
    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, Potencial2, cmap=cm.RdBu, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r2-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')

    plt.show()"""

    # ---------220-230km------------------pot
    """vmax = -60258744.753098436
    vmin = -60442292.09159016
    r3 = R_T + 222e3
    Potencial3 = get_pot(l, m, C, S, THETA, PHI, MU, R_T, r3)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, Potencial3, cmap=cm.RdBu, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r3-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # g for 2 different r
    """r2 =  R_T + 230e3
    g = get_accel(l, m, C, S, THETA, PHI, MU, R_T, r) 
    g2 = get_accel(l, m, C, S, THETA, PHI, MU, R_T, r2)
    g[g==np.inf] = np.nan
    g2[g2==np.inf] = np.nan

    if np.nanmin(g) < np.nanmin(g2):
        vmin = np.nanmin(g)
    else:
        vmin = np.nanmin(g2)

    if np.nanmax(g) > np.nanmax(g2):
        vmax = np.nanmax(g)
    else:
        vmax = np.nanmax(g2)
    
    print(vmin)
    print(vmax)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(121, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, g, cmap=cm.jet, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational accel [Nm/kg]')
    ax.grid(color='k')
    
    ax = plt.subplot(122, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, g2, cmap=cm.jet, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r2-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational accel [Nm/kg]')
    ax.grid(color='k')

    plt.show()"""

    # ---------220-230km------------------accel
    """vmax = 9.170099309219546
    vmin = 9.10043938979901
    r3 = R_T + 225e3
    g3 = get_accel(l, m, C, S, THETA, PHI, MU, R_T, r3)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, g3, cmap=cm.jet, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r3-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # Earth format 3D (?)
    """arr_size = len(l)
    f = 0
    for i in range(arr_size):
        f = f + get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI))
    X, Y, Z = get_cart(PHI, THETA, 150*f+1)

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()
    mlab.mesh(X, Y, Z, scalars=f, colormap='seismic')
    mlab.view(-85,85,30)
    mlab.show()"""

    # Earth format mollweide (?)
    """arr_size = len(l)
    f = 0
    for i in range(arr_size):
        f = f + get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI))
    X, Y, Z = get_cart(PHI, THETA, 150*f+1)
    
    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(PHI, THETA, f, cmap=cm.seismic)
    clrbr = cm.ScalarMappable(cmap=cm.seismic)
    clrbr.set_array(f*100000)
    fig.colorbar(clrbr, orientation='horizontal')
    ax.grid(color='k')
    plt.show()"""

    # Potencial(r) THETA = 0
    """n = 200
    phi = np.linspace(-np.pi, np.pi, n)
    r = np.linspace(R_T, R_T + 8000e3, n)
    [PHI, R] = np.meshgrid(phi, r)
    THETA = 0

    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, R)
    X, Y, Z = get_cart(PHI, THETA, R*1e-3)
    print(Potencial.min())
    print(Potencial.max())

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(X, Y, Potencial, cmap=cm.RdBu)
    ax.set_title(f'elevation angle = {0}')
    ax.set_xlabel('X [Km]')
    ax.set_ylabel('Y [Km]')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    #---------------------2000-8000----------------------------pot
    """n = 200
    phi = np.linspace(-np.pi, np.pi, n)
    r = np.linspace(R_T, R_T + 8000e3, n)
    [PHI, R] = np.meshgrid(phi, r)
    THETA = 0

    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, R)
    X, Y, Z = get_cart(PHI, THETA, R*1e-3)

    vmin = -62529420.408364825
    vmax = -27725589.761912752

    lim = R_T*1e-3 + 8000
    
    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(X, Y, Potencial, cmap=cm.RdBu, vmin=vmin, vmax=vmax)
    ax.set_title(f'Polar Angle = {0}')
    ax.set_xlabel('X [Km]')
    ax.set_ylabel('Y [Km]')
    ax.set_xlim(xmin=-lim,xmax=lim)
    ax.set_ylim(ymin=-lim,ymax=lim)
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # g(r) THETA = 0
    """phi = np.linspace(-np.pi, np.pi, n)
    r = np.linspace(R_T, R_T + 8000e3, n)
    [PHI, R] = np.meshgrid(phi, r)
    THETA = 0.001

    g = get_accel(l, m, C, S, THETA, PHI, MU, R_T, R)
    g[g==np.inf] = np.nan
    X, Y, Z = get_cart(PHI, THETA, R*1e-3)
    print(np.nanmin(g))
    print(np.nanmax(g))

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(X, Y, g, cmap=cm.jet)
    ax.set_title(f'elevation angle ≈{0}')
    ax.set_xlabel('X [Km]')
    ax.set_ylabel('Y [Km]')
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(g)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    #---------------------2000-8000----------------------------accel
    """n = 200
    phi = np.linspace(-np.pi, np.pi, n)
    r = np.linspace(R_T, R_T + 7000e3, n)
    [PHI, R] = np.meshgrid(phi, r)
    THETA = 0.001

    g = get_accel(l, m, C, S, THETA, PHI, MU, R_T, R)
    g[g==np.inf] = np.nan
    X, Y, Z = get_cart(PHI, THETA, R*1e-3)

    save_file(X,Y,g)

    vmin = 1.9287201310684448
    vmax = 9.820921038576518

    lim = R_T*1e-3 + 8000
    
    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(X, Y, g, cmap=cm.jet, vmin=vmin, vmax=vmax)
    ax.set_title(f'Polar Angle ≈ {0}')
    ax.set_xlabel('X [Km]')
    ax.set_ylabel('Y [Km]')
    ax.set_xlim(xmin=-lim,xmax=lim)
    ax.set_ylim(ymin=-lim,ymax=lim)
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational accel [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # Potencial(r) PHI = 0
    """theta = np.linspace(-np.pi/2, np.pi/2, n)
    r = np.linspace(R_T, R_T + 5000e3, n)
    [THETA, R] = np.meshgrid(theta, r)
    PHI = 0

    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, R)
    X, Y, Z = get_cart(PHI, THETA, R*1e-3)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(X, Z, Potencial, cmap=cm.RdBu)
    ax.set_title(f'azimuth angle = {0}')
    ax.set_xlabel('X [Km]')
    ax.set_ylabel('Y [Km]')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # Undulation  [m]
    """N = get_undulation(THETA, PHI, MU, R_T)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    ax.pcolormesh(PHI*180/np.pi, THETA*180/np.pi, N, cmap=cm.jet)
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array([-100, 80])
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Geoid height [m]')
    ax.grid(color='k')
    plt.show()
    
    X, Y, Z = get_cart(PHI, THETA, 10000*N+R_T)

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()
    mlab.mesh(X, Y, Z, scalars=N, colormap='jet')
    mlab.show()"""

    # Undulation (perfect sphere)
    """rm = 6371.0088e3 # [m]
    #Pot = -get_pot(l, m, C, S, THETA, PHI, MU, rm, rm)
    Pot = 1 + (rm / rm)**l[0] * get_ass_leg(l[0], m[0], THETA) * (C[0] * np.cos(m[0] * PHI) + S[0] * np.sin(m[0]* PHI))
    Pot = Pot * MU / rm
    R = rm**2 * Pot / MU
    print(R.min())
    print(R.max())

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    ax.pcolormesh(PHI*180/np.pi, THETA*180/np.pi, R, cmap=cm.jet)
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(R*1e-3)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Ellipsoid [Km]')
    ax.grid(color='k')
    plt.show()

    X, Y, Z = get_cart(PHI, THETA, R)
    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()
    mlab.mesh(X, Y, Z, scalars=R, colormap='jet')
    mlab.show()"""

