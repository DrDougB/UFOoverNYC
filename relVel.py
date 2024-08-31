#
# Calculates the relative velocity vector for NK3380 and the balloon assuming the balloon
# is being caried by the winds aloft at the time of the sighting.
#
# This script was written with the assistance of ChatGPT4. See OpenAI's copyright policy for 
# its use by this author.
#
# Copyright 2024 by Dr. Doug Buettner. All rights Reserved.
#

# Import libraries
import numpy as np
import math
import matplotlib.pyplot as plt

def calculate_relative_velocity():

    kts2fps = 1.68781 # factor used to convert speed from knots to feet per second

    # Constants in some future iteration we can make these inputs... 
    airplane_speed_ft_per_s = 207 * kts2fps  # Speed of the airplane in kts converted into feet per second
    # NK3380 heading is towards the North
    # NOTE: The "90 -" is to rotate so the coordinate system accounts for counterclockwise  from the north.
    #       
    airplane_heading_deg = 90-40   

    # Wind speed
    wind_speed_knots = 33 # Baseline value ... doing error calculations its +/- 7 knots
    wind_speed_ft_per_s = wind_speed_knots * kts2fps  # Convert wind speed from knots to ft/s

    # Wind direction converted to the direction it moves towards 
    # NOTE: The "90 -" is to rotate the wind direction coordinate system as being counterclockwise from 
    #       the north to cartesian coordinates. The winds are coming from 70 degrees, so the direction  
    #       vector is 70+180 degrees to point the vector in the direction that the wind is going to. 
    #       Finally, the result (90-250) will be negative so add 360 to make this a positive value.
    winds_aloft_heading_value = 70 # Baseline value ... doing error calculations its +/- 5 degrees
    wind_heading_deg = (90-(winds_aloft_heading_value+180)) + 360 

    # Airplane velocity components
    v_ax = airplane_speed_ft_per_s * math.cos(math.radians(airplane_heading_deg))  # Eastward component
    v_ay = airplane_speed_ft_per_s * math.sin(math.radians(airplane_heading_deg))  # Northward component
    

    # Wind velocity components
    v_wx = wind_speed_ft_per_s * math.cos(math.radians(wind_heading_deg))  # Eastward component
    v_wy = wind_speed_ft_per_s * math.sin(math.radians(wind_heading_deg))  # Northward component

    # Calculate relative velocity components
    v_relx = v_ax - v_wx
    v_rely = v_ay - v_wy

    # Calculate the magnitude of the relative velocity
    v_rel_magnitude = math.sqrt(v_relx**2 + v_rely**2)

    return v_rel_magnitude, v_ax, v_ay, airplane_speed_ft_per_s, v_wx, v_wy, v_relx, v_rely, wind_speed_ft_per_s, airplane_heading_deg, wind_heading_deg

def rotate_vector(x, y, angle_deg):
    angle_rad = math.radians(angle_deg)
    x_rot = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    y_rot = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return x_rot, y_rot

def plot_velocity_vectors(v_ax, v_ay, v_amag, v_wx, v_wy, v_wmag, v_relx, v_rely):
    fig = plt.figure(figsize=(8, 8))
    xPlusy = (-(v_ax-v_wx),-(v_ay-v_wy))

    array = np.array([[0, 0, v_ax, v_ay], 
                      [0, 0, v_wx, v_wy], 
                      [v_ax, v_ay, xPlusy[0], xPlusy[1]]])

    X, Y, U, V = zip(*array)

    # Plot the tuple of velocity vectors, NK3380 aircraft, wind and the resulting apparent (relative) velocity
    quiverObjects = plt.quiver(X, Y, U, V, color=['r','b','black'], scale=1, scale_units='xy', angles='xy')

    # Plotting the wind's velocity vector correctly

    plt.xlabel('Eastward Component (ft/s)')
    plt.ylabel('Northward Component (ft/s)')
    plt.title('Resulting Relative Velocity Vector')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
 #   plt.legend(quiverObjects, ('NK3380 Velocity', 'Wind Velocity', 'Apparent (Relative) Velocity'))

    plt.xlim(-300, 300)
    plt.ylim(-300, 300)

    plt.gca().set_aspect('equal', adjustable='box')
    fig.savefig('VelVectors.png')
    plt.show()

# Running the function
# v_ax, v_ay - components of the airplane's velocity
# v_wx, v_wy - components of the wind's velocity
# v_relx, v_rely - components of the relative velocity

relative_velocity_magnitude, v_ax, v_ay, v_amag, v_wx, v_wy, v_relx, v_rely, v_wmag, airplane_heading_deg, wind_heading_deg = calculate_relative_velocity()

relative_angle_deg = wind_heading_deg - airplane_heading_deg

# Rotate the relative velocity to the airplane's frame of reference
v_relx_rot, v_rely_rot = rotate_vector(v_relx, v_rely, -relative_angle_deg)

print(f"Relative Velocity Magnitude: {relative_velocity_magnitude} ft/s")
print(f"Relative Velocity X, Y-components (Aircraft Frame): {v_relx_rot, v_rely_rot} ft/s")
print(f"Airplane Velocity X, Y-components: {v_ax, v_ay} ft/s")
print(f"Balloon  Velocity X, Y-components: {v_wx, v_wy} ft/s")

plot_velocity_vectors(v_ax, v_ay, v_amag, v_wx, v_wy, v_wmag, v_relx_rot, v_rely_rot)
