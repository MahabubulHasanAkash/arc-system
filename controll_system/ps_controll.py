import pygame
import rover_nav
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN: #if pressed
                val_pressed = event.button
                if val_pressed == 2:
                    rover_nav.rover_forward()
                elif val_pressed == 0:
                    rover_nav.rover_backward()
                elif val_pressed == 3:
                    rover_nav.rover_left_rotation()
                elif val_pressed == 1:
                    rover_nav.rover_right_rotation()
            elif event.type == pygame.JOYBUTTONUP: #if released
                rover_nav.rover_halt()
except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()