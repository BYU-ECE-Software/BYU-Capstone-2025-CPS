# Initial Setup 

This guide covers the necessary steps to prepare the CAN-TestBed environment. You will first configure the physical connections for the microcontrollers, followed by installing the required backend (Python) and frontend (Node.js) software.

**Quick Links:**
* [Hardware Setup](#hardware-setup)
* [Software Setup](#software-setup)
  * [CAN Testbed Startup Automation](#can-testbed-startup-automation)
* [Troubleshooting](#troubleshooting)

---

## Hardware Setup
To run the testbed, you require the following components:
* (1x) CANable adapter.
* (9x) Longan Labs RP2040 Development Boards
* (9x) Micro USB Cables 
* (1x) 10 Port Powered USB Hub 
* CAN Bus Wire 

> Note:
> Things to Consider when selecting these products above:
> 1. USB Cables: Use Micro USB cables that support both data transfer and power; "charging-only" cables are not suitable for serial communication.
> 2. USB Hub: Utilize a powered USB hub with an external power supply to reliably power all 10 boards simultaneously.
> 3. CAN Wiring: Use twisted pair wiring for CAN High and CAN Low (dedicated wire is best, but twisted pair from a CAT6 Ethernet cable works).
> 4. CANable Hardware: The open-source CANable board can be purchased from various sources; the exact model used here is not required.
> 5. Firmware: This project requires and utilizes the candleLight firmware, not the slcan option.


## Assembling the Components

### Board Preparation:

The CANBed Development boards come with several components that can be soldered on, including a D-Sub Connector, a 4-pin screw terminal, headers for the GPIO and SPI pins, connectors for the I2C and UART pins, and a switch for the 120Ω terminal resistor. The only component that is required for all 9 boards is the 4-pin screw terminal. At least one of the boards will need the switch for the 120Ω terminal resistor (this will be the last board in the loop). If you would like to use the GPIO pins to connect to external sensors or components, you may want to attach the GPIO headers.

### Attaching the 4-pin Screw Terminal:
1. Slide the screw terminal into the 4 holes on the edge of the board as shown.
2. Solder all 4 pins to the board. Do this for all 9 boards.
> Note: These will be used to connect all the boards to the CAN bus.

![Attaching 4-pin to CAN](4-pin_CAN.png)

### Attaching the 120Ω Terminal Resistor Switch:

> You only need to do this on one board.

1. Slide the switch into the 6 holes in the corner of the board as shown.
2. Solder all 6 pins to the board.
3. Slide the switch toward the edge of the board to enable the 120Ω terminal resistor.

> Note: CAN bus uses a 120Ω terminal resistor at each end to ensure signal integrity and proper operation of the network.

![Resistor Switch](Resistor_Switch.png)

### Connecting the Boards:

1. Open the screw terminals marked CANH and CANL on each board. These are the CAN High and CAN Low connections.
2. Connect all 9 boards in a chain, ensuring that the board with the switch is the last in the chain.

>Note: It is best to use two different colors of wire for the CAN High and CAN Low connections to ensure that they are not mixed up. The standard is to use yellow for CAN High and green for CAN Low.

3. Make sure all connections are tight.
4. Connect a Micro USB cable from each board to the USB hub
5. Plug in the USB Hub's power adapter
6. Connect the USB Hub's USB cable to your computer

![Boards](9-boards.png)

### Connecting the CANable Adapter:

1. Open the screw terminals marked CANH and CANL on the CANable adapter and the first board in the chain.
2. Connect the CANable CANH and CANL terminals to the board's CANH and CANL terminals.
3. Make sure the connection is tight.
4. Plug the CANable adapter into the USB hub
5. Push the "R120" switch down to enable the 120Ω resistor
> Note: It might be more convenient to use a USB extension cable to connect the CANable adapter to the USB hub

**The Complete setup should look like this:**

![diagram](system_diagram.png)

## Software Setup

### 1. Update Your System
Make sure your software is up-to-date by running:

```
sudo apt update -y && sudo apt upgrade -y
sudo mkdir TestBED
```

### 2. Getting the Repository
Clone the CAN TestBed repository:

```
sudo git clone https://github.com/trevormcclellan/CAN-TestBed
```

### 3. Preparing Installation
Check if Python 3 is installed:

```
python3 -v
```

#### 3.1 Navigate to the Backend directory:

Install Pip (if not installed):

```
sudo apt install python3-pip -y
```

#### 3.2 Install Python dependencies:

```
sudo pip install -r requirements.txt
```

> If you get an error, bypass the safety warning::

```
sudo pip install -r requirements.txt --break-system-packages
```


### Side Note — Flask Module Issues
If you get an error saying flask modules are missing, uninstall Flask:

```
sudo pip uninstall flask
```

or

```
pip uninstall flask
``` 
Then install the required modules manually:

```
pip install Flask --break-system-packages
pip install Flask_cors --break-system-packages
pip install Flask_socketio --break-system-packages
pip install can --break-system-packages
```
### 4. Run the Backend
Start the backend with:
```
python3 backend.py
```

### 5. Preparing the Web Dashboard (Frontend)

#### 5.1 Install npm
Navigate to the CAN-Frontend directory:

```
cd ../CAN-Frontend
```

Install npm:

```
sudo apt install npm
```

Install frontend packages:

```
sudo npm install
sudo npm audit fix

```
Run the frontend:

```
sudo npm run dev

```

> Note About VITE Issues:
If you encounter Vite-related errors, install newer versions of Python and Node.js.

## CAN Testbed Startup Automation

> ⚠️ IMPORTANT NOTE: Raspberry Pi 5 Specific Configuration
This documentation and the subsequent configuration review are based on the specific hardware and operating environment currently deployed on the Raspberry Pi 5 machine. The file paths and user environment settings (like $HOME/.config/autostart) are tailored for this particular setup and may require modification for other Linux distributions or Raspberry Pi models.


The provided configuration successfully automates three key components upon system boot and user login:

### 1. Chrome Kiosk Auto-Launch (GUI Autostart)
The following file is located at:

```
~/.config/autostart/can-frontend.desktop

```

can-frontend.desktop

```
[Desktop Entry]
Type=Application
Name=CAN Frontend Auto Browser
Exec=/usr/bin/chromium --kiosk --start-fullscreen --noerrdialogs --disable-infobars --disable-session-crashed-bubble http://localhost:5173
X-GNOME-Autostart-enabled=true
Terminal=false

```
**Explanation**
| Key                                   | Meaning                                                                                   |
|---------------------------------------|-------------------------------------------------------------------------------------------|
| `[Desktop Entry]`                     | Tells GNOME this is a standard application launcher.                                      |
| `Type=Application`                    | Indicates this will launch a normal application at login.                                 |
| `Name=CAN Frontend Auto Browser`      | The name that appears in GNOME Startup Applications.                                      |
| `Exec=…`                              | The command executed at login.                                                             |
| `--kiosk`                             | Launches Chromium in full locked-down kiosk mode.                                          |
| `--start-fullscreen`                  | Forces fullscreen even if kiosk mode is bypassed.                                          |
| `--noerrdialogs`                      | Prevents Chromium error popup windows.                                                     |
| `--disable-infobars`                  | Removes automation banners (“Controlled by automated software”).                          |
| `--disable-session-crashed-bubble`    | Suppresses “Restore pages?” message.                                                       |
| `http://localhost:5173`               | The frontend served locally by the dev server.                                             |
| `X-GNOME-Autostart-enabled=true`      | Automatically runs on login.                                                               |
| `Terminal=false`                      | Runs without opening a terminal window.                                                    |

This ensures the Raspberry Pi immediately opens the CAN-Frontend UI in a locked kiosk mode upon boot.

### 2. Frontend Automation (Systemd Service)
Systemd service file located at:

```
/etc/systemd/system/can-frontend.service

```

can-frontend.service

```
[Unit]
Description=CAN Testbed Frontend
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/can-bus/CAN-Testbed/CAN-Frontend
ExecStart=/usr/bin/env npm run dev
Restart=on-failure
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target

```

**Explanation**

| Section                  | Details                                                                      |
|--------------------------|-------------------------------------------------------------------------------|
| `After=network-online.target`   | Ensures the service starts only after the network is fully online.            |
| `Wants=network-online.target`   | Makes systemd attempt to start networking if it is not already active.       |
| `WorkingDirectory=…`            | Points to the location of the CAN Frontend project.                           |
| `ExecStart=…`                   | Runs `npm run dev` to start the Vite/Web server.                               |
| `Restart=on-failure`            | Auto-restarts the service if the process exits with an error.                 |
| `RestartSec=5`                  | Waits 5 seconds before attempting to restart.                                 |
| `User=root`                     | Runs the service as root (can be changed to `can-bus` for hardening).         |
| `WantedBy=multi-user.target`    | Enables the service to start automatically during normal multi-user boot.     |


### 3. Backend Automation (Systemd Service)
Systemd service file located at:

```
/etc/systemd/system/can-backend.service

```

can-backend.service

```
[Unit]
Description=CAN Testbed Backend
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/can-bus/CAN-Testbed/Backend
ExecStart=/usr/bin/python3 backend.py
Restart=on-failure
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target

```
**Explanation**

| Key                           | Meaning                                                                                   |
|-------------------------------|-------------------------------------------------------------------------------------------|
| `After=network-online.target` | Backend starts only after the network is confirmed online.                                |
| `WorkingDirectory`            | Points to the backend Python folder.                                                      |
| `ExecStart`                   | Runs `backend.py` using the system Python3 interpreter.                                   |
| `Restart` & `RestartSec`      | Ensures the service automatically restarts after a failure.                               |
| `User=root`                   | Runs with elevated privileges (CAN interfaces or hardware access may require root).       |
| `WantedBy=multi-user.target`  | Enables automatic startup during the normal multi-user boot process.                      |

### 4. Operational Notes
**Open a terminal**

`Ctrl + Alt + T`

**Exit Kiosk Mode (Chromium)**
1. Switch to TTY1
   `Ctrl + Alt + F1 `

2. Login:
   `Username: can-bus` `Password: Cargovr00m`

3. Kill Chromium:
   `killall chromium`

4. Return to GUI: `Ctrl + Alt + F7`

### 5. Check Service Status
**Frontend**
```
sudo systemctl status can-frontend.service
```

**Backend**
```
sudo systemctl status can-backend.service
```

### 6. Enable Services on Boot (if not already enabled)

```
sudo systemctl enable can-frontend.service
sudo systemctl enable can-backend.service
```

### 7. Start / Restart Manually

```
sudo systemctl restart can-frontend.service
sudo systemctl restart can-backend.service

```

## Troubleshooting

### Issue: Raspberry Pi 5 HDMI Output Fails After Boot
Symptom:

- Boot screen appears

- Once OS loads, display goes black

- Display returns only after switching HDMI ports

This happened because the Raspberry Pi attempted to auto-detect EDID and disabled HDMI when the monitor was slow to respond.

**Fix: Force HDMI Port 1 Always On**
Edit the file: `/boot/firmware/cmdline.txt`

/boot/firmware/cmdline.txt
```
video=HDMI-A-1:e

```

What this does

- Forces HDMI port 1 to stay enabled even without EDID

- Prevents the Pi from disabling HDMI during cold boot

- Stops the issue where video is lost after the OS loads

- Eliminates the need to physically switch HDMI cables

This has been confirmed to resolve the display dropout problem on Raspberry Pi 5.

### Issue: On kiosk display, scrollbars appeared due to screen resolution mismatch.

Fix:
Add the following CSS inside <head> of: `CAN-Testbed/CAN-Frontend/index.html`

CSS: Hide scrollbars
```
<head>
  <style>
    html, body {
      overflow-y: scroll;
      overflow-x: hidden;
      height: 100vh;
    }

    ::-webkit-scrollbar {
      width: 0;
      height: 0;
    }
  </style>
</head>

```
What this does

- Removes visible scrollbars in Chromium kiosk mode

- Prevents users from seeing unnecessary UI elements

- Creates a cleaner, full-screen interface
