import pygame
import json
import sys
import os

pygame.init()

pygame.mixer.music.load("sounds/music.ogg")
pygame.mixer.music.set_volume(0.16)
pygame.mixer.music.play(loops = -1)  # -1 = en boucle infinie

click_sound = pygame.mixer.Sound("sounds/click.wav")  # pour clic cookie
buy_sound = pygame.mixer.Sound("sounds/buy.wav")  # pour achat

# Création de la fenêtre
screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
pygame.display.set_caption("Cookie Clicker")

# Charger les images
image_fond = pygame.image.load("images/fond.jpg")  # Fond
image_fond_rect = image_fond.get_rect(topleft=(0, 0))


image_cookie = pygame.image.load("images/image cookie.png")  # Cookie
image_cookie_rect = image_cookie.get_rect(topleft=(102, 101))

image_autoclick1 = pygame.image.load("images/Autoclick 1.png")  # Autoclick 1
image_autoclick1_rect = image_autoclick1.get_rect(topleft=(740, 230))
image_autoclick2 = pygame.image.load("images/Autoclick 2.png")  # Autoclick 2
image_autoclick2_rect = image_autoclick2.get_rect(topleft=(740, 310))
image_autoclick3 = pygame.image.load("images/Autoclick 3.png")  # Autoclick 3
image_autoclick3_rect = image_autoclick3.get_rect(topleft=(740, 390))

image_click2 = pygame.image.load("images/Click x2.png")  # Click x2
image_click2_rect = image_click2.get_rect(topleft=(800, 160))
image_click5 = pygame.image.load("images/Click x5.png")  # Click x5
image_click5_rect = image_click5.get_rect(topleft=(800, 240))
image_click20 = pygame.image.load("images/Click x20.png")  # Click x20
image_click20_rect = image_click20.get_rect(topleft=(800, 320))
image_click100 = pygame.image.load("images/Click x100.png")  # Click x100
image_click100_rect = image_click100.get_rect(topleft=(800, 400))

image_click2_v = pygame.image.load("images/Click x2 use.png")  # Click x2
image_click2_v_rect = image_click2_v.get_rect(topleft=(800, 160))
image_click5_v = pygame.image.load("images/Click x5 use.png")  # Click x5
image_click5_v_rect = image_click5_v.get_rect(topleft=(800, 240))
image_click20_v = pygame.image.load("images/Click x20 use.png")  # Click x20
image_click20_v_rect = image_click20_v.get_rect(topleft=(800, 320))
image_click100_v = pygame.image.load("images/Click x100 use.png")  # Click x100
image_click100_v_rect = image_click100_v.get_rect(topleft=(800, 400))

image_1 = pygame.image.load("images/1g.png")  # Upgrade x1
image_1_rect = image_1.get_rect(topleft=(820, 150))
image_10 = pygame.image.load("images/10g.png")  # Upgrade x10
image_10_rect = image_10.get_rect(topleft=(885, 150))
image_50 = pygame.image.load("images/50g.png")  # Upgrade x50
image_50_rect = image_50.get_rect(topleft=(961, 150))

image_1_v = pygame.image.load("images/1v.png")  # Upgrade x1 actif
image_10_v = pygame.image.load("images/10v.png")  # Upgrade x10 actif
image_50_v = pygame.image.load("images/50v.png")  # Upgrade x50 actif

image_home = pygame.image.load("images/button.png")  # Home
image_home_rect = image_home.get_rect(topleft=(985, 50))
image_c_page = pygame.image.load("images/cookie.png")  # The other page
image_c_page_rect = image_c_page.get_rect(topleft=(920, 50))


# Déclaration des valeurs
cookie = 0
autoclick1, autoclick2, autoclick3 = 0, 0, 0
prix_autoclick1, prix_autoclick2, prix_autoclick3 = 20, 400, 10000
prix_x2, prix_x5, prix_x20, prix_x100 = 250, 1800, 3200, 6800
cookie_s = 0
click = 1
x2, x5, x20, x100 = True, True, True, True
home = False
c_page = True
upgrade = 1
possible = True
prix = 0
floating_texts = []
SAVE_FILE = "save.json"

SAVE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SAVE_EVENT, 60000)  # 60000 ms = 1 minute


# Afficher quand on click sur le cookie
class FloatingText:
    def __init__(self, text, pos, color=(0, 0, 0), lifetime=60):
        self.text = text
        self.x, self.y = pos
        self.color = color
        self.total_lifetime = lifetime
        self.lifetime = lifetime
        self.alpha = 255

    def update(self):
        self.y -= 1
        self.lifetime -= 1
        # Alpha diminue proportionnellement à la durée restante
        self.alpha = int(255 * (self.lifetime / self.total_lifetime))

    def draw(self, screen, font):
        if self.lifetime > 0:
            surf = font.render(self.text, True, self.color)
            surf.set_alpha(self.alpha)
            screen.blit(surf, (self.x, self.y))

    def is_alive(self):
        return self.lifetime > 0

