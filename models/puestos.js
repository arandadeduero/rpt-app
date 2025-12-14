import { DataTypes } from 'sequelize';

export default (sequelize) => {
  const Puestos = sequelize.define('Puestos', {
    // Identifiers
    ID_Puesto: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false,
    },
    Código_Interno: {
      type: DataTypes.STRING(50),
      allowNull: true,
      unique: true,
    },
    Número_Orden: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },

    // Descriptive Fields (Open Text)
    Denominación_Puesto: {
      type: DataTypes.STRING(255),
      allowNull: false,
    },
    Descripción_Funciones: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    Observaciones: {
      type: DataTypes.TEXT,
      allowNull: true,
    },

    // Quantitative Fields (Numbers)
    Número_Vacantes: {
      type: DataTypes.INTEGER,
      allowNull: true,
      defaultValue: 0,
    },
    Dotación_Presupuestaria: {
      type: DataTypes.DECIMAL(10, 2),
      allowNull: true,
    },
    Sueldo_Base: {
      type: DataTypes.DECIMAL(10, 2),
      allowNull: true,
    },

    // Linkage Fields
    ID_Jefe_Superior: {
      type: DataTypes.INTEGER,
      allowNull: true,
      references: {
        model: 'Puestos',
        key: 'ID_Puesto',
      },
    },
  }, {
    tableName: 'puestos',
    timestamps: true,
  });

  // Define self-referencing association for hierarchy
  Puestos.associate = (models) => {
    Puestos.belongsTo(models.Puestos, {
      foreignKey: 'ID_Jefe_Superior',
      as: 'JefeSuperior',
    });
    Puestos.hasMany(models.Puestos, {
      foreignKey: 'ID_Jefe_Superior',
      as: 'Subordinados',
    });
    
    // A Puesto can have many Factores through PuestoFactores
    Puestos.belongsToMany(models.Factores, {
      through: models.PuestoFactores,
      foreignKey: 'ID_Puesto',
      otherKey: 'ID_Factor',
      as: 'Factores',
    });
  };

  return Puestos;
};
