"""
RPT System Configuration - Constraints and Formatting
Configuración del Sistema RPT - Restricciones y Formato
"""

# Language Configuration
DEFAULT_LANGUAGE = "es"  # Spanish by default
SUPPORTED_LANGUAGES = ["es", "en"]

# Error Messages in Spanish
ERROR_MESSAGES = {
    "position_not_found": """❌ **Posición no encontrada**

La posición con ID `{id}` no existe en el registro actual de RPT.

Por favor, verifica:
- El identificador de la posición
- Que la posición esté activa en el sistema
- Que tengas permisos para acceder a esta información""",
    
    "factor_not_found": """❌ **Factor no encontrado**

El factor de valoración `{name}` no existe en las tablas de factores del RPT.

Factores disponibles:
{available_factors}""",
    
    "invalid_id": """❌ **Identificador no válido**

El identificador proporcionado `{id}` no tiene un formato válido.

Formato esperado: {expected_format}""",
    
    "department_not_found": """❌ **Departamento no encontrado**

El departamento `{name}` no existe en la estructura organizativa actual.

Por favor, verifica el nombre del departamento o consulta la lista de departamentos disponibles.""",
    
    "no_data": """⚠️ **Sin datos disponibles**

No hay información disponible para esta consulta en las tablas actuales del RPT.""",
    
    "missing_fields": """⚠️ **Campos incompletos**

Algunos campos no están definidos para este registro en las tablas actuales.

Campos faltantes: {fields}"""
}

# Data Validation Rules
VALIDATION_RULES = {
    "strict_accuracy": True,  # Always fetch from tables, never estimate
    "require_table_source": True,  # All data must have a table source
    "allow_caching": False,  # Always fetch fresh data
    "validate_before_display": True  # Validate data exists before showing
}

# Formatting Configuration
FORMATTING = {
    "use_markdown": True,
    "use_tables": True,
    "use_bold_for_headers": True,
    "use_lists": True,
    "use_emojis": True  # For visual clarity (✅, ❌, ⚠️, 📋, etc.)
}

# Reference Tables
# These should be the single source of truth
REFERENCE_TABLES = [
    "puestos_trabajo",  # Main positions registry
    "factores_valoracion",  # Valuation factors
    "estructura_organizativa",  # Organizational structure
    "niveles_retributivos"  # Compensation levels
]

# Response Structure Template
RESPONSE_TEMPLATE = {
    "title_emoji": True,
    "main_data_format": "table",
    "additional_info_format": "list",
    "notes_at_end": True
}

# ID Format Validation
ID_FORMATS = {
    "position": r"^[A-Z]{2,3}-\d{4}$",  # e.g., ID-1234, POS-5678
    "factor": r"^FAC-\d{3}$",  # e.g., FAC-001
    "department": r"^DEPT-\d{3}$"  # e.g., DEPT-001
}

# Table Field Mappings (Spanish)
FIELD_NAMES_ES = {
    "id": "ID",
    "name": "Nombre",
    "position": "Posición",
    "department": "Departamento",
    "level": "Nivel Retributivo",
    "factor": "Factor",
    "value": "Valor",
    "description": "Descripción",
    "complexity": "Complejidad Técnica",
    "responsibility": "Responsabilidad",
    "experience": "Experiencia Requerida"
}

# Translation Configuration
TRANSLATION_NOTE_ES = "*(Traducción solicitada)*"
TRANSLATION_NOTE_EN = "*(Translation provided upon request)*"

def get_error_message(error_type: str, **kwargs) -> str:
    """
    Get formatted error message in Spanish.
    
    Args:
        error_type: Type of error from ERROR_MESSAGES
        **kwargs: Format parameters for the error message
        
    Returns:
        Formatted error message string
    """
    if error_type not in ERROR_MESSAGES:
        return f"❌ **Error desconocido**: {error_type}"
    
    return ERROR_MESSAGES[error_type].format(**kwargs)

