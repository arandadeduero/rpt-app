import { test } from 'node:test';
import * as assert from 'node:assert';
import { OrganizationalStructure } from '../src/organizational-structure.js';
import type { RPTEntry } from '../src/types.js';

/**
 * Test suite for OrganizationalStructure
 */

// Test data - simple hierarchical structure
const testData: RPTEntry[] = [
  { ID: '1', Puesto: 'CEO', ID_Jefe_Superior: null },
  { ID: '2', Puesto: 'CTO', ID_Jefe_Superior: '1' },
  { ID: '3', Puesto: 'CFO', ID_Jefe_Superior: '1' },
  { ID: '4', Puesto: 'Dev Manager', ID_Jefe_Superior: '2' },
  { ID: '5', Puesto: 'QA Manager', ID_Jefe_Superior: '2' },
  { ID: '6', Puesto: 'Developer 1', ID_Jefe_Superior: '4' },
  { ID: '7', Puesto: 'Developer 2', ID_Jefe_Superior: '4' },
  { ID: '8', Puesto: 'QA Engineer', ID_Jefe_Superior: '5' },
];

test('OrganizationalStructure - getRootNodes', () => {
  const org = new OrganizationalStructure(testData);
  const roots = org.getRootNodes();
  
  assert.strictEqual(roots.length, 1, 'Should have one root node');
  assert.strictEqual(roots[0].ID, '1', 'Root should be CEO');
  assert.strictEqual(roots[0].Puesto, 'CEO', 'Root position should be CEO');
});

test('OrganizationalStructure - getDirectSubordinates', () => {
  const org = new OrganizationalStructure(testData);
  
  // CEO's direct subordinates
  const ceoSubs = org.getDirectSubordinates('1');
  assert.strictEqual(ceoSubs.length, 2, 'CEO should have 2 direct subordinates');
  
  const subIds = ceoSubs.map(e => e.ID).sort();
  assert.deepStrictEqual(subIds, ['2', '3'], 'CEO subordinates should be CTO and CFO');
  
  // CTO's direct subordinates
  const ctoSubs = org.getDirectSubordinates('2');
  assert.strictEqual(ctoSubs.length, 2, 'CTO should have 2 direct subordinates');
  
  const ctoSubIds = ctoSubs.map(e => e.ID).sort();
  assert.deepStrictEqual(ctoSubIds, ['4', '5'], 'CTO subordinates should be managers');
});

test('OrganizationalStructure - getAllSubordinates', () => {
  const org = new OrganizationalStructure(testData);
  
  // CEO's all subordinates (entire company except CEO)
  const allSubs = org.getAllSubordinates('1');
  assert.strictEqual(allSubs.length, 7, 'CEO should have 7 total subordinates');
  
  // CTO's all subordinates (recursive)
  const ctoAllSubs = org.getAllSubordinates('2');
  assert.strictEqual(ctoAllSubs.length, 5, 'CTO should have 5 total subordinates');
  
  // Dev Manager's subordinates
  const devMgrSubs = org.getAllSubordinates('4');
  assert.strictEqual(devMgrSubs.length, 2, 'Dev Manager should have 2 subordinates');
});

test('OrganizationalStructure - getSuperiors', () => {
  const org = new OrganizationalStructure(testData);
  
  // Developer 1's superiors
  const dev1Superiors = org.getSuperiors('6');
  assert.strictEqual(dev1Superiors.length, 3, 'Developer should have 3 superiors');
  
  // Check the chain: Dev Manager -> CTO -> CEO
  assert.strictEqual(dev1Superiors[0].ID, '4', 'First superior should be Dev Manager');
  assert.strictEqual(dev1Superiors[1].ID, '2', 'Second superior should be CTO');
  assert.strictEqual(dev1Superiors[2].ID, '1', 'Third superior should be CEO');
  
  // CEO has no superiors
  const ceoSuperiors = org.getSuperiors('1');
  assert.strictEqual(ceoSuperiors.length, 0, 'CEO should have no superiors');
});

