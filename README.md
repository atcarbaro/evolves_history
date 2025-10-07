# 🌟 Digimon Evolution Line Service

Servicio en Python para consultar líneas evolutivas de Digimon desde un archivo Excel.

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Crear un entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Correr API

```bash
uvicorn api:app --reload
```

## 📂 Estructura del Proyecto

```
digimon_evolution/
├── ../data/digimon_list.xlsx.xlsx  # Tu archivo Excel
├── digimon_service.py                        # Servicio principal
├── main.py                                   # Script de prueba
├── requirements.txt                          # Dependencias
└── README.md                                 # Este archivo
```

## 💻 Uso

### Opción 1: Ejecutar el script de prueba interactivo

```bash
python main.py
```

Este script te permitirá:
- Ver ejemplos pre-configurados de líneas evolutivas
- Buscar cualquier Digimon de forma interactiva

### Opción 2: Usar la clase directamente en tu código

```python
from digimon_service import DigimonEvolutionService
import json

# Inicializar el servicio
service = DigimonEvolutionService('../data/digimon_list.xlsx.xlsx')

# Buscar un Digimon y obtener JSON string
result_json = service.get_evolution_line('Agumon')
print(result_json)

# O obtener un diccionario Python
result_dict = service.get_evolution_line_dict('Agumon')
print(result_dict)
```

## 📊 Formato del JSON de Respuesta

### Respuesta Exitosa

```json
{
  "success": true,
  "message": "Se encontraron 1 resultado(s) para: Agumon",
  "total_results": 1,
  "results": [
    {
      "digimon": {
        "number": 21,
        "name": "Agumon",
        "stage": "III",
        "attribute": "Vaccine",
        "image": null
      },
      "previous_evolutions": [
        {
          "number": 9,
          "name": "Koromon",
          "stage": "II",
          "attribute": "None",
          "image": null
        }
      ],
      "next_evolutions": [
        {
          "number": 45,
          "name": "Greymon",
          "stage": "IV",
          "attribute": "Vaccine",
          "image": null
        },
        {
          "number": 50,
          "name": "Geo Greymon",
          "stage": "IV",
          "attribute": "Vaccine",
          "image": null
        }
      ],
      "evolution_summary": {
        "total_previous": 1,
        "total_next": 6
      }
    }
  ]
}
```

### Respuesta cuando no se encuentra el Digimon

```json
{
  "success": false,
  "message": "No se encontró el Digimon: DigimonInexistente",
  "results": []
}
```

## 🔧 Características

✅ **Búsqueda case-insensitive**: No importa si escribes "agumon", "Agumon" o "AGUMON"

✅ **Múltiples evoluciones**: Maneja Digimon con múltiples líneas evolutivas

✅ **Evoluciones bidireccionales**: 
   - **Pre-evoluciones**: Digimon de los que proviene
   - **Post-evoluciones**: Digimon a los que puede evolucionar

✅ **Datos completos**: Incluye número, nombre, stage, atributo e imagen

✅ **Formato flexible**: Retorna JSON string o diccionario Python

## 📝 Métodos Disponibles

### `__init__(excel_path: str)`
Inicializa el servicio cargando el archivo Excel.

```python
service = DigimonEvolutionService('ruta/al/archivo.xlsx')
```

### `get_evolution_line(digimon_name: str) -> str`
Retorna la línea evolutiva como JSON string.

```python
json_result = service.get_evolution_line('Agumon')
```

### `get_evolution_line_dict(digimon_name: str) -> Dict`
Retorna la línea evolutiva como diccionario Python.

```python
dict_result = service.get_evolution_line_dict('Agumon')
```

## 🎯 Ejemplos de Uso

### Ejemplo 1: Búsqueda Simple

```python
from digimon_service import DigimonEvolutionService

service = DigimonEvolutionService('../data/digimon_list.xlsx.xlsx')
result = service.get_evolution_line('Koromon')
print(result)
```

### Ejemplo 2: Procesar Múltiples Digimon

```python
../data/digimon_list.xlsx = ['Agumon', 'Gabumon', 'Patamon']

for digimon in ../data/digimon_list.xlsx:
    result = service.get_evolution_line_dict(digimon)
    if result['success']:
        print(f"{digimon} puede evolucionar a {len(result['results'][0]['next_evolutions'])} formas diferentes")
```

### Ejemplo 3: Encontrar el Árbol Evolutivo Completo

```python
import json

result = service.get_evolution_line_dict('Greymon')
data = result['results'][0]

print(f"Pre-evoluciones de Greymon:")
for prev in data['previous_evolutions']:
    print(f"  - {prev['name']}")

print(f"\nGreymon evoluciona a:")
for next_evo in data['next_evolutions']:
    print(f"  - {next_evo['name']}")
```

## ⚠️ Notas Importantes

- El archivo Excel debe tener las columnas: `Number`, `Image`, `Name`, `Stage`, `Attribute`, `Evolutions`
- Las evoluciones pueden estar en múltiples columnas
- La búsqueda es case-insensitive
- Un Digimon puede tener múltiples pre-evoluciones y post-evoluciones

## 🐛 Solución de Problemas

### Error: "No such file or directory"
Asegúrate de que el archivo Excel esté en la misma carpeta que los scripts de Python.

### Error: "Faltan columnas requeridas"
Verifica que tu Excel tenga las columnas correctas.

### Error al importar pandas
Ejecuta: `pip install -r requirements.txt`

## 📧 Soporte

Si encuentras algún problema o tienes sugerencias, no dudes en consultar.

---

**¡Disfruta explorando las líneas evolutivas de tus Digimon favoritos!** 🎮✨