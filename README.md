# LeseKobold 

Intelligent Reading Text Processing and Analysis for Children

**LeseKobold** is an agentic Python application for generating accesible reading texts intended for children. 
It generates graded readers for children in preschool and up to early secondary school.
It was developed to generate texts in German.

## Features

- **Story Specification and Structuring:**  
  Extracts and classifies user requirements, structuring them for the generation of age-appropriate stories.
- **Readability Analysis:**  
  Calculates LIX scores, translates them into grade levels, and helps find suitable text difficulty (see e.g. `src/readability_utils.py`).
- **Wordlists:**  
  Offers curated wordlists for different grades to support vocabulary analysis and educational purposes.
- **Prompt-based Preprocessing:**  
  Well-defined prompts for extracting and structuring requirements from user text input.
- **Unit Testing:**  
  A comprehensive suite of tests.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:LeseKobold/lese_kobold.git
   cd lesekobold
   ```
2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```
   (Requires Python 3.13+. Make sure you have [Poetry](https://python-poetry.org/) installed.)

---

## Project Structure

```
lesekobold/
├── resources/
│   ├── prompts/
│   ├── stories/
│   └── wordlists/
├── src/
│   ├── config.py
│   ├── dataclasses/
│   ├── agent_manager.py
│   ├── app.py
│   ├── prompt_reader.py
│   └── readability_utils.py
├── tests/
│   └── unit_tests/
└── README.md
```

