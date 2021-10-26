import numpy as np
import matplotlib.pyplot as plt

with open('settings.txt', 'r') as settings:
    setting = [float(i) for i in settings.read().split("\n")]

dt = setting[0]
dv = setting[1]
data_array = np.loadtxt("data.txt", dtype = int)
t_array = np.arange(0, dt*len(data_array), dt)
voltage_array = data_array * dv


fgr, ax = plt.subplots(figsize = (10, 15))
ax.plot(t_array, voltage_array, label = 'V(t)', marker = "8", markevery = 25, color = 'blue', linestyle = '-')
ax.set_xlabel('время, с')
ax.set_ylabel('напряжение, В')
ax.set_title("Процесс заряда и разряда конденсатора в RC-цепочке")
ax.set_xlim([t_array.min(), t_array.max()])
ax.set_ylim([voltage_array.min(), voltage_array.max()])
ax.legend()
ax.minorticks_on()
ax.grid(axis = "both", which = 'major', color = 'gray', linewidth = 1)
ax.grid(which = 'minor', color = 'gray', linestyle = ':')
t_zar = dt * voltage_array.argmax()
t_raz = dt*len(data_array) - t_zar
plt.text(7, 1.75, "Время заряда равно {: .2f} \n".format(t_zar), fontsize = 8)
plt.text(7, 1.75, "Время разряда равно {: .2f}".format(t_raz), fontsize = 8)
fgr.savefig("test.png")
plt.show() 


