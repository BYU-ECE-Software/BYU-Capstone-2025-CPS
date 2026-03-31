# Lab 2: Read and Interpret Basic Authorized Badge Data
**Authorized Use Only**

## Objective
Use safe, non-destructive identification commands to understand how badge data is represented and documented in an authorized environment.

## Learning Outcomes
By the end of this lab, students should be able to:
- Explain what a facility code is
- Explain what a card number is
- Understand what hexadecimal output represents
- Document card data in a responsible and repeatable way

## Prerequisites
- Completion of Lab 1
- A lab-owned LF or HF credential
- Permission to inspect the card

## Background

### What is a Facility Code?
A **facility code** is typically a value used to identify a specific site, organization, or system grouping within a badge format.

### What is a Card Number?
A **card number** is the unique identifier assigned to an individual credential within that badge format.

### What is Hex?
**Hex** (hexadecimal) is a base-16 way of representing data.

Why this matters:
- Badge tools often display raw data in hex
- Hex makes binary data easier to read and record
- Some outputs may need to be decoded into human-readable fields

## Procedure

### Step 1: Confirm the card frequency
Use the results from Lab 1 to confirm whether the card is LF or HF.

### Step 2: Search for the exact type of card
Use the appropriate command:

For low frequency:
```bash
lf search
```

For high frequency:
```bash
hf search
```

### Step 3: Review the output
Look for:
- Technology family
- UID or identifier
- Raw hex values
- Any decoded fields shown by the tool

### Step 4: Record your observations
Document:
- Card frequency
- Search results
- Whether the card exposed a UID, hex output, or decoded fields
- Whether the output referenced a facility code or card number

## Interpretation Guidance
When reviewing results, ask:
- Is the output raw hex, decoded data, or both?
- Is the card presenting a simple identifier or a structured credential format?
- Does the card appear to belong to a legacy access system or a modern smart-card deployment?

## Example Documentation Template
```text
Card ID:
Frequency:
Search Command Used:
Likely Technology:
UID Present: Yes / No
Hex Output Present: Yes / No
Decoded Fields Present: Yes / No
Facility Code Present: Yes / No
Card Number Present: Yes / No
Notes:
```

## Check for Understanding
1. What is the difference between a facility code and a card number?
2. Why does badge tooling often display raw data in hex?
3. Did the card expose only an identifier, or did it show structured badge information?
4. Why is it important to document findings without modifying the credential?
