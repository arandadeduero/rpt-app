-- RPT App Database Schema
-- Valoración Factors Tables (A, B, C, D, E)

-- =====================================================
-- Factor A: Valoración Table
-- Defines the valuation criteria for Factor A
-- =====================================================
CREATE TABLE IF NOT EXISTS Valoracion_Factor_A (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel VARCHAR(20) NOT NULL, -- Level: I, II, III, IV, V
    descripcion TEXT,
    puntuacion INTEGER NOT NULL CHECK (puntuacion >= 0 AND puntuacion <= 400),
    UNIQUE(nivel)
);

-- =====================================================
-- Factor B: Valoración Table
-- Defines the valuation criteria for Factor B
-- =====================================================
CREATE TABLE IF NOT EXISTS Valoracion_Factor_B (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel VARCHAR(20) NOT NULL, -- Level: I, II, III, IV, V
    descripcion TEXT,
    puntuacion INTEGER NOT NULL CHECK (puntuacion >= 0 AND puntuacion <= 400),
    UNIQUE(nivel)
);

-- =====================================================
-- Factor C: Valoración Table
-- Defines the valuation criteria for Factor C
-- =====================================================
CREATE TABLE IF NOT EXISTS Valoracion_Factor_C (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel VARCHAR(20) NOT NULL, -- Level: I, II, III, IV, V
    descripcion TEXT,
    puntuacion INTEGER NOT NULL CHECK (puntuacion >= 0 AND puntuacion <= 400),
    UNIQUE(nivel)
);

-- =====================================================
-- Factor D: Valoración Table
-- Defines the valuation criteria for Factor D
-- =====================================================
CREATE TABLE IF NOT EXISTS Valoracion_Factor_D (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel VARCHAR(20) NOT NULL, -- Level: I, II, III, IV, V
    descripcion TEXT,
    puntuacion INTEGER NOT NULL CHECK (puntuacion >= 0 AND puntuacion <= 400),
    UNIQUE(nivel)
);

-- =====================================================
-- Factor E: Valoración Table
-- Defines the valuation criteria for Factor E
-- =====================================================
CREATE TABLE IF NOT EXISTS Valoracion_Factor_E (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel VARCHAR(20) NOT NULL, -- Level: I, II, III, IV, V
    descripcion TEXT,
    puntuacion INTEGER NOT NULL CHECK (puntuacion >= 0 AND puntuacion <= 400),
    UNIQUE(nivel)
);

-- =====================================================
-- RPT Main Table
-- Contains position information with references to valuation levels
-- =====================================================
CREATE TABLE IF NOT EXISTS RPT_Main (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_puesto VARCHAR(50) NOT NULL,
    denominacion VARCHAR(200) NOT NULL,
    
    -- Valoración Fields: Link to specific levels achieved for each factor
    valoracion_A VARCHAR(20), -- References nivel in Valoracion_Factor_A
    valoracion_B VARCHAR(20), -- References nivel in Valoracion_Factor_B
    valoracion_C VARCHAR(20), -- References nivel in Valoracion_Factor_C
    valoracion_D VARCHAR(20), -- References nivel in Valoracion_Factor_D
    valoracion_E VARCHAR(20), -- References nivel in Valoracion_Factor_E
    
    -- Calculated total score
    puntuacion_total INTEGER,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (valoracion_A) REFERENCES Valoracion_Factor_A(nivel),
    FOREIGN KEY (valoracion_B) REFERENCES Valoracion_Factor_B(nivel),
    FOREIGN KEY (valoracion_C) REFERENCES Valoracion_Factor_C(nivel),
    FOREIGN KEY (valoracion_D) REFERENCES Valoracion_Factor_D(nivel),
    FOREIGN KEY (valoracion_E) REFERENCES Valoracion_Factor_E(nivel)
);

-- =====================================================
-- View: RPT with Calculated Scores
-- Joins RPT_Main with all factor tables to show complete scoring
-- =====================================================
CREATE VIEW IF NOT EXISTS RPT_View_Complete AS
SELECT 
    r.id,
    r.codigo_puesto,
    r.denominacion,
    r.valoracion_A,
    fa.puntuacion AS puntuacion_A,
    r.valoracion_B,
    fb.puntuacion AS puntuacion_B,
    r.valoracion_C,
    fc.puntuacion AS puntuacion_C,
    r.valoracion_D,
    fd.puntuacion AS puntuacion_D,
    r.valoracion_E,
    fe.puntuacion AS puntuacion_E,
    COALESCE(fa.puntuacion, 0) + 
    COALESCE(fb.puntuacion, 0) + 
    COALESCE(fc.puntuacion, 0) + 
    COALESCE(fd.puntuacion, 0) + 
    COALESCE(fe.puntuacion, 0) AS puntuacion_total,
    r.created_at,
    r.updated_at
FROM RPT_Main r
LEFT JOIN Valoracion_Factor_A fa ON r.valoracion_A = fa.nivel
LEFT JOIN Valoracion_Factor_B fb ON r.valoracion_B = fb.nivel
LEFT JOIN Valoracion_Factor_C fc ON r.valoracion_C = fc.nivel
LEFT JOIN Valoracion_Factor_D fd ON r.valoracion_D = fd.nivel
LEFT JOIN Valoracion_Factor_E fe ON r.valoracion_E = fe.nivel;
