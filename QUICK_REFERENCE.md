# RPT App - Quick Reference Guide

## Guía Rápida de Uso / Quick Usage Guide

Esta guía proporciona ejemplos rápidos de cómo usar la aplicación RPT para realizar las tareas principales.

### Inicialización / Initialization

```python
from rpt_app import RPTManager

# Crear una instancia del gestor
rpt = RPTManager()

# O cargar datos desde un archivo JSON
rpt = RPTManager(data_file='data/puestos.json')
```

## 1. CONSULTAS (Querying)

### Buscar un puesto por código interno

```python
puesto = rpt.get_by_codigo_interno('ADM2025')
print(f"Puesto: {puesto.Denominacion}")
print(f"Salario: {puesto.Salario}€")
```

### Buscar por nombre

```python
puesto = rpt.get_by_denominacion('Tesorero')
```

### Buscar por ID

```python
puesto = rpt.get_by_id(45)
```

### Listar puestos con más de 1 vacante

```python
puestos = rpt.list_positions(numero_vacantes__gt=1)
for p in puestos:
    print(f"{p.Denominacion}: {p.Número_Vacantes} vacantes")
```

### Listar puestos de un área específica

```python
puestos = rpt.list_positions(area='Cultura')
```

### Obtener detalles completos de un puesto

```python
details = rpt.get_position_details('Administrativo')
# Devuelve un diccionario con toda la información, incluida jerarquía
```

## 2. ANÁLISIS (Analysis)

### Calcular puntuación total de valoración

```python
score = rpt.calculate_total_valoracion('Técnico de Urbanismo')
print(f"Puntuación total: {score} puntos")
```

### Filtrar puestos por nivel de valoración mínimo

```python
# Puestos con Factor C igual o superior a Nivel III
puestos = rpt.filter_by_valoracion_level('C', 'Nivel III')
```

### Obtener estadísticas por área

```python
stats = rpt.get_statistics_by_area()
for area, data in stats.items():
    print(f"{area}: {data['count']} puestos, salario medio {data['avg_salary']:.2f}€")
```

## 3. ORGANIZACIONAL (Organizational)

### Obtener cadena jerárquica completa

```python
chain = rpt.get_hierarchy_chain(45)
for i, puesto in enumerate(chain):
    print(f"Nivel {i}: {puesto.Denominacion}")
```

### Describir jerarquía en formato texto

```python
description = rpt.describe_hierarchy(45)
print(description)
```

### Obtener subordinados directos

```python
subordinates = rpt.get_direct_subordinates(45)
for s in subordinates:
    print(f"- {s.Denominacion}")
```

### Obtener todos los subordinados (recursivo)

```python
all_subs = rpt.get_all_subordinates(1)
print(f"Total subordinados: {len(all_subs)}")
```

## 4. COMPARACIÓN (Comparison)

### Comparar dos puestos en factores específicos

```python
comparison = rpt.compare_positions(
    ['Auxiliar Administrativo', 'Administrativo'],
    factors=['A', 'D']
)

# Acceder a los resultados
for factor, data in comparison['factors'].items():
    print(f"\nFactor {factor}:")
    for puesto_name, valores in data.items():
        print(f"  {puesto_name}: {valores['nivel']} ({valores['puntuacion']} puntos)")
```

### Obtener salario medio de un área

```python
avg = rpt.get_average_salary_by_area('Cultura')
print(f"Salario medio en Cultura: {avg:.2f}€")
```

## 5. EXPLICACIÓN DE DATOS (Data Explanation)

### Explicar un factor de valoración

```python
explanation = rpt.explain_factor('B')
print(explanation)
# Output: "Experiencia (Experience) - Evalúa los años de experiencia profesional necesarios"
```

### Obtener puntuación estándar por nivel

```python
score = rpt.get_factor_score_by_level('Nivel IV')
print(f"Nivel IV = {score} puntos")
```

### Explicar todos los factores

```python
all_factors = rpt.explain_all_factors()
for factor, description in all_factors.items():
    print(f"Factor {factor}: {description}")
```

## Factores de Valoración

| Factor | Descripción | Niveles |
|--------|-------------|---------|
| A | Formación (Education/Training) | I-V |
| B | Experiencia (Experience) | I-V |
| C | Complejidad (Complexity) | I-V |
| D | Responsabilidad (Responsibility) | I-V |
| E | Condiciones de trabajo (Working conditions) | I-V |

### Puntuaciones por Nivel

| Nivel | Puntuación |
|-------|------------|
| Nivel I | 10 |
| Nivel II | 20 |
| Nivel III | 30 |
| Nivel IV | 40 |
| Nivel V | 50 |

## Guardar y Cargar Datos

### Guardar datos a archivo JSON

```python
rpt.save_data('data/mi_rpt.json')
```

### Cargar datos desde archivo JSON

```python
rpt = RPTManager(data_file='data/mi_rpt.json')
```

## Ejemplos Completos

Para ver ejemplos completos de todas las funcionalidades, ejecuta:

```bash
python examples.py
```

Para ejecutar los tests:

```bash
python test_rpt_app.py
```

## Estructura de Datos de un Puesto

```python
{
    "ID_Puesto": 1,
    "Código_Interno": "ADM2025",
    "Denominacion": "Administrativo",
    "Número_Vacantes": 3,
    "Área": "Administración General",
    "Descripción_Funciones": "Tramitación de expedientes...",
    "Salario": 24000.0,
    "Valoración_A": {"nivel": "Nivel III", "puntuacion": 30},
    "Valoración_B": {"nivel": "Nivel III", "puntuacion": 30},
    "Valoración_C": {"nivel": "Nivel III", "puntuacion": 30},
    "Valoración_D": {"nivel": "Nivel III", "puntuacion": 30},
    "Valoración_E": {"nivel": "Nivel II", "puntuacion": 20},
    "ID_Superior": 45
}
```

## Soporte

Para más información, consulta el archivo README.md o ejecuta los ejemplos.
