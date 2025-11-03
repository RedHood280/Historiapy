import re

def create_single_line_prompt(image_name, title, description):
    """Genera un prompt detallado en una sola línea."""

    # Inicia la construcción del prompt
    prompt_parts = []

    # Título y descripción base
    prompt_parts.append(f"Archivo: {image_name};")
    prompt_parts.append(f"Título: {title};")
    prompt_parts.append(f"Descripción: {description};")

    # Análisis de palabras clave para detalles adicionales
    lower_title_desc = (title + " " + description).lower()

    # Personajes
    characters = []
    if 'damian' in lower_title_desc: characters.append("Damian Wayne")
    if 'tim' in lower_title_desc or 'red robin' in lower_title_desc: characters.append("Tim Drake")
    if 'dick' in lower_title_desc or 'nightwing' in lower_title_desc: characters.append("Dick Grayson")
    if 'jason' in lower_title_desc or 'red hood' in lower_title_desc: characters.append("Jason Todd")
    if 'bruce' in lower_title_desc or 'batman' in lower_title_desc: characters.append("Batman")
    if 'alfred' in lower_title_desc: characters.append("Alfred Pennyworth")
    if 'talia' in lower_title_desc: characters.append("Talia al Ghul")
    if 'ra\'s' in lower_title_desc: characters.append("Ra's al Ghul")
    if 'joker' in lower_title_desc: characters.append("Joker")
    if characters:
        prompt_parts.append(f"Personajes: {', '.join(list(set(characters)))};")

    # Emoción/Acción
    if any(word in lower_title_desc for word in ['pelea', 'lucha', 'combate', 'ataque', 'batalla', 'confrontación']):
        prompt_parts.append("Tono: Escena de acción dinámica y tensa, violencia moderada, poses enérgicas;")
    elif any(word in lower_title_desc for word in ['triste', 'dolor', 'muerte', 'culpa', 'duda', 'soledad']):
        prompt_parts.append("Tono: Dramático y emocional, enfocado en el conflicto interno del personaje, melancolía;")

    # Ubicación
    if 'batcueva' in lower_title_desc:
        prompt_parts.append("Ubicación: Batcueva, oscura, iluminada por monitores;")
    elif 'azotea' in lower_title_desc or 'gotham' in lower_title_desc:
         prompt_parts.append("Ubicación: Azotea en Gotham de noche, arquitectura gótica, lluvia o niebla;")
    elif 'mansión wayne' in lower_title_desc:
        prompt_parts.append("Ubicación: Interior de la Mansión Wayne, lujoso pero solitario, iluminación tenue;")

    # Estilo general
    prompt_parts.append("Estilo: Cómic neo-noir, cinematográfico, atmosférico, iluminación de alto contraste, colores desaturados con acentos de color intensos.")

    # Une todas las partes en una sola línea, eliminando saltos de línea residuales
    single_line_prompt = ' '.join(prompt_parts).replace('\n', ' ').replace('\r', ' ')
    return single_line_prompt

