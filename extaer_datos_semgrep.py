import json
import csv

def json_to_csv(json_file='resultados_semgrep.json', csv_file='resultados_semgrep.csv'):
    # Abrir y cargar el JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Preparar la lista de filas
    rows = []
    for result in data.get('results', []):
        # Extraer campos con valores por defecto si faltan
        archivo = result.get('path', '')
        linea = result.get('start', {}).get('line', '')
        
        # CWE: tomar el primer elemento de la lista, si existe
        cwe_list = result.get('extra', {}).get('metadata', {}).get('cwe', [])
        cwe = cwe_list[0] if cwe_list else ''
        
        tipo = result.get('check_id', '')
        severidad = result.get('extra', {}).get('severity', '')
        mensaje = result.get('extra', {}).get('message', '')
        
        rows.append([archivo, linea, cwe, tipo, severidad, mensaje])
    
    # Escribir el CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Cabeceras
        writer.writerow(['archivo', 'linea', 'cwe', 'tipo', 'severidad', 'mensaje'])
        writer.writerows(rows)
    
    print(f"Conversión completada. Se generó {csv_file} con {len(rows)} registros.")

if __name__ == '__main__':
    json_to_csv()