import os
import pygame
import time
import random
import gphoto2 as gp

class photobooth :
    screen = None;
    
    def __init__(self):
        "Initialize a new pygame screen using the framebuffer"
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
        if not found:
            raise Exception('No suitable video driver found!')
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print('Framebuffer initialized')
        print('=======')
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        print('=======')
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def connectDSLR(self):
        print('Please connect and switch on your camera')
        context = gp.gp_context_new()
        camera = gp.check_result(gp.gp_camera_new())
        while True:
            error = gp.gp_camera_init(camera, context)
            if error >= gp.GP_OK:
                # operation completed successfully so exit loop
                break
            if error != gp.GP_ERROR_MODEL_NOT_FOUND:
                # some other error we can't handle here
                raise gp.GPhoto2Error(error)
            # no camera, try again in 2 seconds
            time.sleep(2)
        if hasattr(gp, 'gp_camera_autodetect'):
            # gphoto2 version 2.5+
            cameras = gp.check_result(gp.gp_camera_autodetect(context))
        else:
            port_info_list = gp.check_result(gp.gp_port_info_list_new())
            gp.check_result(gp.gp_port_info_list_load(port_info_list))
            abilities_list = gp.check_result(gp.gp_abilities_list_new())
            gp.check_result(gp.gp_abilities_list_load(abilities_list, context))
            cameras = gp.check_result(gp.gp_abilities_list_detect(
                abilities_list, port_info_list, context))
        n = 0
        for name, value in cameras:
            print('camera number', n)
            print('===============')
            print(name)
            print(value)
            print
            n += 1
        return 0

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()
    
    def captureMovie(self):
        print('Please connect and switch on your camera')
        context = gp.gp_context_new()
        camera = gp.check_result(gp.gp_camera_new())
        while True:
            error = gp.gp_camera_init(camera, context)
            if error >= gp.GP_OK:
                # operation completed successfully so exit loop
                break
            if error != gp.GP_ERROR_MODEL_NOT_FOUND:
                # some other error we can't handle here
                raise gp.GPhoto2Error(error)
            # no camera, try again in 2 seconds
            time.sleep(2)
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context))
        print('Success : GP_CAPTURE_IMAGE path: {0}/{1}'.format(file_path.folder, file_path.name))
        file_path = gp.check_result(gp.gp_camera_capture_preview(camera, context))
        file_path = gp.check_result(gp.gp_camera_capture_preview(camera, context))
        print('Success : capture_preview path: {0}/{1}'.format(file_path.folder, file_path.name))
        #picture = pygame.image.load(file)
        #main_surface.blit(picture, (0, 0))
        #pygame.display.flip()
        gp.check_result(gp.gp_camera_exit(camera, context))

# Create an instance of the photobooth class
photobooth = photobooth()
photobooth.captureMovie()
# time.sleep(10)
