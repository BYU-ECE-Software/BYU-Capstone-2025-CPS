# CAN-TestBed

The CAN Simulator is a hands-on tool designed to teach car network security. It connects real hardware to a web app, effectively creating a "virtual car" on your desk. 

This tool allows students and researchers to replay real-life CAN traffic logs (`candumps`), configure ID filtering, and perform security assessments by simulating attacks like ID spoofing and Denial of Service (DoS) in a safe, controlled environment.

One major contributor to this project is **Trevor McClellan**, who pioneered this particular Can-TestBed that the prototype was based on. Because of this, some of the documentation here is similar to, or quotes from, his [GitHub repo for his CAN-TestBed project](https://github.com/trevormcclellan/CAN-Testbed/wiki).

## Documentation Pages

| Page | Description |
| :--- | :--- |
| [Background](Background.md) | Introduction to CAN Bus, its various components, and its vulnerabilities. |
| [Initial Setup](Initial-Setup.md) | Step-by-step guide for setting up the hardware (RP2040, CANable) and installing the required software (Python Backend, Node.js Frontend). Start here if you are building from scratch. |
| [Using the TestBed](Using-the-TestBed.md) | Instructions on connecting devices to the web dashboard, identifying boards, loading `candump` logs, and running normal simulations. Start here if you already have a complete simulator. |
| [Attack Simulation](Attack-Simulation.md) | Detailed procedures for executing real-time attacks, specifically covering Denial of Service (DoS) and ID Spoofing. |
| [Student Lab](Student-Labs.md) | Educational exercises focused on learning how the CAN bus works and how to execute basic attacks on it. |
