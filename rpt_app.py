"""
RPT App - Relación de Puestos de Trabajo
Main application module for managing and analyzing job positions.
"""

import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ValoracionFactor:
    """Represents a valuation factor with level and score."""
    nivel: str  # e.g., "Nivel III"
    puntuacion: int


@dataclass
class Puesto:
    """Represents a job position with all its attributes."""
    ID_Puesto: int
    Código_Interno: str
    Denominacion: str
    Número_Vacantes: int
    Área: str
    Descripción_Funciones: str
    Salario: float
    Valoración_A: ValoracionFactor
    Valoración_B: ValoracionFactor
    Valoración_C: ValoracionFactor
    Valoración_D: ValoracionFactor
    Valoración_E: ValoracionFactor
    ID_Superior: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert position to dictionary."""
        result = asdict(self)
        result['Valoración_A'] = asdict(self.Valoración_A)
        result['Valoración_B'] = asdict(self.Valoración_B)
        result['Valoración_C'] = asdict(self.Valoración_C)
        result['Valoración_D'] = asdict(self.Valoración_D)
        result['Valoración_E'] = asdict(self.Valoración_E)
        return result
    
    def get_total_valoracion(self) -> int:
        """Calculate total valuation score (sum of all factors)."""
        return (
            self.Valoración_A.puntuacion +
            self.Valoración_B.puntuacion +
            self.Valoración_C.puntuacion +
            self.Valoración_D.puntuacion +
            self.Valoración_E.puntuacion
        )


class RPTManager:
    """Main manager class for RPT operations."""
    
    # Factor descriptions
    FACTOR_DESCRIPTIONS = {
        'A': 'Formación (Education/Training) - Evalúa el nivel de formación académica y especialización requerida',
        'B': 'Experiencia (Experience) - Evalúa los años de experiencia profesional necesarios',
        'C': 'Complejidad (Complexity) - Evalúa la dificultad técnica y variedad de las tareas',
        'D': 'Responsabilidad (Responsibility) - Evalúa el nivel de responsabilidad en toma de decisiones y supervisión',
        'E': 'Condiciones de trabajo (Working conditions) - Evalúa las condiciones físicas y psicológicas del trabajo'
    }
    
    # Standard scoring by level
    STANDARD_SCORES = {
        'Nivel I': 10,
        'Nivel II': 20,
        'Nivel III': 30,
        'Nivel IV': 40,
        'Nivel V': 50
    }
    
    def __init__(self, data_file: Optional[str] = None):
        """Initialize the RPT Manager with optional data file."""
        self.puestos: List[Puesto] = []
        if data_file and Path(data_file).exists():
            self.load_data(data_file)
        else:
            self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for demonstration."""
        self.puestos = [
            Puesto(
                ID_Puesto=1,
                Código_Interno='SEC2025',
                Denominacion='Secretario General',
                Número_Vacantes=1,
                Área='Secretaría',
                Descripción_Funciones='Dirección y coordinación de todos los servicios administrativos del Ayuntamiento. Fe pública. Asesoramiento legal.',
                Salario=45000.0,
                Valoración_A=ValoracionFactor('Nivel V', 50),
                Valoración_B=ValoracionFactor('Nivel V', 50),
                Valoración_C=ValoracionFactor('Nivel V', 50),
                Valoración_D=ValoracionFactor('Nivel V', 50),
                Valoración_E=ValoracionFactor('Nivel II', 20),
                ID_Superior=None
            ),
            Puesto(
                ID_Puesto=2,
                Código_Interno='TES2025',
                Denominacion='Tesorero',
                Número_Vacantes=1,
                Área='Hacienda',
                Descripción_Funciones='Gestión financiera y presupuestaria del Ayuntamiento. Control de tesorería, pagos y cobros. Gestión de inversiones.',
                Salario=42000.0,
                Valoración_A=ValoracionFactor('Nivel V', 50),
                Valoración_B=ValoracionFactor('Nivel IV', 40),
                Valoración_C=ValoracionFactor('Nivel IV', 40),
                Valoración_D=ValoracionFactor('Nivel V', 50),
                Valoración_E=ValoracionFactor('Nivel II', 20),
                ID_Superior=1
            ),
            Puesto(
                ID_Puesto=45,
                Código_Interno='JEF-HAC-2025',
                Denominacion='Jefe de Servicio de Hacienda',
                Número_Vacantes=1,
                Área='Hacienda',
                Descripción_Funciones='Coordinación del servicio de Hacienda. Elaboración de presupuestos. Supervisión de contabilidad y fiscalidad.',
                Salario=38000.0,
                Valoración_A=ValoracionFactor('Nivel IV', 40),
                Valoración_B=ValoracionFactor('Nivel IV', 40),
                Valoración_C=ValoracionFactor('Nivel IV', 40),
                Valoración_D=ValoracionFactor('Nivel IV', 40),
                Valoración_E=ValoracionFactor('Nivel II', 20),
                ID_Superior=2
            ),
            Puesto(
                ID_Puesto=3,
                Código_Interno='ADM2025',
                Denominacion='Administrativo',
                Número_Vacantes=3,
                Área='Administración General',
                Descripción_Funciones='Tramitación de expedientes administrativos. Registro y archivo de documentos. Atención al público.',
                Salario=24000.0,
                Valoración_A=ValoracionFactor('Nivel III', 30),
                Valoración_B=ValoracionFactor('Nivel III', 30),
                Valoración_C=ValoracionFactor('Nivel III', 30),
                Valoración_D=ValoracionFactor('Nivel III', 30),
                Valoración_E=ValoracionFactor('Nivel II', 20),
                ID_Superior=45
            ),
            Puesto(
                ID_Puesto=4,
                Código_Interno='AUX2025',
                Denominacion='Auxiliar Administrativo',
                Número_Vacantes=2,
                Área='Administración General',
                Descripción_Funciones='Apoyo administrativo. Registro de entrada y salida. Archivo y digitalización de documentos.',
                Salario=18000.0,
                Valoración_A=ValoracionFactor('Nivel II', 20),
                Valoración_B=ValoracionFactor('Nivel II', 20),
                Valoración_C=ValoracionFactor('Nivel II', 20),
                Valoración_D=ValoracionFactor('Nivel II', 20),
                Valoración_E=ValoracionFactor('Nivel II', 20),
                ID_Superior=45
            ),
            Puesto(
                ID_Puesto=5,
                Código_Interno='TEC-URB-2025',
                Denominacion='Técnico de Urbanismo',
                Número_Vacantes=2,
                Área='Urbanismo',
                Descripción_Funciones='Elaboración de planes urbanísticos. Tramitación de licencias de obras. Inspección técnica de edificaciones.',
                Salario=32000.0,
                Valoración_A=ValoracionFactor('Nivel IV', 40),
                Valoración_B=ValoracionFactor('Nivel III', 30),
                Valoración_C=ValoracionFactor('Nivel IV', 40),
                Valoración_D=ValoracionFactor('Nivel III', 30),
                Valoración_E=ValoracionFactor('Nivel III', 30),
                ID_Superior=1
            ),
            Puesto(
                ID_Puesto=6,
                Código_Interno='TEC-CUL-2025',
                Denominacion='Técnico de Cultura',
                Número_Vacantes=1,
                Área='Cultura',
                Descripción_Funciones='Organización de eventos culturales. Gestión de espacios culturales. Coordinación con asociaciones culturales.',
                Salario=28000.0,
                Valoración_A=ValoracionFactor('Nivel III', 30),
                Valoración_B=ValoracionFactor('Nivel III', 30),
                Valoración_C=ValoracionFactor('Nivel III', 30),
                Valoración_D=ValoracionFactor('Nivel III', 30),
                Valoración_E=ValoracionFactor('Nivel II', 20),
                ID_Superior=1
            ),
            Puesto(
                ID_Puesto=7,
                Código_Interno='AUX-CUL-2025',
                Denominacion='Auxiliar de Cultura',
                Número_Vacantes=2,
                Área='Cultura',
                Descripción_Funciones='Apoyo en eventos culturales. Atención al público en espacios culturales. Gestión de reservas.',
                Salario=20000.0,
                Valoración_A=ValoracionFactor('Nivel II', 20),
                Valoración_B=ValoracionFactor('Nivel II', 20),
                Valoración_C=ValoracionFactor('Nivel II', 20),
                Valoración_D=ValoracionFactor('Nivel II', 20),
                Valoración_E=ValoracionFactor('Nivel II', 20),
                ID_Superior=6
            ),
        ]
    
    def load_data(self, data_file: str):
        """Load positions from JSON file."""
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.puestos = []
            for item in data:
                puesto = Puesto(
                    ID_Puesto=item['ID_Puesto'],
                    Código_Interno=item['Código_Interno'],
                    Denominacion=item['Denominacion'],
                    Número_Vacantes=item['Número_Vacantes'],
                    Área=item['Área'],
                    Descripción_Funciones=item['Descripción_Funciones'],
                    Salario=item['Salario'],
                    Valoración_A=ValoracionFactor(**item['Valoración_A']),
                    Valoración_B=ValoracionFactor(**item['Valoración_B']),
                    Valoración_C=ValoracionFactor(**item['Valoración_C']),
                    Valoración_D=ValoracionFactor(**item['Valoración_D']),
                    Valoración_E=ValoracionFactor(**item['Valoración_E']),
                    ID_Superior=item.get('ID_Superior')
                )
                self.puestos.append(puesto)
    
    def save_data(self, data_file: str):
        """Save positions to JSON file."""
        data = [p.to_dict() for p in self.puestos]
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # QUERYING FUNCTIONS
    
    def get_by_codigo_interno(self, codigo: str) -> Optional[Puesto]:
        """Retrieve a position by its internal code."""
        for puesto in self.puestos:
            if puesto.Código_Interno == codigo:
                return puesto
        return None
    
    def get_by_id(self, id_puesto: int) -> Optional[Puesto]:
        """Retrieve a position by its ID."""
        for puesto in self.puestos:
            if puesto.ID_Puesto == id_puesto:
                return puesto
        return None
    
    def get_by_denominacion(self, denominacion: str) -> Optional[Puesto]:
        """Retrieve a position by its name."""
        for puesto in self.puestos:
            if puesto.Denominacion.lower() == denominacion.lower():
                return puesto
        return None
    
    def list_positions(self, **criteria) -> List[Puesto]:
        """
        List positions based on criteria.
        Supports: numero_vacantes__gt, numero_vacantes__lt, area, etc.
        """
        results = []
        
        for puesto in self.puestos:
            match = True
            
            for key, value in criteria.items():
                if '__gt' in key:
                    field = key.replace('__gt', '')
                    if field == 'numero_vacantes':
                        if puesto.Número_Vacantes <= value:
                            match = False
                            break
                elif '__lt' in key:
                    field = key.replace('__lt', '')
                    if field == 'numero_vacantes':
                        if puesto.Número_Vacantes >= value:
                            match = False
                            break
                elif '__gte' in key:
                    field = key.replace('__gte', '')
                    if field == 'numero_vacantes':
                        if puesto.Número_Vacantes < value:
                            match = False
                            break
                elif key == 'area':
                    if puesto.Área.lower() != value.lower():
                        match = False
                        break
            
            if match:
                results.append(puesto)
        
        return results
    
    # ANALYSIS FUNCTIONS
    
    def calculate_total_valoracion(self, denominacion: str) -> Optional[int]:
        """Calculate total valoration score for a position."""
        puesto = self.get_by_denominacion(denominacion)
        if puesto:
            return puesto.get_total_valoracion()
        return None
    
    def filter_by_valoracion_level(self, factor: str, min_nivel: str) -> List[Puesto]:
        """
        Filter positions by minimum valoración level for a specific factor.
        Example: filter_by_valoracion_level('C', 'Nivel III')
        """
        nivel_values = {
            'Nivel I': 1,
            'Nivel II': 2,
            'Nivel III': 3,
            'Nivel IV': 4,
            'Nivel V': 5
        }
        
        min_value = nivel_values.get(min_nivel, 0)
        results = []
        
        for puesto in self.puestos:
            factor_attr = f'Valoración_{factor}'
            if hasattr(puesto, factor_attr):
                valoracion = getattr(puesto, factor_attr)
                current_value = nivel_values.get(valoracion.nivel, 0)
                if current_value >= min_value:
                    results.append(puesto)
        
        return results
    
    # ORGANIZATIONAL FUNCTIONS
    
    def get_hierarchy_chain(self, id_puesto: int) -> List[Puesto]:
        """
        Get the full hierarchy chain from a position to the top level.
        Returns list from position to root (top-level position).
        """
        chain = []
        current = self.get_by_id(id_puesto)
        
        while current:
            chain.append(current)
            if current.ID_Superior is None:
                break
            current = self.get_by_id(current.ID_Superior)
        
        return chain
    
    def get_direct_subordinates(self, id_puesto: int) -> List[Puesto]:
        """Get direct subordinates of a position."""
        subordinates = []
        for puesto in self.puestos:
            if puesto.ID_Superior == id_puesto:
                subordinates.append(puesto)
        return subordinates
    
    def get_all_subordinates(self, id_puesto: int) -> List[Puesto]:
        """Get all subordinates (recursive) of a position."""
        all_subordinates = []
        direct = self.get_direct_subordinates(id_puesto)
        
        for subordinate in direct:
            all_subordinates.append(subordinate)
            all_subordinates.extend(self.get_all_subordinates(subordinate.ID_Puesto))
        
        return all_subordinates
    
    def describe_hierarchy(self, id_puesto: int) -> str:
        """
        Describe the hierarchy chain in text format.
        """
        chain = self.get_hierarchy_chain(id_puesto)
        if not chain:
            return "Puesto no encontrado"
        
        chain.reverse()  # Show from top to position
        
        lines = []
        lines.append("Cadena de mando:")
        for i, puesto in enumerate(chain):
            indent = "  " * i
            arrow = "└─ " if i > 0 else ""
            lines.append(f"{indent}{arrow}{puesto.Denominacion} (ID: {puesto.ID_Puesto})")
        
        return "\n".join(lines)
    
    # COMPARISON FUNCTIONS
    
    def compare_positions(self, denominaciones: List[str], factors: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Compare multiple positions based on specific factors.
        If factors is None, compares all factors.
        """
        if factors is None:
            factors = ['A', 'B', 'C', 'D', 'E']
        
        comparison = {
            'positions': [],
            'factors': {}
        }
        
        puestos = []
        for denominacion in denominaciones:
            puesto = self.get_by_denominacion(denominacion)
            if puesto:
                puestos.append(puesto)
                comparison['positions'].append(denominacion)
        
        for factor in factors:
            comparison['factors'][factor] = {}
            for puesto in puestos:
                factor_attr = f'Valoración_{factor}'
                if hasattr(puesto, factor_attr):
                    valoracion = getattr(puesto, factor_attr)
                    comparison['factors'][factor][puesto.Denominacion] = {
                        'nivel': valoracion.nivel,
                        'puntuacion': valoracion.puntuacion
                    }
        
        return comparison
    
    def get_average_salary_by_area(self, area: str) -> Optional[float]:
        """Calculate average salary for positions in a specific area."""
        positions_in_area = [p for p in self.puestos if p.Área.lower() == area.lower()]
        
        if not positions_in_area:
            return None
        
        total_salary = sum(p.Salario for p in positions_in_area)
        return total_salary / len(positions_in_area)
    
    def get_statistics_by_area(self) -> Dict[str, Any]:
        """Get statistics grouped by area."""
        areas = {}
        
        for puesto in self.puestos:
            if puesto.Área not in areas:
                areas[puesto.Área] = {
                    'count': 0,
                    'total_salary': 0,
                    'avg_salary': 0,
                    'total_vacantes': 0,
                    'positions': []
                }
            
            areas[puesto.Área]['count'] += 1
            areas[puesto.Área]['total_salary'] += puesto.Salario
            areas[puesto.Área]['total_vacantes'] += puesto.Número_Vacantes
            areas[puesto.Área]['positions'].append(puesto.Denominacion)
        
        for area in areas:
            areas[area]['avg_salary'] = areas[area]['total_salary'] / areas[area]['count']
        
        return areas
    
    # DATA EXPLANATION FUNCTIONS
    
    def explain_factor(self, factor: str) -> str:
        """Explain what a valuation factor represents."""
        return self.FACTOR_DESCRIPTIONS.get(factor, f"Factor {factor} no encontrado")
    
    def get_factor_score_by_level(self, nivel: str) -> int:
        """Get the standard score for a given level."""
        return self.STANDARD_SCORES.get(nivel, 0)
    
    def explain_all_factors(self) -> Dict[str, str]:
        """Get explanations for all valuation factors."""
        return self.FACTOR_DESCRIPTIONS.copy()
    
    def get_position_details(self, denominacion: str) -> Optional[Dict[str, Any]]:
        """Get complete details of a position in a structured format."""
        puesto = self.get_by_denominacion(denominacion)
        if not puesto:
            return None
        
        details = puesto.to_dict()
        details['Puntuación_Total'] = puesto.get_total_valoracion()
        
        # Add hierarchy information
        chain = self.get_hierarchy_chain(puesto.ID_Puesto)
        if len(chain) > 1:
            details['Superior'] = chain[1].Denominacion
        else:
            details['Superior'] = 'Ninguno (Nivel máximo)'
        
        subordinates = self.get_direct_subordinates(puesto.ID_Puesto)
        details['Subordinados_Directos'] = [s.Denominacion for s in subordinates]
        
        return details
