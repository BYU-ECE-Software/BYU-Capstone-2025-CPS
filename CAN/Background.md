## 💡 General Information

### What is a CAN Bus System

The Controller Area Network (CAN) bus is a communication system that lets multiple electronic components, called Electronic Control Units (ECUs), talk to each other inside vehicles or machines. It was developed by Bosch in the 1980s to reduce the number of wires in cars and to make communication between systems more efficient and reliable.

Before CAN, each device needs a direct connection to others, creating large, heavy wiring harnesses. CAN replaced this with a shared digital network, where all devices connect to the same two wires and exchange messages.

Today, CAN is used not just in cars but also in trucks, airplanes, factory equipment, medical devices, and robotics. Almost every modern vehicle relies on CAN to make the engine, brakes, airbags, and sensors communicate seamlessly.

### How a CAN Bus Works

CAN is like a group chat for machines. Every device on the network can send and receive messages, but only one can “talk” at a time. If two try to talk, the one with higher priority (lower ID number) continues while the other waits - preveting data collisions.

Communication happens over two wires:

* CAN_H (High)
* CAN_L (Low)

These carry opposite electrical signals (called differential signaling) to cancel out electrical noise and ensure reliable communication even in harsh environmets like an engine bay.

Each CAN message contains:

* **A Unique ID** (shows what the data represents and its priority)
* **A data field** (up to 8 bytes)
* **Error-checking bits** (to verify accuracy)

### Why the CAN Is Important ###

* **Efficiency:** Instead of hundreds of wires, a single network connects everything.
* **Reliability:** Built-in error detection and noise resistance.
* **Speed:** Data moves up to 1 megabit per second
* **Scalability:** More devices can be added without redesigning the system.
* **Real-time Communication:** Essential for safety-critical systems like braking or airbag deployments.

### Weaknesses in a CAN Bus ###

CAN wasn’t designed with cybersecurity in mind because it was created before modern, internet connected vehicles existed. As a result, there is little to ensure the confidentiality, integrity, and availability of data on the CAN bus. Here are some specific vulnerabilities:

* **No passwords or encryption:** Any connected device can read and send messages.

* **No identity checks:** A fake device can impersonate real one.

* **Physical access ponits:** Attackers can plug into ports (like the OBD-II diagnostic port) to send commands.

* **Replay and Denial-of-Service Attacks:** Attackers can flood or repeat data to disrupt normal operation.

Example: A malicious message could disable traction control or even killswitch the vehicle if the attacker understands the CAN IDs.

### What CAN IDs Do ###

Every message has a numeric identifier (ID) that defines:

* **Prority:** Lower ID = Higher Prority
* **Purpose:** Each ID corresponds to a specific function (e.g.; throttle position, wheel speed, or door lock status)
* **Readability:** Anyone with access to the network can see and send messages with these IDs, since they’re not encrypted.

### CAN ID Filters ###

To avoid overwhelming devices, ECUs use filters that decide which messages to accept.

* **Acceptance Filters:** Only messages with certain IDs are processed, others are ignored.
* **Hardware Filtering:** Filtering often happens on the chip itself to save CPU time.

**Advantages:**

* Improves performance by ignoring irrelevant data.
* Reduces exposure to spoofed or noisy messages.

**Limitations:**

* Filters are static and can’t delete fake messages using valid IDs.
* Still no built-in message authentication or encryption.

### Example: Reading a candump log ###

Developers and engineers ofter record CAN traffice for debugging. Example entry:

(12345.6789) can0 123#1122334455667788

**Meaning:**

* **(12345.6789):** Time since the log started (seconds)
* **can0:** CAN network interface name.
* **123:** Message ID (in hexadecimal)
* **1122334455667788:** Data payload (in hexadecimal bytes)

To interpret:

1. Identify what system uses ID 123 (e.g., engine control).
2. Decode the data (for example, bytes 3-4 might reprsent RPM)
3. Look for unusual values or timing patterns that suggest errors or tampering.

---

### Summary ###

The CAN bus is the nervous system of modern vehicles. It connects everything - from engine sensors to window controls - using a shared, efficient network. Understanding how it works is essential for mechanics, engineers, cybersecurity professionals, and consumers, especially as vehicles become increasingly connected and automated. While the CAN bus underpins nearly every critical vehicle function, traditional attacks against it generally require physical access to the vehicle’s internal network. However, in newer internet-connected vehicles, vulnerabilities in infotainment, telematics, or wireless interfaces can expose the CAN bus to remote attacks, dramatically raising the stakes and turning what was once a localized risk into a serious, large-scale cybersecurity threat.
