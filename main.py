import pygame
from Deck import Deck
import math
import os
import sys
import time
import random

from llama_cpp import Llama

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 900, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tarot con Miaustica")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Cargar imagen de fondo
background_img = pygame.image.load('background.jpeg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Posiciones de las cartas
cards_position = [(75, 250), (350, 250), (625, 250)]

# Posición del gatito
cat_position = (175, 120)

# Crear instancia del mazo
deck = Deck()

# Cargar imágenes de las cartas
cards_img = {}
back_img_path = 'Cards/00. Back.png'
back_img = pygame.transform.scale(pygame.image.load(back_img_path), (200, 350))

for card in deck.original_cards:
    img_path = deck.get_img(card)
    if img_path:
        cards_img[card] = pygame.transform.scale(pygame.image.load(img_path), (200, 350))


# Cargar las imágenes del gato
def load_cat_images(folder_path):
    cat_images = []
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                img_path = os.path.join(folder_path, filename)
                image = pygame.image.load(img_path).convert_alpha()
                image = pygame.transform.scale(image, (270, 270))
                cat_images.append(image)
        print(f"Cargadas {len(cat_images)} imágenes de gatos desde: {folder_path}")
        return cat_images
    except FileNotFoundError:
        print(f"Error: No se encontró la carpeta {folder_path}. Verifica la ruta.")
        return []
    except Exception as e:
        print(f"Error al cargar las imágenes: {str(e)}")
        return []


cat_images = load_cat_images("Sprites/Sprites")


def select_cat_image(cat_images_list):
    if not cat_images_list:
        print("No hay imágenes disponibles para seleccionar. Verifica la carpeta.")
        return None
    image_index = random.randint(0, len(cat_images_list) - 1)
    print(f"Imagen seleccionada con índice: {image_index}")
    return cat_images_list[image_index]


cat_sprite = select_cat_image(cat_images)

if cat_sprite is None:
    print("No se pudo cargar la imagen. Creando un rectángulo rojo como placeholder.")
    cat_sprite = pygame.Surface((270, 270))
    cat_sprite.fill(RED)

# Variables para la animación
ANIMATION_FRAMES = [0, 2, 3]
animation_active = True
frame_time = pygame.time.get_ticks()
FRAME_DELAY = 200
frame_change_count = 0

llm = Llama.from_pretrained(
    repo_id="lmstudio-community/Llama-3.2-3B-Instruct-GGUF",
    filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
)


# Generar el mensaje de bienvenida usando CHAT COMPLETION
def generate_welcome_message():
    """Genera el mensaje de bienvenida usando chat_completion de forma local"""
    try:
        print("Generando mensaje de bienvenida con LLM local...")
        # Llamada síncrona (sin stream=True para el saludo inicial)
        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres Miaustica, una anciana gata pitonisa mística. "
                        "Hablas en primera persona con lenguaje poético, dramático pero cálido. "
                        "Usas metáforas sobre el cosmos, estrellas y ronroneos del universo."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Saluda al humano que entra a tu tienda. "
                        "Menciona: (1) bienvenida mística, (2) que el Universo ronronea revelando secretos, "
                        "(3) tres cartas ancestrales esperan, (4) invítalo a hacer click. "
                        "3-4 frases. Dramático pero acogedor."
                    )
                }
            ],
            max_tokens=150,
            temperature=0.8
        )
        # El acceso correcto en llama-cpp-python es por diccionario
        response_text = response['choices'][0]['message']['content'].strip()
        print(f"Respuesta generada: {response_text[:100]}...")
        return response_text
    except Exception as e:
        print(f"Error al generar mensaje de bienvenida: {str(e)}")
        return get_fallback_welcome()


def get_fallback_welcome():
    """Mensajes de respaldo si falla la API"""
    mensajes = [
        "¡Ah, un alma curiosa cruza el umbral de mi santuario! El Universo ronronea tu llegada, querido humano. Ante ti aguardan tres cartas ancestrales, portadoras de verdades ocultas. ¿Te atreves a descubrir lo que el Destino ha tejido para ti? Haz click y deja que la magia comience...",

        "¡Bienvenido, viajero del cosmos! Las estrellas me susurraron tu nombre antes de que llegaras. El Destino ronronea inquieto mientras tres cartas místicas descansan ante ti, listas para revelar los secretos de tu pasado, presente y futuro. Toca cada una y deja que el Universo te hable...",

        "¡Saludos, querido humano! Soy Miaustica, guardiana de los arcanos felinos, y el Cosmos ha preparado un mensaje especial para ti. Observa estas tres cartas sagradas que brillan con energía ancestral. Cada una guarda un fragmento de tu destino. ¿Estás listo para ver lo que la Luna revela?",

        "¡Ah, qué sorpresa más mística! El Universo ronronea melodías de bienvenida. Tres cartas ancestrales aguardan silenciosas, como ventanas al alma del tiempo. Tu pasado susurra, tu presente danza, y tu futuro espera ser descubierto. Haz click, humano valiente, y permite que Miaustica ilumine tu camino..."
    ]
    return random.choice(mensajes)


