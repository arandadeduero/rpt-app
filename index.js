import express from 'express';
import AdminJS from 'adminjs';
import * as AdminJSExpress from '@adminjs/express';
import * as AdminJSSequelize from '@adminjs/sequelize';
import session from 'express-session';
import { sequelize, Puestos, syncDatabase } from './models/index.js';

// Register the Sequelize adapter
AdminJS.registerAdapter({
  Resource: AdminJSSequelize.Resource,
  Database: AdminJSSequelize.Database,
});

// Initialize the app
const app = express();
const PORT = process.env.PORT || 3000;

// Configure AdminJS
const adminOptions = {
  resources: [
    {
      resource: Puestos,
      options: {
        properties: {
          ID_Puesto: {
            isVisible: { list: true, filter: true, show: true, edit: false },
          },
          Código_Interno: {
            isVisible: true,
            isTitle: true,
          },
          Denominación_Puesto: {
            isVisible: true,
          },
          Descripción_Funciones: {
            type: 'textarea',
            isVisible: { list: false, filter: false, show: true, edit: true },
          },
          Observaciones: {
            type: 'textarea',
            isVisible: { list: false, filter: false, show: true, edit: true },
          },
          Número_Orden: {
            isVisible: true,
          },
          Número_Vacantes: {
            isVisible: true,
          },
          Dotación_Presupuestaria: {
            isVisible: true,
          },
          Sueldo_Base: {
            isVisible: true,
          },
          ID_Jefe_Superior: {
            isVisible: true,
          },
          createdAt: {
            isVisible: { list: false, filter: false, show: true, edit: false },
          },
          updatedAt: {
            isVisible: { list: false, filter: false, show: true, edit: false },
          },
        },
        navigation: {
          name: 'RPT',
          icon: 'Users',
        },
      },
    },
  ],
  rootPath: '/admin',
  branding: {
    companyName: 'Aranda de Duero - RPT',
    logo: false,
    softwareBrothers: false,
  },
};

const admin = new AdminJS(adminOptions);

// Build and use the admin router with session
const adminRouter = AdminJSExpress.buildRouter(admin);

app.use(
  session({
    secret: process.env.SESSION_SECRET || 'rpt-app-secret-key-change-in-production',
    resave: false,
    saveUninitialized: true,
    cookie: {
      secure: false, // Set to true if using HTTPS
      maxAge: 1000 * 60 * 60 * 24, // 24 hours
    },
  })
);

app.use(admin.options.rootPath, adminRouter);

// Root route
app.get('/', (req, res) => {
  res.redirect('/admin');
});

// Start server
const startServer = async () => {
  try {
    // Sync database
    await syncDatabase();

    // Start listening
    app.listen(PORT, () => {
      console.log(`Server is running on http://localhost:${PORT}`);
      console.log(`AdminJS is available at http://localhost:${PORT}/admin`);
    });
  } catch (error) {
    console.error('Error starting server:', error);
    process.exit(1);
  }
};

startServer();
