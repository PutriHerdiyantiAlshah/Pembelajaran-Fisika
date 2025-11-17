import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulasi Lensa Cembung - Versi Tombol Detail")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)
GREEN = (0, 200, 0)
BLUE = (50, 100, 255)
GRAY = (210, 210, 210)
DARKGRAY = (160, 160, 160)
BROWN = (139, 69, 19)
ORANGE = (255, 140, 0)
PURPLE = (180, 0, 180)

font = pygame.font.SysFont("arial", 20)

# Variabel utama
angle_incident = 30
n1, n2 = 1.0, 1.5
show_refraction = True
show_reflection = True
object_list = ["Panah", "Pensil", "Kaca", "Bola", "Buku"]
object_index = 0
object_type = object_list[object_index]
lens_diameter = 120

# --- Fungsi fisika dasar ---
def snell(theta_inc, n1, n2):
    try:
        theta_i_rad = math.radians(theta_inc)
        theta_r_rad = math.asin(n1 * math.sin(theta_i_rad) / n2)
        return math.degrees(theta_r_rad)
    except ValueError:
        return None  # Total internal reflection


# --- Fungsi gambar ---
def draw_optical_axis():
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)
    text = font.render("Sumbu Optik", True, BLACK)
    screen.blit(text, (20, HEIGHT // 2 - 30))


def draw_object(center):
    """Menggambar objek (Panah, Pensil, Kaca, Bola, Buku) di sisi kiri"""
    base_x = center[0] - 300
    base_y = center[1]

    if object_type == "Panah":
        pygame.draw.line(screen, BLUE, (base_x, base_y), (base_x, base_y - 100), 6)
        pygame.draw.polygon(screen, BLUE, [(base_x - 10, base_y - 100),
                                           (base_x + 10, base_y - 100),
                                           (base_x, base_y - 120)])
    elif object_type == "Pensil":
        pygame.draw.rect(screen, BROWN, (base_x - 8, base_y - 100, 16, 100))
        pygame.draw.polygon(screen, ORANGE, [(base_x - 8, base_y - 100),
                                             (base_x + 8, base_y - 100),
                                             (base_x, base_y - 115)])
    elif object_type == "Kaca":
        pygame.draw.rect(screen, (180, 240, 255), (base_x - 25, base_y - 100, 50, 100))
        pygame.draw.rect(screen, BLACK, (base_x - 25, base_y - 100, 50, 100), 2)
    elif object_type == "Bola":
        pygame.draw.circle(screen, RED, (base_x, base_y - 50), 30)
        pygame.draw.circle(screen, WHITE, (base_x, base_y - 50), 30, 2)
    elif object_type == "Buku":
        pygame.draw.rect(screen, PURPLE, (base_x - 30, base_y - 80, 60, 80))
        pygame.draw.line(screen, WHITE, (base_x, base_y - 80), (base_x, base_y), 2)
        pygame.draw.rect(screen, BLACK, (base_x - 30, base_y - 80, 60, 80), 2)


def draw_lens(center):
    """Menggambar lensa cembung"""
    pygame.draw.ellipse(screen, (150, 200, 255),
                        (center[0] - 10, center[1] - lens_diameter // 2,
                         20, lens_diameter))
    text = font.render("Lensa Cembung", True, BLACK)
    screen.blit(text, (center[0] - 60, center[1] + lens_diameter // 2 + 10))


def draw_rays(center):
    """Menggambar sinar datang, pantul, dan bias"""
    inc_len = 250
    inc_x = center[0] - inc_len * math.cos(math.radians(angle_incident))
    inc_y = center[1] - inc_len * math.sin(math.radians(angle_incident))

    # Sinar datang
    pygame.draw.line(screen, YELLOW, (inc_x, inc_y), center, 3)

    if show_reflection:
        # Sinar pantul
        pygame.draw.line(screen, RED, center,
                         (center[0] - inc_len * math.cos(math.radians(angle_incident)),
                          center[1] + inc_len * math.sin(math.radians(angle_incident))), 3)

    if show_refraction:
        refr_angle = snell(angle_incident, n1, n2)
        if refr_angle:
            refr_len = 350
            refr_x = center[0] + refr_len * math.cos(math.radians(refr_angle))
            refr_y = center[1] + refr_len * math.sin(math.radians(refr_angle))
            pygame.draw.line(screen, GREEN, center, (refr_x, refr_y), 3)
        else:
            msg = font.render("Total Internal Reflection!", True, RED)
            screen.blit(msg, (50, 600))


def draw_info():
    info = [
        f"Sudut Datang: {angle_incident}°",
        f"n1 (Udara): {n1}",
        f"n2 (Medium): {n2}",
        f"Objek: {object_type}",
        f"Diameter Lensa: {lens_diameter}px",
        f"Refleksi: {'Ya' if show_reflection else 'Tidak'}",
        f"Refraksi: {'Ya' if show_refraction else 'Tidak'}"
    ]
    for i, t in enumerate(info):
        txt = font.render(t, True, BLACK)
        screen.blit(txt, (20, 20 + i * 25))


# --- Tombol interaktif ---
def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    color = DARKGRAY if rect.collidepoint(mouse) else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=8)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (x + 10, y + 8))

    if rect.collidepoint(mouse) and click[0] == 1 and action:
        pygame.time.wait(150)
        action()


# --- Aksi tombol ---
def tambah_sudut():
    global angle_incident
    if angle_incident < 89:
        angle_incident += 1


def kurang_sudut():
    global angle_incident
    if angle_incident > 0:
        angle_incident -= 1


def ganti_objek():
    global object_index, object_type
    object_index = (object_index + 1) % len(object_list)
    object_type = object_list[object_index]


def tambah_diameter():
    global lens_diameter
    if lens_diameter < 300:
        lens_diameter += 10


def kurang_diameter():
    global lens_diameter
    if lens_diameter > 60:
        lens_diameter -= 10


def toggle_refleksi():
    global show_reflection
    show_reflection = not show_reflection


def toggle_refraksi():
    global show_refraction
    show_refraction = not show_refraction


# --- Loop utama ---
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    center = (WIDTH // 2, HEIGHT // 2)

    draw_optical_axis()
    draw_object(center)
    draw_lens(center)
    draw_rays(center)
    draw_info()

    # Tombol kontrol
    draw_button("Tambah Sudut (+1°)", 750, 40, 200, 40, tambah_sudut)
    draw_button("Kurangi Sudut (-1°)", 750, 90, 200, 40, kurang_sudut)
    draw_button("Ganti Objek", 750, 140, 200, 40, ganti_objek)
    draw_button("Tambah Diameter", 750, 190, 200, 40, tambah_diameter)
    draw_button("Kurangi Diameter", 750, 240, 200, 40, kurang_diameter)
    draw_button("Tampilkan / Sembunyikan Refleksi", 700, 290, 280, 40, toggle_refleksi)
    draw_button("Tampilkan / Sembunyikan Refraksi", 700, 340, 280, 40, toggle_refraksi)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

sys.exit()



