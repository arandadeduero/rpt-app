#!/usr/bin/env python
"""
RPT App CLI - Command Line Interface
Simple interactive interface for querying the RPT system.
"""

import sys
from rpt_app import RPTManager
from tabulate import tabulate


class RPTCLI:
    """Command line interface for RPT App."""
    
    def __init__(self):
        self.rpt = RPTManager()
        self.commands = {
            'buscar': self.cmd_buscar,
            'listar': self.cmd_listar,
            'puntuacion': self.cmd_puntuacion,
            'jerarquia': self.cmd_jerarquia,
            'comparar': self.cmd_comparar,
            'media': self.cmd_media,
            'factor': self.cmd_factor,
            'ayuda': self.cmd_ayuda,
            'help': self.cmd_ayuda,
            'salir': self.cmd_salir,
            'exit': self.cmd_salir,
        }
    
    def cmd_buscar(self, args):
        """Buscar un puesto por código o nombre."""
        if not args:
            print("Uso: buscar <codigo_interno o nombre>")
            return
        
        query = ' '.join(args)
        
        # Try by code first
        puesto = self.rpt.get_by_codigo_interno(query)
        
        # If not found, try by name
        if not puesto:
            puesto = self.rpt.get_by_denominacion(query)
        
        if puesto:
            details = self.rpt.get_position_details(puesto.Denominacion)
            print(f"\n{'='*70}")
            print(f"  {details['Denominacion']}")
            print(f"{'='*70}")
            print(f"Código Interno:  {details['Código_Interno']}")
            print(f"ID Puesto:       {details['ID_Puesto']}")
            print(f"Área:            {details['Área']}")
            print(f"Vacantes:        {details['Número_Vacantes']}")
            print(f"Salario:         {details['Salario']:.2f} €")
            print(f"\nValoración:")
            print(f"  Factor A: {details['Valoración_A']['nivel']} ({details['Valoración_A']['puntuacion']} pts)")
            print(f"  Factor B: {details['Valoración_B']['nivel']} ({details['Valoración_B']['puntuacion']} pts)")
            print(f"  Factor C: {details['Valoración_C']['nivel']} ({details['Valoración_C']['puntuacion']} pts)")
            print(f"  Factor D: {details['Valoración_D']['nivel']} ({details['Valoración_D']['puntuacion']} pts)")
            print(f"  Factor E: {details['Valoración_E']['nivel']} ({details['Valoración_E']['puntuacion']} pts)")
            print(f"  TOTAL:    {details['Puntuación_Total']} puntos")
            print(f"\nJerarquía:")
            print(f"  Superior:     {details['Superior']}")
            subordinados = ', '.join(details['Subordinados_Directos']) if details['Subordinados_Directos'] else 'Ninguno'
            print(f"  Subordinados: {subordinados}")
            print(f"\nFunciones:")
            print(f"  {details['Descripción_Funciones']}")
        else:
            print(f"No se encontró el puesto '{query}'")
    
    def cmd_listar(self, args):
        """Listar puestos por criterio."""
        if not args:
            # List all positions
            puestos = self.rpt.puestos
        elif args[0] == 'area' and len(args) > 1:
            area = ' '.join(args[1:])
            puestos = self.rpt.list_positions(area=area)
        elif args[0] == 'vacantes' and len(args) > 1:
            try:
                min_vacantes = int(args[1])
                puestos = self.rpt.list_positions(numero_vacantes__gt=min_vacantes)
            except ValueError:
                print("Error: número de vacantes debe ser un entero")
                return
        else:
            print("Uso: listar [area <nombre>] [vacantes <minimo>]")
            return
        
        if puestos:
            table_data = []
            for p in puestos:
                table_data.append([
                    p.ID_Puesto,
                    p.Código_Interno,
                    p.Denominacion,
                    p.Área,
                    p.Número_Vacantes,
                    f"{p.Salario:.0f} €"
                ])
            print(f"\nEncontrados {len(puestos)} puesto(s):\n")
            print(tabulate(
                table_data,
                headers=['ID', 'Código', 'Denominación', 'Área', 'Vacantes', 'Salario'],
                tablefmt='grid'
            ))
        else:
            print("No se encontraron puestos con los criterios especificados")
    
    def cmd_puntuacion(self, args):
        """Calcular puntuación total de un puesto."""
        if not args:
            print("Uso: puntuacion <nombre_puesto>")
            return
        
        denominacion = ' '.join(args)
        score = self.rpt.calculate_total_valoracion(denominacion)
        
        if score:
            puesto = self.rpt.get_by_denominacion(denominacion)
            print(f"\n{puesto.Denominacion}:")
            print(f"  Factor A: {puesto.Valoración_A.puntuacion} pts")
            print(f"  Factor B: {puesto.Valoración_B.puntuacion} pts")
            print(f"  Factor C: {puesto.Valoración_C.puntuacion} pts")
            print(f"  Factor D: {puesto.Valoración_D.puntuacion} pts")
            print(f"  Factor E: {puesto.Valoración_E.puntuacion} pts")
            print(f"  ─────────────────────")
            print(f"  TOTAL:    {score} puntos")
        else:
            print(f"No se encontró el puesto '{denominacion}'")
    
    def cmd_jerarquia(self, args):
        """Mostrar jerarquía de un puesto."""
        if not args:
            print("Uso: jerarquia <nombre_puesto o ID>")
            return
        
        # Try as ID first
        try:
            id_puesto = int(args[0])
            puesto = self.rpt.get_by_id(id_puesto)
        except ValueError:
            # Not an ID, try as name
            denominacion = ' '.join(args)
            puesto = self.rpt.get_by_denominacion(denominacion)
        
        if puesto:
            description = self.rpt.describe_hierarchy(puesto.ID_Puesto)
            print(f"\n{description}")
        else:
            print(f"No se encontró el puesto")
    
    def cmd_comparar(self, args):
        """Comparar dos puestos."""
        if len(args) < 2:
            print("Uso: comparar <puesto1> y <puesto2>")
            print("Ejemplo: comparar Administrativo y Auxiliar Administrativo")
            return
        
        # Find 'y' separator
        if 'y' in args:
            y_index = args.index('y')
            puesto1 = ' '.join(args[:y_index])
            puesto2 = ' '.join(args[y_index+1:])
        else:
            print("Error: use 'y' para separar los dos puestos")
            return
        
        comparison = self.rpt.compare_positions([puesto1, puesto2])
        
        if len(comparison['positions']) < 2:
            print(f"No se encontraron ambos puestos")
            return
        
        print(f"\nComparación entre '{puesto1}' y '{puesto2}':\n")
        
        for factor in ['A', 'B', 'C', 'D', 'E']:
            if factor in comparison['factors']:
                table_data = []
                for puesto_name, data in comparison['factors'][factor].items():
                    table_data.append([puesto_name, data['nivel'], data['puntuacion']])
                print(f"Factor {factor}:")
                print(tabulate(table_data, headers=['Puesto', 'Nivel', 'Puntos'], tablefmt='simple'))
                print()
    
    def cmd_media(self, args):
        """Calcular media salarial por área."""
        if not args:
            # Show all areas
            stats = self.rpt.get_statistics_by_area()
            table_data = []
            for area, data in stats.items():
                table_data.append([area, data['count'], f"{data['avg_salary']:.2f} €"])
            print("\nMedia salarial por área:\n")
            print(tabulate(table_data, headers=['Área', 'Nº Puestos', 'Salario Medio'], tablefmt='grid'))
        else:
            area = ' '.join(args)
            avg = self.rpt.get_average_salary_by_area(area)
            if avg:
                print(f"\nMedia salarial en {area}: {avg:.2f} €")
            else:
                print(f"No se encontraron puestos en el área '{area}'")
    
    def cmd_factor(self, args):
        """Explicar un factor de valoración."""
        if not args:
            # Show all factors
            print("\nFactores de Valoración:\n")
            for factor, desc in self.rpt.explain_all_factors().items():
                print(f"Factor {factor}:")
                print(f"  {desc}\n")
            
            print("Puntuaciones por nivel:")
            table_data = [
                ['Nivel I', 10],
                ['Nivel II', 20],
                ['Nivel III', 30],
                ['Nivel IV', 40],
                ['Nivel V', 50]
            ]
            print(tabulate(table_data, headers=['Nivel', 'Puntos'], tablefmt='simple'))
        else:
            factor = args[0].upper()
            if factor in ['A', 'B', 'C', 'D', 'E']:
                explanation = self.rpt.explain_factor(factor)
                print(f"\nFactor {factor}:")
                print(f"  {explanation}")
            else:
                print(f"Factor '{factor}' no válido. Use A, B, C, D o E.")
    
    def cmd_ayuda(self, args):
        """Mostrar ayuda."""
        print("""
RPT App - Sistema de Gestión de Puestos de Trabajo
═══════════════════════════════════════════════════

Comandos disponibles:

  buscar <codigo|nombre>        Buscar un puesto por código o nombre
  listar [area|vacantes ...]    Listar puestos por criterio
  puntuacion <nombre>           Calcular puntuación total de valoración
  jerarquia <nombre|ID>         Mostrar cadena jerárquica
  comparar <puesto1> y <puesto2> Comparar dos puestos
  media [area]                  Media salarial por área
  factor [A-E]                  Explicar factores de valoración
  ayuda / help                  Mostrar esta ayuda
  salir / exit                  Salir del programa

Ejemplos:

  buscar ADM2025
  buscar Administrativo
  listar area Cultura
  listar vacantes 1
  puntuacion Técnico de Urbanismo
  jerarquia 45
  jerarquia Jefe de Servicio de Hacienda
  comparar Administrativo y Auxiliar Administrativo
  media Cultura
  factor B
        """)
    
    def cmd_salir(self, args):
        """Salir del programa."""
        print("\n¡Hasta luego!")
        sys.exit(0)
    
    def run(self):
        """Run the CLI in interactive mode."""
        print("\n" + "═" * 70)
        print("  RPT App - Sistema de Gestión de Puestos de Trabajo")
        print("  Aranda de Duero")
        print("═" * 70)
        print("\nEscriba 'ayuda' para ver los comandos disponibles")
        print("Escriba 'salir' para terminar\n")
        
        while True:
            try:
                line = input("rpt> ").strip()
                
                if not line:
                    continue
                
                parts = line.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Comando desconocido: '{command}'. Use 'ayuda' para ver comandos disponibles.")
                
                print()  # Empty line after each command
                
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except EOFError:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point."""
    cli = RPTCLI()
    
    # If arguments provided, execute single command
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        args = sys.argv[2:]
        
        if command in cli.commands:
            cli.commands[command](args)
        else:
            print(f"Comando desconocido: '{command}'")
            cli.cmd_ayuda([])
    else:
        # Interactive mode
        cli.run()


if __name__ == '__main__':
    main()
