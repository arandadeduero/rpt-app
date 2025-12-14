import { OrganizationalStructure } from '../src/organizational-structure.js';
import type { RPTEntry } from '../src/types.js';

/**
 * Example: Municipal organizational structure for Aranda de Duero
 * This demonstrates how to use the OrganizationalStructure class
 */

// Define the RPT entries with hierarchical relationships
const rptEntries: RPTEntry[] = [
  // Top level - Alcaldía
  {
    ID: '1',
    Puesto: 'Alcalde/sa',
    ID_Jefe_Superior: null,
  },

  // Second level - Concejalías
  {
    ID: '2',
    Puesto: 'Concejal/a de Hacienda',
    ID_Jefe_Superior: '1',
  },
  {
    ID: '3',
    Puesto: 'Concejal/a de Urbanismo',
    ID_Jefe_Superior: '1',
  },
  {
    ID: '4',
    Puesto: 'Concejal/a de Servicios Sociales',
    ID_Jefe_Superior: '1',
  },

  // Third level - Jefes de Departamento
  {
    ID: '5',
    Puesto: 'Jefe/a de Tesorería',
    ID_Jefe_Superior: '2',
  },
  {
    ID: '6',
    Puesto: 'Jefe/a de Contabilidad',
    ID_Jefe_Superior: '2',
  },
  {
    ID: '7',
    Puesto: 'Arquitecto/a Municipal',
    ID_Jefe_Superior: '3',
  },
  {
    ID: '8',
    Puesto: 'Trabajador/a Social',
    ID_Jefe_Superior: '4',
  },

  // Fourth level - Personal administrativo
  {
    ID: '9',
    Puesto: 'Auxiliar Administrativo Tesorería',
    ID_Jefe_Superior: '5',
  },
  {
    ID: '10',
    Puesto: 'Auxiliar Administrativo Contabilidad',
    ID_Jefe_Superior: '6',
  },
  {
    ID: '11',
    Puesto: 'Técnico de Urbanismo',
    ID_Jefe_Superior: '7',
  },
];

// Create the organizational structure
const orgStructure = new OrganizationalStructure(rptEntries);

console.log('=== Organizational Structure Example ===\n');

// Example 1: Get all root nodes (top-level positions)
console.log('1. Root positions (no superior):');
const roots = orgStructure.getRootNodes();
roots.forEach(entry => {
  console.log(`   - ${entry.Puesto} (ID: ${entry.ID})`);
});

// Example 2: Get direct subordinates
console.log('\n2. Direct subordinates of Alcalde/sa:');
const alcaldeSubordinates = orgStructure.getDirectSubordinates('1');
alcaldeSubordinates.forEach(entry => {
  console.log(`   - ${entry.Puesto} (ID: ${entry.ID})`);
});

// Example 3: Get all subordinates (recursive)
console.log('\n3. All subordinates of Concejal/a de Hacienda (recursive):');
const allHaciendaSubordinates = orgStructure.getAllSubordinates('2');
allHaciendaSubordinates.forEach(entry => {
  console.log(`   - ${entry.Puesto} (ID: ${entry.ID})`);
});

// Example 4: Get chain of command (superiors)
console.log('\n4. Chain of command for Auxiliar Administrativo Tesorería:');
const superiors = orgStructure.getSuperiors('9');
console.log('   Reporting to:');
superiors.forEach((entry, index) => {
  console.log(`   ${index + 1}. ${entry.Puesto} (ID: ${entry.ID})`);
});

// Example 5: Check if one position is superior to another
console.log('\n5. Checking superior relationships:');
console.log(`   Is Alcalde/sa superior to Auxiliar Administrativo? ${orgStructure.isSuperior('1', '9')}`);
console.log(`   Is Concejal/a de Urbanismo superior to Auxiliar Tesorería? ${orgStructure.isSuperior('3', '9')}`);
console.log(`   Is Jefe/a de Tesorería superior to Auxiliar Tesorería? ${orgStructure.isSuperior('5', '9')}`);

// Example 6: Display tree structure
console.log('\n6. Full organizational tree structure:');
function printTree(nodes: any[], indent: string = ''): void {
  for (const node of nodes) {
    console.log(`${indent}├─ ${node.entry.Puesto} (ID: ${node.entry.ID})`);
    if (node.subordinados.length > 0) {
      printTree(node.subordinados, indent + '   ');
    }
  }
}
printTree(orgStructure.getTree());

console.log('\n=== End of Example ===');
