#!/usr/bin/env python3

DATOS_BUQUE_GRUPO9 = {
    'nombre': 'Buque de carga general - Grupo 9',
    'tipo': 'Granelero / Carga general',
    
    'dimensiones_principales': {
        'eslora_total_m': 107.0,
        'eslora_entre_perpendiculares_m': 105.2,
        'manga_m': 15.99,
        'puntal_m': 7.90,
        'calado_diseno_m': 6.20,
        'calado_escantillonado_m': 6.477
    },
    
    'coeficientes_forma': {
        'coeficiente_bloque': 0.7252,
        'coeficiente_prismatico': 0.74,
        'coeficiente_seccion_media': 0.98
    },
    
    'estructura': {
        'doble_fondo': {
            'altura_m': 1.20,
            'descripcion': 'Altura desde línea base hasta techo de doble fondo'
        },
        'doble_costado': {
            'ancho_m': 1.80,
            'descripcion': 'Ancho desde forro exterior hasta mamparo longitudinal'
        },
        'cuaderna_maestra': {
            'posicion_longitudinal_m': 52.6,
            'estacion': 15,
            'manga_total_m': 15.99,
            'puntal_total_m': 7.90,
            'calado_m': 6.20
        },
        'espaciado_cuadernas': {
            'zona_central_mm': 700,
            'zona_transicion_mm': 600,
            'descripcion': 'Espaciado entre cuadernas según DNV'
        },
        'espesores': {
            'forro_exterior_mm': 10.5,
            'forro_fondo_mm': 12.0,
            'cubierta_principal_mm': 8.0,
            'cubierta_segunda_mm': 6.0,
            'mamparos_transversales_mm': 8.0,
            'mamparos_longitudinales_mm': 7.0
        }
    },
    
    'material': {
        'acero': 'AH36',
        'limite_elastico_mpa': 355,
        'resistencia_traccion_mpa': 490,
        'modulo_young_gpa': 206,
        'coeficiente_poisson': 0.3,
        'densidad_kg_m3': 7850
    },
    
    'cargas_diseno': {
        'presion_hidrostatica': {
            'densidad_agua_mar_t_m3': 1.025,
            'gravedad_m_s2': 9.81,
            'calado_m': 6.20,
            'presion_fondo_kpa': 62.3
        },
        'cargas_cubierta': {
            'carga_general_kn_m2': 10.0,
            'contenedores_kn_m2': 15.0,
            'equipos_kn_m2': 20.0
        },
        'cargas_bodega': {
            'carga_graneles_t_m3': 1.0,
            'altura_carga_m': 5.0
        }
    },
    
    'mamparos': [
        {'nombre': 'Mamparo pique de popa', 'posicion_m': 0.0},
        {'nombre': 'Mamparo cámara de máquinas (popa)', 'posicion_m': 8.2},
        {'nombre': 'Mamparo cámara de máquinas (proa)', 'posicion_m': 23.2},
        {'nombre': 'Mamparo pique de proa', 'posicion_m': 99.2}
    ],
    
    'normativa': {
        'sociedad_clasificacion': 'DNV',
        'reglas': 'DNV-RU-SHIP Part 3',
        'clase': 'DNV 1A1 General Cargo Ship',
        'notacion_hielo': 'No',
        'area_navegacion': 'Unrestricted'
    }
}


def obtener_datos_buque():
    """Retorna los datos correctos del buque."""
    return DATOS_BUQUE_GRUPO9


def obtener_dimensiones_cuaderna_maestra():
    """Retorna las dimensiones de la cuaderna maestra."""
    return {
        'manga_total_m': 15.99,
        'manga_interior_m': 15.99 - 2 * 1.80,
        'puntal_total_m': 7.90,
        'altura_doble_fondo_m': 1.20,
        'altura_bodega_m': 7.90 - 1.20,
        'calado_m': 6.20,
        'posicion_longitudinal_m': 52.6
    }


def obtener_propiedades_material():
    """Retorna las propiedades del material AH36."""
    return DATOS_BUQUE_GRUPO9['material']


def obtener_cargas_diseno():
    """Retorna las cargas de diseño."""
    return DATOS_BUQUE_GRUPO9['cargas_diseno']


def obtener_espesores_estructura():
    """Retorna los espesores de la estructura."""
    return DATOS_BUQUE_GRUPO9['estructura']['espesores']


if __name__ == '__main__':
    import json
    print("=" * 80)
    print("DATOS CORRECTOS DEL BUQUE GRUPO 9")
    print("=" * 80)
    print(json.dumps(DATOS_BUQUE_GRUPO9, indent=2, ensure_ascii=False))
