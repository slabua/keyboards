# AtreuSLB50+ Mechanical Keyboard
###### tags: `Raspberry Pi` `RaspberryPi` `Raspberry` `Pi` `Pico` `RaspberryPiPico` `MicroPython`
Status: Currently under development.

### A hand-wired custom Mechanical Keyboard based on the [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/).


Finally I had the time to wrap up my little side project started about three months ago, and I thought to share it here. Although inspired by the Atreus, I couldn't quite find the right compromise among the non-split ergo keyboards, so I decided to make my own.

## Components:
- 1x RP2040 (KMK on Raspberry Pi Pico), USB-C port
- 50x switches
- 1x SSD1306 128x64px 0.96in IIC OLED display
- 2x EC11 rotary encoders
- 1x EVQWGD001 rotary encoder
- 1x Pimoroni IIC trackball breakout
- 1x Active buzzer
- 2x micro switches (bootsel, reset)
- 3D printed case (5-10° tilt), plate, pcb

## Story
The design started from a semi-automated customised process by forking an OpenSCAD hotswap pcb generator repository, subsequently heavily worked on Blender. I had also added cutouts for per-key rgb, but in the end I gave up the idea of hand wiring the LEDs. At least in this version which, for me, has been an insightful experience.
I am slowly finalising the firmware configuration and I will eventually put it on github as usual. Wiring diagram and key layout will come along later.

## Keymap
[Coming Soon]

## Repository
[Coming Soon]

## 3D Model
3D model of AtreuSLB50+ v1 available on Thingiverse and Printables:
https://www.thingiverse.com/thing:5458679
https://www.printables.com/model/262446-atreuslb50-v1

## Some photographs
![](https://preview.redd.it/by89l5iuvxr91.jpg?width=4032&format=pjpg&auto=webp&s=fdcf4890802f44207e813c551c8d05d4a425c93b)

![](https://preview.redd.it/r71hvm8tvxr91.jpg?width=4032&format=pjpg&auto=webp&s=58ac29f5b1def6d11f49a1a23007bf6e484d98b9)

![](https://preview.redd.it/fttgez0uvxr91.jpg?width=4032&format=pjpg&auto=webp&s=52e817c0994529b7c309dc66521fbdf402360683)

![](https://preview.redd.it/ibiy8910wxr91.jpg?width=4032&format=pjpg&auto=webp&s=f439bdc82f43a4ab8cb5a897f337cff2a4c501d7)

![](https://preview.redd.it/xi2cjmi0wxr91.jpg?width=4032&format=pjpg&auto=webp&s=f45f572dd4d0b8e15e035926d678dd7473d5f8a7)

![](https://preview.redd.it/zntdv2lwvxr91.jpg?width=4032&format=pjpg&auto=webp&s=32b9563aa4a3dcba64fa90bf3244f9cdecf18d19)

![](https://preview.redd.it/ws6n538xvxr91.jpg?width=4032&format=pjpg&auto=webp&s=7e20985d11295b50b5d9a646b767ede51118eeb1)

![](https://preview.redd.it/fjrch7kxvxr91.jpg?width=4032&format=pjpg&auto=webp&s=1f00d5c165f395b89f9d8261484f2524a7e046bf)

![](https://preview.redd.it/xjj2dv3yvxr91.jpg?width=4032&format=pjpg&auto=webp&s=388d64ca4509c78ea6678420b1a73ccbb04189bf)

![](https://preview.redd.it/u2xzrteyvxr91.jpg?width=4032&format=pjpg&auto=webp&s=0b52b4458956fef54b64d0baa70c83ec2bb76906)
