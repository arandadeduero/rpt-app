import { DataTypes } from 'sequelize';

export default (sequelize) => {
  const Niveles = sequelize.define('Niveles', {
    ID_Nivel: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false,
    },
    ID_Factor: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: 'factores',
        key: 'ID_Factor',
      },
    },
    Nombre: {
      type: DataTypes.STRING(255),
      allowNull: false,
    },
    Descripción: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    Puntos: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
    },
  }, {
    tableName: 'niveles',
    timestamps: true,
  });

  Niveles.associate = (models) => {
    // A Level belongs to a Factor
    Niveles.belongsTo(models.Factores, {
      foreignKey: 'ID_Factor',
      as: 'Factor',
    });
  };

  return Niveles;
};
