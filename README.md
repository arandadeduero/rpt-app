# rpt-app
RPT app para Aranda de Duero

## Organizational Structure (Organigrama)

This module implements the organizational structure (Organigrama) for the RPT (Relación de Puestos de Trabajo) system.

### Key Concept

The organizational structure is a **tree dependency** based on the `ID_Jefe_Superior` field in the RPT Main Table:

- **Structure**: Defines the hierarchical relationship (who reports to whom)
- **Superior**: A position that has subordinates reporting to it
- **Subordinado**: A position that reports to a superior

### Installation

```bash
npm install
```

### Building

```bash
npm run build
```

### Usage

```typescript
import { OrganizationalStructure, RPTEntry } from 'rpt-app';

// Define your RPT entries with hierarchical relationships
const rptData: RPTEntry[] = [
  { ID: '1', Puesto: 'Director General', ID_Jefe_Superior: null },
  { ID: '2', Puesto: 'Subdirector', ID_Jefe_Superior: '1' },
  { ID: '3', Puesto: 'Jefe de Departamento A', ID_Jefe_Superior: '2' },
  { ID: '4', Puesto: 'Jefe de Departamento B', ID_Jefe_Superior: '2' },
  { ID: '5', Puesto: 'Empleado A1', ID_Jefe_Superior: '3' },
  { ID: '6', Puesto: 'Empleado A2', ID_Jefe_Superior: '3' },
];

// Create the organizational structure
const orgStructure = new OrganizationalStructure(rptData);

// Query the structure
const superiors = orgStructure.getSuperiors('5'); // Returns chain: [Jefe Dept A, Subdirector, Director]
const subordinates = orgStructure.getDirectSubordinates('2'); // Returns: [Jefe Dept A, Jefe Dept B]
const allSubs = orgStructure.getAllSubordinates('2'); // Returns all recursive subordinates
const roots = orgStructure.getRootNodes(); // Returns top-level positions

// Check relationships
const isSuper = orgStructure.isSuperior('1', '5'); // Returns true (Director is superior of Empleado)
```

### API Reference

#### `OrganizationalStructure`

Main class for building and querying the organizational structure.

**Constructor:**
- `new OrganizationalStructure(entries: RPTEntry[])` - Creates the organizational structure from RPT data

**Methods:**
- `getSuperiors(id: string): RPTEntry[]` - Get all superiors in the chain of command
- `getDirectSubordinates(id: string): RPTEntry[]` - Get direct reports
- `getAllSubordinates(id: string): RPTEntry[]` - Get all subordinates recursively
- `getRootNodes(): RPTEntry[]` - Get top-level positions (no superior)
- `isSuperior(superiorId: string, subordinateId: string): boolean` - Check if one position is superior to another
- `getTree(): OrganizationalNode[]` - Get the full organizational tree structure
- `getEntry(id: string): RPTEntry | undefined` - Get a specific entry by ID
- `getNode(id: string): OrganizationalNode | undefined` - Get the organizational node for a specific ID

#### Types

**`RPTEntry`** - Represents a position in the RPT table:
- `ID: string` - Unique identifier
- `Puesto: string` - Position title
- `ID_Jefe_Superior?: string | null` - ID of the superior (null for root positions)

**`OrganizationalNode`** - Tree node with relationships:
- `entry: RPTEntry` - The position data
- `subordinados: OrganizationalNode[]` - Direct subordinates
- `superior?: OrganizationalNode` - Reference to superior

### Examples

See the `examples/` directory for complete usage examples.

### License

ISC
