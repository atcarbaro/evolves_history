"""
Ejemplos avanzados de uso del servicio de líneas evolutivas de Digimon
"""

from digimon_service import DigimonEvolutionService
import json


def example_1_basic_search():
    """Ejemplo 1: Búsqueda básica"""
    print("\n" + "="*80)
    print("EJEMPLO 1: Búsqueda Básica")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    result = service.get_evolution_line('Agumon')
    print(result)


def example_2_multiple_searches():
    """Ejemplo 2: Búsquedas múltiples"""
    print("\n" + "="*80)
    print("EJEMPLO 2: Búsquedas Múltiples")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    digimon_list = ['Agumon', 'Gabumon', 'Patamon', 'Koromon']
    
    for digimon_name in digimon_list:
        result = service.get_evolution_line_dict(digimon_name)
        
        if result['success']:
            data = result['results'][0]
            prev_count = len(data['previous_evolutions'])
            next_count = len(data['next_evolutions'])
            
            print(f"\n{digimon_name}:")
            print(f"  Pre-evoluciones: {prev_count}")
            print(f"  Post-evoluciones: {next_count}")


def example_3_evolution_chain():
    """Ejemplo 3: Construir cadena evolutiva completa"""
    print("\n" + "="*80)
    print("EJEMPLO 3: Cadena Evolutiva Completa")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    
    # Seguir la cadena: Botamon -> Koromon -> Agumon -> Greymon
    chain = ['Botamon', 'Koromon', 'Agumon', 'Greymon']
    
    print("\n🔗 Cadena evolutiva:")
    for i, digimon in enumerate(chain):
        result = service.get_evolution_line_dict(digimon)
        
        if result['success']:
            data = result['results'][0]['digimon']
            arrow = " ➜ " if i < len(chain) - 1 else ""
            print(f"{data['name']} (Stage {data['stage']}){arrow}", end="")
    
    print("\n")


def example_4_find_all_paths():
    """Ejemplo 4: Encontrar todos los caminos evolutivos desde un Digimon"""
    print("\n" + "="*80)
    print("EJEMPLO 4: Todos los Caminos Evolutivos")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    digimon_name = 'Koromon'
    
    result = service.get_evolution_line_dict(digimon_name)
    
    if result['success']:
        data = result['results'][0]
        
        print(f"\n📍 Desde {digimon_name}, puedes llegar a:\n")
        
        for i, next_evo in enumerate(data['next_evolutions'], 1):
            print(f"{i}. {next_evo['name']} ({next_evo['stage']})")
            
            # Buscar las evoluciones del siguiente nivel
            next_result = service.get_evolution_line_dict(next_evo['name'])
            if next_result['success']:
                second_level = next_result['results'][0]['next_evolutions']
                if second_level:
                    for second_evo in second_level[:3]:  # Mostrar solo 3
                        print(f"   └─ {second_evo['name']}")
                    if len(second_level) > 3:
                        print(f"   └─ ... y {len(second_level) - 3} más")


def example_5_statistics():
    """Ejemplo 5: Estadísticas de evoluciones"""
    print("\n" + "="*80)
    print("EJEMPLO 5: Estadísticas de Evoluciones")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    
    # Analizar varios Digimon
    digimon_to_analyze = ['Agumon', 'Koromon', 'Greymon', 'Gabumon', 'Patamon']
    
    stats = {
        'max_previous': {'count': 0, 'name': ''},
        'max_next': {'count': 0, 'name': ''},
        'no_previous': [],
        'no_next': []
    }
    
    for digimon in digimon_to_analyze:
        result = service.get_evolution_line_dict(digimon)
        
        if result['success']:
            data = result['results'][0]
            prev_count = len(data['previous_evolutions'])
            next_count = len(data['next_evolutions'])
            
            # Actualizar estadísticas
            if prev_count > stats['max_previous']['count']:
                stats['max_previous'] = {'count': prev_count, 'name': digimon}
            
            if next_count > stats['max_next']['count']:
                stats['max_next'] = {'count': next_count, 'name': digimon}
            
            if prev_count == 0:
                stats['no_previous'].append(digimon)
            
            if next_count == 0:
                stats['no_next'].append(digimon)
    
    print(f"\n📊 Estadísticas:")
    print(f"  • Más pre-evoluciones: {stats['max_previous']['name']} ({stats['max_previous']['count']})")
    print(f"  • Más post-evoluciones: {stats['max_next']['name']} ({stats['max_next']['count']})")
    print(f"  • Sin pre-evoluciones: {', '.join(stats['no_previous']) if stats['no_previous'] else 'Ninguno'}")
    print(f"  • Sin post-evoluciones: {', '.join(stats['no_next']) if stats['no_next'] else 'Ninguno'}")


