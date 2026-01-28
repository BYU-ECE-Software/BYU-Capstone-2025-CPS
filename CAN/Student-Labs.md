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

[Need to Upload Photo of our lab](CAN/Using-the-TestBed.md#Uploading-a-CANdump)

## Objective 2

Part 1
[instructions for uploading the test.log file to the web app here]()

Now run the simulation to confirm everything is set up and operating correctly. You’ll know everything is running properly if the dashboard lights up during the simulation and if each board has received all of the expected messages (indicated by a checkmark).

As you’ve just seen, CAN bus messages are not encrypted, which makes it very easy to inject our own. Using the IDs and data fields you identified during the setup phase, you will now configure a board to inject messages into the network.

Run the simulation again.

Did anything behave differently during the simulation?

Do you see the messages you configured coming through? Provide a picture showing the injected messages that were received as your answer to this question.

Part 2
Now, you will inject a specially crafted message to attack a specific ECU: the speedometer.

To do this, you need to understand that a car’s speed is calculated from the wheels’ speed. The sensors that measure wheel speed are a part of the car’s Anti-lock Braking System (ABS). The ABS is one of the many ECUs in the car’s CAN network, and it regularly broadcasts this speed data on the CAN bus. If we can reverse engineer how these broadcast messages work, we can spoof our own messages to influence any ECUs that listen to ABS data.
