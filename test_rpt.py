"""
Unit Tests for RPT System Constraints
Pruebas unitarias para las restricciones del sistema RPT
"""

import unittest
import re
from rpt_config import (
    get_error_message,
    format_table_data,
    format_list_data,
    validate_id_format,
    should_respond_in_spanish,
    ConstraintsValidator,
    FIELD_NAMES_ES
)
from rpt_example import RPTSystem


class TestConstraints(unittest.TestCase):
    """Test that all constraints are properly enforced."""
    
    def setUp(self):
        self.system = RPTSystem()
        self.validator = ConstraintsValidator()
    
    def test_spanish_language_default(self):
        """Test that responses are in Spanish by default."""
        result = self.system.get_position_info("ID-1234")
        
        # Check for Spanish-specific words
        self.assertIn("Información", result)
        self.assertIn("Puesto", result)
        self.assertIn("Departamento", result)
        
        # Should not contain English equivalents
        self.assertNotIn("Information", result)
        self.assertNotIn("Position", result)
    
    def test_error_messages_in_spanish(self):
        """Test that error messages are in Spanish."""
        result = self.system.get_position_info("ID-9999")
        
        # Check for Spanish error message
        self.assertIn("no encontrada", result)
        self.assertIn("Por favor", result)
        self.assertIn("verifica", result)
    
    def test_markdown_formatting(self):
        """Test that responses use Markdown formatting."""
        result = self.system.get_position_info("ID-1234")
        
        # Check for Markdown elements
        self.assertIn("**", result)  # Bold
        self.assertIn("|", result)   # Tables
        self.assertIn("#", result)   # Headers
        self.assertIn("-", result)   # Lists or table dividers
    
    def test_table_formatting(self):
        """Test that data is presented in Markdown tables."""
        result = self.system.get_position_info("ID-1234")
        
        # Check for table structure
        self.assertIn("| Campo | Valor |", result)
        self.assertTrue("|----" in result or "|-----" in result)
    
    def test_error_handling_position_not_found(self):
        """Test polite error handling for missing position."""
        result = self.system.get_position_info("ID-9999")
        
        # Should contain error indicator
        self.assertIn("❌", result)
        self.assertIn("no encontrada", result)
        
        # Should be polite and helpful
        self.assertIn("Por favor", result)
        self.assertIn("verifica", result)
    
    def test_error_handling_invalid_id(self):
        """Test error handling for invalid ID format."""
        result = self.system.get_position_info("INVALID")
        
        self.assertIn("❌", result)
        self.assertIn("no válido", result)
        self.assertIn("Formato esperado", result)
    
    def test_id_format_validation(self):
        """Test ID format validation."""
        # Valid IDs
        self.assertTrue(validate_id_format("ID-1234", "position"))
        self.assertTrue(validate_id_format("POS-5678", "position"))
        
        # Invalid IDs
        self.assertFalse(validate_id_format("INVALID", "position"))
        self.assertFalse(validate_id_format("1234", "position"))
        self.assertFalse(validate_id_format("ID1234", "position"))
    
    def test_data_from_tables(self):
        """Test that data comes from defined tables."""
        result = self.system.get_position_info("ID-1234")
        
        # Check that actual data from mock tables appears
        self.assertIn("ID-1234", result)
        self.assertIn("Técnico de Sistemas Senior", result)
        self.assertIn("Tecnologías de la Información", result)
        self.assertIn("22", result)  # Level
    
    def test_no_estimated_data(self):
        """Test that no data is estimated or calculated."""
        result = self.system.get_position_info("ID-1234")
        
        # Should not contain estimation language
        self.assertNotIn("aproximadamente", result.lower())
        self.assertNotIn("estimado", result.lower())
        self.assertNotIn("alrededor de", result.lower())
    
    def test_list_formatting(self):
        """Test that lists are properly formatted."""
        result = self.system.get_position_info("ID-1234")
        
        # Check for list items
        self.assertIn("- ", result)
        
        # Check for list title
        self.assertIn("**Factores de Valoración:**", result)
    
    def test_emoji_usage(self):
        """Test that emojis are used for clarity."""
        # Success case
        result_success = self.system.get_position_info("ID-1234")
        self.assertIn("📋", result_success)
        
        # Error case
        result_error = self.system.get_position_info("ID-9999")
        self.assertIn("❌", result_error)
    
    def test_field_names_in_spanish(self):
        """Test that field names are translated to Spanish."""
        data = {"id": "123", "name": "Test", "department": "IT"}
        result = format_table_data(data)
        
        # Check Spanish field names
        self.assertIn("ID", result)
        self.assertIn("Nombre", result)
        self.assertIn("Departamento", result)
    
    def test_language_detection(self):
        """Test language detection for translation requests."""
        # Should respond in Spanish
        self.assertTrue(should_respond_in_spanish("Muestra el puesto ID-1234"))
        self.assertTrue(should_respond_in_spanish("Dame información"))
        
        # Should detect translation request
        self.assertFalse(should_respond_in_spanish("translate to english"))
        self.assertFalse(should_respond_in_spanish("en inglés por favor"))
    
    def test_markdown_validation(self):
        """Test Markdown validation."""
        valid_md = "# Title\n**Bold** text with |table|"
        invalid_md = "Plain text without any formatting"
        
        self.assertTrue(self.validator.validate_markdown(valid_md))
        self.assertFalse(self.validator.validate_markdown(invalid_md))
    
    def test_spanish_validation(self):
        """Test Spanish language validation."""
        spanish_text = "Esta es una respuesta en español con ñ y acentos: información"
        english_text = "This is a response in English without Spanish markers"
        
        self.assertTrue(self.validator.validate_language(spanish_text, "es"))
        self.assertFalse(self.validator.validate_language(english_text, "es"))
    
    def test_complete_validation(self):
        """Test complete constraint validation."""
        result = self.system.get_position_info("ID-1234")
        data = {"id": "ID-1234", "name": "Test"}
        
        validation = self.validator.validate_all(data, result, "puestos_trabajo")
        
        self.assertTrue(validation["language"])
        self.assertTrue(validation["markdown"])
        self.assertTrue(validation["data_source"])
        self.assertTrue(validation["all_passed"])
    
    def test_list_all_positions_format(self):
        """Test that list all positions uses proper format."""
        result = self.system.list_all_positions()
        
        # Should be in Spanish
        self.assertIn("Listado", result)
        self.assertIn("Puestos de Trabajo", result)
        
        # Should use table format
        self.assertIn("| ID |", result)
        self.assertIn("| Nombre |", result)
        
        # Should have total count
        self.assertIn("Total", result)
    
    def test_search_results_in_spanish(self):
        """Test that search results are in Spanish."""
        result = self.system.search_by_level(22)
        
        self.assertIn("Búsqueda", result)
        self.assertIn("Nivel Retributivo", result)
        self.assertIn("Total encontrado", result)
    
    def test_department_info_format(self):
        """Test department information formatting."""
        result = self.system.get_department_info("DEPT-001")
        
        # Should use proper formatting
        self.assertIn("🏢", result)
        self.assertIn("Departamento", result)
        self.assertIn("**", result)
        self.assertIn("|", result)
    
    def test_factors_format(self):
        """Test factors information formatting."""
        result = self.system.get_factor_info("ID-1234")
        
        # Should be in Spanish
        self.assertIn("Factores de Valoración", result)
        
        # Should use table
        self.assertIn("| Factor | Valor |", result)
        
        # Should have Spanish factor names
        self.assertIn("Complejidad Técnica", result)
        self.assertIn("Responsabilidad", result)


