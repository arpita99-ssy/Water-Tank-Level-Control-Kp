'''
LICENSE AGREEMENT
In relation to this Python file:
1. Copyright of this Python file is owned by the author: Mark Misin
2. This Python code can be freely used and distributed
3. The copyright label in this Python file such as
copyright=ax_main.text(x,y,'© Mark Misin Engineering',size=z)
that indicate that the Copyright is owned by Mark Misin MUST NOT be removed.
'''

# ---------------------------------------------------
# Modified by: Arpita Priyadarshini Sahoo
# Purpose    : Educational / Student Project
# ---------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
import numpy as np

radius = 5
bottom = 0
final_volume = 100
dVol = 10
width_ratio = 1
dt = 0.04
t0 = 0
t_end = 50
frame_amount = int(t_end/dt)
t = np.arange(t0, t_end+dt, dt)
density_water = 1000

Kp1 = 1000
Kp2 = 1000
Kp3 = 5000

vol_o1_i = 30
vol_r1_i = 70
vol_o2_i = 40
vol_r2_i = 10
vol_o3_i = 50
vol_r3_i = 20

# ---------------- Tank 1 ----------------
vol_r1 = np.zeros(len(t))
vol_r1[0] = vol_r1_i
volume_Tank1 = np.zeros(len(t))
volume_Tank1[0] = vol_o1_i
error1 = np.zeros(len(t))
m_dot1 = Kp1 * error1

# ---------------- Tank 2 ----------------
vol_r2 = np.zeros(len(t))
vol_r2[0] = vol_r2_i
volume_Tank2 = np.zeros(len(t))
volume_Tank2[0] = vol_o2_i
error2 = np.zeros(len(t))
m_dot2 = Kp2 * error2

# ---------------- Tank 3 ----------------
vol_r3 = vol_o3_i + 1*t*np.sin(2*np.pi*(0.005*t)*t)
volume_Tank3 = np.zeros(len(t))
error3 = np.zeros(len(t))
m_dot3 = Kp3 * error3

# ---------------- Simulation ----------------
for i in range(1, len(t)):
    if i < 300:
        vol_r1[i] = vol_r1_i
        vol_r2[i] = vol_r2_i + 3*t[i]
    elif i < 600:
        vol_r1[i] = 20
        vol_r2[i] = vol_r2_i + 3*t[i]
        time_temp2 = t[i]
        temp2 = vol_r2[i]
    elif i < 900:
        vol_r1[i] = 90
        vol_r2[i] = temp2 - 1*(t[i]-time_temp2)
    else:
        vol_r1[i] = 50
        vol_r2[i] = temp2 - 1*(t[i]-time_temp2)

    error1[i-1] = vol_r1[i-1] - volume_Tank1[i-1]
    error2[i-1] = vol_r2[i-1] - volume_Tank2[i-1]
    error3[i-1] = vol_r3[i-1] - volume_Tank3[i-1]

    m_dot1[i] = Kp1 * error1[i-1]
    m_dot2[i] = Kp2 * error2[i-1]
    m_dot3[i] = Kp3 * error3[i-1]

    volume_Tank1[i] = volume_Tank1[i-1] + (m_dot1[i-1]+m_dot1[i])/(2*density_water)*dt
    volume_Tank2[i] = volume_Tank2[i-1] + (m_dot2[i-1]+m_dot2[i])/(2*density_water)*dt
    volume_Tank3[i] = volume_Tank3[i-1] + (m_dot3[i-1]+m_dot3[i])/(2*density_water)*dt

# ---------------- Animation ----------------
fig = plt.figure(figsize=(16,9), dpi=120, facecolor=(0.8,0.8,0.8))
gs = gridspec.GridSpec(2,3)

ax0 = fig.add_subplot(gs[0,0])
vol_r1_plot, = ax0.plot([],[],'r',lw=2)
tank_12, = ax0.plot([],[],'royalblue',lw=260)
ax0.set_xlim(-radius, radius)
ax0.set_ylim(bottom, final_volume)
ax0.set_title("Tank 1")
ax0.set_ylabel("tank volume [m³]")
ax0.text(-radius, final_volume+5, "© Mark Misin Engineering", fontsize=10)
ax0.text(-radius, final_volume-5, "Modified by Arpita P. Sahoo", fontsize=9)

ax1 = fig.add_subplot(gs[0,1])
vol_r2_plot, = ax1.plot([],[],'r',lw=2)
tank_22, = ax1.plot([],[],'royalblue',lw=260)
ax1.set_xlim(-radius, radius)
ax1.set_ylim(bottom, final_volume)
ax1.set_title("Tank 2")

ax2 = fig.add_subplot(gs[0,2])
vol_r3_plot, = ax2.plot([],[],'r',lw=2)
tank_32, = ax2.plot([],[],'royalblue',lw=260)
ax2.set_xlim(-radius, radius)
ax2.set_ylim(bottom, final_volume)
ax2.set_title("Tank 3")

ax3 = fig.add_subplot(gs[1,:])
t1, = ax3.plot([],[],'b',lw=3,label="Tank 1")
t2, = ax3.plot([],[],'g',lw=3,label="Tank 2")
t3, = ax3.plot([],[],'r',lw=3,label="Tank 3")
ax3.set_xlim(0,t_end)
ax3.set_ylim(0,final_volume)
ax3.grid(True)
ax3.legend()

def update(i):
    tank_12.set_data([0,0],[0,volume_Tank1[i]])
    tank_22.set_data([0,0],[0,volume_Tank2[i]])
    tank_32.set_data([0,0],[0,volume_Tank3[i]])

    vol_r1_plot.set_data([-radius,radius],[vol_r1[i],vol_r1[i]])
    vol_r2_plot.set_data([-radius,radius],[vol_r2[i],vol_r2[i]])
    vol_r3_plot.set_data([-radius,radius],[vol_r3[i],vol_r3[i]])

    t1.set_data(t[:i], volume_Tank1[:i])
    t2.set_data(t[:i], volume_Tank2[:i])
    t3.set_data(t[:i], volume_Tank3[:i])

    return tank_12,tank_22,tank_32,t1,t2,t3

ani = animation.FuncAnimation(fig, update, frames=frame_amount, interval=20)
plt.show()
