import { DataTypes } from 'sequelize';

export default (sequelize) => {
  const PuestoFactores = sequelize.define('PuestoFactores', {
    ID_Puesto_Factor: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false,
    },
    ID_Puesto: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'puestos',
        key: 'ID_Puesto',
      },
    },
    ID_Factor: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'factores',
        key: 'ID_Factor',
      },
    },
    ID_Nivel: {
      type: DataTypes.INTEGER,
      allowNull: true,
      references: {
        model: 'niveles',
        key: 'ID_Nivel',
      },
    },
  }, {
    tableName: 'puesto_factores',
    timestamps: true,
  });

  PuestoFactores.associate = (models) => {
    // PuestoFactores belongs to Puesto
    PuestoFactores.belongsTo(models.Puestos, {
      foreignKey: 'ID_Puesto',
      as: 'Puesto',
    });
    
    // PuestoFactores belongs to Factor
    PuestoFactores.belongsTo(models.Factores, {
      foreignKey: 'ID_Factor',
      as: 'Factor',
    });
    
    // PuestoFactores belongs to Nivel (the selected level for this factor)
    PuestoFactores.belongsTo(models.Niveles, {
      foreignKey: 'ID_Nivel',
      as: 'Nivel',
    });
  };

  return PuestoFactores;
};
