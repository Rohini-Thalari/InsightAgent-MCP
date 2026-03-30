# 🤖 AI Data Analyst — MCP Server

> An AI-powered data analysis server built on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) using **FastMCP**. Gives AI agents a rich, standardized toolset to connect to databases, explore schemas, execute secure SQL queries, profile data, generate interactive visualizations, and manage datasets — all through a single, consistent interface.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Adding to Claude Desktop](#-adding-to-claude-desktop)
- [MCP Tools Reference](#-mcp-tools-reference)
- [Supported Databases](#-supported-databases)
- [Security](#-security)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---|---|
| **Database Connectivity** | Connect to any SQLAlchemy-supported database — SQLite, PostgreSQL, MySQL, MSSQL, and more |
| **Schema Exploration** | Inspect tables, columns, primary keys, foreign keys, and indexes with a single tool call |
| **Secure SQL Execution** | Read-only query validation blocks all destructive operations before they reach the database |
| **Data Profiling** | Automated per-column statistics: null rates, unique counts, min/max, mean, and top values |
| **Smart Chart Generation** | Auto-detects the best chart type and aggregation; outputs interactive Plotly visualizations |
| **Dataset Upload** | Import CSV, Excel, and JSON files directly as fully queryable SQL tables |
| **Session Management** | Isolated, per-session database engines and caches keep concurrent analyses independent |
| **Caching** | 5-minute TTL in-memory cache for schemas, profiles, and analysis results |

---

## 🗂 Project Structure

```
ai-analyst/
├── server.py                    # FastMCP server entry point & tool registration
├── create_test_db.py            # Generates a sample SQLite e-commerce database
│
├── database/
│   ├── connection_manager.py    # SQLAlchemy connection management (singleton)
│   └── schema_loader.py         # Schema inspection & caching
│
├── datasets/
│   └── dataset_manager.py       # CSV / Excel / JSON upload & query engine
│
├── security/
│   └── sql_validator.py         # SQL whitelist validator (SELECT / WITH only)
│
├── tools/
│   ├── analyze_schema.py        # Schema relationship analysis tool
│   ├── connect_database.py      # Database connection tool
│   ├── dataset_tools.py         # Dataset upload / list / query tools
│   ├── generate_chart.py        # Chart generation tool
│   ├── get_schema.py            # Schema fetching tool
│   ├── get_schema2.py           # Schema fetching — plain-text format (optional)
│   ├── profile_table.py         # Data profiling tool
│   ├── run_query.py             # SQL query execution tool
│   ├── sample_rows.py           # Table row sampling tool
│   └── session_tools.py         # Session creation tool
│
├── utils/
│   ├── cache_manager.py         # In-memory TTL cache
│   ├── chart_utils.py           # Plotly chart creation & auto-detection
│   ├── data_profiler.py         # SQL / pandas data profiling engine
│   ├── generate_chart.py        # Chart generation wrapper
│   ├── schema_analyzer.py       # Relationship & index analysis
│   ├── session_manager.py       # UUID session management (singleton)
│   └── sql_generator.py         # LLM-based SQL generation
│
└── logs/                        # Runtime log files
```

---

## 🛠 Prerequisites

- **Python 3.11**

---

## 📦 Installation

**1. Clone the repository**

```bash
git clone <repo-url>
cd ai-analyst
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### (Optional) Generate the sample database

```bash
python create_test_db.py
```

Creates `sample_store.db` — a ready-to-query SQLite e-commerce database containing `customers`, `products`, `orders`, and `order_items` tables, preloaded with sample data.

### Start the MCP server

```bash
python server.py
```

---

## 🖥 Adding to Claude Desktop

1. Open **Claude Desktop** and go to **Settings → Developer**
2. Click **Edit Config** to open `claude_desktop_config.json`
3. Add the following entry inside `"mcpServers"`:

```json
"AI Data Analyst MCP Server": {
  "command": "<path-to-your-python>",
  "args": [
    "<path-to-project>/server.py"
  ],
  "env": {},
  "transport": "stdio"
}
```

## 🖥 Adding to your own chatbot

```python
SERVICES = {
  "AI Data Analyst MCP Server": {
  "command": "<path-to-your-python>",
  "args": [
    "<path-to-project>/server.py"
  ],
  "env": {},
  "transport": "stdio"
  }
}

```
In your chatbot code, initialize the client:
```python
from langchain_mcp_adapters.client import MultiServerMCPClient
client = MultiServerMCPClient (SERVERS)
```
Add in your chatbot's llm tools:
```python
tools = client.get_tools()
llm_with_tools = llm.bind_tools(tools)
```
Now your chatbot can call any of the MCP tools defined in `server.py`!

Replace the placeholder values:

| Placeholder | Example |
|---|---|
| `<path-to-your-python>` | `C:\Users\you\ai-analyst\venv\Scripts\python.exe` (Windows) or `/home/you/ai-analyst/venv/bin/python` (macOS/Linux) |
| `<path-to-project>` | `C:\Users\you\ai-analyst` or `/home/you/ai-analyst` |

4. **Save** the file and **restart** Claude Desktop.

---

## 🔧 MCP Tools Reference

| Tool | Description |
|---|---|
| `hello` | Health check — confirms the server is running |
| `create_session` | Creates a new isolated analysis session |
| `connect_database_tool` | Connects to a database using a SQLAlchemy URI |
| `get_schema` | Retrieves the table and column schema for the connected database |
| `sample_rows_tool` | Samples up to 50 rows from a specified table |
| `run_query_tool` | Executes a validated, read-only SQL query |
| `profile_table` | Generates column-level statistics for a table |
| `analyze_schema` | Detects table relationships, keys, and indexes |
| `generate_chart_tool` | Creates an interactive Plotly chart with automatic type detection |
| `upload_dataset` | Uploads a CSV, Excel, or JSON file as a queryable SQL table |
| `list_datasets` | Lists all datasets uploaded in the current session |
| `query_dataset` | Runs SQL against previously uploaded datasets |

---

## 🗄 Supported Databases

Connect to any SQLAlchemy-compatible database using a standard URI:

```bash
# SQLite
sqlite:///path/to/database.db

# PostgreSQL
postgresql://user:password@host:port/dbname

# MySQL
mysql://user:password@host:port/dbname

# Microsoft SQL Server
mssql+pyodbc://user:password@host/dbname?driver=ODBC+Driver+17+for+SQL+Server
```

---

## 🔒 Security

The server enforces strict read-only SQL execution to protect your data.

**Allowed statements**
- `SELECT`
- `WITH` (Common Table Expressions / CTEs)

**Blocked keywords**

`DROP` · `DELETE` · `UPDATE` · `ALTER` · `INSERT` · `TRUNCATE` · `MERGE` · `GRANT` · `REVOKE`

**Additional protections**
- Multi-statement queries (`;`-separated) are rejected outright
- Validation is case-insensitive and uses regex word boundaries to prevent bypass attempts

---

## 📄 License

This project is provided **as-is** for educational and research purposes.