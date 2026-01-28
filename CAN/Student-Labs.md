# CAN Bus Hacking Lab

## Learning Objectives
- Understand the CAN bus and the function it performs in a vehicle.

- Demonstrate how to physically modify user-crafted messages to target specific car systems.

- Demonstrate the use of false, high-priority messages to disrupt board functions.

- Learn how to mitigate the risk of CAN bus attacks.

## SETUP

[Inital Setup](Initial-Setup.md)

**NOTE:** These instructions are for Professors or TAs to initially configure the lab environment.
These steps should have already been accomplished for any students starting the lab. If you are
a student, begin with Objective 1.

## Objective 1

The Controller Area Network (CAN) bus is a communication system that vehicles use to coordinate and share information between key components. The CAN bus links important systems together such as the dashboard, brakes, engine, headlights, and infotainment system. Like any other network of devices, the CAN bus can be hacked and disrupted. To attack and defend a CAN bus, you must first understand how it works.

Read the following article and answer the questions to show your understanding: https://www.csselectronics.com/pages/can-bus-simple-intro-tutorial

1. What does the acronym “CAN” stand for, and what is the primary role of a CAN bus in a vehicle or machine?

2. Describe the physical wiring of a typical CAN network—what kind of cable is used and how are the two wires named/colored (according to the article)?

3. What are the “Top 4 benefits” of using a CAN bus network, and how does each one specifically improve real-world automotive or industrial systems?

4. In the context of the seven-layer OSI model, which layers does CAN cover?

5. What is a standard CAN data frame (11-bit identifier) made up of? Name the fields and briefly state what they do.

6. Explain how arbitration works on a CAN bus (i.e., when two nodes attempt to transmit at once).

**Check out this YouTube video that shows CAN bus attacks in real time! (3:06 and on specifically talks about the CAN Bus): https://youtu.be/MK0SrxBC1xs**


## Our CAN bus lab configuration
In the photo below, you can see an example configuration of this CAN bus lab. Each Printed Circuit Board (PCB) represents a distinct Electronic Control Unit (ECU) in a given car. An ECU acts as a small computer that controls a specific automotive system, while the PCB provides the physical mounting and electrical connections for its components. For example, one of the boards could be the brakes ECU, one could be the engine ECU, and so on. The dashboard itself acts as several ECUs in one, receiving and transmitting for several different systems.

[Need to Upload Photo of our lab]

## Objective 2

Part 1

[Instructions for uploading the test.log file](Using-the-TestBed.md#uploading-a-candump) **Look at Section:Uploading a CANdump**

Now run the simulation to confirm everything is set up and operating correctly. You’ll know everything is running properly if the dashboard lights up during the simulation and if each board has received all of the expected messages (indicated by a checkmark).

As you’ve just seen, CAN bus messages are not encrypted, which makes it very easy to inject our own. Using the IDs and data fields you identified during the setup phase, you will now configure a board to inject messages into the network.

Run the simulation again.

Did anything behave differently during the simulation?

Do you see the messages you configured coming through? Provide a picture showing the injected messages that were received as your answer to this question.

### Part 2
Now, you will inject a specially crafted message to attack a specific ECU: the speedometer.

To do this, you need to understand that a car’s speed is calculated from the wheels’ speed. The sensors that measure wheel speed are a part of the car’s Anti-lock Braking System (ABS). The ABS is one of the many ECUs in the car’s CAN network, and it regularly broadcasts this speed data on the CAN bus. If we can reverse engineer how these broadcast messages work, we can spoof our own messages to influence any ECUs that listen to ABS data.

#### Understanding the Parts of a CAN Message
> A few key things to keep in mind as you go through these lines of the DBC:  

> - The DBC is designed to be human-readable, so everything is in decimal 

> - Actual CAN frames will be in hex, not decimal 

> - This DBC shows that speeds on the CAN bus are sent in km/h, so remember to convert to and from mph. 

> - We only care about the first 5 lines of this entry. The last for are for data validation, which we don’t care about in our attack. 

> - You’ll execute this attack in the same way as the injection you performed in Part 1. This time however, your message will be curated to affect the speedometer. This means **you must use the correct CAN ID and message.**

The image below shows the entry in the DBC file for the ABS of a Hyundai Sonata. This entry
breaks down the parts of an ABS CAN frame.

<img width="840" height="229" alt="image" src="https://github.com/user-attachments/assets/1cadf146-d029-4f97-ae57-9c4fb7e1e503" />

Line 1 gives us the CAN ID, 902. 

Lines 2-5 dictate the way wheel speeds are encoded into the CAN frame. 

Lines 5-9 show how checksums/data validation is included in the frame. 

See the image below for a breakdown of what’s contained in line 2 (3-5 will be the same):

<img width="720" height="124" alt="image" src="https://github.com/user-attachments/assets/40c40e39-b5ce-466e-8491-1691fc1cba03" />

Now apply this to an actual CAN frame. 

### 🔎 Example Analysis: Speed Data Frame

Let’s break down the following CAN frame as an example:

386#0D090D090D090D09

1. Data Structure Every four hex digits represent the current speed of one wheel. In this frame, 0D09 is repeated four times, meaning all four wheels are traveling at the exact same speed. 

To figure out what speed this frame is reporting, we should convert 0D09 into mph using the information from the DBC file. 

To start, remember that the DBC file says this is using little endian. So, to account for that we should rearrange the hex to 090D. 

Normally we would need to convert to binary to mask out the checksum bits, but that won’t be necessary for this example. So, we can just convert straight to decimal: 2,317 

We then multiply by the scaling factor to get our speed (0.03125 * 2,317) = 72.41 

Remember that this is in km/h, so we need to convert to mph. (72.41 * 0.621371) = 44.99 

So, we see that the CAN frame, 386#0D090D090D090D09, indicates that the car is traveling at a speed of 45mph. 

To create a false frame, just repeat these steps in reverse: 

1. Choose target speed in mph 

2. Convert to km/h 

3. Divide by scaling factor 

4. Convert to hex 

5. Convert to little endian 

6. Format like a CAN frame 

Now create a CAN frame that indicates a speed of 160 mph and configure an injection using the web app to trick the speedometer into hitting 160 for a few seconds. Provide your CAN frame and capture a picture of the speedometer as proof. 

Should see something like 386#2F202F202F202F20 or 386#8020802080208020 (remove this, this is a note for professors/TAs only) 
