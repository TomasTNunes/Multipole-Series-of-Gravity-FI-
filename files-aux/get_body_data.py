import os
from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
import math
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import sympy as sym
import pandas as pd

from PyQt5.QtWidgets import QWidget, QHBoxLayout
import visvis as vv
class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.fig = vv.backends.backend_pyqt5.Figure(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.fig._widget)
        self.setLayout(layout)
        self.setWindowTitle('OBJ')
        self.show()

def get_series_SH(coeff, l_max, PHI, THETA, basis_matrix):  
    f = PHI * 0
    for l in range(l_max+1):
        for m in range(-l,l+1):
            j = l**2 + l + m
            #f = f + coeff[l][m+l] * get_spherical_harmonic(l, m, PHI, THETA).astype(complex).real
            f = f + coeff[l][m+l] * basis_matrix[:,j]

    return f

def get_spherical_harmonic(l, m, PHI, THETA):
    a = np.sqrt(((2 * l + 1) / (4 * np.pi)) * (((math.factorial(l - abs(m))) / (math.factorial(l + abs(m))))))
    s = sym.Symbol('s')
    G = (s ** 2 - 1) ** l
    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = ((-1) ** abs(m) / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)
    P_lm = sym.lambdify(s, P_lm)
    Y_lm = a * np.exp(1j * abs(m) * PHI) * P_lm(np.cos(THETA))
    if m<0: Y_lm = (-1)**m * Y_lm.conj()

    return Y_lm

def get_Vertices_Faces(Body_name):
    folder = Body_name.split('-')[0]
    OBJ = pd.read_csv(f'data/{folder}/{Body_name}.OBJ', delim_whitespace=True, \
                                    names=['TYPE', 'X1', 'X2', 'X3'])

    VERTICES = OBJ.loc[OBJ['TYPE'] == 'v'][['X1', 'X2', 'X3']].values \
                .tolist()

    FACES = OBJ.loc[OBJ['TYPE'] == 'f'][['X1', 'X2', 'X3']].values
    FACES = FACES - 1
    FACES = FACES.astype(int)
    FACES = FACES.tolist()

    return VERTICES, FACES

def get_cart_vertices(r, phi, theta):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    VERTICES = np.zeros((len(x),3)) 
    VERTICES[:,0] = x
    VERTICES[:,1] = y
    VERTICES[:,2] = z

    return VERTICES

def get_polar_vertices(VERTICES):
    N = len(VERTICES)
    r = np.tile(0.0, N)
    theta = np.tile(0.0, N)
    phi = np.tile(0.0, N)
    for i in range(N):
        r[i] = np.sqrt(VERTICES[i][0]**2 + VERTICES[i][1]**2 + VERTICES[i][2]**2)
        theta[i] = np.arccos(VERTICES[i][2]/r[i]) # beteween 0 and PI
        phi[i] = math.atan2(VERTICES[i][1],VERTICES[i][0]) # beteween -PI and PI

    return r, theta, phi
    
def get_basis_matrix(phi, theta, l_max):
    k = (l_max+1)**2
    basis_matrix = np.zeros((len(phi),k)) # dtype=np.complex128 onde ha np.zero
    for l in range(l_max+1):
        for m in range(-l,l+1):
            j = l**2 + l + m
            basis_matrix[:,j] = get_spherical_harmonic(l, m, phi, theta).astype(complex).real

    return basis_matrix

def get_coeff_least_square(A, f):
    f = f.reshape(len(f),1)
    B = A.T @ A
    print(f'det(B)={np.linalg.det(B)}')
    if np.linalg.det(B) == 0:
        coeff = np.linalg.pinv(B) @ A.T @ f
    else:
        coeff = np.linalg.inv(B) @ A.T @ f

    residual_error = f - A @ coeff

    return coeff, residual_error


def vector2matrix (vector, l_max):
    k = 0
    matrix = np.zeros((l_max+1, 2*l_max+1))
    for i in range(l_max+1):
        for j in range(1+2*i):
            matrix[i][j] = vector[k]
            k = k+1

    return matrix

def save_SH_file(lmax, Body_name, VERTICES, FACES):
    FACES = np.array(FACES) + 1
    f = open(f'data/{Body_name}/{Body_name}-lmax{lmax}.OBJ', 'w')
    for i in range(len(VERTICES)):
        f.write(f'v {VERTICES[i][0]} {VERTICES[i][1]} {VERTICES[i][2]}\n')
    for i in range(len(FACES)):
        f.write(f'f {FACES[i][0]} {FACES[i][1]} {FACES[i][2]}\n')
    f.close()

def check_body_file_exists(lmax, Body_name):
    return os.path.isfile(f'data/{Body_name}/{Body_name}-lmax{lmax}.OBJ')



#https://www.hindawi.com/journals/mpe/2015/582870/#introduction

VERTICES = 0
FACES = 0
bodys = ['Asteroide', 'Mithra_4486']
lmax = [5, 80]

	

for Body_name in bodys:
    del VERTICES, FACES
    print('getting vertices & faces....')
	
    VERTICES, FACES = get_Vertices_Faces(Body_name)

	
    print('vertices & faces acquired')

	
    for l_max in lmax:

		
        if not check_body_file_exists(l_max, Body_name):
		    
            print('calculating r_Ver & theta_Ver & phi_Ver....')
		    
            r_Ver, theta_Ver, phi_Ver = get_polar_vertices(VERTICES)
		    
            print('r_Ver & theta_Ver & phi_Ver calculated')

		    
            print('calculating Basis Matrix ....')
		    
            Basis_Matrix = get_basis_matrix(phi_Ver, theta_Ver, l_max)
		    
            print('Basis Matrix calculated')

		    
            print('calculating Coeff_LS & Residual_error_LS....')
		    
            coeff_LS, res_error_LS = get_coeff_least_square(Basis_Matrix, r_Ver)
		    
            print(f'Mean Residual error: {np.mean(abs(res_error_LS)*1000)}')
		    
            print(f'Max Residual error: {abs(res_error_LS.max())*1000}')
		    
            print('Coeff_LS & Residual_error_LS calculated')
		    
		    
            print('tranforming vector coeff in matrix....')
		    
            coeff_LS_matrix = vector2matrix(coeff_LS, l_max)
		    
            print('vector coeff in matrix calculated')
            
            print('calculating series')
		    
            f = get_series_SH(coeff_LS_matrix, l_max, phi_Ver, theta_Ver, Basis_Matrix)
		    
            print('series calculated')

		    
            print('calculating vertices_SH....')
		    
            VERT_SH = get_cart_vertices(f, phi_Ver, theta_Ver)
		    
            print('vertices_SH calculated')

		    
            print('saving file....')
		    
            save_SH_file(l_max, Body_name, VERT_SH, FACES)
		    
            print('file saved')

		    
            del r_Ver, theta_Ver, phi_Ver, Basis_Matrix, coeff_LS, res_error_LS, coeff_LS_matrix, f, VERT_SH
		
        else:
		    
            pass