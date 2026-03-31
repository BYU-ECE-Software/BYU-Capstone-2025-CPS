# Lab 1: Identify What Frequency a Card Uses
**Authorized Use Only**

## Objective
Determine whether a sample credential is **low frequency (LF)** or **high frequency (HF)** and record the likely technology family.

## Learning Outcomes
By the end of this lab, students should be able to:
- Explain the difference between LF and HF RFID credentials
- Use Proxmark in a basic identification workflow
- Record findings in a repeatable way

## Prerequisites
- VM with Kali Linux
- Proxmark software installed
- USB 2.0+ port or adapter
- Proxmark-compatible hardware
- A small set of **lab-owned** RFID credentials
- Permission to test

## Background

### What types of frequencies can a card use?

#### Low Frequency (LF)
Low-frequency RFID cards are commonly associated with **125 kHz** systems.

Typical traits of LF cards:
- Often used in older physical access control systems
- Common in legacy proximity badge deployments
- Usually simpler than modern smart cards
- Often store more limited data structures
- Frequently used for building entry and basic badge systems

#### High Frequency (HF)
High-frequency RFID cards are commonly associated with **13.56 MHz** systems.

Typical traits of HF cards:
- Common in smart card and NFC-based systems
- Often support richer protocols and more advanced features
- May support more secure authentication depending on the card family
- Common in newer enterprise badge systems
- May be used for both physical access and logical access

#### Summary of the Differences
| Feature | Low Frequency (LF) | High Frequency (HF) |
|---|---|---|
| Common Frequency | 125 kHz | 13.56 MHz |
| Typical Use Case | Legacy proximity access | Smart cards, modern access systems |
| Complexity | Simpler | More advanced |
| Common Security Level | Often lower | Often higher, depending on implementation |
| Common Examples | Legacy prox cards | MIFARE, DESFire, Seos, NFC-like systems |

## Ways to Identify What Kind of Card It Is
There are multiple ways to identify a card:
- Vendor labeling
- Reader documentation
- Badge system documentation
- Testing with Proxmark

For this lab, you will use **Proxmark**.

## Procedure

### Step 1: Start the Proxmark client
```bash
pm3
```

### Step 2: Test for LF response
Place the credential on the **LF antenna area** and run:
```bash
lf tune
```

### Step 3: Test for HF response
Place the credential on the **HF antenna area** and run:
```bash
hf tune
```

> **Important:** Make sure you are touching the card to the correct antenna when testing.

### Step 4: Attempt to identify the technology family
If the card responds as LF, run:
```bash
lf search
```

If the card responds as HF, run:
```bash
hf search
```

## What to Record
For each credential, document:
- Card label or identifier
- Whether it responded as LF or HF
- Whether the search command identified a specific technology
- Any relevant notes about reader positioning or behavior

## Expected Results
At the end of this lab, students should be able to answer:
- Is the card LF or HF?
- Did the card appear to match a known card family?
- Does the card appear to be legacy or modern?

## Check for Understanding
1. What frequency did the card respond to?
2. Did `lf search` or `hf search` identify a likely card family?
3. Why is it useful to know whether a card is LF or HF?
4. How can this information help a security team assess badge-system risk?
