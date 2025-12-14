"""
RPT System - Example Implementation
Sistema RPT - Implementación de Ejemplo

This module demonstrates how to implement the constraints and formatting
guidelines defined in CONSTRAINTS.md and rpt_config.py
"""

from rpt_config import (
    get_error_message,
    format_table_data,
    format_list_data,
    validate_id_format,
    should_respond_in_spanish,
    ConstraintsValidator,
    FIELD_NAMES_ES
)


# Example: Mock database tables
# In a real application, these would be actual database tables
MOCK_TABLES = {
    "puestos_trabajo": {
        "ID-1234": {
            "id": "ID-1234",
            "name": "Técnico de Sistemas Senior",
            "department": "Tecnologías de la Información",
            "level": 22,
            "description": "Gestión y mantenimiento de sistemas informáticos"
        },
        "ID-5678": {
            "id": "ID-5678",
            "name": "Analista de Recursos Humanos",
            "department": "Recursos Humanos",
            "level": 18,
            "description": "Análisis y gestión de personal"
        }
    },
    "factores_valoracion": {
        "ID-1234": {
            "complexity": "8/10",
            "responsibility": "7/10",
            "experience": "5 años"
        },
        "ID-5678": {
            "complexity": "6/10",
            "responsibility": "6/10",
            "experience": "3 años"
        }
    },
    "estructura_organizativa": {
        "DEPT-001": {
            "id": "DEPT-001",
            "name": "Tecnologías de la Información",
            "head": "Juan García",
            "employees": 15
        },
        "DEPT-002": {
            "id": "DEPT-002",
            "name": "Recursos Humanos",
            "head": "María López",
            "employees": 8
        }
    },
    "niveles_retributivos": {
        18: {"salary_min": 28000, "salary_max": 35000, "benefits": "Estándar"},
        22: {"salary_min": 35000, "salary_max": 45000, "benefits": "Completo"}
    }
}


