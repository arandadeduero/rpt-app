"""
Examples of RPT App usage demonstrating all core tasks.
"""

from rpt_app import RPTManager
from tabulate import tabulate
import json


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def example_querying():
    """Examples of querying operations."""
    print_section("1. QUERYING - Consultas")
    
    rpt = RPTManager()
    
    # Example 1: Show complete details of a position by internal code
    print("Query 1: Muestra el detalle completo del puesto con Código_Interno 'ADM2025'")
    print("-" * 80)
    puesto = rpt.get_by_codigo_interno('ADM2025')
    if puesto:
        details = rpt.get_position_details(puesto.Denominacion)
        print(f"Denominación: {details['Denominacion']}")
        print(f"Código Interno: {details['Código_Interno']}")
        print(f"ID Puesto: {details['ID_Puesto']}")
        print(f"Área: {details['Área']}")
        print(f"Número de Vacantes: {details['Número_Vacantes']}")
        print(f"Salario: {details['Salario']:.2f} €")
        print(f"Descripción de Funciones: {details['Descripción_Funciones']}")
        print(f"\nValoración:")
        print(f"  Factor A: {details['Valoración_A']['nivel']} ({details['Valoración_A']['puntuacion']} puntos)")
        print(f"  Factor B: {details['Valoración_B']['nivel']} ({details['Valoración_B']['puntuacion']} puntos)")
        print(f"  Factor C: {details['Valoración_C']['nivel']} ({details['Valoración_C']['puntuacion']} puntos)")
        print(f"  Factor D: {details['Valoración_D']['nivel']} ({details['Valoración_D']['puntuacion']} puntos)")
        print(f"  Factor E: {details['Valoración_E']['nivel']} ({details['Valoración_E']['puntuacion']} puntos)")
        print(f"  Total: {details['Puntuación_Total']} puntos")
        print(f"\nJerarquía:")
        print(f"  Superior: {details['Superior']}")
        print(f"  Subordinados Directos: {', '.join(details['Subordinados_Directos']) if details['Subordinados_Directos'] else 'Ninguno'}")
    else:
        print("Puesto no encontrado")
    
    print("\n")
    
    # Example 2: List all positions with more than 1 vacancy
    print("Query 2: Lista todos los puestos con Número_Vacantes mayor que 1")
    print("-" * 80)
    puestos = rpt.list_positions(numero_vacantes__gt=1)
    
    if puestos:
        table_data = []
        for p in puestos:
            table_data.append([
                p.Denominacion,
                p.Código_Interno,
                p.Número_Vacantes,
                p.Área,
                f"{p.Salario:.2f} €"
            ])
        
        print(tabulate(
            table_data,
            headers=['Denominación', 'Código Interno', 'Vacantes', 'Área', 'Salario'],
            tablefmt='grid'
        ))
    else:
        print("No se encontraron puestos con más de 1 vacante")


def example_analysis():
    """Examples of analysis operations."""
    print_section("2. ANALYSIS - Análisis")
    
    rpt = RPTManager()
    
    # Example 1: Calculate total valuation score
    print("Analysis 1: ¿Cuál es la puntuación total de valoración del puesto 'Técnico de Urbanismo'")
    print("            (suma de A+B+C+D+E)?")
    print("-" * 80)
    denominacion = 'Técnico de Urbanismo'
    score = rpt.calculate_total_valoracion(denominacion)
    if score:
        puesto = rpt.get_by_denominacion(denominacion)
        print(f"Puesto: {denominacion}")
        print(f"\nDesglose de puntuación:")
        print(f"  Factor A (Formación): {puesto.Valoración_A.puntuacion} puntos")
        print(f"  Factor B (Experiencia): {puesto.Valoración_B.puntuacion} puntos")
        print(f"  Factor C (Complejidad): {puesto.Valoración_C.puntuacion} puntos")
        print(f"  Factor D (Responsabilidad): {puesto.Valoración_D.puntuacion} puntos")
        print(f"  Factor E (Condiciones): {puesto.Valoración_E.puntuacion} puntos")
        print(f"\n  PUNTUACIÓN TOTAL: {score} puntos")
    else:
        print(f"No se encontró el puesto '{denominacion}'")
    
    print("\n")
    
    # Example 2: Filter by valuation level
    print("Analysis 2: Dime qué puestos tienen un nivel de 'Valoración_C' igual o superior al Nivel III")
    print("-" * 80)
    puestos = rpt.filter_by_valoracion_level('C', 'Nivel III')
    
    if puestos:
        table_data = []
        for p in puestos:
            table_data.append([
                p.Denominacion,
                p.Área,
                p.Valoración_C.nivel,
                p.Valoración_C.puntuacion
            ])
        
        print(tabulate(
            table_data,
            headers=['Denominación', 'Área', 'Nivel Factor C', 'Puntuación C'],
            tablefmt='grid'
        ))
    else:
        print("No se encontraron puestos con el nivel especificado")


