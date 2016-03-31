import os
import pygame
import time
import random
import gphoto2 as gp

from PIL import Image

class photobooth :
    screen = None;
    context = None;
    camera = None;
    
    def __init__(self):
        self.connectFrameBuffer();
        self.connectSLR();

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
        gp.check_result(gp.gp_camera_exit(self.camera, self.context))

    def connectFrameBuffer(self):
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

    def connectDSLR(self):
        print('Please connect and switch on your camera')
        self.context = gp.gp_context_new()
        self.camera = gp.check_result(gp.gp_camera_new())
        while True:
            error = gp.gp_camera_init(self.camera, self.context)
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
            cameras = gp.check_result(gp.gp_camera_autodetect(self.context))
        else:
            port_info_list = gp.check_result(gp.gp_port_info_list_new())
            gp.check_result(gp.gp_port_info_list_load(port_info_list))
            abilities_list = gp.check_result(gp.gp_abilities_list_new())
            gp.check_result(gp.gp_abilities_list_load(abilities_list, self.context))
            cameras = gp.check_result(gp.gp_abilities_list_detect(
                abilities_list, port_info_list, self.context))
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
    
    def captureImage(self):
        print('Capture image')
        file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE, self.context))
        target = os.path.join('/tmp', file_path.name)
        print('Copying image to', target)
        camera_file = gp.check_result(gp.gp_camera_file_get(
                                            self.camera, file_path.folder,
                                            file_path.name,
                                            gp.GP_FILE_TYPE_NORMAL,
                                            self.context))
        gp.check_result(gp.gp_file_save(camera_file, target))

    def capturePreviewLoop(self):
        print('Capture PreviewLoop')
        camera_file = gp.check_result(gp.gp_camera_capture_preview(self.camera, self.context))
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
        image = Image.open(io.BytesIO(file_data))
        #img = pygame.image.fromstring(image.tostring(), (image.size[0],image.size[1]), 'RGB', False)
        #main_surface.blit(img, (0, 0))
        #time.sleep(10)

# Create an instance of the photobooth class
photobooth = photobooth()
photobooth.captureImage()
#picture = pygame.image.load(file)
#main_surface.blit(picture, (0, 0))
#pygame.display.flip()
# time.sleep(10)
