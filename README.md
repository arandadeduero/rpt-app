# RPT App - Relación de Puestos de Trabajo

RPT application for Aranda de Duero with AdminJS backend for managing work positions.

## Description

This application provides a complete backend system for managing "Relación de Puestos de Trabajo" (RPT - Work Position Registry) with an intuitive administrative interface powered by AdminJS.

## Features

- **Complete CRUD operations** for work positions (Puestos)
- **AdminJS interface** for easy data management
- **SQLite database** for simplicity and portability
- **Hierarchical structure** support (positions linked to superior positions)

### RPT Main Table (Puestos)

The core table includes the following fields:

**Identifiers:**
- `ID_Puesto`: Auto-incrementing primary key
- `Código_Interno`: Internal code (unique)
- `Número_Orden`: Order number

**Descriptive Fields:**
- `Denominación_Puesto`: Position name/title (required)
- `Descripción_Funciones`: Function description (text)
- `Observaciones`: Observations/notes (text)

**Quantitative Fields:**
- `Número_Vacantes`: Number of vacancies
- `Dotación_Presupuestaria`: Budget allocation
- `Sueldo_Base`: Base salary

**Linkage Fields:**
- `ID_Jefe_Superior`: Links to superior position (creates dependency tree)

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rpt-app
```

2. Install dependencies:
```bash
npm install
```

## Usage

### Start the application

```bash
npm start
```

The application will:
- Start on `http://localhost:3000`
- Create/sync the SQLite database automatically
- Make AdminJS interface available at `http://localhost:3000/admin`

### Development mode

```bash
npm run dev
```

## Access the Admin Panel

Open your browser and navigate to:
```
http://localhost:3000/admin
```

From there you can:
- View all positions (Puestos)
- Create new positions
- Edit existing positions
- Delete positions
- Filter and search positions
- Manage hierarchical relationships between positions

## Database

The application uses SQLite with the database file stored as `database.sqlite` in the project root. This file is automatically created on first run and is excluded from version control via `.gitignore`.

## Project Structure

```
rpt-app/
├── models/
│   ├── index.js          # Database configuration and model exports
│   └── puestos.js        # Puestos model definition
├── index.js              # Main application file with AdminJS setup
├── package.json          # Project dependencies and scripts
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Configuration

### Environment Variables

You can customize the following settings using environment variables:

- `PORT`: Server port (default: 3000)
- `SESSION_SECRET`: Session secret key (change in production)

Example:
```bash
PORT=8080 SESSION_SECRET=your-secret-key npm start
```

## License

ISC

## Author

Aranda de Duero