def sauvegarder():
    data = {
        "cookie": cookie,
        "autoclick1": autoclick1,
        "autoclick2": autoclick2,
        "autoclick3": autoclick3,
        "prix_autoclick1": prix_autoclick1,
        "prix_autoclick2": prix_autoclick2,
        "prix_autoclick3": prix_autoclick3,
        "click": click,
        "x2": x2,
        "x5": x5,
        "x20": x20,
        "x100": x100
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def charger():
    global cookie, autoclick1, autoclick2, autoclick3
    global prix_autoclick1, prix_autoclick2, prix_autoclick3
    global click, x2, x5, x20, x100

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            cookie = data.get("cookie", 0)
            autoclick1 = data.get("autoclick1", 0)
            autoclick2 = data.get("autoclick2", 0)
            autoclick3 = data.get("autoclick3", 0)
            prix_autoclick1 = data.get("prix_autoclick1", 20)
            prix_autoclick2 = data.get("prix_autoclick2", 400)
            prix_autoclick3 = data.get("prix_autoclick3", 10000)
            click = data.get("click", 1)
            x2 = data.get("x2", True)
            x5 = data.get("x5", True)
            x20 = data.get("x20", True)
            x100 = data.get("x100", True)

# Agrandir les boutons quand on passe dessus
def draw_hover_image(image, rect, scale=1.05):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        w, h = rect.width, rect.height
        new_size = (int(w * scale), int(h * scale))
        scaled_img = pygame.transform.scale(image, new_size)
        new_rect = scaled_img.get_rect(center=rect.center)
        screen.blit(scaled_img, new_rect)
    else:
        screen.blit(image, rect)

# Fonction afficher les nombre cookie arrondie
def format_cookie_count(n):
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.2f}B"
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.2f}K"
    else:
        return str(int(n))
    
# Fonction couleur prix autoclick
def can_afford(cookies, price, quantity, coefficient):
    for _ in range(quantity):
        if cookies < price:
            return False
        cookies -= int(price)
        price *= coefficient
    return True

