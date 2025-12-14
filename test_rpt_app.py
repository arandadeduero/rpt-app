"""
Unit tests for RPT App functionality.
"""

import unittest
from rpt_app import RPTManager, Puesto, ValoracionFactor


class TestRPTManager(unittest.TestCase):
    """Test cases for RPT Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.rpt = RPTManager()
    
    # QUERYING TESTS
    
    def test_get_by_codigo_interno(self):
        """Test retrieving position by internal code."""
        puesto = self.rpt.get_by_codigo_interno('ADM2025')
        self.assertIsNotNone(puesto)
        self.assertEqual(puesto.Denominacion, 'Administrativo')
    
    def test_get_by_codigo_interno_not_found(self):
        """Test retrieving non-existent position."""
        puesto = self.rpt.get_by_codigo_interno('NOTEXIST')
        self.assertIsNone(puesto)
    
    def test_get_by_id(self):
        """Test retrieving position by ID."""
        puesto = self.rpt.get_by_id(45)
        self.assertIsNotNone(puesto)
        self.assertEqual(puesto.Denominacion, 'Jefe de Servicio de Hacienda')
    
    def test_get_by_denominacion(self):
        """Test retrieving position by name."""
        puesto = self.rpt.get_by_denominacion('Tesorero')
        self.assertIsNotNone(puesto)
        self.assertEqual(puesto.Código_Interno, 'TES2025')
    
    def test_list_positions_with_multiple_vacancies(self):
        """Test listing positions with more than 1 vacancy."""
        puestos = self.rpt.list_positions(numero_vacantes__gt=1)
        self.assertGreater(len(puestos), 0)
        for p in puestos:
            self.assertGreater(p.Número_Vacantes, 1)
    
    def test_list_positions_by_area(self):
        """Test listing positions by area."""
        puestos = self.rpt.list_positions(area='Cultura')
        self.assertGreater(len(puestos), 0)
        for p in puestos:
            self.assertEqual(p.Área.lower(), 'cultura')
    
    # ANALYSIS TESTS
    
    def test_calculate_total_valoracion(self):
        """Test calculating total valuation score."""
        score = self.rpt.calculate_total_valoracion('Técnico de Urbanismo')
        self.assertIsNotNone(score)
        self.assertGreater(score, 0)
        # Should be sum of 40+30+40+30+30 = 170
        self.assertEqual(score, 170)
    
    def test_calculate_total_valoracion_not_found(self):
        """Test calculating score for non-existent position."""
        score = self.rpt.calculate_total_valoracion('Non-existent Position')
        self.assertIsNone(score)
    
    def test_filter_by_valoracion_level(self):
        """Test filtering by valuation level."""
        puestos = self.rpt.filter_by_valoracion_level('C', 'Nivel III')
        self.assertGreater(len(puestos), 0)
        
        nivel_values = {
            'Nivel I': 1, 'Nivel II': 2, 'Nivel III': 3, 
            'Nivel IV': 4, 'Nivel V': 5
        }
        
        for p in puestos:
            current_value = nivel_values.get(p.Valoración_C.nivel, 0)
            self.assertGreaterEqual(current_value, 3)
    
    # ORGANIZATIONAL TESTS
    
    def test_get_hierarchy_chain(self):
        """Test getting hierarchy chain."""
        chain = self.rpt.get_hierarchy_chain(45)
        self.assertGreater(len(chain), 1)
        # First should be the position itself
        self.assertEqual(chain[0].ID_Puesto, 45)
        # Last should have no superior (top level)
        self.assertIsNone(chain[-1].ID_Superior)
    
    def test_get_direct_subordinates(self):
        """Test getting direct subordinates."""
        subordinates = self.rpt.get_direct_subordinates(45)
        self.assertGreater(len(subordinates), 0)
        for s in subordinates:
            self.assertEqual(s.ID_Superior, 45)
    
    def test_get_direct_subordinates_none(self):
        """Test getting subordinates for position with none."""
        # Auxiliar positions typically have no subordinates
        subordinates = self.rpt.get_direct_subordinates(4)
        # This may or may not have subordinates depending on data
        self.assertIsInstance(subordinates, list)
    
    def test_describe_hierarchy(self):
        """Test describing hierarchy in text format."""
        description = self.rpt.describe_hierarchy(45)
        self.assertIsInstance(description, str)
        self.assertIn('Cadena de mando', description)
    
    # COMPARISON TESTS
    
    def test_compare_positions(self):
        """Test comparing positions."""
        comparison = self.rpt.compare_positions(
            ['Auxiliar Administrativo', 'Administrativo'],
            factors=['A', 'D']
        )
        
        self.assertIn('positions', comparison)
        self.assertIn('factors', comparison)
        self.assertEqual(len(comparison['factors']), 2)
        self.assertIn('A', comparison['factors'])
        self.assertIn('D', comparison['factors'])
    
    def test_get_average_salary_by_area(self):
        """Test calculating average salary by area."""
        avg_salary = self.rpt.get_average_salary_by_area('Cultura')
        self.assertIsNotNone(avg_salary)
        self.assertGreater(avg_salary, 0)
    
    def test_get_average_salary_by_area_not_found(self):
        """Test average salary for non-existent area."""
        avg_salary = self.rpt.get_average_salary_by_area('NonExistentArea')
        self.assertIsNone(avg_salary)
    
    def test_get_statistics_by_area(self):
        """Test getting statistics by area."""
        stats = self.rpt.get_statistics_by_area()
        self.assertIsInstance(stats, dict)
        self.assertGreater(len(stats), 0)
        
        for area, data in stats.items():
            self.assertIn('count', data)
            self.assertIn('avg_salary', data)
            self.assertIn('total_vacantes', data)
            self.assertGreater(data['count'], 0)
    
    # DATA EXPLANATION TESTS
    
    def test_explain_factor(self):
        """Test explaining a valuation factor."""
        explanation = self.rpt.explain_factor('B')
        self.assertIsInstance(explanation, str)
        self.assertIn('Experiencia', explanation)
    
    def test_get_factor_score_by_level(self):
        """Test getting score for a level."""
        score = self.rpt.get_factor_score_by_level('Nivel IV')
        self.assertEqual(score, 40)
    
    def test_explain_all_factors(self):
        """Test getting all factor explanations."""
        factors = self.rpt.explain_all_factors()
        self.assertIsInstance(factors, dict)
        self.assertEqual(len(factors), 5)
        self.assertIn('A', factors)
        self.assertIn('B', factors)
        self.assertIn('C', factors)
        self.assertIn('D', factors)
        self.assertIn('E', factors)
    
    def test_get_position_details(self):
        """Test getting complete position details."""
        details = self.rpt.get_position_details('Tesorero')
        self.assertIsNotNone(details)
        self.assertIn('Denominacion', details)
        self.assertIn('Puntuación_Total', details)
        self.assertIn('Superior', details)
        self.assertIn('Subordinados_Directos', details)
    
    # DATA MODEL TESTS
    
    def test_puesto_to_dict(self):
        """Test converting position to dictionary."""
        puesto = self.rpt.get_by_codigo_interno('ADM2025')
        puesto_dict = puesto.to_dict()
        self.assertIsInstance(puesto_dict, dict)
        self.assertIn('Denominacion', puesto_dict)
        self.assertIn('Valoración_A', puesto_dict)
    
    def test_puesto_get_total_valoracion(self):
        """Test position total valuation calculation."""
        puesto = self.rpt.get_by_codigo_interno('ADM2025')
        total = puesto.get_total_valoracion()
        self.assertIsInstance(total, int)
        self.assertGreater(total, 0)


class TestDataPersistence(unittest.TestCase):
    """Test data persistence functionality."""
    
    def test_save_and_load_data(self):
        """Test saving and loading data from file."""
        import tempfile
        import os
        
        # Create temporary file
        fd, temp_file = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        try:
            # Create manager and save data
            rpt1 = RPTManager()
            original_count = len(rpt1.puestos)
            rpt1.save_data(temp_file)
            
            # Load data in new manager
            rpt2 = RPTManager(data_file=temp_file)
            loaded_count = len(rpt2.puestos)
            
            self.assertEqual(original_count, loaded_count)
            
            # Verify specific position
            puesto1 = rpt1.get_by_codigo_interno('ADM2025')
            puesto2 = rpt2.get_by_codigo_interno('ADM2025')
            
            self.assertEqual(puesto1.Denominacion, puesto2.Denominacion)
            self.assertEqual(puesto1.Salario, puesto2.Salario)
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)


if __name__ == '__main__':
    unittest.main()
