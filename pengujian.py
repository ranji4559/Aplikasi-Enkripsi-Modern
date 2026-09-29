import os
import time
from crypto_engine import encrypt_file, decrypt_file

def uji_waktu_eksekusi():
    print("=== PENGUJIAN WAKTU ENKRIPSI & DEKRIPSI (AES-256-GCM) ===")
    ukuran_file = {
        "1 KB": 1024,
        "1 MB": 1024 * 1024,
        "10 MB": 10 * 1024 * 1024
    }
    password = "password_super_aman_123"
    
    for nama, ukuran in ukuran_file.items():
        data_dummy = os.urandom(ukuran)
        
        # Enkripsi
        start_enc = time.perf_counter()
        data_enc = encrypt_file(password, data_dummy)
        waktu_enc = time.perf_counter() - start_enc
        
        # Dekripsi
        start_dec = time.perf_counter()
        data_dec = decrypt_file(password, data_enc)
        waktu_dec = time.perf_counter() - start_dec
        
        print(f"Ukuran {nama}:")
        print(f" - Waktu Enkripsi: {waktu_enc:.5f} detik")
        print(f" - Waktu Dekripsi: {waktu_dec:.5f} detik")
    print("=" * 55 + "\n")

def uji_avalanche_effect():
    print("=== PENGUJIAN AVALANCHE EFFECT ===")
    # Teks asli dan teks yang diubah hanya 1 byte/karakter
    teks_asli = b"SistemKeamananInformasi"
    teks_ubah = b"TistemKeamananInformasi" # Huruf 'S' diubah ke 'T'
    password = "password_uji_123"
    
    cipher1 = encrypt_file(password, teks_asli)
    cipher2 = encrypt_file(password, teks_ubah)
    
    min_len = min(len(cipher1), len(cipher2))
    perbedaan_bit = 0
    
    for i in range(min_len):
        xor_result = cipher1[i] ^ cipher2[i]
        perbedaan_bit += bin(xor_result).count('1')
        
    total_bit = min_len * 8
    persentase = (perbedaan_bit / total_bit) * 100
    print(f"Total Bit Diuji    : {total_bit} bit")
    print(f"Jumlah Bit Berubah : {perbedaan_bit} bit")
    print(f"Avalanche Effect   : {persentase:.2f} % (Standar baik di atas 45-50%)")
    print("=" * 55)

if __name__ == "__main__":
    uji_waktu_eksekusi()
    uji_avalanche_effect()