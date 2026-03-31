# Developer Guide — Adding Labs

This site is a static website. No build step, no framework. To add or edit labs you only need a text editor.

---

## Running Locally

```bash
./start.sh
# then open http://localhost:8080
```

---

## Adding a New Lab

### 1. Create the lab folder

```bash
mkdir labs/lab5
```

### 2. Write the lab content

Create `labs/lab5/content.md` — standard markdown, no special syntax needed.

```markdown
# Lab 5: Your Lab Title
**Authorized Use Only**

## Objective
...

## Background
...

## Procedure
...
```

### 3. Write the quiz questions

Create `labs/lab5/questions.json` — a JSON array of question objects.

#### Multiple Choice
```json
{
  "type": "multiple-choice",
  "question": "What does X do?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct": 2
}
```
`correct` is the **zero-based index** of the right answer (0 = first option).

#### True / False
```json
{
  "type": "true-false",
  "question": "X is always true.",
  "correct": false
}
```

#### Short Answer
```json
{
  "type": "short-answer",
  "question": "What command starts the Proxmark client?",
  "correct": "pm3"
}
```
Matching is **case-insensitive** and **trimmed**, so `PM3`, `pm3`, and `  pm3  ` all count as correct.

---

### 4. Register the lab in config.json

Open `labs/config.json` and add your lab to the array **in the order you want it to appear**:

```json
{
  "labs": [
    { "id": "lab1", "title": "Lab 1: Identify What Frequency a Card Uses" },
    { "id": "lab2", "title": "Lab 2: Read and Interpret Basic Badge Data" },
    { "id": "lab3", "title": "Lab 3: Defensive Risk Assessment" },
    { "id": "lab4", "title": "Lab 4: Card Handling and Decommissioning" },
    { "id": "lab5", "title": "Lab 5: Your New Lab Title" }
  ]
}
```

The `id` must match the folder name exactly.

---

## Deploying to Apache (Ubuntu)

```bash
sudo cp -r /path/to/Capstone_labs/* /var/www/html/
```

Apache serves the static files with zero configuration. No `.htaccess` needed.

---

## Editing an Existing Lab

- **Change lab content** → edit `labs/labN/content.md`
- **Change questions** → edit `labs/labN/questions.json`
- **Reorder labs** → reorder entries in `labs/config.json`
- **Rename a lab title** → update the `title` field in `labs/config.json`

---

## Project Structure Reference

```
index.html              # entire app — routing, rendering, quiz engine
start.sh                # local dev server (python3 -m http.server 8080)
BYU_Capstone.png        # logo — white, used in header and nav
CLAUDE.md               # context file for Claude Code sessions
DEVELOPER_README.md     # this file
labs/
  config.json           # ordered lab list
  lab1/
    content.md
    questions.json
  lab2/ ...
docs/
  superpowers/specs/    # design documents
```

---

## Tips

- You can mix question types freely in a single `questions.json`
- Aim for 5–8 questions per lab — enough to test understanding without fatigue
- Short-answer questions work best for single-word or short-phrase answers (commands, numbers, proper nouns). Avoid them for answers that could be phrased multiple ways.
- The nav sidebar auto-populates from `config.json` — no HTML edits needed to add a lab
