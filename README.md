# 🎮 Turn-Based RPG Game (Python OOP)

Proyek ini adalah sebuah **game RPG berbasis turn-based** yang dikembangkan menggunakan paradigma **Object-Oriented Programming (OOP)** di Python. Pemain akan memilih tim hero, melawan boss, menggunakan skill, special skill, item, dan melewati sistem battle & shop secara bergantian per turn.

---

## 🧩 Fitur Utama

- Sistem turn-based battle antara 5 Hero vs 1 Boss
- Skill dan Special Skill dengan sistem MP, efek area/single, dan rarity
- Sistem item dan equipment (maks 5 slot)
- Shop system dengan refresh stock tiap turn
- Sistem income per turn (aritmetik)
- Game over jika seluruh hero mati/retreat atau boss dikalahkan
- OOP terstruktur dan scalable

---

## 🔁 Alur Permainan (Flow)

1. **Inisialisasi Awal**
   - Generate semua skill, special skill, dan item
   - Generate hero pool & boss
   - Pilih 5 hero
   - Bagikan 3 item awal ke hero secara acak

2. **Turn 1: Battle Langsung**
   - Setiap hero & boss menyerang sesuai giliran

3. **Turn ≥ 2**
   - Tambah income ke setiap hero: `100 * turn_number`
   - Shop Phase (beli/jual item)
   - Battle Phase
   - Check Game Over
   - turn_number += 1

---

## 📜 Ketentuan Sistem

- 5 Hero dan 1 Boss aktif di setiap game
- Skill terdiri dari:
  - Tipe: `atk`, `healing`, `buff`, `debuff`
  - Target: `single`, `multi`
  - Rarity: `common (45%)`, `uncommon (25%)`, `rare (15%)`, `epic (10%)`, `legendary (5%)`
- Special Skill hanya 1 per karakter
- Item hanya bisa di-*equip*, tidak dikonsumsi
- Setiap hero hanya bisa membawa **maksimal 5 item**
- Item bisa dijual ke shop (50% dari harga beli)
- Boss memiliki AI untuk memilih aksi: 30% attack, 50% skill, 20% special (restore jika MP tidak cukup)
- Retreat dihitung seperti hero mati
- Gold per hero bersifat individual

---

## 🧱 Struktur OOP

### 🧍‍♂️ Character System
- `Character` (base class)
- `Player` (hero)
- `Enemy` (boss)

### 🛠️ Skill System
- `Skill` (skill biasa)
- `SpecialSkill` (skill khusus, hanya 1)

### 🎒 Item System
- `Item`: memodifikasi stat saat equip

### 🏪 Shop System
- `Shop`: stock item, sistem beli/jual

### 🎮 Game Manager
- `GameManager`: mengelola alur game per turn, loop, pengecekan game over

---

## 👥 Anggota Tim & Tugas

| Nama    | Tugas                                                                 |
|---------|-----------------------------------------------------------------------|
| **Rafa**    | `Character`, `Player`, `Enemy` (HP/MP, attack, skill use, logic dasar) |
| **Juan**    | `Skill`, `SpecialSkill` (penggunaan skill, efek, target area)         |
| **Ariq**    | `Item`, `equip_item`, `sell_item` (sistem equip item dan stat)        |
| **Jaydan**  | `Shop`, `refresh_stock`, `buy` (toko dan sistem transaksi)            |
| **Ramdan**  | `GameManager` (`run_battle_turn`, `give_income`, `check_game_over`, `display_team_status`)  |
| **Gilang**  | Setup awal: `init_skills_and_items`, `create_heroes_and_bosses`, `choose_heroes`, `distribute_starting_items` |

---

## ▶️ Cara Menjalankan

1. Pastikan Python 3.8+ sudah terpasang
2. install kivy dan kivymd:
   ```bash
   pip install kivy[base] kivymd
2. Clone repository ini:
   ```bash
   git clone https://github.com/USERNAME/turn_based_oop.git
   cd turn_based_oop
   cd game_turn_based
3. Jalankan game:
   ```bash
   python main.py
