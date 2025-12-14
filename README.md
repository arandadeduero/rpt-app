# RPT App - Sistema de Registro de Puestos de Trabajo

RPT app para Aranda de Duero - Sistema de gestión y consulta de puestos de trabajo con restricciones estrictas de precisión y formato.

## 📋 Descripción

Este sistema implementa un registro de puestos de trabajo (RPT) con restricciones estrictas para garantizar:

- ✅ **Precisión absoluta**: Todos los datos provienen directamente de tablas definidas
- ✅ **Idioma español**: Todas las respuestas en español por defecto
- ✅ **Formato claro**: Uso de Markdown (tablas, listas, énfasis)
- ✅ **Manejo de errores**: Mensajes educados y útiles cuando no se encuentran datos

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/arandadeduero/rpt-app.git
cd rpt-app

# No se requieren dependencias adicionales (usa Python estándar)
```

### Uso

```bash
# Ejecutar el ejemplo de demostración
python rpt_example.py
```

Este comando mostrará varios ejemplos de consultas al sistema RPT, incluyendo:
- Consultas exitosas con datos completos
- Manejo de posiciones no encontradas
- Validación de formatos de ID
- Listados y búsquedas
- Información de departamentos

## 📚 Documentación

### Archivos Principales

- **`CONSTRAINTS.md`**: Documentación completa de restricciones y directrices de formato
- **`rpt_config.py`**: Configuración y utilidades del sistema
- **`rpt_example.py`**: Implementación de ejemplo y casos de uso

### Restricciones Principales

#### 1. ⚙️ Precisión Estricta

Todos los datos numéricos y categóricos DEBEN recuperarse directamente de las tablas definidas:

- `puestos_trabajo`: Registro principal de puestos
- `factores_valoracion`: Factores de valoración
- `estructura_organizativa`: Estructura de departamentos
- `niveles_retributivos`: Niveles salariales

#### 2. 🌍 Idioma

**Siempre responder en español**, a menos que el usuario solicite explícitamente una traducción.

#### 3. 📝 Formato

Usar formato Markdown para claridad:
- **Tablas** para datos estructurados
- **Listas** para enumeraciones
- **Negritas** para campos importantes
- **Emojis** para indicadores visuales (✅, ❌, ⚠️)

#### 4. ❌ Manejo de Errores

Si una posición/factor/ID no se encuentra, indicar educadamente que no existe en los datos actuales.

## 💡 Ejemplos de Uso

### Consultar Información de un Puesto

```python
from rpt_example import RPTSystem

system = RPTSystem()
result = system.get_position_info("ID-1234")
print(result)
```

**Salida esperada**:
```markdown
# 📋 Información del Puesto

| Campo | Valor |
|-------|-------|
| **ID** | ID-1234 |
| **Nombre** | Técnico de Sistemas Senior |
| **Departamento** | Tecnologías de la Información |
| **Nivel Retributivo** | 22 |

**Factores de Valoración:**
- Complejidad Técnica: 8/10
- Responsabilidad: 7/10
- Experiencia Requerida: 5 años
```

### Manejar Errores

```python
result = system.get_position_info("ID-9999")
print(result)
```

**Salida esperada**:
```markdown
❌ **Posición no encontrada**

La posición con ID `ID-9999` no existe en el registro actual de RPT.

Por favor, verifica:
- El identificador de la posición
- Que la posición esté activa en el sistema
- Que tengas permisos para acceder a esta información
```

## 🧪 Validación

El sistema incluye un validador de restricciones (`ConstraintsValidator`) que verifica:

- ✅ Precisión de datos (sin estimaciones)
- ✅ Idioma correcto (español)
- ✅ Formato Markdown apropiado
- ✅ Fuente de datos válida (tablas de referencia)

## 🔧 Configuración

Todas las configuraciones se encuentran en `rpt_config.py`:

```python
# Idioma por defecto
DEFAULT_LANGUAGE = "es"

# Reglas de validación
VALIDATION_RULES = {
    "strict_accuracy": True,
    "require_table_source": True,
    "allow_caching": False,
    "validate_before_display": True
}

# Configuración de formato
FORMATTING = {
    "use_markdown": True,
    "use_tables": True,
    "use_bold_for_headers": True,
    "use_lists": True,
    "use_emojis": True
}
```

## 📖 Estructura del Proyecto

```
rpt-app/
├── README.md                 # Este archivo
├── CONSTRAINTS.md            # Documentación detallada de restricciones
├── rpt_config.py            # Configuración y utilidades
├── rpt_example.py           # Implementación de ejemplo
└── LICENSE                  # Licencia del proyecto
```

## 🤝 Contribuir

Al contribuir a este proyecto, asegúrate de:

1. Seguir todas las restricciones definidas en `CONSTRAINTS.md`
2. Mantener las respuestas en español
3. Usar formato Markdown apropiado
4. Validar que los datos provienen de tablas definidas
5. Manejar errores de manera educada y útil

## 📄 Licencia

Ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

Para preguntas o soporte, contacta con el equipo de desarrollo de Aranda de Duero.

---

**Última actualización**: Diciembre 2025
**Versión**: 1.0