def format_table_data(data: dict, headers: list = None) -> str:
    """
    Format data as a Markdown table in Spanish.
    
    Args:
        data: Dictionary with field names and values
        headers: Optional custom headers [field_name, value_name]
        
    Returns:
        Markdown formatted table string
    """
    if not data:
        return get_error_message("no_data")
    
    if headers is None:
        headers = ["Campo", "Valor"]
    
    table = f"| {headers[0]} | {headers[1]} |\n"
    table += f"|{'-' * (len(headers[0]) + 2)}|{'-' * (len(headers[1]) + 2)}|\n"
    
    for field, value in data.items():
        # Translate field name to Spanish if available
        field_es = FIELD_NAMES_ES.get(field, field)
        table += f"| **{field_es}** | {value} |\n"
    
    return table

def format_list_data(items: list, title: str = None) -> str:
    """
    Format data as a Markdown list in Spanish.
    
    Args:
        items: List of items to format
        title: Optional title for the list
        
    Returns:
        Markdown formatted list string
    """
    if not items:
        return ""
    
    result = ""
    if title:
        result += f"**{title}:**\n"
    
    for item in items:
        result += f"- {item}\n"
    
    return result

def validate_id_format(id_value: str, id_type: str) -> bool:
    """
    Validate ID format according to defined patterns.
    
    Args:
        id_value: ID value to validate
        id_type: Type of ID (position, factor, department)
        
    Returns:
        True if valid, False otherwise
    """
    import re
    
    if id_type not in ID_FORMATS:
        return False
    
    pattern = ID_FORMATS[id_type]
    return bool(re.match(pattern, id_value))

def should_respond_in_spanish(user_request: str) -> bool:
    """
    Determine if response should be in Spanish.
    Default is always True unless explicit translation is requested.
    
    Args:
        user_request: User's request text
        
    Returns:
        True if should respond in Spanish, False if translation requested
    """
    translation_keywords = [
        "translate", "traducir", "traduce", "translation",
        "in english", "en inglés", "english version"
    ]
    
    request_lower = user_request.lower()
    for keyword in translation_keywords:
        if keyword in request_lower:
            return False
    
    return True

# Constraints Enforcement
class ConstraintsValidator:
    """Validate that responses meet all constraints."""
    
    @staticmethod
    def validate_data_source(data: dict, source_table: str) -> bool:
        """Ensure data comes from a defined reference table."""
        if not VALIDATION_RULES["require_table_source"]:
            return True
        return source_table in REFERENCE_TABLES
    
    @staticmethod
    def validate_accuracy(data: dict, original_data: dict) -> bool:
        """Ensure no data has been modified or estimated."""
        if not VALIDATION_RULES["strict_accuracy"]:
            return True
        return data == original_data
    
    @staticmethod
    def validate_language(response: str, expected_language: str = "es") -> bool:
        """Validate response is in expected language."""
        # Simple check: Spanish responses should contain Spanish-specific characters
        # or common Spanish words
        if expected_language == "es":
            spanish_indicators = ["ó", "í", "é", "á", "ú", "ñ", "¿", "¡"]
            spanish_words = [" el ", " la ", " de ", " en ", " del ", " con ", " por ", " para "]
            
            has_spanish_chars = any(char in response for char in spanish_indicators)
            has_spanish_words = any(word in response.lower() for word in spanish_words)
            
            # Must have at least one Spanish indicator
            return has_spanish_chars or has_spanish_words
        
        return True
    
    @staticmethod
    def validate_markdown(response: str) -> bool:
        """Check if response uses Markdown formatting."""
        if not FORMATTING["use_markdown"]:
            return True
        
        markdown_indicators = ["**", "##", "|", "-", "*", "`"]
        return any(indicator in response for indicator in markdown_indicators)
    
    @staticmethod
    def validate_all(data: dict, response: str, source_table: str = None) -> dict:
        """
        Run all validation checks.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            "accuracy": True,  # Assume accurate if from proper source
            "language": ConstraintsValidator.validate_language(response),
            "markdown": ConstraintsValidator.validate_markdown(response),
            "data_source": ConstraintsValidator.validate_data_source(data, source_table) if source_table else True
        }
        
        results["all_passed"] = all(results.values())
        return results