class RPTSystem:
    """
    RPT System implementation that follows all constraints.
    Sistema RPT que sigue todas las restricciones definidas.
    """
    
    def __init__(self):
        self.validator = ConstraintsValidator()
    
    def get_position_info(self, position_id: str, translate: bool = False) -> str:
        """
        Get information about a position.
        Always responds in Spanish unless translate=True.
        
        Args:
            position_id: Position ID to query
            translate: Whether to provide translation
            
        Returns:
            Formatted response in Markdown
        """
        # Validation: Check ID format
        if not validate_id_format(position_id, "position"):
            return get_error_message(
                "invalid_id",
                id=position_id,
                expected_format="ID-XXXX (ej: ID-1234)"
            )
        
        # Strict Accuracy: Fetch directly from table
        position_data = MOCK_TABLES["puestos_trabajo"].get(position_id)
        
        # Error Handling: Position not found
        if not position_data:
            return get_error_message("position_not_found", id=position_id)
        
        # Format response in Spanish with Markdown
        response = "# 📋 Información del Puesto\n\n"
        
        # Use table formatting
        response += format_table_data(position_data)
        
        # Add valuation factors if available
        factors = MOCK_TABLES["factores_valoracion"].get(position_id)
        if factors:
            response += "\n**Factores de Valoración:**\n"
            for factor, value in factors.items():
                factor_es = FIELD_NAMES_ES.get(factor, factor)
                response += f"- {factor_es}: {value}\n"
        
        # Add salary information
        level = position_data.get("level")
        if level and level in MOCK_TABLES["niveles_retributivos"]:
            salary_info = MOCK_TABLES["niveles_retributivos"][level]
            response += f"\n**Información Retributiva:**\n"
            response += f"- Salario Mínimo: €{salary_info['salary_min']:,}\n"
            response += f"- Salario Máximo: €{salary_info['salary_max']:,}\n"
            response += f"- Beneficios: {salary_info['benefits']}\n"
        
        # Validate constraints
        validation = self.validator.validate_all(
            position_data,
            response,
            "puestos_trabajo"
        )
        
        if not validation["all_passed"]:
            response += "\n\n⚠️ *Advertencia: La respuesta no cumple todos los requisitos de formato*"
        
        return response
    
    def get_factor_info(self, position_id: str) -> str:
        """
        Get valuation factors for a position.
        
        Args:
            position_id: Position ID to query
            
        Returns:
            Formatted response in Markdown (Spanish)
        """
        # Check if position exists
        if position_id not in MOCK_TABLES["puestos_trabajo"]:
            return get_error_message("position_not_found", id=position_id)
        
        # Fetch factors from table
        factors = MOCK_TABLES["factores_valoracion"].get(position_id)
        
        if not factors:
            return f"""# 📊 Factores de Valoración - {position_id}

⚠️ **Sin datos disponibles**

No hay factores de valoración definidos para este puesto en las tablas actuales del RPT."""
        
        # Format response
        response = f"# 📊 Factores de Valoración - {position_id}\n\n"
        
        # Create table with factors
        factors_table = "| Factor | Valor |\n"
        factors_table += "|--------|-------|\n"
        
        for factor, value in factors.items():
            factor_es = FIELD_NAMES_ES.get(factor, factor)
            factors_table += f"| **{factor_es}** | {value} |\n"
        
        response += factors_table
        
        return response
    
    def list_all_positions(self) -> str:
        """
        List all available positions.
        
        Returns:
            Formatted list in Spanish with Markdown
        """
        response = "# 📋 Listado de Puestos de Trabajo\n\n"
        
        if not MOCK_TABLES["puestos_trabajo"]:
            return response + get_error_message("no_data")
        
        response += "| ID | Nombre | Departamento | Nivel |\n"
        response += "|----|--------|--------------|-------|\n"
        
        for pos_id, pos_data in MOCK_TABLES["puestos_trabajo"].items():
            response += f"| {pos_data['id']} | {pos_data['name']} | "
            response += f"{pos_data['department']} | {pos_data['level']} |\n"
        
        response += f"\n**Total de puestos**: {len(MOCK_TABLES['puestos_trabajo'])}\n"
        
        return response
    
    def get_department_info(self, dept_id: str) -> str:
        """
        Get information about a department.
        
        Args:
            dept_id: Department ID
            
        Returns:
            Formatted response in Spanish with Markdown
        """
        # Fetch from organizational structure table
        dept_data = MOCK_TABLES["estructura_organizativa"].get(dept_id)
        
        if not dept_data:
            available = list(MOCK_TABLES["estructura_organizativa"].keys())
            return get_error_message(
                "department_not_found",
                name=dept_id
            ) + f"\n\nDepartamentos disponibles: {', '.join(available)}"
        
        response = "# 🏢 Información del Departamento\n\n"
        response += format_table_data(dept_data)
        
        # List positions in this department
        dept_name = dept_data["name"]
        positions_in_dept = [
            pos_data for pos_data in MOCK_TABLES["puestos_trabajo"].values()
            if pos_data["department"] == dept_name
        ]
        
        if positions_in_dept:
            response += "\n**Puestos en este departamento:**\n"
            for pos in positions_in_dept:
                response += f"- {pos['name']} ({pos['id']})\n"
        
        return response
    
    def search_by_level(self, level: int) -> str:
        """
        Search positions by retributive level.
        
        Args:
            level: Retributive level to search
            
        Returns:
            Formatted response in Spanish
        """
        matching_positions = [
            pos_data for pos_data in MOCK_TABLES["puestos_trabajo"].values()
            if pos_data.get("level") == level
        ]
        
        response = f"# 🔍 Búsqueda por Nivel Retributivo: {level}\n\n"
        
        if not matching_positions:
            response += f"⚠️ No se encontraron puestos con nivel retributivo {level}.\n"
            return response
        
        response += "| ID | Nombre | Departamento |\n"
        response += "|----|--------|-------------|\n"
        
        for pos in matching_positions:
            response += f"| {pos['id']} | {pos['name']} | {pos['department']} |\n"
        
        response += f"\n**Total encontrado**: {len(matching_positions)} puesto(s)\n"
        
        # Add level salary information if available
        if level in MOCK_TABLES["niveles_retributivos"]:
            salary_info = MOCK_TABLES["niveles_retributivos"][level]
            response += f"\n**Información del Nivel {level}:**\n"
            response += f"- Rango salarial: €{salary_info['salary_min']:,} - €{salary_info['salary_max']:,}\n"
            response += f"- Beneficios: {salary_info['benefits']}\n"
        
        return response


def main():
    """
    Demonstrate the RPT system with examples.
    Demostración del sistema RPT con ejemplos.
    """
    system = RPTSystem()
    
    print("=" * 80)
    print("SISTEMA RPT - DEMOSTRACIÓN DE RESTRICCIONES Y FORMATO")
    print("=" * 80)
    print()
    
    # Example 1: Successful query
    print("Ejemplo 1: Consulta exitosa")
    print("-" * 80)
    result1 = system.get_position_info("ID-1234")
    print(result1)
    print()
    
    # Example 2: Position not found
    print("Ejemplo 2: Posición no encontrada")
    print("-" * 80)
    result2 = system.get_position_info("ID-9999")
    print(result2)
    print()
    
    # Example 3: Invalid ID format
    print("Ejemplo 3: Formato de ID inválido")
    print("-" * 80)
    result3 = system.get_position_info("INVALID")
    print(result3)
    print()
    
    # Example 4: List all positions
    print("Ejemplo 4: Listado de todas las posiciones")
    print("-" * 80)
    result4 = system.list_all_positions()
    print(result4)
    print()
    
    # Example 5: Search by level
    print("Ejemplo 5: Búsqueda por nivel retributivo")
    print("-" * 80)
    result5 = system.search_by_level(22)
    print(result5)
    print()
    
    # Example 6: Department info
    print("Ejemplo 6: Información de departamento")
    print("-" * 80)
    result6 = system.get_department_info("DEPT-001")
    print(result6)
    print()
    
    # Example 7: Factors for a position
    print("Ejemplo 7: Factores de valoración")
    print("-" * 80)
    result7 = system.get_factor_info("ID-1234")
    print(result7)
    print()


if __name__ == "__main__":
    main()
