# Initial Setup

This guide covers the necessary steps to prepare the CAN-TestBed environment. You will first configure the physical connections for the microcontrollers, followed by installing the required backend (Python) and frontend (Node.js) software.

**Quick Links:**
* [Hardware Setup](#hardware-setup)
* [Software Setup](#software-setup)

---

## Hardware Setup
To run the testbed, you require the following components:
* **Microcontrollers:** RP2040 boards (e.g., PicoArduino) to act as ECUs.
* **Adapter:** A CANable USB adapter for the main bus interface.

**Steps:**
1.  Connect the RP2040 boards to your computer via USB.
2.  Connect the CANable adapter to the same computer via USB.
3.  Ensure all devices are powered on.

## Software Setup

### Step 1: Clone the Repository
```bash
sudo git clone [https://github.com/trevormcclellan/CAN-TestBed](https://github.com/trevormcclellan/CAN-TestBed)
sudo mkdir TestBED
```
### Step 2: Install the Arduino IDE and Libraries

**Recommended: Automatic Setup (Arduino CLI)**

For most users, the easiest way to install dependencies is to use the provided setup script. The install_deps.sh is located in the rp2040 directory. This script will install arduino-cli to the user's home directory if it is not found, then install all required libraries, including the custom CANBed RP2040 library from Longan Labs. If you have the Arduino IDE installed, this script should add all of the dependencies there as well, if you would like to use it later. Run the script using the following command:

```bash
./rp2040/install_deps.sh
```
