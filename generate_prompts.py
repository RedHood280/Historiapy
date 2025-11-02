import re

def create_detailed_prompt(image_name, title, description):
    """Genera un prompt detallado y evocador para la IA de generación de imágenes."""

    prompt = f"**Archivo de imagen:** `{image_name}`\n\n"
    prompt += "**Prompt para IA Generativa (Estilo Cómic Neo-Noir):**\n"
    prompt += f"Una ilustración digital cinematográfica y atmosférica para una novela visual de DC, estilo cómic neo-noir. La escena se titula '{title}'.\n\n"

    prompt += f"**Descripción de la Escena:** {description}\n\n"

    specifics = []
    lower_title_desc = (title + " " + description).lower()

    characters = []
    if 'damian' in lower_title_desc: characters.append("Damian Wayne (como Robin, aproximadamente 10-13 años, con expresión arrogante pero determinada)")
    if 'tim' in lower_title_desc or 'red robin' in lower_title_desc: characters.append("Tim Drake (como Red Robin o Robin, adolescente, de complexión delgada, aspecto inteligente y analítico)")
    if 'dick' in lower_title_desc or 'nightwing' in lower_title_desc: characters.append("Dick Grayson (como Nightwing o un Robin mayor, atlético, con una presencia más ligera que la de Batman)")
    if 'jason' in lower_title_desc or 'red hood' in lower_title_desc: characters.append("Jason Todd (como Red Hood o un Robin más rudo, con una complexión más fuerte y una mirada intensa)")
    if 'bruce' in lower_title_desc or 'batman' in lower_title_desc: characters.append("Batman (Bruce Wayne, imponente, con una mandíbula marcada, su expresión es severa y melancólica)")
    if 'alfred' in lower_title_desc: characters.append("Alfred Pennyworth (mayor, con bigote fino, expresión de dignidad, calidez y preocupación)")
    if 'talia' in lower_title_desc: characters.append("Talia al Ghul (elegante, exótica, con una mirada peligrosa y calculadora)")
    if 'ra\'s' in lower_title_desc: characters.append("Ra's al Ghul (mayor pero imponente, con una mirada sabia y amenazante, a menudo con vestimenta ornamentada)")
    if 'joker' in lower_title_desc: characters.append("El Joker (delgado, con su característica sonrisa maníaca, cabello verde y traje morado)")

    if characters:
        specifics.append(f"- **Personajes Clave:** {', '.join(list(set(characters)))}. Sus expresiones y lenguaje corporal son cruciales.")

    if any(word in lower_title_desc for word in ['pelea', 'lucha', 'combate', 'ataque', 'asalto', 'batalla', 'confrontación', 'vs', 'guerra', 'brutal']):
        specifics.append("- **Acción y Violencia (Moderada):** La escena es dinámica y tensa. Usa ángulos de cámara bajos para magnificar el impacto. En lugar de sangre explícita, muestra el resultado de la violencia: trajes rasgados, escombros, personajes agotados o expresiones de dolor. Las poses deben ser enérgicas y llenas de movimiento.")
    elif any(word in lower_title_desc for word in ['triste', 'dolor', 'muerte', 'culpa', 'duda', 'llorar', 'perdido', 'crisis', 'miedo', 'traición', 'soledad']):
        specifics.append("- **Emoción y Drama:** El enfoque debe ser el conflicto interno. Un primer plano o plano medio del personaje principal es ideal. La expresión facial (melancolía, ira contenida, confusión) es clave. Un ambiente lluvioso, una habitación oscura o un paisaje desolado intensificará la emoción.")
    elif any(word in lower_title_desc for word in ['consejo', 'hablar', 'conversación', 'diálogo', 'lección', 'acuerdo', 'reflexión']):
        specifics.append("- **Diálogo e Intimidad:** Es una escena de conversación, ya sea íntima o tensa. La composición debe centrarse en la interacción y la conexión (o desconexión) entre los personajes. La iluminación suave (una lámpara, la luna) puede crear un ambiente de confianza, mientras que las sombras marcadas pueden sugerir conflicto o secretos.")

    if 'batcueva' in lower_title_desc:
        specifics.append("- **Ubicación:** La Batcueva. Un espacio vasto y cavernoso, lleno de sombras profundas. La luz principal debe provenir de la Batcomputadora, bañando a los personajes en un resplandor azulado. Elementos icónicos como el Batmóvil o trajes en exhibición pueden estar en el fondo, desenfocados.")
    elif 'azotea' in lower_title_desc or 'gotham' in lower_title_desc:
         specifics.append("- **Ubicación:** Una azotea en Gotham City de noche. La arquitectura gótica y opresiva de la ciudad debe ser un personaje más. Gárgolas, rascacielos puntiagudos y zepelines en la distancia. La atmósfera debe ser densa, con lluvia, niebla o una luna llena brillante.")
    elif 'mansión wayne' in lower_title_desc:
        specifics.append("- **Ubicación:** Interior de la Mansión Wayne (biblioteca, estudio). Muebles de madera oscura, estanterías altas, una chimenea crepitante. Debe sentirse lujoso pero solitario. La iluminación es cálida pero tenue, creando un espacio de calma o de tensa reflexión.")

    if specifics:
        prompt += "**Instrucciones Específicas para esta Imagen:**\n"
        prompt += "\n".join(specifics)
        prompt += "\n\n"

    prompt += "**Instrucciones Generales de Estilo:**\n"
    prompt += "- **Estilo Visual:** Arte de cómic digital, neo-noir, con fuerte enfoque en la atmósfera y la narrativa visual. Estilo similar a Greg Capullo o Jim Lee, pero más oscuro y cinematográfico.\n"
    prompt += "- **Iluminación:** Dramática, de alto contraste (chiaroscuro). Usar la luz para guiar el ojo y enfatizar la emoción.\n"
    prompt += "- **Paleta de Colores:** Mayormente desaturada (negros, grises, azules fríos). Los colores de los trajes deben ser puntos de saturación que resalten intensamente.\n"
    prompt += "- **Composición:** Ángulos de cámara dinámicos. El enfoque debe estar claro: la expresión de un personaje, una acción clave o un detalle importante."

    return prompt

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

    # Patrón para encontrar bloques de definición de NodoHistoria
    node_pattern = re.compile(r'(\w+\s*=\s*NodoHistoria\(.*?\))', re.DOTALL)

    # Patrones más específicos para extraer detalles de cada bloque
    title_pattern = re.compile(r'"(.*?)"')
    desc_pattern = re.compile(r'(?:"""(.*?)"""|"(.*?)")', re.DOTALL)
    image_pattern = re.compile(r'"([a-zA-Z0-9_]+\.png)"')

    all_prompts = []

    # Primero, encontrar todos los bloques de NodoHistoria
    node_definitions = node_pattern.findall(script_content)

    for node_def in node_definitions:
        # Dividir los argumentos por comas, pero con cuidado de no dividir dentro de las strings
        # Esta es una simplificación; un parser completo sería más robusto.
        # Asumimos que los 4 argumentos principales están separados por comas en el nivel superior.
        try:
            # Extraer solo el contenido dentro de NodoHistoria(...)
            args_content = node_def[node_def.find('(') + 1 : node_def.rfind(')')]

            # 1. Extraer ID
            id_match = re.search(r'^\s*"(.*?)"\s*,', args_content)
            id_str = id_match.group(0)
            args_content = args_content[len(id_str):] # Resto de los argumentos

            # 2. Extraer Título
            title_match = re.search(r'^\s*"(.*?)"\s*,', args_content)
            title = title_match.group(1).strip().replace('\\n', ' ')
            title_str = title_match.group(0)
            args_content = args_content[len(title_str):]

            # 3. Extraer Descripción
            if args_content.lstrip().startswith('"""'):
                desc_match = re.search(r'^\s*"""(.*?)"""\s*,', args_content, re.DOTALL)
                description_raw = desc_match.group(1)
            else:
                desc_match = re.search(r'^\s*"(.*?)"\s*,', args_content, re.DOTALL)
                description_raw = desc_match.group(1)

            description = ' '.join(description_raw.strip().split())
            desc_str = desc_match.group(0)
            args_content = args_content[len(desc_str):]

            # 4. Extraer Imagen
            image_match = re.search(r'^\s*"(.*?)"', args_content)
            image_name = image_match.group(1)

            if image_name and image_name.endswith('.png'):
                 if image_name not in existing_images:
                    prompt = create_detailed_prompt(image_name, title, description)
                    all_prompts.append(prompt)

        except (AttributeError, IndexError):
            # Si el parsing de un bloque falla, simplemente lo saltamos.
            continue

    # Manejar imágenes que no están en NodosHistoria (placeholders, etc.)
    required_images = set(re.findall(r'[a-zA-Z0-9_]+\.png', script_content))
    missing_images = sorted(list(required_images - existing_images))

    handled_images = {re.search(r'`(.*?)\.png`', p).group(1)+'.png' for p in all_prompts if re.search(r'`(.*?)\.png`', p)}

    for image in missing_images:
        if image not in handled_images:
            if 'placeholder' in image:
                prompt = f"**Archivo de imagen:** `{image}`\n\n**Prompt:** Imagen genérica de marcador de posición con un estilo de diagrama de flujo o estructura de código, en tonos grises y rojos oscuros, para indicar un nodo de historia de relleno.\n"
            else:
                clean_name = image.replace('.png', '').replace('_', ' ').title()
                prompt = f"**Archivo de imagen:** `{image}`\n\n**Prompt para IA Generativa (Estilo Cómic Neo-Noir):**\nUna ilustración digital cinematográfica y atmosférica para una novela visual de DC, estilo cómic neo-noir, que represente el concepto de '{clean_name}'. La escena debe ser evocadora y encajar con el tono oscuro de Gotham. Usar iluminación dramática de alto contraste y una paleta de colores desaturada.\n"
            all_prompts.append(prompt)


    with open('prompts.txt', 'w', encoding='utf-8') as f:
        f.write("\n---\n\n".join(all_prompts))

    print(f"Archivo prompts.txt generado con {len(all_prompts)} prompts detallados.")

if __name__ == "__main__":
    main()
