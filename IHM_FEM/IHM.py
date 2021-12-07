import scipy.io
from scipy.signal import find_peaks

import numpy as np
import numpy.matlib

import matplotlib.pyplot as plt

# pip install plotly==5.4.0 || conda install -c plotly plotly=5.4.0
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# pip insatll pandas
import pandas as pd

# pip install dash
import dash
from dash import dcc
from dash import html

def forwprobihm(dip, elec, sbr, R):
    nbdip = len(dip)
    nel = len(elec)
    
    
    LF = np.zeros((nel, nbdip*3))
    velec = np.zeros([nel, nbdip])
    
    for idip in range(nbdip):
        orr=np.zeros([1,3],dtype=float)     
        darro = dip[idip,0:3]               
        amp = np.linalg.norm(dip[idip,3:6]) 
        orr[0,0:4] = dip[idip,3:6]/amp      
        Xd = elec - np.matlib.repmat(darro, nel, 1) 
        LF[:,idip*3:(idip+1)*3] = 1/(4*np.pi*sbr)*np.true_divide(Xd,(np.power(np.reshape(np.sum(np.power(Xd, 2),1), (nel,1)),(3/2))*np.ones((1,3))) )
        velec[:,idip,None]=LF[:,idip*3:(idip+1)*3].dot(np.transpose(orr))*amp
    return LF, velec

if __name__ == "__main__":
    n_dip = 250
    mni_electrode = scipy.io.loadmat("04_Practical\MNI-electrodes.mat")
    mni_surface_mesh = scipy.io.loadmat("04_Practical\MNI-GMSurfaceMesh10.mat")
    
    mni_electrode_elp = mni_electrode['elp']
    dippos = mni_electrode['dippos']
    LFel2t = mni_electrode['LFel2t']
    electrode_names = mni_electrode['XelnamesIn']
    
    print("==================")
    for key, value in mni_electrode.items():
        print(key)
        
    n_dippos = np.array([dippos[n_dip]])    

    dippos_x, dippos_y, dippos_z = dippos[n_dip].T
    dippos_x = np.array(dippos_x)
    dippos_y = np.array(dippos_y)
    dippos_z = np.array(dippos_z)    
    
    
    electrode_x = mni_electrode_elp[:, 0]
    electrode_y = mni_electrode_elp[:, 1] 
    electrode_z = mni_electrode_elp[:, 2] 
    
    gm_surface_mesh_point_cooords = mni_surface_mesh['GMSurfaceMesh'][0][0][0]
    gm_surface_mesh_faces = mni_surface_mesh['GMSurfaceMesh'][0][0][1]
    
    ordered_faces = []
    
    for i in range(gm_surface_mesh_faces.shape[0]):
        for j in range(3):
            ordered_faces.append(gm_surface_mesh_faces[i, j])
    
    
    x = []
    y = []
    z = []
    
    for point in ordered_faces:
        x.append(gm_surface_mesh_point_cooords[point-1, 0])
        y.append(gm_surface_mesh_point_cooords[point-1, 1])
        z.append(gm_surface_mesh_point_cooords[point-1, 2])
    
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    
    fig = make_subplots(rows=1, cols=2)
    
    fig.add_trace(go.Mesh3d(x=x,
                            y=y,
                            z=z,
                            alphahull=2,
                            opacity=0.3), row=1, col=1)
    
    fig.add_trace(go.Scatter3d(x=electrode_x,
                               y=electrode_y,
                               z=electrode_z,
                               mode="markers"),
                  row=1, col=1)
    
    fig.add_trace(go.Scatter3d(x=dippos_x,
                               y=dippos_y,
                               z=dippos_z,
                               mode="markers",
                               marker=dict(
                                   size=5,
                                   color="DarkSlateGrey"
                               )),
                  row=1, col=1)
    
    # fig.add_trace(go.Scatter(x=dip_LF))
    fig.update_layout(autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))
    
    
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    
    app.run_server(debug=True, use_reloader=True)