# Capstone Labs — Claude Context

## What this project is
A static multi-lab website for a BYU Capstone security course. Students read a markdown-rendered lab, take a per-question quiz, then navigate to the next lab. Fully stateless — no auth, no backend, no persistence beyond page refresh.

## Hosting
Intended to run on an Ubuntu machine with Apache serving static files from `/var/www/html/`. No build step, no Node, no server-side code. Can be tested locally with `./start.sh` (runs `python3 -m http.server 8080`).

## Stack
- Vanilla HTML/CSS/JS — single `index.html`
- `marked.js` from CDN for markdown rendering
- BYU branding: navy `#002E5D`, white, `BYU_Capstone.png` logo

## File structure
```
index.html              # entire app
start.sh                # local dev server
BYU_Capstone.png        # white logo, used in header + nav
labs/
  config.json           # ordered list of labs (id + title)
  lab1/
    content.md          # lab content in markdown
    questions.json      # quiz questions for this lab
  lab2/ ...
  lab3/ ...
  lab4/ ...
```

## Lab content
All four labs are about RFID/badge security (Proxmark, LF/HF cards, risk assessment, card handling). They are authorized-use-only training labs for physical security assessment.

- Lab 1: Identify card frequency (LF vs HF) using Proxmark
- Lab 2: Read and interpret badge data (facility codes, UIDs, hex)
- Lab 3: Defensive risk assessment of badge environments
- Lab 4: Card handling, procurement, and decommissioning

## Quiz behavior
- Each question has its own **Check** button
- Check shows only ✓ Correct / ✗ Incorrect — no answer revealed yet
- Once all questions are checked, score + **Reveal Correct Answers** button appear
- Reveal highlights correct/incorrect choices and shows correct answers for wrong short-answer questions
- Then **Next Lab →** appears

## Question types (questions.json)
```json
{ "type": "multiple-choice", "question": "...", "options": ["A","B","C","D"], "correct": 0 }
{ "type": "true-false",      "question": "...", "correct": true }
{ "type": "short-answer",    "question": "...", "correct": "exact string" }
```
Short-answer matching is case-insensitive, trimmed.

## User preferences
- No auth, no storage, stateless only
- BYU colors throughout
- Keep it simple — no frameworks, no build tools