class TestErrorMessages(unittest.TestCase):
    """Test error message formatting and content."""
    
    def test_error_message_position_not_found(self):
        """Test position not found error message."""
        msg = get_error_message("position_not_found", id="ID-9999")
        
        self.assertIn("❌", msg)
        self.assertIn("ID-9999", msg)
        self.assertIn("no existe", msg)
        self.assertIn("Por favor", msg)
    
    def test_error_message_invalid_id(self):
        """Test invalid ID error message."""
        msg = get_error_message("invalid_id", id="BAD", expected_format="ID-XXXX")
        
        self.assertIn("❌", msg)
        self.assertIn("BAD", msg)
        self.assertIn("no válido", msg)
        self.assertIn("ID-XXXX", msg)
    
    def test_error_message_no_data(self):
        """Test no data error message."""
        msg = get_error_message("no_data")
        
        self.assertIn("⚠️", msg)
        self.assertIn("Sin datos", msg)
    
    def test_unknown_error_type(self):
        """Test handling of unknown error type."""
        msg = get_error_message("unknown_error_type")
        
        self.assertIn("❌", msg)
        self.assertIn("Error desconocido", msg)


class TestFormatting(unittest.TestCase):
    """Test formatting functions."""
    
    def test_format_table_data(self):
        """Test table data formatting."""
        data = {"id": "123", "name": "Test Name"}
        result = format_table_data(data)
        
        # Check table structure
        self.assertIn("| Campo | Valor |", result)
        self.assertIn("|----", result)
        self.assertIn("| **ID** | 123 |", result)
    
    def test_format_list_data(self):
        """Test list data formatting."""
        items = ["Item 1", "Item 2", "Item 3"]
        result = format_list_data(items, "Test List")
        
        self.assertIn("**Test List:**", result)
        self.assertIn("- Item 1", result)
        self.assertIn("- Item 2", result)
        self.assertIn("- Item 3", result)
    
    def test_format_empty_data(self):
        """Test formatting with empty data."""
        result_table = format_table_data({})
        result_list = format_list_data([])
        
        self.assertIn("Sin datos", result_table)
        self.assertEqual("", result_list)


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConstraints))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorMessages))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatting))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("RESUMEN DE PRUEBAS / TEST SUMMARY")
    print("=" * 80)
    print(f"Total de pruebas ejecutadas: {result.testsRun}")
    print(f"Éxitos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
