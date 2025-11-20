# CAN-TestBed

The CAN-TestBed is a hands-on tool designed to teach car network security. It connects real hardware to a web dashboard, effectively creating a "virtual car" on your desk. 

This tool allows students and researchers to replay authentic CAN traffic logs (`candump`), configure hardware-level ID filtering, and perform real-time security assessments by simulating attacks like ID spoofing and Denial of Service (DoS) in a safe, controlled environment.

## Documentation Pages

| Page | Description |
| :--- | :--- |
| [Initial Setup](docs/Initial-Setup.md) | Step-by-step guide for setting up the hardware (RP2040, CANable) and installing the required software (Python Backend, Node.js Frontend). |
| [Using the TestBed](docs/Using-the-TestBed.md) | Instructions on connecting devices to the web dashboard, identifying boards, loading `candump` logs, and running normal traffic simulations. |
| [Attack Simulation](docs/Attack-Simulation.md) | Detailed procedures for executing real-time attacks using the injection panel, specifically covering Denial of Service (DoS) and ID Spoofing. |
| [Student Labs](docs/Student-Labs.md) | Educational exercises focused on modifying ECU firmware to implement security mitigations, such as message authentication and encryption. |
