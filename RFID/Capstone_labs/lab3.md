# Lab 3: Defensive Risk Assessment of Badge Technology
**Authorized Use Only**

## Objective
Assess whether a badge environment is relying on older, lower-assurance credential technology and recommend safer future-state improvements.

## Learning Outcomes
By the end of this lab, students should be able to:
- Identify badge-system risk indicators
- Distinguish between legacy and more modern credential types
- Recommend practical hardening and migration steps

## Prerequisites
- Completion of Lab 1 and Lab 2
- Multiple lab-owned credentials or sample data
- Access to reader model information if available

## Background
Not all badge systems provide the same level of security.

Common risk themes include:
- Legacy LF proximity systems
- Readers that accept older technologies without stronger validation
- Environments that still depend on older badge formats for day-to-day access
- Lack of a migration plan to more secure smart credentials

## Procedure

### Step 1: Build a credential inventory
For each credential, document:
- LF, HF, or dual-technology
- Likely card family
- Known reader compatibility
- Whether it appears legacy or modern

### Step 2: Build a reader inventory
Document each reader:
- Reader model
- Supported frequencies
- Whether the reader accepts LF, HF, or both
- Whether legacy support appears enabled

### Step 3: Identify risk indicators
Mark the following if observed:
- Heavy reliance on 125 kHz legacy prox
- No modern smart-card deployment
- Dual-tech cards using legacy functionality in production
- No documented lifecycle or revocation process
- No migration path toward stronger credentials

### Step 4: Write recommendations
Possible recommendations:
- Reduce reliance on legacy LF prox
- Standardize on stronger HF smart-card technologies
- Replace readers that only support older formats
- Keep test credentials separate from production credentials
- Maintain clear issuance, revocation, and decommissioning procedures

## Deliverable
Write a one-page assessment memo with the following sections:
- Current State
- Identified Risks
- Immediate Remediation Recommendations
- Long-Term Migration Plan

## Example Risk Memo Template
```markdown
### Current State
The current badge environment appears to rely on the following credential types:
- 
- 

### Identified Risks
- 
- 
- 

### Immediate Remediation Recommendations
- 
- 
- 

### Long-Term Migration Plan
- 
- 
- 
```

## Check for Understanding
1. What signs indicate a badge environment may be relying on legacy technology?
2. Why is dual-tech support sometimes a risk during migration periods?
3. What short-term improvements can reduce exposure?
4. What long-term changes create a more secure badge environment?