test('OrganizationalStructure - isSuperior', () => {
  const org = new OrganizationalStructure(testData);
  
  // Direct superior
  assert.strictEqual(org.isSuperior('4', '6'), true, 'Dev Manager is superior to Developer 1');
  
  // Indirect superior
  assert.strictEqual(org.isSuperior('2', '6'), true, 'CTO is superior to Developer 1');
  assert.strictEqual(org.isSuperior('1', '6'), true, 'CEO is superior to Developer 1');
  
  // Not superior
  assert.strictEqual(org.isSuperior('3', '6'), false, 'CFO is not superior to Developer 1');
  assert.strictEqual(org.isSuperior('5', '6'), false, 'QA Manager is not superior to Developer 1');
  
  // Same person
  assert.strictEqual(org.isSuperior('6', '6'), false, 'Person cannot be superior to themselves');
  
  // Reverse relationship
  assert.strictEqual(org.isSuperior('6', '4'), false, 'Developer is not superior to Dev Manager');
});

test('OrganizationalStructure - empty data', () => {
  const org = new OrganizationalStructure([]);
  
  assert.strictEqual(org.getRootNodes().length, 0, 'Empty data should have no roots');
  assert.strictEqual(org.getDirectSubordinates('1').length, 0, 'Empty data should return no subordinates');
  assert.strictEqual(org.getSuperiors('1').length, 0, 'Empty data should return no superiors');
});

test('OrganizationalStructure - single entry', () => {
  const org = new OrganizationalStructure([
    { ID: '1', Puesto: 'Solo Position', ID_Jefe_Superior: null }
  ]);
  
  const roots = org.getRootNodes();
  assert.strictEqual(roots.length, 1, 'Should have one root');
  assert.strictEqual(roots[0].ID, '1', 'Root should be the only entry');
  assert.strictEqual(org.getDirectSubordinates('1').length, 0, 'Single entry has no subordinates');
});

test('OrganizationalStructure - multiple root nodes', () => {
  const multiRootData: RPTEntry[] = [
    { ID: '1', Puesto: 'Company A CEO', ID_Jefe_Superior: null },
    { ID: '2', Puesto: 'Company B CEO', ID_Jefe_Superior: null },
    { ID: '3', Puesto: 'Employee A', ID_Jefe_Superior: '1' },
    { ID: '4', Puesto: 'Employee B', ID_Jefe_Superior: '2' },
  ];
  
  const org = new OrganizationalStructure(multiRootData);
  const roots = org.getRootNodes();
  
  assert.strictEqual(roots.length, 2, 'Should have two root nodes');
  const rootIds = roots.map(r => r.ID).sort();
  assert.deepStrictEqual(rootIds, ['1', '2'], 'Both companies should be roots');
  
  // Check separation
  assert.strictEqual(org.isSuperior('1', '4'), false, 'Company A CEO is not superior to Company B employee');
  assert.strictEqual(org.isSuperior('2', '3'), false, 'Company B CEO is not superior to Company A employee');
});

test('OrganizationalStructure - getTree', () => {
  const org = new OrganizationalStructure(testData);
  const tree = org.getTree();
  
  assert.strictEqual(tree.length, 1, 'Should have one root in tree');
  assert.strictEqual(tree[0].entry.ID, '1', 'Root should be CEO');
  assert.strictEqual(tree[0].subordinados.length, 2, 'CEO should have 2 direct subordinates');
});

test('OrganizationalStructure - getEntry', () => {
  const org = new OrganizationalStructure(testData);
  
  const entry = org.getEntry('4');
  assert.ok(entry, 'Entry should exist');
  assert.strictEqual(entry?.Puesto, 'Dev Manager', 'Should return correct entry');
  
  const missing = org.getEntry('999');
  assert.strictEqual(missing, undefined, 'Non-existent entry should return undefined');
});

test('OrganizationalStructure - getNode', () => {
  const org = new OrganizationalStructure(testData);
  
  const node = org.getNode('4');
  assert.ok(node, 'Node should exist');
  assert.strictEqual(node?.entry.Puesto, 'Dev Manager', 'Should return correct node');
  assert.ok(node?.superior, 'Node should have superior');
  assert.strictEqual(node?.superior?.entry.ID, '2', 'Superior should be CTO');
  
  const missing = org.getNode('999');
  assert.strictEqual(missing, undefined, 'Non-existent node should return undefined');
});

console.log('All tests completed!');
