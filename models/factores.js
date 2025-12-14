import { DataTypes } from 'sequelize';

export default (sequelize) => {
  const Factores = sequelize.define('Factores', {
    ID_Factor: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false,
    },
    Nombre: {
      type: DataTypes.STRING(255),
      allowNull: false,
    },
    Definición: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
  }, {
    tableName: 'factores',
    timestamps: true,
  });

  Factores.associate = (models) => {
    // A Factor has many Levels
    Factores.hasMany(models.Niveles, {
      foreignKey: 'ID_Factor',
      as: 'Niveles',
      onDelete: 'CASCADE',
    });
    
    // A Factor can be associated with many Puestos through PuestoFactores
    Factores.belongsToMany(models.Puestos, {
      through: models.PuestoFactores,
      foreignKey: 'ID_Factor',
      otherKey: 'ID_Puesto',
      as: 'Puestos',
    });
  };

  return Factores;
};
