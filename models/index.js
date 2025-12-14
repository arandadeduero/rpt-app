import { Sequelize } from 'sequelize';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import puestosModel from './puestos.js';
import factoresModel from './factores.js';
import nivelesModel from './niveles.js';
import puestoFactoresModel from './puestoFactores.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Initialize Sequelize with SQLite
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: join(__dirname, '..', 'database.sqlite'),
  logging: false, // Set to console.log to see SQL queries
});

// Import models
const Puestos = puestosModel(sequelize);
const Factores = factoresModel(sequelize);
const Niveles = nivelesModel(sequelize);
const PuestoFactores = puestoFactoresModel(sequelize);

// Setup associations
const models = { Puestos, Factores, Niveles, PuestoFactores };
Object.values(models).forEach((model) => {
  if (model.associate) {
    model.associate(models);
  }
});

// Sync database
const syncDatabase = async () => {
  try {
    // In production, consider using migrations instead of auto-sync
    // alter: true can cause data loss in production environments
    const syncOptions = process.env.NODE_ENV === 'production' 
      ? { alter: false } 
      : { alter: true };
    
    await sequelize.sync(syncOptions);
    console.log('Database synced successfully');
  } catch (error) {
    console.error('Error syncing database:', error);
  }
};

export { sequelize, Puestos, Factores, Niveles, PuestoFactores, syncDatabase };
