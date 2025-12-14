# rpt-app
RPT app para Aranda de Duero

## Overview

This application manages the RPT (Relación de Puestos de Trabajo - Job Position Register) for the municipality of Aranda de Duero.

## Features

### Valoración System

The application includes a comprehensive valuation system for job positions based on five factors (A, B, C, D, E). Each factor has five levels with associated scores ranging from 0 to 400 points.

For detailed documentation, see [VALORACION_FACTORS.md](VALORACION_FACTORS.md)

## Database Schema

The database schema includes:
- **5 Factor Tables**: Valoracion_Factor_A through Valoracion_Factor_E
- **RPT Main Table**: Stores job positions with links to valuation levels
- **Complete View**: Automatically calculates total scores for positions

For a visual representation of the schema, see [SCHEMA_DIAGRAM.md](SCHEMA_DIAGRAM.md)

### Quick Start

```bash
# Initialize the database
sqlite3 rpt_database.db < schema.sql

# Load sample data
sqlite3 rpt_database.db < sample_data.sql

# Query positions with scores
sqlite3 rpt_database.db "SELECT * FROM RPT_View_Complete;"
```

## Files

- `schema.sql`: Database schema definition
- `sample_data.sql`: Sample data for testing
- `VALORACION_FACTORS.md`: Detailed documentation of the valuation system

## License

See [LICENSE](LICENSE) file for details.
