VERSION = "0.0"

try:
    import sys
    import os
    import pygame
    import time
    import random
    import getopt
    import math
    #import gphoto2
    #from PIL import Image
    from socket import *
    from pygame.locals import *
except ImportError, err:
    print "Module not loaded : %s" % (err)
    sys.exit(2)

class RemoteDSLR:
    context = None
    camera = None
    def __init__(self):
        #Initialize
        self.context = gphoto2.gp_context_new()
        self.camera = gphoto2.check_result(gp.gp_camera_new())
        self.connect()
    def connect(self):
        print('Please connect and switch on your camera')
        while True:
            error = gphoto2.gp_camera_init(self.camera, self.context)
            if error >= gphoto2.GP_OK:
                # operation completed successfully so exit loop
                break
            if error != gphoto2.GP_ERROR_MODEL_NOT_FOUND:
                # some other error we can't handle here
                raise gphoto2.GPhoto2Error(error)
            # no camera, try again in 2 seconds
            time.sleep(2)
        print('Camera connected')   
    def capturePreview(self):
        print 'CapturePreview'
        try:
            camera_file = gphoto2.check_result(
                                        gphoto2.gp_camera_capture_preview(
                                                                    self.camera,
                                                                    self.context))
            file_data = gphoto2.check_result(
                                        gphoto2.gp_file_get_data_and_size(camera_file))
            image = Image.open(io.BytesIO(file_data))
        except:
            print "Preview not captured : %s" % (err)
            image = None
        return image
    def captureImage(self,target):
        print('Capture image')
        #target = os.path.join('/tmp', file_path.name)
        try:
            file_path = gphoto2.check_result(
                                gphoto2.gp_camera_capture(
                                                self.camera,
                                                gphoto2.GP_CAPTURE_IMAGE,
                                                self.context))
            camera_file = gphoto2.check_result(
                                gphoto2.gp_camera_file_get(
                                                self.camera,
                                                file_path.folder,
                                                file_path.name,
                                                gphoto2.GP_FILE_TYPE_NORMAL,
                                                self.context))
            gphoto2.check_result(gphoto2.gp_file_save(camera_file, target))
        except err:
            print "Image not captured : %s" % (err)

def main():
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
        print('No suitable video driver found ! Fallback without framebuffer')
        os.unsetenv('SDL_VIDEODRIVER')
        pygame.init()
        screen = pygame.display.set_mode((1200, 860)) #, pygame.FULLSCREEN
    else:
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    # turn off the mouse pointer
    pygame.mouse.set_visible(0)
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    # Initialize components
    remoteDSLR = RemoteDSLR()
    # Update screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    # Initialize clock
    clock = pygame.time.Clock()
    mainLoopRunning = True
    inPreviewLoop = True
    # Events Loop
    while mainLoopRunning:
        # Limit FPS to 60fps
        # clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                mainLoopRunning = False
                return
        if inPreviewLoop:
            remoteDSLR.capturePreview
        pygame.display.flip()

if __name__ == '__main__': main()
