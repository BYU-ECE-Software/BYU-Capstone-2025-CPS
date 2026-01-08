# CAN-TestBed

The CAN-TestBed is a hands-on tool designed to teach car network security. It connects real hardware to a web app, effectively creating a "virtual car" on your desk. 

This tool allows students and researchers to replay real-life CAN traffic logs (`candumps`), configure ID filtering, and perform security assessments by simulating attacks like ID spoofing and Denial of Service (DoS) in a safe, controlled environment.

## Documentation Pages

| Page | Description |
| :--- | :--- |
| [Background](Background.md) | Introduction to CAN Bus, its various components, vulnerabilities. |
| [Initial Setup](Initial-Setup.md) | Step-by-step guide for setting up the hardware (RP2040, CANable) and installing the required software (Python Backend, Node.js Frontend). |
| [Using the TestBed](Using-the-TestBed.md) | Instructions on connecting devices to the web dashboard, identifying boards, loading `candump` logs, and running normal traffic simulations. |
| [Attack Simulation](Attack-Simulation.md) | Detailed procedures for executing real-time attacks using the injection panel, specifically covering Denial of Service (DoS) and ID Spoofing. |
| [Student Lab](Student-Labs.md) | Educational exercises focused on learning how the CAN bus works and how to execute basic attacks on it. |