def main():
    """Función principal para generar el archivo de prompts."""
    try:
        with open('Robins.py', 'r', encoding='utf-8') as f:
            script_content = f.read()
    except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo Robins.py")
        return

    existing_images_str = "accion_directa.png batcave.png batman_chase.png batman_explica.png batman_jason.png conflicto_batman.png crime_alley.png dificil_acelerar_plan.png dificil_acuerdo_desacuerdo.png dificil_aliados_inesperados.png dificil_arkham_equipo.png dificil_arkham_solo.png dificil_buscar_joker_gas.png dificil_buscar_joker_redentor.png dificil_buscar_joker.png dificil_buscar_redencion.png dificil_camino_intermedio.png dificil_camino_luz.png dificil_camino_oscuro.png dificil_camino_solo_advertencia.png dificil_campana_solitaria.png dificil_capturar_joker.png dificil_caza_jefes.png dificil_codigo_propio.png dificil_colaboracion.png dificil_confrontacion_temprana.png dificil_convencer_batman.png dificil_culpar_batman.png dificil_debate_filosofico.png dificil_descenso_oscuridad.png dificil_dialogo_azotea.png dificil_disparar_joker.png dificil_disparo_traicionero.png dificil_duda_oscura.png dificil_duelo_batman.png dificil_duelo_joker.png dificil_enfoque_joker.png dificil_entrada_explosiva.png dificil_equilibrio_gris.png dificil_escape_batman.png dificil_escape_gas.png dificil_golpear_joker.png dificil_heroe_oscuro.png dificil_ignorar_batman.png dificil_infiltracion_teatro.png dificil_mostrar_codigo.png dificil_muelles_equipo.png dificil_muelles_solo.png dificil_operacion_independiente.png dificil_partir_sin_palabras.png dificil_pedir_guia.png dificil_pelea_brutal_joker.png dificil_plan_secreto.png dificil_preparar_doble_conflicto.png dificil_preparar_encuentro.png dificil_primera_victima.png dificil_redencion_solitaria.png dificil_ruptura_total.png dificil_solo_final.png dificil_suprimir_dudas.png dificil_verdad_completa.png duelo_batman.png entrenamiento_combate.png etiopia.png a f333a952-b149-437e-bOeO-71340824280a.png final_antiheroe.png final_oscuridad.png final_redencion.png final_robin.png final_salvado.png final_tragico.png jason_batman_confrontacion.png jason_ladron_final.png jason_solo.png jason_triste.png jason_valiente.png laboratorio.png mensaje_joker.png normal_argumento.png normal_batman_muere.png normal_busqueda.png normal_compromiso.png normal_consecuencias_graves.png normal_contencion.png normal_desobediencia.png normal_disculpa.png normal_enfrentar_joker.png normal_escape_conjunto.png normal_etiopia_equipo.png normal_impulso_peligroso.png normal_intento_escape.png normal_ira.png normal_justificacion.png normal_leccion_dura.png normal_lucha_interna.png normal_mensaje_conjunto.png normal_nuevo_comienzo.png normal_plan_batman.png normal_preparacion.png normal_progreso.png normal_promesa.png normal_rebelion.png normal_reconciliacion.png normal_recuperacion.png normal_reflexion.png normal_rescate_tardio.png normal_retorno.png normal_segunda_oportunidad.png normal_suspension.png normal_tortura.png primera_patrulla.png red_hood_accion.png red_hood.png robin_heroe.png robin_oscuro.png sigilo.png traje_robin.png"
    existing_images = set(existing_images_str.split())

    # Patrón para encontrar todas las imágenes en orden de aparición
    image_pattern = re.compile(r'"([a-zA-Z0-9_]+\.png)"')

    all_prompts = []
    found_images_in_order = []

    # 1. Obtener todas las imágenes en el orden en que aparecen
    for match in image_pattern.finditer(script_content):
        image_name = match.group(1)
        if image_name not in found_images_in_order:
            found_images_in_order.append(image_name)

    # 2. Crear un mapa de imagen a su contexto para una búsqueda rápida
    context_map = {}
    node_pattern_for_context = re.compile(
        r'NodoHistoria\s*\(\s*".*?",\s*"(.*?)",\s*(?:"""(.*?)"""|"(.*?)"),\s*"([a-zA-Z0-9_]+\.png)"\s*\)',
        re.DOTALL
    )
    for match in node_pattern_for_context.finditer(script_content):
        title = match.group(1).strip().replace('\\n', ' ')
        description_raw = match.group(2) if match.group(2) is not None else match.group(3)
        description = ' '.join(description_raw.strip().split())
        image_name = match.group(4)
        context_map[image_name] = (title, description)

    # 3. Generar prompts para las imágenes faltantes en el orden de aparición
    for image_name in found_images_in_order:
        if image_name not in existing_images:
            if image_name in context_map:
                title, description = context_map[image_name]
                prompt = create_single_line_prompt(image_name, title, description)
                all_prompts.append(prompt)
            else:
                # Manejar placeholders u otras imágenes sin un NodoHistoria claro
                if 'placeholder' in image_name:
                    prompt = f"Archivo: {image_name}; Tono: Placeholder; Descripción: Imagen genérica de marcador de posición con estilo de diagrama de flujo en tonos grises y rojos oscuros."
                else:
                    clean_name = image_name.replace('.png', '').replace('_', ' ').title()
                    prompt = f"Archivo: {image_name}; Título: {clean_name}; Descripción: Escena evocadora de cómic neo-noir que represente '{clean_name}' en Gotham, con iluminación dramática y colores desaturados."
                all_prompts.append(prompt)


    with open('prompts.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(all_prompts))

    print(f"Archivo prompts.txt generado con {len(all_prompts)} prompts en una sola línea y en orden de aparición.")

if __name__ == "__main__":
    main()
