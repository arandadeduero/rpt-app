#!/bin/bash
# Test script for Valoración Factors Tables implementation

set -e

echo "=========================================="
echo "RPT App - Valoración Factors Tables Test"
echo "=========================================="
echo ""

# Create temporary test database
TEST_DB="test_rpt_$(date +%s).db"
echo "Creating test database: $TEST_DB"

# Load schema
echo "Loading schema..."
sqlite3 "$TEST_DB" < schema.sql

# Load sample data
echo "Loading sample data..."
sqlite3 "$TEST_DB" < sample_data.sql

echo ""
echo "=========================================="
echo "Test Results"
echo "=========================================="
echo ""

# Test 1: Check all tables exist
echo "Test 1: Checking all tables exist..."
TABLES=$(sqlite3 "$TEST_DB" "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'Valoracion_Factor_%' OR name='RPT_Main';")
if [ "$TABLES" -eq 6 ]; then
    echo "✓ All 6 tables created successfully"
else
    echo "✗ Expected 6 tables, found $TABLES"
    exit 1
fi

# Test 2: Check view exists
echo ""
echo "Test 2: Checking view exists..."
VIEWS=$(sqlite3 "$TEST_DB" "SELECT COUNT(*) FROM sqlite_master WHERE type='view' AND name='RPT_View_Complete';")
if [ "$VIEWS" -eq 1 ]; then
    echo "✓ RPT_View_Complete view created successfully"
else
    echo "✗ View not found"
    exit 1
fi

# Test 3: Check each factor has 5 levels
echo ""
echo "Test 3: Checking each factor has 5 levels..."
for FACTOR in A B C D E; do
    COUNT=$(sqlite3 "$TEST_DB" "SELECT COUNT(*) FROM Valoracion_Factor_$FACTOR;")
    if [ "$COUNT" -eq 5 ]; then
        echo "✓ Factor $FACTOR has 5 levels"
    else
        echo "✗ Factor $FACTOR has $COUNT levels (expected 5)"
        exit 1
    fi
done

# Test 4: Check score ranges
echo ""
echo "Test 4: Checking score ranges (0-400)..."
for FACTOR in A B C D E; do
    MIN=$(sqlite3 "$TEST_DB" "SELECT MIN(puntuacion) FROM Valoracion_Factor_$FACTOR;")
    MAX=$(sqlite3 "$TEST_DB" "SELECT MAX(puntuacion) FROM Valoracion_Factor_$FACTOR;")
    if [ "$MIN" -ge 0 ] && [ "$MAX" -le 400 ]; then
        echo "✓ Factor $FACTOR scores in valid range ($MIN-$MAX)"
    else
        echo "✗ Factor $FACTOR scores out of range ($MIN-$MAX)"
        exit 1
    fi
done

# Test 5: Check RPT Main table has sample data
echo ""
echo "Test 5: Checking RPT Main table has sample data..."
RPT_COUNT=$(sqlite3 "$TEST_DB" "SELECT COUNT(*) FROM RPT_Main;")
if [ "$RPT_COUNT" -gt 0 ]; then
    echo "✓ RPT Main table has $RPT_COUNT sample positions"
else
    echo "✗ RPT Main table is empty"
    exit 1
fi

# Test 6: Check view calculates scores correctly
echo ""
echo "Test 6: Checking view calculates scores correctly..."
RESULT=$(sqlite3 "$TEST_DB" "SELECT codigo_puesto, puntuacion_total FROM RPT_View_Complete WHERE codigo_puesto='P003';")
if [[ $RESULT == *"1880"* ]]; then
    echo "✓ View calculates total scores correctly"
else
    echo "✗ View score calculation failed: $RESULT"
    exit 1
fi

# Test 7: Check constraints work
echo ""
echo "Test 7: Testing CHECK constraint (score > 400)..."
if sqlite3 "$TEST_DB" "INSERT INTO Valoracion_Factor_A (nivel, descripcion, puntuacion) VALUES ('TEST', 'Invalid', 500);" 2>&1 | grep -q "CHECK constraint failed"; then
    echo "✓ CHECK constraint prevents invalid scores"
else
    echo "✗ CHECK constraint not working"
    exit 1
fi

# Test 8: Check foreign key constraints
echo ""
echo "Test 8: Testing FOREIGN KEY constraint..."
if sqlite3 "$TEST_DB" "PRAGMA foreign_keys = ON; INSERT INTO RPT_Main (codigo_puesto, denominacion, valoracion_A) VALUES ('TEST', 'Test', 'INVALID');" 2>&1 | grep -q "FOREIGN KEY constraint failed"; then
    echo "✓ FOREIGN KEY constraint prevents invalid references"
else
    echo "✗ FOREIGN KEY constraint not working"
    exit 1
fi

# Display sample data
echo ""
echo "=========================================="
echo "Sample Data from RPT_View_Complete"
echo "=========================================="
echo ""
sqlite3 -header -column "$TEST_DB" "SELECT codigo_puesto, denominacion, puntuacion_total FROM RPT_View_Complete ORDER BY puntuacion_total DESC;"

# Cleanup
echo ""
echo "Cleaning up test database..."
rm -f "$TEST_DB"

echo ""
echo "=========================================="
echo "All tests passed! ✓"
echo "=========================================="
