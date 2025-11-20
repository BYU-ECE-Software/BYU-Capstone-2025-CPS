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

### 1. Clone the Repository
```bash
sudo git clone [https://github.com/trevormcclellan/CAN-TestBed](https://github.com/trevormcclellan/CAN-TestBed)
sudo mkdir TestBED
