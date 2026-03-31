# Lab Website Design

**Date:** 2026-03-25

## Overview

A static multi-lab website hosted on Apache/Ubuntu. Users read a markdown-rendered lab, take a short quiz, then navigate to the next lab. Fully stateless — no auth, no persistence beyond page refresh.

## File Structure

```
/var/www/html/
├── index.html
├── labs/
│   ├── config.json          # ordered list of labs
│   ├── lab1/
│   │   ├── content.md
│   │   └── questions.json
│   ├── lab2/
│   │   ├── content.md
│   │   └── questions.json
```

## User Flow

1. Page loads → fetches `labs/config.json` → loads first lab
2. Lab markdown rendered in main content area
3. "Start Quiz" button at bottom of lab content
4. Quiz renders all questions for the lab
5. User submits → inline correct/incorrect feedback shown per question
6. "Next Lab →" button navigates to next lab (wraps to first on last lab)

## Question Types (questions.json)

```json
[
  { "type": "multiple-choice", "question": "...", "options": ["A","B","C","D"], "correct": 0 },
  { "type": "true-false",      "question": "...", "correct": true },
  { "type": "short-answer",    "question": "...", "correct": "exact answer" }
]
```

## Styling

- BYU Navy `#002E5D` for header/nav, white content area
- Clean readable typography, mobile-friendly
- Marked.js (CDN) for markdown rendering

## Constraints

- No backend, no auth, no localStorage — pure stateless
- Works with Apache serving static files
- No build step required
