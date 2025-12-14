# Database Schema Diagram

```
┌─────────────────────────────────┐
│   Valoracion_Factor_A           │
├─────────────────────────────────┤
│ id (PK)                         │
│ nivel (UNIQUE) ◄────────────┐   │
│ descripcion                  │   │
│ puntuacion (0-400)           │   │
└─────────────────────────────────┘
                                │
┌─────────────────────────────────┐
│   Valoracion_Factor_B           │
├─────────────────────────────────┤
│ id (PK)                         │
│ nivel (UNIQUE) ◄────────────┐   │
│ descripcion                  │   │
│ puntuacion (0-400)           │   │
└─────────────────────────────────┘
                                │
┌─────────────────────────────────┐
│   Valoracion_Factor_C           │
├─────────────────────────────────┤
│ id (PK)                         │
│ nivel (UNIQUE) ◄────────────┐   │
│ descripcion                  │   │
│ puntuacion (0-400)           │   │
└─────────────────────────────────┘
                                │
┌─────────────────────────────────┐
│   Valoracion_Factor_D           │
├─────────────────────────────────┤
│ id (PK)                         │
│ nivel (UNIQUE) ◄────────────┐   │
│ descripcion                  │   │
│ puntuacion (0-400)           │   │
└─────────────────────────────────┘
                                │
┌─────────────────────────────────┐
│   Valoracion_Factor_E           │
├─────────────────────────────────┤
│ id (PK)                         │
│ nivel (UNIQUE) ◄────────────┐   │
│ descripcion                  │   │
│ puntuacion (0-400)           │   │
└─────────────────────────────────┘
                                │
                                │
        ┌───────────────────────┴───────────────────────┐
        │                 RPT_Main                      │
        ├───────────────────────────────────────────────┤
        │ id (PK)                                       │
        │ codigo_puesto                                 │
        │ denominacion                                  │
        │ valoracion_A (FK) ────────────────────────────┘
        │ valoracion_B (FK)
        │ valoracion_C (FK)
        │ valoracion_D (FK)
        │ valoracion_E (FK)
        │ created_at
        │ updated_at
        └───────────────────────────────────────────────┘
                                │
                                │ (used by)
                                ▼
        ┌───────────────────────────────────────────────┐
        │          RPT_View_Complete (VIEW)             │
        ├───────────────────────────────────────────────┤
        │ • All RPT_Main fields                         │
        │ • puntuacion_A (from Factor A)                │
        │ • puntuacion_B (from Factor B)                │
        │ • puntuacion_C (from Factor C)                │
        │ • puntuacion_D (from Factor D)                │
        │ • puntuacion_E (from Factor E)                │
        │ • puntuacion_total (calculated sum)           │
        └───────────────────────────────────────────────┘
```

## Key Relationships

- Each factor table (A, B, C, D, E) is independent
- Each factor has exactly 5 levels (I, II, III, IV, V)
- RPT_Main references factor tables via foreign keys
- RPT_View_Complete joins all tables to show complete data
- Total score is calculated dynamically (not stored)

## Data Flow

1. **Define Factor Levels**: Insert levels (I-V) with scores (0-400) into each factor table
2. **Create Position**: Insert position into RPT_Main with references to factor levels
3. **Query Complete Data**: Use RPT_View_Complete to see position with all scores calculated

## Example Query

```sql
-- Get position P003 with complete scoring
SELECT 
    codigo_puesto,
    denominacion,
    valoracion_A, puntuacion_A,
    valoracion_B, puntuacion_B,
    valoracion_C, puntuacion_C,
    valoracion_D, puntuacion_D,
    valoracion_E, puntuacion_E,
    puntuacion_total
FROM RPT_View_Complete
WHERE codigo_puesto = 'P003';
```

Result:
```
P003 | Jefe de Servicio | V | 400 | V | 400 | V | 400 | V | 400 | IV | 280 | 1880
```
