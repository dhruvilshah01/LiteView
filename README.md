# LiteView

LiteView is a terminal-based SQLite client (TUI) designed for developers to quickly view tables, write queries, and analyze query execution plans without leaving the terminal.

---

## Features

- **Table Tree**: View database schemas and tables in a navigable tree.  
- **Query Area**: Write and execute SQL queries.  
- **Query Results**: View results of `SELECT` queries directly in the terminal. Results will not be paginated if < 100 or if the LIMIT keyword is used.
- **Commit / Rollback**: For queries that modify data (`INSERT`, `UPDATE`, `DELETE`), you can choose to commit or rollback.  
- **Query Analyzer**: Analyze queries and view execution plans, with the option to export the plan to a `.txt` file.  

---

## Requirements

- Python 3.8+
- [UV](https://uv.run/) for project management and dependency installation
- SQLite (any version supported by Python)

---

## Installation

1. Clone the repository:

```bash
git clone <ssh|https repository_url>
cd LiteView
```

## Running the Project

To run the project - ```code python src/main.py [sqlite db path]```. If you pass in a path that is not valid, it will create the file for you.

## Future Development

- **View and Index Support**: Browse database views and indexes in the table tree alongside tables.
- **In-Table Updates**: Edit table rows directly from the TUI, with commit/rollback support.
- **Database Adapters**: Support for additional database engines beyond SQLite (PostgreSQL, MySQL, etc.).
- **Enhanced Query Analyzer**: More detailed query plan visualizations and performance metrics.
- **Export Options**: Ability to export table data, query results, and execution plans to CSV or JSON files.
- **Custom Themes & Configurations**: User-configurable UI themes and settings for improved workflow.




