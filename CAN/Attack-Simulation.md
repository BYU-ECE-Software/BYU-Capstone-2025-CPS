# Running Attack Simulations
The following sections are step by step instructions on how to perform certain attacks on a CAN Bus network. These instructions assume that you are working on the simulator this capstone team built. If you have not yet constructed the simulator, follow the instructions in [Initial-Setup](Initial-Setup.md) first.

This first step in either attack, is to choose a board to act as your attacking board.

## Message Injection/Spoofing
1. Find your attacking board in the web interface.
2. Click on its "Configure Injection" button.
3. Input the message you want to inject into the "Message" field.
>The message should follow the format ID#Message with the ID being the CANID of the intended recipient of the message. Everything should be in hexadecimal.
4. Enter the number of times you'd like to repeat the message into the "Repeat" field.
>If you are attempting to attack the physical speedometer on the 2017 Hyundai Dashboard included with the simulator, you must repeat this message a large number of times in order to see the effect.
5. Input the interval at which you'd like the messages to be sent into the "Interval" field.
>Again, if attacking the speedometer, this must be a relatively small interval to have a consistent effect.
6. Enter how many miliseconds you want the attacking board to wait before beginning the attack into the "Start Time" field.
7. Click "Configure" to save your changes.
8. Start the simulation. You should see your injected messages in the log upon completion of the simulation.

## Denial of Service
The DOS attack is unique in the fact that it is not configured using the web interface. You must instead flash your chosen attacker board with DOS firmware. If you are working on a newly constructed simulator, you can follow these instructions to flash a board with DOS firmware:

***Need to add steps to obtain the DOS firmware here. Perhaps just copy paste the code from Trevor's stuff. Then put a link to the part of Initial-Setup.md that goes over how to flash boards.***

Once you have a board flashed with the DOS firmware, a DOS attack is as simple as powering on the attacking board during the simulation. When the board is powered on, the network is flooded, preventing any expected messages from coming through. You can only see this during a simulation if you have some kind of physical output devices connected to the bus, like the 2017 Hyundai Sonata dashboard included in the capstone team's simulator. On the dashboard, all lights and funcitonality will immediately shut off upon activation of the DOS attacker board. You can power the attacking board on and off to see how the dashboard immediately reacts to the influence of the attacker.

>If you do not have any physical output devices connected to the network, you can still see the effects of the DOS attack by viewing the messages recieved on each board after the simulation completes. You should see blocks of missing messages that correspond to whenever the attacking board was powered on.
