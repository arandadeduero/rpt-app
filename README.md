# RPT App - Relación de Puestos de Trabajo

RPT (Job Position Relationship) application for Aranda de Duero municipal administration.

## Overview

This application manages and analyzes job positions (puestos) in the municipal organization, supporting:

- **Querying**: Retrieve detailed information about positions
- **Analysis**: Calculate and analyze valoración scores
- **Organizational**: Navigate hierarchical dependencies
- **Comparison**: Compare positions and calculate statistics
- **Data Explanation**: Explain valuation systems and codes

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Python API

```python
from rpt_app import RPTManager

# Initialize the manager
rpt = RPTManager()

# Query by internal code
puesto = rpt.get_by_codigo_interno('ADM2025')
print(puesto)

# List positions by criteria
puestos = rpt.list_positions(numero_vacantes__gt=1)
for p in puestos:
    print(p['Denominacion'], p['Número_Vacantes'])

# Calculate total valoración score
score = rpt.calculate_total_valoracion('Técnico de Urbanismo')
print(f"Puntuación total: {score}")

# Get organizational hierarchy
hierarchy = rpt.get_hierarchy_chain(45)
print(hierarchy)

# Compare positions
comparison = rpt.compare_positions(['Auxiliar Administrativo', 'Administrativo'], 
                                   factors=['A', 'D'])
print(comparison)

# Get average salary by area
avg_salary = rpt.get_average_salary_by_area('Cultura')
print(f"Media salarial: {avg_salary}")
```

## Data Structure

Job positions include the following fields:

- **ID_Puesto**: Unique position identifier
- **Código_Interno**: Internal code (e.g., 'ADM2025')
- **Denominacion**: Position name
- **Número_Vacantes**: Number of vacancies
- **Área**: Department/Area
- **Descripción_Funciones**: Function description
- **Salario**: Salary information
- **Valoración_A** through **Valoración_E**: Valuation factors with levels and scores
- **ID_Superior**: Parent position ID for organizational hierarchy

## Valoración Factors

The valuation system uses five factors (A-E):

- **Factor A**: Formación (Education/Training)
- **Factor B**: Experiencia (Experience)
- **Factor C**: Complejidad (Complexity)
- **Factor D**: Responsabilidad (Responsibility)
- **Factor E**: Condiciones de trabajo (Working conditions)

Each factor has levels (I, II, III, IV, V) with associated scores.

## Example Queries

See `examples.py` for complete examples of all supported operations.

## License

See LICENSE file.
