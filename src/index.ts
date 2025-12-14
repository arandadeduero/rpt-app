/**
 * RPT App - Organizational Structure Module
 * 
 * This module provides tools for managing and querying organizational structures
 * based on hierarchical relationships defined in the RPT (Relación de Puestos de Trabajo).
 * 
 * Key Concept: The organizational structure (Organigrama) is a tree dependency
 * based on the ID_Jefe_Superior field in the RPT Main Table. This field defines
 * who reports to whom, creating a hierarchical relationship where positions are
 * either "Superior" (boss) or "Subordinado" (subordinate).
 * 
 * @module rpt-app
 */

export { OrganizationalStructure } from './organizational-structure.js';
export type { RPTEntry, OrganizationalNode, OrganizationalQuery } from './types.js';