# Generar el mensaje de bienvenida al inicio
print("Iniciando generación del mensaje de bienvenida...")
welcome_message = generate_welcome_message()
print(f"Mensaje listo: {len(welcome_message)} caracteres")
displayed_welcome = ""
welcome_typing_index = 0
welcome_last_typed_time = 0

# Estado del juego
game_state = "welcome"
revealed_cards = [None, None, None]
rotation_angles = [0, 0, 0]
animating = [False, False, False]
story = ""
displayed_story = ""
typing_index = 0
typing_speed = 0.05
last_typed_time = 0
scroll_y = 0
max_visible_lines = 4

# Velocidad de animación
ROTATION_SPEED = 5

# Reloj
clock = pygame.time.Clock()

deck.shuffle()


# Generar la historia usando CHAT COMPLETION
def generate_hf_story(revealed_cards, deck):
    """Genera la interpretación localmente"""
    active_cards = [card for card in revealed_cards if card is not None]
    if len(active_cards) != 3:
        return ""

    positions = ["Pasado", "Presente", "Futuro"]
    card_descriptions = []
    for i, (card_num, is_reversed) in enumerate(active_cards):
        pred = deck.get_pred((card_num, is_reversed))
        reversal = " (invertida)" if is_reversed else ""
        card_descriptions.append(f"{positions[i]}: {pred}{reversal}")

    cards_info = "\n".join(card_descriptions)

    try:
        print("Miaustica está consultando los astros locales...")
        print(f"Cartas a interpretar: {cards_info}")

        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres Miaustica, una sabia gata pitonisa. Hablas en segunda persona (tú) con lenguaje poético y místico. "
                        "Usas metáforas celestiales: 'las estrellas susurran', 'el destino teje', 'el cosmos ronronea'."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Interpreta estas 3 cartas del tarot:\n{cards_info}\n\n"
                        "Crea una lectura mística en 6-8 frases que conecte Pasado → Presente → Futuro. "
                        "Termina con un consejo sabio y felino. Máximo 200 palabras."
                    )
                }
            ],
            max_tokens=300,
            temperature=0.75
        )

        result = response['choices'][0]['message']['content'].strip()
        print(f"Interpretación generada exitosamente: {len(result)} caracteres")
        return result
    except Exception as e:
        print(f"Error en la interpretación: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        return get_fallback_story(card_descriptions)


def get_fallback_story(card_descriptions):
    """Historia de respaldo si falla la API"""
    pasado = card_descriptions[0].split(': ')[1]
    presente = card_descriptions[1].split(': ')[1]
    futuro = card_descriptions[2].split(': ')[1]

    return (
        f"Ah, querido humano... las cartas han hablado y el Universo ronronea revelaciones profundas. "
        f"Observo en el tapiz del tiempo que {pasado.lower()} marcó tu sendero como las huellas en la arena cósmica. "
        f"Esas experiencias te han traído hasta este momento presente, donde {presente.lower()} despliega sus alas "
        f"como mariposas de luz en tu realidad actual. "
        f"Y mira, las estrellas susurran que si continúas este camino, {futuro.lower()} se manifestará en tu horizonte. "
        f"Mi consejo felino es este: confía en tu intuición como los gatos confiamos en nuestros bigotes cósmicos. "
        f"El Destino ha tejido su tapiz, pero eres tú quien decide cómo caminar sobre él. "
        f"Que la sabiduría del Universo ilumine tu sendero, valiente humano..."
    )


running = True

while running:
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == "welcome":
                # Girar solo la carta clicada
                for i, pos in enumerate(cards_position):
                    carta_rect = pygame.Rect(pos[0], pos[1], 200, 350)
                    if carta_rect.collidepoint(mouse_pos) and revealed_cards[i] is None:
                        selected_card = deck.select_card()
                        revealed_cards[i] = selected_card
                        animating[i] = True
                        print(f"Carta {i + 1} girada.")
                        # Si todas las cartas están reveladas, generar la historia y cambiar estado
                        if all(card is not None for card in revealed_cards):
                            story = generate_hf_story(revealed_cards, deck)
                            displayed_story = ""
                            typing_index = 0
                            scroll_y = 0
                            game_state = "game"
                            animation_active = True
                            frame_time = pygame.time.get_ticks()
                            frame_change_count = 0
                            print("Todas las cartas giradas. Transición a juego principal.")
                        break
            elif game_state == "game":
                pass
        elif event.type == pygame.MOUSEWHEEL and game_state == "game":
            scroll_y += event.y * 20
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                cat_sprite = select_cat_image(cat_images)
                if cat_sprite is None:
                    print("No se pudo cargar una nueva imagen. Usando placeholder.")
                    cat_sprite = pygame.Surface((270, 270))
                    cat_sprite.fill(RED)
            elif event.key == pygame.K_r and game_state == "game":
                print("Reiniciando juego...")
                deck.shuffle()
                revealed_cards = [None, None, None]
                rotation_angles = [0, 0, 0]
                animating = [False, False, False]
                story = ""
                displayed_story = ""
                typing_index = 0
                scroll_y = 0
                welcome_message = generate_welcome_message()
                displayed_welcome = ""
                welcome_typing_index = 0
                game_state = "welcome"
                animation_active = True

    # Animación de rotación de cartas
    for i in range(len(revealed_cards)):
        if animating[i]:
            rotation_angles[i] += ROTATION_SPEED
            if rotation_angles[i] >= 180:
                rotation_angles[i] = 180
                animating[i] = False

    # Efecto de escritura para el mensaje de bienvenida
    if game_state == "welcome" and welcome_message and welcome_typing_index < len(welcome_message):
        if current_time - welcome_last_typed_time >= typing_speed:
            displayed_welcome = welcome_message[:welcome_typing_index + 1]
            welcome_typing_index += 1
            welcome_last_typed_time = current_time
            animation_active = True
    # Efecto de escritura para la historia
    elif game_state == "game" and story and typing_index < len(story):
        if current_time - last_typed_time >= typing_speed:
            displayed_story = story[:typing_index + 1]
            typing_index += 1
            last_typed_time = current_time
            animation_active = True
    else:
        animation_active = False if game_state == "game" else animation_active

    # Animación del gato
    if animation_active and len(cat_images) > max(ANIMATION_FRAMES):
        current_time_ms = pygame.time.get_ticks()
        if current_time_ms - frame_time >= FRAME_DELAY:
            frame_time = current_time_ms
            frame_change_count += 1
            if frame_change_count % 2 == 0:
                current_frame = random.choice(ANIMATION_FRAMES)
            else:
                current_frame = random.choices(
                    [0] + ANIMATION_FRAMES,
                    weights=[0.7, 0.1, 0.1, 0.1]
                )[0]
            cat_sprite = cat_images[current_frame]

    # Dibujar fondo
    screen.blit(background_img, (0, 0))

    # Dibujar cartas
    for i, pos in enumerate(cards_position):
        if revealed_cards[i] is not None:
            card_num, is_reversed = revealed_cards[i]
            if animating[i]:
                scale_factor = abs(math.cos(math.radians(rotation_angles[i])))
                new_height = int(350 * scale_factor)
                if rotation_angles[i] <= 90:
                    scaled_img = pygame.transform.scale(back_img, (200, new_height))
                else:
                    card_img = cards_img[card_num]
                    if is_reversed:
                        card_img = pygame.transform.rotate(card_img, 180)
                    scaled_img = pygame.transform.scale(card_img, (200, new_height))
                rect = scaled_img.get_rect(midbottom=(pos[0] + 100, pos[1] + 350))
                screen.blit(scaled_img, rect.topleft)
            else:
                final_img = pygame.transform.rotate(cards_img[card_num], 180) if is_reversed else cards_img[card_num]
                screen.blit(final_img, pos)
        else:
            screen.blit(back_img, pos)

    # Dibujar cuadro de texto
    if game_state == "welcome":
        margin = 20
        rect_x = margin
        rect_y = 620
        rect_width = WIDTH - 2 * margin
        rect_height = HEIGHT - rect_y - margin
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), 2)

        if displayed_welcome:
            font = pygame.font.Font(None, 24)
            text_x = margin + 30
            max_width = rect_width - 60
            y_offset = rect_y + 20 + scroll_y
            lines = []
            current_line = ''
            words = displayed_welcome.split(' ')
            for word in words:
                test_line = current_line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + ' '
            lines.append(current_line)

            total_lines = len(lines)
            line_height = font.get_height()
            if total_lines > max_visible_lines:
                scroll_y = -((total_lines - max_visible_lines) * line_height)

            for i, line in enumerate(lines):
                text_y = y_offset + i * line_height
                if rect_y <= text_y < rect_y + rect_height:
                    text = font.render(line, True, BLACK)
                    screen.blit(text, (text_x, text_y))
    elif game_state == "game":
        margin = 20
        rect_x = margin
        rect_y = 620
        rect_width = WIDTH - 2 * margin
        rect_height = HEIGHT - rect_y - margin
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), 2)

        if displayed_story:
            font = pygame.font.Font(None, 24)
            text_x = margin + 30
            max_width = rect_width - 60
            y_offset = rect_y + 20 + scroll_y
            lines = []
            current_line = ''
            words = displayed_story.split(' ')
            for word in words:
                test_line = current_line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + ' '
            lines.append(current_line)

            total_lines = len(lines)
            line_height = font.get_height()
            if total_lines > max_visible_lines:
                scroll_y = -((total_lines - max_visible_lines) * line_height)

            for i, line in enumerate(lines):
                text_y = y_offset + i * line_height
                if rect_y <= text_y < rect_y + rect_height:
                    text = font.render(line, True, BLACK)
                    screen.blit(text, (text_x, text_y))

        # Mostrar instrucción para reiniciar
        help_font = pygame.font.Font(None, 20)
        help_text = help_font.render("Presiona R para reiniciar", True, BLACK)
        screen.blit(help_text, (WIDTH - 200, HEIGHT - 15))

    # Dibujar gatito
    if cat_sprite:
        cat_rect = cat_sprite.get_rect(center=cat_position)
        screen.blit(cat_sprite, cat_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()