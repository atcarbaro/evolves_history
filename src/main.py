"""
Script principal para probar el servicio de líneas evolutivas de Digimon
"""

from digimon_service import DigimonEvolutionService
import json


def print_evolution_line(service: DigimonEvolutionService, digimon_name: str):
    """
    Imprime la línea evolutiva de un Digimon de forma legible
    """
    print(f"\n{'='*80}")
    print(f"🔍 Buscando línea evolutiva de: {digimon_name}")
    print('='*80)
    
    result_json = service.get_evolution_line(digimon_name)
    result = json.loads(result_json)
    
    # Verificar si hay error
    if 'error' in result and result['error']:
        print(f"❌ {result['message']}")
        return
    
    # Si hay múltiples resultados
    if 'results' in result:
        print(f"✓ {result['message']}\n")
        results = result['results']
    else:
        # Un solo resultado
        results = [result]
    
    for idx, data in enumerate(results, 1):
        if len(results) > 1:
            print(f"\n--- Resultado {idx} ---")
        
        digimon = data['currentDigimon']
        print(f"\n📌 DIGIMON ACTUAL:")
        print(f"   Nombre: {digimon['name']}")
        print(f"   Número: #{digimon['number']}")
        print(f"   Stage: {digimon['stage']}")
        print(f"   Atributo: {digimon['attribute']}")
        
        # Pre-evoluciones
        prev_evos = data['preEvolutions']
        print(f"\n⬅️  PRE-EVOLUCIONES ({len(prev_evos)}):")
        if prev_evos:
            for evo in prev_evos:
                print(f"   • {evo['name']} (Stage: {evo['stage']}, #{evo['number']})")
        else:
            print("   (No tiene pre-evoluciones)")
        
        # Post-evoluciones
        next_evos = data['postEvolutions']
        print(f"\n➡️  POST-EVOLUCIONES ({len(next_evos)}):")
        if next_evos:
            for evo in next_evos:
                stage_info = f"Stage: {evo['stage']}" if evo['stage'] else "Info no disponible"
                num_info = f"#{evo['number']}" if evo['number'] else ""
                print(f"   • {evo['name']} ({stage_info}, {num_info})")
        else:
            print("   (No tiene post-evoluciones)")
    
    print("\n" + "="*80)


def main():
    """Función principal"""
    print("\n🌟 Servicio de Líneas Evolutivas de Digimon 🌟")
    print("=" * 80)
    
    # Inicializar el servicio
    try:
        service = DigimonEvolutionService('../data/digimon_list.xlsx')
    except Exception as e:
        print(f"\n❌ Error al inicializar el servicio: {e}")
        return
    
    # Lista de Digimon para probar
    test_digimon = [
        'Agumon',
        'Koromon',
        'Greymon',
        'WarGreymon',
        'Gabumon'
    ]
    
    # Probar cada uno
    for digimon_name in test_digimon:
        print_evolution_line(service, digimon_name)
    
    # Ejemplo de uso interactivo
    print("\n\n💡 Modo Interactivo")
    print("=" * 80)
    print("Ingresa el nombre de un Digimon para ver su línea evolutiva")
    print("(Escribe 'salir' para terminar)\n")
    
    while True:
        try:
            user_input = input("🔎 Nombre del Digimon: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit', '']:
                print("\n👋 ¡Hasta luego!")
                break
            
            print_evolution_line(service, user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == '__main__':
    main()