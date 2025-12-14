import type { RPTEntry, OrganizationalNode, OrganizationalQuery } from './types.js';

/**
 * Builds and manages the organizational structure from RPT data
 */
export class OrganizationalStructure implements OrganizationalQuery {
  private entries: Map<string, RPTEntry>;
  private nodes: Map<string, OrganizationalNode>;
  private rootNodes: OrganizationalNode[];

  constructor(entries: RPTEntry[]) {
    this.entries = new Map();
    this.nodes = new Map();
    this.rootNodes = [];

    // Store all entries
    for (const entry of entries) {
      this.entries.set(entry.ID, entry);
    }

    // Build the tree structure
    this.buildTree();
  }

  /**
   * Build the hierarchical tree from the flat list of entries
   */
  private buildTree(): void {
    // First pass: create all nodes
    for (const entry of this.entries.values()) {
      const node: OrganizationalNode = {
        entry,
        subordinados: [],
      };
      this.nodes.set(entry.ID, node);
    }

    // Second pass: establish relationships
    for (const node of this.nodes.values()) {
      const superiorId = node.entry.ID_Jefe_Superior;
      
      if (superiorId && this.nodes.has(superiorId)) {
        // This position has a superior
        const superiorNode = this.nodes.get(superiorId)!;
        node.superior = superiorNode;
        superiorNode.subordinados.push(node);
      } else {
        // This is a root node (no superior or superior not found)
        this.rootNodes.push(node);
      }
    }
  }

  /**
   * Get all superiors in the chain of command up to the top
   */
  getSuperiors(id: string): RPTEntry[] {
    const node = this.nodes.get(id);
    if (!node) {
      return [];
    }

    const superiors: RPTEntry[] = [];
    let current = node.superior;
    
    while (current) {
      superiors.push(current.entry);
      current = current.superior;
    }

    return superiors;
  }

  /**
   * Get all direct subordinates of a position
   */
  getDirectSubordinates(id: string): RPTEntry[] {
    const node = this.nodes.get(id);
    if (!node) {
      return [];
    }

    return node.subordinados.map(sub => sub.entry);
  }

  /**
   * Get all subordinates (recursive) under a position
   */
  getAllSubordinates(id: string): RPTEntry[] {
    const node = this.nodes.get(id);
    if (!node) {
      return [];
    }

    const subordinates: RPTEntry[] = [];
    
    const collectSubordinates = (n: OrganizationalNode): void => {
      for (const sub of n.subordinados) {
        subordinates.push(sub.entry);
        collectSubordinates(sub);
      }
    };

    collectSubordinates(node);
    return subordinates;
  }

  /**
   * Get the root nodes (top-level positions with no superior)
   */
  getRootNodes(): RPTEntry[] {
    return this.rootNodes.map(node => node.entry);
  }

  /**
   * Check if one position is a superior of another
   */
  isSuperior(superiorId: string, subordinateId: string): boolean {
    if (superiorId === subordinateId) {
      return false;
    }

    const subordinateNode = this.nodes.get(subordinateId);
    if (!subordinateNode) {
      return false;
    }

    let current = subordinateNode.superior;
    while (current) {
      if (current.entry.ID === superiorId) {
        return true;
      }
      current = current.superior;
    }

    return false;
  }

  /**
   * Get the full organizational tree
   */
  getTree(): OrganizationalNode[] {
    return this.rootNodes;
  }

  /**
   * Get a specific entry by ID
   */
  getEntry(id: string): RPTEntry | undefined {
    return this.entries.get(id);
  }

  /**
   * Get the organizational node for a specific ID
   */
  getNode(id: string): OrganizationalNode | undefined {
    return this.nodes.get(id);
  }
}
