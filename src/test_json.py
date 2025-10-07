"""
Script rápido para probar el formato JSON de salida
"""

from digimon_service import DigimonEvolutionService

# Inicializar el servicio
service = DigimonEvolutionService('../data/digimon_list.xlsx')

# Probar con Patamon
print("="*80)
print("JSON para Patamon:")
print("="*80)
result = service.get_evolution_line('Patamon')
print(result)

print("\n\n")

# Probar con Agumon
print("="*80)
print("JSON para Agumon:")
print("="*80)
result = service.get_evolution_line('Agumon')
print(result)

print("\n\n")

# Probar con un Digimon que no existe
print("="*80)
print("JSON para un Digimon inexistente:")
print("="*80)
result = service.get_evolution_line('DigimonFalso')
print(result)

print("\n\n")

# Obtener como diccionario para manipular en código
print("="*80)
print("Ejemplo de uso como diccionario:")
print("="*80)
result_dict = service.get_evolution_line_dict('Koromon')
print(f"Digimon: {result_dict['currentDigimon']['name']}")
print(f"Pre-evoluciones: {len(result_dict['preEvolutions'])}")
print(f"Post-evoluciones: {len(result_dict['postEvolutions'])}")

if result_dict['postEvolutions']:
    print("\nPuede evolucionar a:")
    for evo in result_dict['postEvolutions']:
        print(f"  - {evo['name']}")