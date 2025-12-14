/**
 * RPT Main Table Entry
 * Represents a position in the organizational structure
 */
export interface RPTEntry {
  /**
   * Unique identifier for this position
   */
  ID: string;

  /**
   * Position title/name
   */
  Puesto: string;

  /**
   * ID of the superior (boss) for this position
   * If null or undefined, this is a top-level position
   */
  ID_Jefe_Superior?: string | null;

  /**
   * Additional metadata for the position
   */
  [key: string]: any;
}

/**
 * Organizational tree node representing a position and its relationships
 */
export interface OrganizationalNode {
  /**
   * The RPT entry for this position
   */
  entry: RPTEntry;

  /**
   * Direct subordinates reporting to this position
   */
  subordinados: OrganizationalNode[];

  /**
   * Reference to the superior (if any)
   */
  superior?: OrganizationalNode;
}

/**
 * Result of organizational structure queries
 */
export interface OrganizationalQuery {
  /**
   * Get all superiors in the chain of command up to the top
   */
  getSuperiors(id: string): RPTEntry[];

  /**
   * Get all direct subordinates of a position
   */
  getDirectSubordinates(id: string): RPTEntry[];

  /**
   * Get all subordinates (recursive) under a position
   */
  getAllSubordinates(id: string): RPTEntry[];

  /**
   * Get the root nodes (top-level positions with no superior)
   */
  getRootNodes(): RPTEntry[];

  /**
   * Check if one position is a superior of another
   */
  isSuperior(superiorId: string, subordinateId: string): boolean;

  /**
   * Get the full organizational tree
   */
  getTree(): OrganizationalNode[];
}