def example_6_export_to_file():
    """Ejemplo 6: Exportar resultados a archivo JSON"""
    print("\n" + "="*80)
    print("EJEMPLO 6: Exportar a Archivo JSON")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    
    # Buscar múltiples Digimon y guardar en un archivo
    digimon_list = ['Agumon', 'Gabumon', 'Patamon']
    all_results = []
    
    for digimon in digimon_list:
        result = service.get_evolution_line_dict(digimon)
        all_results.append(result)
    
    # Guardar en archivo
    output_file = 'digimon_evolutions_export.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Resultados exportados a: {output_file}")
    print(f"📄 Total de Digimon analizados: {len(all_results)}")


def example_7_filter_by_stage():
    """Ejemplo 7: Filtrar evoluciones por Stage"""
    print("\n" + "="*80)
    print("EJEMPLO 7: Filtrar por Stage")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    digimon_name = 'Koromon'
    target_stage = 'III'
    
    result = service.get_evolution_line_dict(digimon_name)
    
    if result['success']:
        data = result['results'][0]
        
        print(f"\n🔍 Evoluciones de {digimon_name} que son Stage {target_stage}:\n")
        
        filtered_evolutions = [
            evo for evo in data['next_evolutions'] 
            if evo['stage'] == target_stage
        ]
        
        for evo in filtered_evolutions:
            print(f"  • {evo['name']} ({evo['attribute']})")
        
        print(f"\n✅ Total encontrado: {len(filtered_evolutions)}")


def example_8_check_evolution_exists():
    """Ejemplo 8: Verificar si existe una evolución específica"""
    print("\n" + "="*80)
    print("EJEMPLO 8: Verificar Evolución Específica")
    print("="*80)
    
    service = DigimonEvolutionService('../data/digimon_list.xlsx')
    
    # Verificar si Koromon puede evolucionar a Agumon
    from_digimon = 'Koromon'
    to_digimon = 'Agumon'
    
    result = service.get_evolution_line_dict(from_digimon)
    
    if result['success']:
        data = result['results'][0]
        evolution_names = [evo['name'].lower() for evo in data['next_evolutions']]
        
        can_evolve = to_digimon.lower() in evolution_names
        
        print(f"\n❓ ¿{from_digimon} puede evolucionar a {to_digimon}?")
        print(f"{'✅ SÍ' if can_evolve else '❌ NO'}")
        
        if can_evolve:
            print(f"\n🎯 {from_digimon} puede evolucionar a:")
            for evo in data['next_evolutions']:
                marker = "👉 " if evo['name'].lower() == to_digimon.lower() else "   "
                print(f"{marker}{evo['name']}")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "🌟"*40)
    print("      EJEMPLOS AVANZADOS - DIGIMON EVOLUTION SERVICE")
    print("🌟"*40)
    
    try:
        example_1_basic_search()
        example_2_multiple_searches()
        example_3_evolution_chain()
        example_4_find_all_paths()
        example_5_statistics()
        example_6_export_to_file()
        example_7_filter_by_stage()
        example_8_check_evolution_exists()
        
        print("\n" + "="*80)
        print("✅ Todos los ejemplos ejecutados exitosamente!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error al ejecutar ejemplos: {e}\n")


if __name__ == '__main__':
    main()