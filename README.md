# janbaunooo_photobooth
[WIP] A photobooth using a Raspberry Pi and a DSLR written in Python and running from framebuffer.

Goals :
- [x] running from framebuffer
- [x] showing live preview
- [ ] textual guidance
- [x] take photos after pushing a physical button
- [ ] show photos sequence
- [ ] store photos localy

Take photos sequence :
- [ ] countdown
- [x] turn on lights
- [x] capture photo
- [x] show captured photo briefly

Using :
- libgphoto2
- pyGame
- RPi.GPIO
    - Need to connect Button to GPIO 3
    - Need to connect Relay  to GPIO 5

Tested with :
- Canon EOS 1200D

Inspired by :
- https://github.com/contractorwolf/RaspberryPiPhotobooth
- https://github.com/drumminhands/drumminhands_photobooth
- https://github.com/jcupitt/rtiacquire

