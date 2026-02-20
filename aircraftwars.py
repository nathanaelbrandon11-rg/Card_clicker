import pygame
import random
import math

# Inisialisasi Pygame
pygame.init()

# Konstanta
LEBAR = 800
TINGGI = 600
FPS = 60
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
MERAH = (255, 0, 0)
BIRU = (50, 150, 255)
KUNING = (255, 255, 0)
HIJAU = (0, 255, 0)

# Setup layar
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Space Shooter dengan List Python")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Class untuk Pemain
class Pemain:
    def __init__(self):
        self.x = LEBAR // 2
        self.y = TINGGI - 80
        self.lebar = 40
        self.tinggi = 40
        self.kecepatan = 5
        self.nyawa = 3
        
    def gerak(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.kecepatan
        if keys[pygame.K_RIGHT] and self.x < LEBAR - self.lebar:
            self.x += self.kecepatan
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.kecepatan
        if keys[pygame.K_DOWN] and self.y < TINGGI - self.tinggi:
            self.y += self.kecepatan
            
    def gambar(self):
        # Body pesawat
        pygame.draw.polygon(layar, BIRU, [
            (self.x + self.lebar//2, self.y),
            (self.x, self.y + self.tinggi),
            (self.x + self.lebar, self.y + self.tinggi)
        ])
        # Cockpit
        pygame.draw.circle(layar, PUTIH, (self.x + self.lebar//2, self.y + 20), 8)

# Class untuk Peluru (menggunakan list)
class Peluru:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.kecepatan = 8
        self.radius = 4
        
    def update(self):
        self.y -= self.kecepatan
        
    def gambar(self):
        pygame.draw.circle(layar, KUNING, (int(self.x), int(self.y)), self.radius)

# Class untuk Musuh
class Musuh:
    def __init__(self):
        self.x = random.randint(20, LEBAR - 20)
        self.y = random.randint(-100, -40)
        self.lebar = 30
        self.tinggi = 30
        self.kecepatan = random.randint(2, 5)
        self.warna = random.choice([MERAH, (255, 100, 0), (200, 0, 100)])
        
    def update(self):
        self.y += self.kecepatan
        
    def gambar(self):
        # Body musuh
        pygame.draw.rect(layar, self.warna, 
                        (self.x, self.y, self.lebar, self.tinggi))
        # Mata
        pygame.draw.circle(layar, HITAM, (int(self.x + 10), int(self.y + 10)), 3)
        pygame.draw.circle(layar, HITAM, (int(self.x + 20), int(self.y + 10)), 3)

# Class untuk Partikel (efek ledakan)
class Partikel:
    def __init__(self, x, y, warna):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.radius = random.randint(2, 5)
        self.warna = warna
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.radius = max(1, self.radius - 0.1)
        
    def gambar(self):
        if self.lifetime > 0:
            pygame.draw.circle(layar, self.warna, (int(self.x), int(self.y)), int(self.radius))

# Class untuk Bintang latar belakang
class Bintang:
    def __init__(self):
        self.x = random.randint(0, LEBAR)
        self.y = random.randint(0, TINGGI)
        self.kecepatan = random.uniform(0.5, 2)
        self.ukuran = random.randint(1, 3)
        
    def update(self):
        self.y += self.kecepatan
        if self.y > TINGGI:
            self.y = 0
            self.x = random.randint(0, LEBAR)
            
    def gambar(self):
        pygame.draw.circle(layar, PUTIH, (int(self.x), int(self.y)), self.ukuran)

# Fungsi untuk membuat ledakan
def buat_ledakan(x, y, warna, jumlah=20):
    for _ in range(jumlah):
        partikel_list.append(Partikel(x, y, warna))

# Fungsi cek tabrakan
def cek_tabrakan(obj1_x, obj1_y, obj1_lebar, obj1_tinggi, obj2_x, obj2_y, obj2_lebar, obj2_tinggi):
    return (obj1_x < obj2_x + obj2_lebar and
            obj1_x + obj1_lebar > obj2_x and
            obj1_y < obj2_y + obj2_tinggi and
            obj1_y + obj1_tinggi > obj2_y)

# Inisialisasi objek game
pemain = Pemain()

# LIST-LIST UTAMA YANG DIGUNAKAN


# TUGAS: Buat 3 list kosong untuk menyimpan objek-objek game
# 1. Buat list bernama peluru_list untuk menyimpan semua peluru yang ditembakkan
# 2. Buat list bernama musuh_list untuk menyimpan semua musuh yang muncul
# 3. Buat list bernama partikel_list untuk menyimpan efek partikel ledakan
peluru_list = []
musuh_list = []
partikel_list = []
      
bintang_list = [Bintang() for _ in range(50)] 

# Variabel game
skor = 0
game_over = False
spawn_timer = 0

# Game Loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Tembak peluru saat tekan SPACE
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                peluru_baru = Peluru(pemain.x + pemain.lebar//2, pemain.y)
                peluru_list.append(peluru_baru)  # Menambah ke list
                
            # Restart game
            if event.key == pygame.K_r and game_over:
                pemain = Pemain()
                peluru_list.clear()
                musuh_list.clear()
                partikel_list.clear()
                skor = 0
                game_over = False
    
    if not game_over:
        # Input pemain
        keys = pygame.key.get_pressed()
        pemain.gerak(keys)
        
        # Spawn musuh menggunakan timer
        spawn_timer += 1
        if spawn_timer > 40:  # Spawn setiap 40 frame
            musuh_list.append(Musuh())
            spawn_timer = 0
        
        # Update bintang
        for bintang in bintang_list:
            bintang.update()
        
        # Update peluru dan hapus yang keluar layar
        for peluru in peluru_list[:]:  # Gunakan slice untuk iterasi aman
            peluru.update()
            if peluru.y < 0:
                peluru_list.remove(peluru)
        
        # Update musuh
        for musuh in musuh_list[:]:
            musuh.update()
            
            # Hapus musuh yang keluar layar
            if musuh.y > TINGGI:
                musuh_list.remove(musuh)
                
            # Cek tabrakan dengan pemain
            if cek_tabrakan(pemain.x, pemain.y, pemain.lebar, pemain.tinggi,
                           musuh.x, musuh.y, musuh.lebar, musuh.tinggi):
                buat_ledakan(musuh.x + musuh.lebar//2, musuh.y + musuh.tinggi//2, MERAH, 30)
                musuh_list.remove(musuh)
                pemain.nyawa -= 1
                if pemain.nyawa <= 0:
                    game_over = True
        
        # Cek tabrakan peluru dengan musuh
        for peluru in peluru_list[:]:
            for musuh in musuh_list[:]:
                if cek_tabrakan(peluru.x - peluru.radius, peluru.y - peluru.radius, 
                               peluru.radius * 2, peluru.radius * 2,
                               musuh.x, musuh.y, musuh.lebar, musuh.tinggi):
                    # Buat ledakan
                    buat_ledakan(musuh.x + musuh.lebar//2, musuh.y + musuh.tinggi//2, 
                               musuh.warna, 15)
                    if peluru in peluru_list:
                        peluru_list.remove(peluru)
                    if musuh in musuh_list:
                        musuh_list.remove(musuh)
                    skor += 10
                    break
        
        # Update partikel
        for partikel in partikel_list[:]:
            partikel.update()
            if partikel.lifetime <= 0:
                partikel_list.remove(partikel)
    
    # Render
    layar.fill(HITAM)
    
    # Gambar bintang
    for bintang in bintang_list:
        bintang.gambar()
    
    # Gambar semua objek
    pemain.gambar()
    
    for peluru in peluru_list:
        peluru.gambar()
    
    for musuh in musuh_list:
        musuh.gambar()
    
    for partikel in partikel_list:
        partikel.gambar()
    
    # Gambar UI
    teks_skor = font.render(f"Skor: {skor}", True, PUTIH)
    layar.blit(teks_skor, (10, 10))
    
    teks_nyawa = font.render(f"Nyawa: {pemain.nyawa}", True, HIJAU)
    layar.blit(teks_nyawa, (10, 50))
    
    # Info jumlah objek di list (untuk pembelajaran)
    info_font = pygame.font.Font(None, 20)
    info_peluru = info_font.render(f"Peluru: {len(peluru_list)}", True, KUNING)
    info_musuh = info_font.render(f"Musuh: {len(musuh_list)}", True, MERAH)
    info_partikel = info_font.render(f"Partikel: {len(partikel_list)}", True, (255, 150, 0))
    
    layar.blit(info_peluru, (LEBAR - 120, 10))
    layar.blit(info_musuh, (LEBAR - 120, 30))
    layar.blit(info_partikel, (LEBAR - 120, 50))
    
    # Game Over screen
    if game_over:
        overlay = pygame.Surface((LEBAR, TINGGI))
        overlay.set_alpha(180)
        overlay.fill(HITAM)
        layar.blit(overlay, (0, 0))
        
        teks_game_over = font.render("GAME OVER!", True, MERAH)
        teks_skor_akhir = font.render(f"Skor Akhir: {skor}", True, PUTIH)
        teks_restart = font.render("Tekan R untuk Main Lagi", True, HIJAU)
        
        layar.blit(teks_game_over, (LEBAR//2 - 100, TINGGI//2 - 50))
        layar.blit(teks_skor_akhir, (LEBAR//2 - 120, TINGGI//2))
        layar.blit(teks_restart, (LEBAR//2 - 160, TINGGI//2 + 50))
    
    pygame.display.flip()

pygame.quit()