def example_organizational():
    """Examples of organizational operations."""
    print_section("3. ORGANIZATIONAL - Organizacional")
    
    rpt = RPTManager()
    
    # Example 1: Show hierarchy chain
    print("Organizational 1: Dibuja (o describe) la cadena de mando del puesto")
    print("                  'Jefe de Servicio de Hacienda' hasta el puesto de máximo nivel")
    print("-" * 80)
    puesto = rpt.get_by_denominacion('Jefe de Servicio de Hacienda')
    if puesto:
        hierarchy_text = rpt.describe_hierarchy(puesto.ID_Puesto)
        print(hierarchy_text)
        
        print("\n\nDetalle de la cadena:")
        chain = rpt.get_hierarchy_chain(puesto.ID_Puesto)
        chain.reverse()
        for i, p in enumerate(chain):
            print(f"\n{i+1}. {p.Denominacion}")
            print(f"   - Código: {p.Código_Interno}")
            print(f"   - Área: {p.Área}")
            if p.ID_Superior:
                superior = rpt.get_by_id(p.ID_Superior)
                print(f"   - Reporta a: {superior.Denominacion if superior else 'N/A'}")
            else:
                print(f"   - Reporta a: Ninguno (Máximo nivel)")
    else:
        print("Puesto no encontrado")
    
    print("\n")
    
    # Example 2: Show direct subordinates
    print("Organizational 2: ¿Qué puestos son subordinados directos del puesto con ID_Puesto 45?")
    print("-" * 80)
    id_puesto = 45
    jefe = rpt.get_by_id(id_puesto)
    if jefe:
        print(f"Puesto superior: {jefe.Denominacion} (ID: {jefe.ID_Puesto})")
        print(f"\nSubordinados directos:")
        
        subordinates = rpt.get_direct_subordinates(id_puesto)
        if subordinates:
            table_data = []
            for s in subordinates:
                table_data.append([
                    s.ID_Puesto,
                    s.Código_Interno,
                    s.Denominacion,
                    s.Área,
                    s.Número_Vacantes
                ])
            
            print(tabulate(
                table_data,
                headers=['ID', 'Código', 'Denominación', 'Área', 'Vacantes'],
                tablefmt='grid'
            ))
        else:
            print("  No tiene subordinados directos")
    else:
        print(f"No se encontró el puesto con ID {id_puesto}")


def example_comparison():
    """Examples of comparison operations."""
    print_section("4. COMPARISON - Comparación")
    
    rpt = RPTManager()
    
    # Example 1: Compare specific factors between positions
    print("Comparison 1: Compara las puntuaciones de los Factores A y D entre los puestos")
    print("              'Auxiliar Administrativo' y 'Administrativo'")
    print("-" * 80)
    denominaciones = ['Auxiliar Administrativo', 'Administrativo']
    comparison = rpt.compare_positions(denominaciones, factors=['A', 'D'])
    
    print("Comparación de puestos:\n")
    
    # Table for Factor A
    print("Factor A (Formación):")
    table_a = []
    for puesto_name in comparison['positions']:
        if puesto_name in comparison['factors']['A']:
            data = comparison['factors']['A'][puesto_name]
            table_a.append([puesto_name, data['nivel'], data['puntuacion']])
    print(tabulate(table_a, headers=['Puesto', 'Nivel', 'Puntuación'], tablefmt='grid'))
    
    print("\nFactor D (Responsabilidad):")
    table_d = []
    for puesto_name in comparison['positions']:
        if puesto_name in comparison['factors']['D']:
            data = comparison['factors']['D'][puesto_name]
            table_d.append([puesto_name, data['nivel'], data['puntuacion']])
    print(tabulate(table_d, headers=['Puesto', 'Nivel', 'Puntuación'], tablefmt='grid'))
    
    print("\n")
    
    # Example 2: Average salary by area
    print("Comparison 2: Dame la media salarial de los puestos del área 'Cultura'")
    print("-" * 80)
    area = 'Cultura'
    avg_salary = rpt.get_average_salary_by_area(area)
    
    if avg_salary:
        print(f"Área: {area}")
        print(f"Media salarial: {avg_salary:.2f} €")
        
        # Show individual positions in the area
        positions_in_area = rpt.list_positions(area=area)
        print(f"\nPuestos en el área de {area}:")
        table_data = []
        for p in positions_in_area:
            table_data.append([p.Denominacion, f"{p.Salario:.2f} €"])
        print(tabulate(table_data, headers=['Puesto', 'Salario'], tablefmt='grid'))
    else:
        print(f"No se encontraron puestos en el área '{area}'")


