# Valoración Factors Tables Documentation

## Overview

This document describes the implementation of the Valoración (Valuation) system for the RPT (Relación de Puestos de Trabajo - Job Position Register) application for Aranda de Duero.

## System Components

### 1. Factor Tables (A, B, C, D, E)

The system includes five independent factor tables, each representing a different competency or requirement for job positions:

- **Valoracion_Factor_A**: Factor A valuation criteria
- **Valoracion_Factor_B**: Factor B valuation criteria
- **Valoracion_Factor_C**: Factor C valuation criteria
- **Valoracion_Factor_D**: Factor D valuation criteria
- **Valoracion_Factor_E**: Factor E valuation criteria

### 2. Factor Structure

Each factor table has the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `nivel` | VARCHAR(20) | Level identifier (I, II, III, IV, V) |
| `descripcion` | TEXT | Description of the level |
| `puntuacion` | INTEGER | Score value (0-400) |

#### Constraints:
- **Unique**: Each `nivel` must be unique within a factor table
- **Score Range**: `puntuacion` must be between 0 and 400 (inclusive)

### 3. Levels

Each factor has exactly **5 levels**:
- **Level I** (Nivel I)
- **Level II** (Nivel II)
- **Level III** (Nivel III)
- **Level IV** (Nivel IV)
- **Level V** (Nivel V)

### 4. Scoring System

- **Range**: 0 to 400 points per factor
- **Total Maximum Score**: 2000 points (5 factors × 400 points)
- **Purpose**: Provides a quantitative valuation of position requirements

## RPT Main Table

### Structure

The RPT Main Table stores job position information and links to the valuation levels:

| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key |
| `codigo_puesto` | VARCHAR(50) | Position code |
| `denominacion` | VARCHAR(200) | Position name/title |
| `valoracion_A` | VARCHAR(20) | Level achieved for Factor A |
| `valoracion_B` | VARCHAR(20) | Level achieved for Factor B |
| `valoracion_C` | VARCHAR(20) | Level achieved for Factor C |
| `valoracion_D` | VARCHAR(20) | Level achieved for Factor D |
| `valoracion_E` | VARCHAR(20) | Level achieved for Factor E |
| `puntuacion_total` | INTEGER | Calculated total score |
| `created_at` | TIMESTAMP | Record creation timestamp |
| `updated_at` | TIMESTAMP | Record update timestamp |

### Foreign Key Relationships

Each `valoracion_X` field references the `nivel` field in the corresponding factor table:
- `valoracion_A` → `Valoracion_Factor_A.nivel`
- `valoracion_B` → `Valoracion_Factor_B.nivel`
- `valoracion_C` → `Valoracion_Factor_C.nivel`
- `valoracion_D` → `Valoracion_Factor_D.nivel`
- `valoracion_E` → `Valoracion_Factor_E.nivel`

## Complete View (RPT_View_Complete)

A database view is provided that automatically calculates scores and presents a complete picture of each position:

### Columns:
- All RPT_Main fields
- `puntuacion_A`: Score for Factor A
- `puntuacion_B`: Score for Factor B
- `puntuacion_C`: Score for Factor C
- `puntuacion_D`: Score for Factor D
- `puntuacion_E`: Score for Factor E
- `puntuacion_total`: Sum of all factor scores

### Usage Example:

```sql
-- Get all positions with their complete valuation
SELECT * FROM RPT_View_Complete;

-- Find positions with highest valuation
SELECT * FROM RPT_View_Complete 
ORDER BY puntuacion_total DESC 
LIMIT 10;

-- Filter positions by minimum score in a specific factor
SELECT * FROM RPT_View_Complete 
WHERE puntuacion_C >= 160;
```

## Sample Data

The system includes sample data (`sample_data.sql`) with example interpretations for each factor:

### Factor A - Example: Education/Academic Qualification
- Level I: No specific academic requirements (0 points)
- Level II: Compulsory Secondary Education (80 points)
- Level III: High School or Vocational Training (160 points)
- Level IV: Advanced Vocational Training or Diploma (280 points)
- Level V: Bachelor's Degree or higher (400 points)

### Factor B - Example: Professional Experience
- Level I: No experience required (0 points)
- Level II: Up to 1 year of experience (80 points)
- Level III: 1 to 3 years of experience (160 points)
- Level IV: 3 to 5 years of experience (280 points)
- Level V: More than 5 years of experience (400 points)

### Factor C - Example: Complexity and Responsibility
- Level I: Simple and routine tasks (0 points)
- Level II: Some variety and low complexity (80 points)
- Level III: Varied tasks with medium complexity (160 points)
- Level IV: Complex tasks with high responsibility (280 points)
- Level V: Very complex tasks with maximum responsibility (400 points)

### Factor D - Example: Autonomy and Decision Making
- Level I: Constant supervision, no autonomy (0 points)
- Level II: Frequent supervision, limited autonomy (80 points)
- Level III: Occasional supervision, moderate autonomy (160 points)
- Level IV: Minimal supervision, high autonomy (280 points)
- Level V: Complete autonomy, strategic decisions (400 points)

### Factor E - Example: Skills and Competencies
- Level I: Basic competencies (0 points)
- Level II: Area-specific competencies (80 points)
- Level III: Advanced competencies in multiple areas (160 points)
- Level IV: Expert and leadership competencies (280 points)
- Level V: Exceptional and strategic competencies (400 points)

## Implementation Files

1. **schema.sql**: Database schema definition
   - Creates all factor tables
   - Creates RPT Main table
   - Creates RPT_View_Complete view
   - Defines constraints and relationships

2. **sample_data.sql**: Sample data for testing
   - Populates all factor tables with example levels
   - Includes 5 sample positions in RPT_Main

## Database Setup

### Initialize the Database:

```bash
# Using SQLite
sqlite3 rpt_database.db < schema.sql
sqlite3 rpt_database.db < sample_data.sql
```

### Verify Installation:

```sql
-- Check factor tables
SELECT COUNT(*) FROM Valoracion_Factor_A; -- Should return 5
SELECT COUNT(*) FROM Valoracion_Factor_B; -- Should return 5
SELECT COUNT(*) FROM Valoracion_Factor_C; -- Should return 5
SELECT COUNT(*) FROM Valoracion_Factor_D; -- Should return 5
SELECT COUNT(*) FROM Valoracion_Factor_E; -- Should return 5

-- Check sample positions
SELECT COUNT(*) FROM RPT_Main; -- Should return 5

-- View complete data with scores
SELECT * FROM RPT_View_Complete;
```

## Customization

The sample data provides one possible interpretation of the factors. Organizations should customize the factor definitions according to their specific needs:

1. Modify the `descripcion` field in each factor table to match organizational criteria
2. Adjust `puntuacion` values to reflect the importance of each level
3. Define what each factor (A, B, C, D, E) represents for your organization

## Data Integrity

The system ensures data integrity through:

1. **Foreign Key Constraints**: Ensure valoracion fields reference valid levels
2. **Check Constraints**: Score values must be between 0 and 400
3. **Unique Constraints**: Each level is unique within a factor table
4. **NOT NULL Constraints**: Critical fields cannot be empty

## Future Enhancements

Potential improvements to consider:

1. **Factor Descriptions**: Add a separate table to store detailed descriptions of what each factor represents
2. **Historical Tracking**: Track changes to position valuations over time
3. **Weight System**: Allow different weights for different factors
4. **Approval Workflow**: Add approval status for position valuations
5. **Audit Log**: Track who made changes and when
6. **Reports**: Pre-built queries for common reporting needs
