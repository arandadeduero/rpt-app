-- Sample Data for Valoración Factors Tables
-- This file contains example data for the five valuation factors

-- =====================================================
-- Factor A: Sample Data
-- Example: Education/Academic Qualification
-- =====================================================
INSERT INTO Valoracion_Factor_A (nivel, descripcion, puntuacion) VALUES
('I', 'Sin requisitos académicos específicos', 0),
('II', 'Educación Secundaria Obligatoria (ESO)', 80),
('III', 'Bachillerato o Formación Profesional de Grado Medio', 160),
('IV', 'Formación Profesional de Grado Superior o Diplomatura', 280),
('V', 'Licenciatura, Grado Universitario o superior', 400);

-- =====================================================
-- Factor B: Sample Data
-- Example: Professional Experience
-- =====================================================
INSERT INTO Valoracion_Factor_B (nivel, descripcion, puntuacion) VALUES
('I', 'Sin experiencia requerida', 0),
('II', 'Hasta 1 año de experiencia', 80),
('III', 'De 1 a 3 años de experiencia', 160),
('IV', 'De 3 a 5 años de experiencia', 280),
('V', 'Más de 5 años de experiencia', 400);

-- =====================================================
-- Factor C: Sample Data
-- Example: Complexity and Responsibility
-- =====================================================
INSERT INTO Valoracion_Factor_C (nivel, descripcion, puntuacion) VALUES
('I', 'Tareas simples y rutinarias', 0),
('II', 'Tareas con alguna variedad y complejidad baja', 80),
('III', 'Tareas variadas con complejidad media', 160),
('IV', 'Tareas complejas con alta responsabilidad', 280),
('V', 'Tareas muy complejas con máxima responsabilidad', 400);

-- =====================================================
-- Factor D: Sample Data
-- Example: Autonomy and Decision Making
-- =====================================================
INSERT INTO Valoracion_Factor_D (nivel, descripcion, puntuacion) VALUES
('I', 'Supervisión constante, sin autonomía', 0),
('II', 'Supervisión frecuente, autonomía limitada', 80),
('III', 'Supervisión ocasional, autonomía moderada', 160),
('IV', 'Supervisión mínima, alta autonomía', 280),
('V', 'Autonomía completa, decisiones estratégicas', 400);

-- =====================================================
-- Factor E: Sample Data
-- Example: Skills and Competencies
-- =====================================================
INSERT INTO Valoracion_Factor_E (nivel, descripcion, puntuacion) VALUES
('I', 'Competencias básicas', 0),
('II', 'Competencias específicas del área', 80),
('III', 'Competencias avanzadas en múltiples áreas', 160),
('IV', 'Competencias expertas y de liderazgo', 280),
('V', 'Competencias excepcionales y estratégicas', 400);

-- =====================================================
-- Sample RPT Main Table Data
-- Example positions with their valuation levels
-- =====================================================
INSERT INTO RPT_Main (codigo_puesto, denominacion, valoracion_A, valoracion_B, valoracion_C, valoracion_D, valoracion_E) VALUES
('P001', 'Auxiliar Administrativo', 'II', 'I', 'II', 'II', 'I'),
('P002', 'Técnico de Gestión', 'IV', 'III', 'III', 'III', 'III'),
('P003', 'Jefe de Servicio', 'V', 'V', 'V', 'V', 'IV'),
('P004', 'Operario de Mantenimiento', 'III', 'II', 'II', 'II', 'II'),
('P005', 'Coordinador de Proyectos', 'V', 'IV', 'IV', 'IV', 'IV');