charger()
# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Fermer la fenêtre
            running = False
            sauvegarder()
        elif event.type == SAVE_EVENT:
            sauvegarder()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if image_home_rect.collidepoint(event.pos):
                c_page = False
                home = True
            if image_c_page_rect.collidepoint(event.pos):
                c_page = True
                home = False
                
            if image_cookie_rect.collidepoint(event.pos):  # +1 si click sur le cookie
                   cookie += click
                   click_sound.play()
                   floating_texts.append(FloatingText(f"+{click}", event.pos, (0, 0, 0), lifetime = 180))
            
            if c_page:
                if image_1_rect.collidepoint(event.pos):
                    upgrade = 1
                if image_10_rect.collidepoint(event.pos):
                    upgrade = 10
                if image_50_rect.collidepoint(event.pos):
                    upgrade = 50
                    
                if image_autoclick1_rect.collidepoint(event.pos):  # +1 si click sur autoclick 1
                    possible = True
                    temp_cookie = cookie
                    temp_prix = prix_autoclick1
                    temp_autoclick1 = autoclick1

                    for i in range(upgrade):
                        if temp_cookie >= temp_prix:
                            temp_cookie -= int(temp_prix)
                            temp_autoclick1 += 1
                            temp_prix *= 1.2
                        else:
                            possible = False
                            break

                    if possible:
                        cookie = temp_cookie
                        prix_autoclick1 = temp_prix
                        autoclick1 = temp_autoclick1
                        buy_sound.play()
                if image_autoclick2_rect.collidepoint(event.pos):  # +1 si click sur autoclick 2
                    possible = True
                    temp_cookie = cookie
                    temp_prix = prix_autoclick2
                    temp_autoclick2 = autoclick2

                    for i in range(upgrade):
                        if temp_cookie >= temp_prix:
                            temp_cookie -= int(temp_prix)
                            temp_autoclick2 += 1
                            temp_prix *= 1.3
                        else:
                            possible = False
                            break

                    if possible:
                        cookie = temp_cookie
                        prix_autoclick2 = temp_prix
                        autoclick2 = temp_autoclick2
                        buy_sound.play()
                if image_autoclick3_rect.collidepoint(event.pos):  # +1 si click sur autoclick 3
                    possible = True
                    temp_cookie = cookie
                    temp_prix = prix_autoclick3
                    temp_autoclick3 = autoclick3

                    for i in range(upgrade):
                        if temp_cookie >= temp_prix:
                            temp_cookie -= int(temp_prix)
                            temp_autoclick3 += 1
                            temp_prix *= 1.4
                        else:
                            possible = False
                            break

                    if possible:
                        cookie = temp_cookie
                        prix_autoclick3 = temp_prix
                        autoclick3 = temp_autoclick3
                        buy_sound.play()

            if home:
                if image_click2_rect.collidepoint(event.pos) and cookie >= 250 and x2 == True:  # Click x2
                    click = 2
                    cookie -= 250
                    x2 = False
                    buy_sound.play()
                if image_click5_rect.collidepoint(event.pos) and cookie >= 1800 and x5 == True:  # Click x5
                    click = 5
                    cookie -= 1800
                    x5 = False
                    buy_sound.play()
                if image_click20_rect.collidepoint(event.pos) and cookie >= 3200 and x20 == True:  # Click x20
                    click = 20
                    cookie -= 3200
                    x20 = False
                    buy_sound.play()
                if image_click100_rect.collidepoint(event.pos) and cookie >= 6800 and x100 == True:  # Click x100
                    click = 100
                    cookie -= 6800
                    x100 = False
                    buy_sound.play()


        # Timer toutes les 1/100 secondes
        ADDVALUE = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDVALUE, 9)

        if autoclick1 > 0:
            if event.type == ADDVALUE:
                cookie += autoclick1 / 100 + autoclick2 / 10 + autoclick3  # Ajouter 'autoclick' toutes les secondes
                cookie_s = autoclick1 + autoclick2 * 10 + autoclick3 * 100  # Calcule le nombre de cookies par secondes


    screen.fill((255, 255, 255))  # Fond blanc 
    screen.blit(image_fond, image_fond_rect) # Fond cookie

    screen.blit(pygame.font.Font(None, 43).render(f"Cookies = {format_cookie_count(cookie)}", True, (0, 0, 0)), (210, 60))
    screen.blit(pygame.font.Font(None, 30).render(f"{cookie_s} cookies/s", True, (0, 0, 0)), (250, 100))
    
    if c_page:
        # Autoclicks
        if upgrade == 1:
            draw_hover_image(image_1_v, image_1_rect)
            draw_hover_image(image_10, image_10_rect)
            draw_hover_image(image_50, image_50_rect)
        elif upgrade == 10:
            draw_hover_image(image_1, image_1_rect)
            draw_hover_image(image_10_v, image_10_rect)
            draw_hover_image(image_50, image_50_rect)
        elif upgrade == 50:
            draw_hover_image(image_1, image_1_rect)
            draw_hover_image(image_10, image_10_rect)
            draw_hover_image(image_50_v, image_50_rect)
        
        
        # AUTCLICK 1
        draw_hover_image(image_autoclick1, image_autoclick1_rect)
        if can_afford(cookie, prix_autoclick1, upgrade, 1.2):
            color = (0, 169, 0)
        else:
            color = (255, 255, 255)
        screen.blit(pygame.font.Font(None, 30).render(f"lvl {autoclick1}    prix: {int(prix_autoclick1)}", True, color), (925, 241))

        # AUTCLICK 2
        draw_hover_image(image_autoclick2, image_autoclick2_rect)
        if can_afford(cookie, prix_autoclick2, upgrade, 1.3):
            color = (0, 169, 0)
        else:
            color = (255, 255, 255)
        screen.blit(pygame.font.Font(None, 30).render(f"lvl {autoclick2}    prix: {int(prix_autoclick2)}", True, color), (925, 321))

        # AUTCLICK 3
        draw_hover_image(image_autoclick3, image_autoclick3_rect)
        if can_afford(cookie, prix_autoclick3, upgrade, 1.4):
            color = (0, 169, 0)
        else:
            color = (255, 255, 255)
        screen.blit(pygame.font.Font(None, 30).render(f"lvl {autoclick3}    prix: {int(prix_autoclick3)}", True, color), (925, 401))

    if home:
        # Click upgrades
        if x2:
            draw_hover_image(image_click2, image_click2_rect)
            prix_txt = "prix: 250"
            color = (0, 169, 0) if cookie >= 250 else (255, 255, 255)
            screen.blit(pygame.font.Font(None, 30).render(prix_txt, True, color), (960, 170))
        else:
            draw_hover_image(image_click2_v, image_click2_v_rect)

        if x5:
            draw_hover_image(image_click5, image_click5_rect)
            prix_txt = "prix: 1800"
            color = (0, 169, 0) if cookie >= 1800 else (255, 255, 255)
            screen.blit(pygame.font.Font(None, 30).render(prix_txt, True, color), (960, 250))
        else:
            draw_hover_image(image_click5_v, image_click5_v_rect)

        if x20:
            draw_hover_image(image_click20, image_click20_rect)
            prix_txt = "prix: 3200"
            color = (0, 169, 0) if cookie >= 3200 else (255, 255, 255)
            screen.blit(pygame.font.Font(None, 30).render(prix_txt, True, color), (960, 330))
        else:
            draw_hover_image(image_click20_v, image_click20_v_rect)

        if x100:
            draw_hover_image(image_click100, image_click100_rect)
            prix_txt = "prix: 6800"
            color = (0, 169, 0) if cookie >= 6800 else (255, 255, 255)
            screen.blit(pygame.font.Font(None, 30).render(prix_txt, True, color), (960, 410))
        else:
            draw_hover_image(image_click100_v, image_click100_v_rect)
            
    draw_hover_image(image_cookie, image_cookie_rect)
    
    font = pygame.font.Font(None, 30)
    for text in floating_texts[:]:
        text.update()
        text.draw(screen, font)
        if not text.is_alive():
            floating_texts.remove(text)
            
    # Barre de navigation
    pygame.draw.rect(screen, (200, 173, 127), (910, 40, 141, 68), border_radius = 15)
    draw_hover_image(image_home, image_home_rect)
    draw_hover_image(image_c_page, image_c_page_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()

n