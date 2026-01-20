# Using the Test Bed

These instructions will guide you through the basic setup and operation of the CAN Simulator.

>Note: These instructions assume that the CAN Simulator is fully put together and running out of its portable case.  <br><br>
If you are trying to build it from scratch or something is not working properly, ensure that the initial hardware and software setup instructions have been followed. You can find them in [Initial-Setup.md](Initial-Setup.md)


## Powering It On

When you first open the carrying case, it should look like this:

***insert picture here***

Make sure everything is plugged in like it is in the photo.

There is no power button for the Raspberry Pi, so to power it on and off just plug or unplug it's usb-c power cord.

Once powered, give the Pi a few minutes to boot up. The web app for the CAN Bus Simulator should pop up automatically.

***add note about troubleshooting power issues and/or auto setup issues like not recognizing screen***

## Configuring the Boards

***go over things like adding boards (might not be needed) and add troubleshooting notes for how to flash boards***

Make sure that all the boards (except the attacker board) are powered on. 
***Make sure to label DOS attacker board***

If all the boards are powered on, and the web app is started, you should see them on the homepage. Skip to [Uploading a CANdump](#uploading-a-candump).

If they don't show up, you'll need to connect the boards to the web app. To do this:

1. Power down all boards
2. Click on "Connect Device"
3. Power on a board
4. Click "Add Device"
5. A window should pop up asking which serial port to connect. There will most likely only be one port to choose from at this point, and it should be named "PicoArduino". If you only have one board connected, there will only be one option with this name. As you add more boards, you will see other options with different names. Select the port of the board you are connecting and click "Connect".

>Note: You can click the "Identify" button for any of the connected ports. This will blink the LED 6 times to indicate which board corresponds to that port.

6. Repeat steps 3-5 to connect and add the remaining boards, **one at a time**. You do not have to disconnect or power off boards once added. Previously added ports will show up as "Paired". When adding the next board, select the port that does not say "Paired". Give each board a unique name.

## Uploading a CANdump

If you haven't already, return to the homepage.

You should see a serial console for each connected and powered-on board. If you don't, follow the steps in the previous section, [Configuring the Boards](#configuring-the-boards).

Now upload a CANdump log file by clicking "Choose File". You should see your selected file's name next to the button upon a successful upload.

## Setting ID Filtering

Once you have successfully uploaded a log file, you can set ID filtering on each board's serial console. To do this, click the drop down menu on a board's serial console and select an ID. The list should contain only IDs that are found within your uploaded log. 

Some things to keep in mind:
 
* Each board supports filtering up to 6 different IDs at once.
* If you don't specify any ID for a board, that board will recieve *all* CAN messages.


After you make any changes to the ID filtering, press "Upload IDs to ECUs". **Don't forget to upload the IDs or your simulation will not show results.**


## Running a Simulation

After you've uploaded a log and set ID filters, you are good to run the simulation! You do that by clicking "Start Simulation". There isn't much of a visual indicator that a simulation is running, especially if the physical dashboard is not connected to the simulator. When a simulation is running, the "Start Simulation" button will instead read "Restart Simulation".

After the simulation has completed, each of the active board's serial consoles will update with a list of the messages they recieved. 
* These messages will have a checkmark icon if they were recieved as expected (✔️). 
* If an expected message was *not* recieved, then there will be no icon. 
* If an unexpected message is recieved (like if you injected an attack) then an exclamation icon will appear next to the unexpected messages (❗).

You've now learned the basic operation of the CAN Simulator! Next, you can learn to perform [CAN bus attacks](Attack-Simulation.md), or follow along with the [student lab](Student-Labs.md).

## Additional Troubleshooting Notes
