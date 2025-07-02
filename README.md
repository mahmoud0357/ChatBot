# 🧠💬 Querymancer by Mahmoud Khalid Alkodousy

An intelligent AI-powered assistant that **transforms natural language into optimized SQL queries** over your own **SQLite database** using **LangChain**, **LLMs**, and custom tools for smart exploration.

---

## 🚀 Features

- ✅ Translate natural language into SQL
- 📊 Automatic database exploration (list tables, sample rows, describe schema)
- 🧠 Multi-step reasoning with tool-based strategy
- 🛠️ Tool calls with transparent reasoning and context
- 🤖 Supports local (Ollama) and cloud-based (Groq/OpenRouter) LLMs
- 💾 Works on any SQLite database

---

## 🧠 How It Works

1. You ask a **natural language query** like:
   > *"What are the top 5 customers by balance?"*

2. The chatbot:
   - Lists available tables
   - Samples relevant ones
   - Describes schema
   - Constructs and executes **optimized SQL query**

3. You get the **exact result** — in a friendly, formatted Markdown response.

---

## 🧰 Tech Stack

- **Python**
- **LangChain**
- **LLMs** (Groq / Ollama / OpenRouter)
- **SQLite**
- **Rich** (for logging + visuals)

---

## 🛠️ Tools Used in Reasoning

| Tool           | Description                                        |
|----------------|----------------------------------------------------|
| `list_tables`  | Get all non-system tables                         |
| `sample_table` | View sample rows from any table                   |
| `describe_table` | Get column types and constraints of a table     |
| `execute_sql`  | Run the final constructed SQL query               |

Each tool call includes **strategic reasoning** and is fully traceable.

---

## 🧾 Prompt Engineering

Built-in **system prompt** that sets the agent behavior:

> 🎯 Act like a senior DB engineer.
>
> 🧠 Think strategically.
>
> 📉 Optimize before executing.
>
> 🔎 Always explain reasoning behind tool use.

---

## 📁 Project Structure

```bash
querymancer/
│
├── core.py               # Main logic (ask, loop, validation)
├── tools.py              # Custom tool functions (list, describe, sample, execute)
├── config.py             # Model config + path setup
├── logging.py            # Rich logging for terminal
├── llm.py                # Loads LLM (Groq, Ollama, etc.)
├── data/
│   └── banking.sqlite    # Sample SQLite database (replaceable)
└── README.md
