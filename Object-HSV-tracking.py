import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
from matplotlib.widgets import Slider, Button

# Create a subplot
fig, ax = plt.subplots(1,2)

plt.subplots_adjust(bottom=0.35)

#Se crean los 6 sliders
ax_h = plt.axes([0.15, 0.2, 0.30, 0.03])
ax_s = plt.axes([0.15, 0.15, 0.30, 0.03])
ax_v = plt.axes([0.15, 0.1, 0.30, 0.03])

h_min_slider = Slider(ax_h, 'H-min', 0.0, 179.0, valinit=38.0)
s_min_slider = Slider(ax_s, 'S-min', 0.0, 255.0, valinit=50.0)
v_min_slider = Slider(ax_v, 'V-min', 0.0, 255.0, valinit=0.0)

ax_h_max = plt.axes([0.60, 0.2, 0.30, 0.03])
ax_s_max = plt.axes([0.60, 0.15, 0.30, 0.03])
ax_v_max = plt.axes([0.60, 0.1, 0.30, 0.03])

h_max_slider = Slider(ax_h_max, 'H-max', 0.0, 179.0, valinit=75.0)
s_max_slider = Slider(ax_s_max, 'S-max', 0.0, 255.0, valinit=255)
v_max_slider = Slider(ax_v_max, 'V-max', 0.0, 255.0, valinit=255.0)


# Create axes for reset button and create button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color='gold',
				hovercolor='skyblue')

# Create a function resetSlider to set slider to
# initial values when Reset button is clicked

def resetSlider(event):
    h_min_slider.reset()
    s_min_slider.reset()
    v_min_slider.reset()
    h_max_slider.reset()
    s_max_slider.reset()
    v_max_slider.reset()


# Call resetSlider function when clicked on reset button
button.on_clicked(resetSlider)

#Mostrando video en los subplots
capture = cv2.VideoCapture(0)

if capture.isOpened() is False:
    print("Error opening the camera")
    exit()
    
frame_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = capture.get(cv2.CAP_PROP_FPS)

# Variable para controlar si la ventana está abierta
window_open = True

# Función que se ejecuta al cerrar la ventana
def on_close(event):
    global window_open
    window_open = False

# Conectar la función de cierre al evento de cierre de la ventana
fig.canvas.mpl_connect('close_event', on_close)

while window_open and capture.isOpened():

    ret, frame = capture.read()

    if ret:

        frame = cv2.resize(frame, (150,0), fx = 0.4, fy = 0.4) 
        frame_original = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #Arrays que almacenarán los valores minimos y maximos modificados mediante los sliders
        min_hsv = np.array([h_min_slider.val, s_min_slider.val, v_min_slider.val])
        max_hsv = np.array([h_max_slider.val, s_max_slider.val, v_max_slider.val])
        
        mask = cv2.inRange(hsv_frame, min_hsv, max_hsv)
        result = cv2.bitwise_and(hsv_frame, hsv_frame, mask=mask)

        # Mostrar el video original en el primer subplot
        ax[0].imshow(frame_original)
        ax[0].set_title("Original frame")
        ax[0].axis('off') 

        # Mostrar el video resultado de la aplicación de la máscara en el segundo subplot
        ax[1].imshow(cv2.cvtColor(result, cv2.COLOR_HSV2RGB))
        ax[1].set_title("Mask")
        ax[1].axis('off')  

        plt.pause(0.001)
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    # Break the loop
    else:
        break
 
# Release everything:
capture.release()
cv2.destroyAllWindows()