def example_data_explanation():
    """Examples of data explanation operations."""
    print_section("5. DATA EXPLANATION - Explicación de datos")
    
    rpt = RPTManager()
    
    # Example 1: Explain a specific factor and its level
    print("Explanation 1: ¿Qué representa el Factor B y qué Puntuación tiene el Nivel IV en ese factor?")
    print("-" * 80)
    factor = 'B'
    nivel = 'Nivel IV'
    
    explanation = rpt.explain_factor(factor)
    score = rpt.get_factor_score_by_level(nivel)
    
    print(f"Factor {factor}:")
    print(f"  {explanation}")
    print(f"\n{nivel}:")
    print(f"  Puntuación estándar: {score} puntos")
    
    # Show examples of positions with this level
    print(f"\nEjemplos de puestos con Factor {factor} en {nivel}:")
    example_positions = []
    for p in rpt.puestos:
        valoracion = getattr(p, f'Valoración_{factor}')
        if valoracion.nivel == nivel:
            example_positions.append([p.Denominacion, p.Área, valoracion.puntuacion])
    
    if example_positions:
        print(tabulate(example_positions, headers=['Puesto', 'Área', 'Puntuación'], tablefmt='grid'))
    else:
        print("  No hay puestos con este nivel en este factor")
    
    print("\n")
    
    # Example 2: Explain job functions
    print("Explanation 2: Explica brevemente la Descripción_Funciones del puesto 'Tesorero'")
    print("-" * 80)
    denominacion = 'Tesorero'
    details = rpt.get_position_details(denominacion)
    
    if details:
        print(f"Puesto: {details['Denominacion']}")
        print(f"Código: {details['Código_Interno']}")
        print(f"Área: {details['Área']}")
        print(f"\nDescripción de Funciones:")
        print(f"  {details['Descripción_Funciones']}")
    else:
        print(f"No se encontró el puesto '{denominacion}'")


def example_all_factors():
    """Show all valuation factors and their descriptions."""
    print_section("BONUS: Sistema de Valoración Completo")
    
    rpt = RPTManager()
    
    print("Factores de Valoración del Sistema RPT:\n")
    
    all_factors = rpt.explain_all_factors()
    for factor, description in all_factors.items():
        print(f"Factor {factor}:")
        print(f"  {description}\n")
    
    print("\nNiveles y Puntuaciones Estándar:")
    print("-" * 80)
    table_data = []
    for nivel in ['Nivel I', 'Nivel II', 'Nivel III', 'Nivel IV', 'Nivel V']:
        score = rpt.get_factor_score_by_level(nivel)
        table_data.append([nivel, score])
    
    print(tabulate(table_data, headers=['Nivel', 'Puntuación'], tablefmt='grid'))


def example_statistics():
    """Show general statistics."""
    print_section("BONUS: Estadísticas Generales")
    
    rpt = RPTManager()
    
    stats = rpt.get_statistics_by_area()
    
    print("Estadísticas por Área:\n")
    
    table_data = []
    for area, data in stats.items():
        table_data.append([
            area,
            data['count'],
            data['total_vacantes'],
            f"{data['avg_salary']:.2f} €"
        ])
    
    print(tabulate(
        table_data,
        headers=['Área', 'Nº Puestos', 'Total Vacantes', 'Salario Medio'],
        tablefmt='grid'
    ))


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "RPT APP - SISTEMA DE GESTIÓN DE PUESTOS" + " " * 19 + "║")
    print("║" + " " * 25 + "Aranda de Duero" + " " * 38 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Run all example categories
    example_querying()
    example_analysis()
    example_organizational()
    example_comparison()
    example_data_explanation()
    example_all_factors()
    example_statistics()
    
    print("\n")
    print("=" * 80)
    print("  Ejemplos completados. Todas las funcionalidades han sido demostradas.")
    print("=" * 80)
    print("\n")


if __name__ == "__main__":
    main()
