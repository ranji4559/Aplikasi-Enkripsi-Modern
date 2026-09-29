import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

def derive_key(password: str, salt: bytes) -> bytes:
    """Menurunkan kunci 256-bit (32 byte) dari kata sandi memakai PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return kdf.derive(password.encode())

def encrypt_text(password: str, plaintext: str) -> str:
    """Mengenkripsi teks dengan AES-256-GCM dan mengembalikan string Base64."""
    # 1. Bangkitkan salt (16 byte) dan nonce (12 byte) secara acak
    salt = os.urandom(16)
    nonce = os.urandom(12)
    
    # 2. Buat kunci dari kata sandi dan salt
    key = derive_key(password, salt)
    
    # 3. Proses Enkripsi
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    
    # 4. Gabungkan salt + nonce + ciphertext, lalu ubah ke Base64
    encrypted_data = salt + nonce + ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_text(password: str, b64_token: str) -> str:
    """Mendekripsi string Base64 kembali ke teks asli."""
    try:
        # 1. Decode dari Base64
        encrypted_data = base64.b64decode(b64_token)
        
        # 2. Ekstrak salt (16 byte awal), nonce (12 byte berikutnya), dan ciphertext (sisanya)
        salt = encrypted_data[:16]
        nonce = encrypted_data[16:28]
        ciphertext = encrypted_data[28:]
        
        # 3. Buat ulang kunci dari kata sandi dan salt yang diekstrak
        key = derive_key(password, salt)
        
        # 4. Proses Dekripsi
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
        
    except InvalidTag:
        return "ERROR: Kata sandi salah atau data telah dimanipulasi (Gagal verifikasi tag)!"
    except Exception as e:
        return f"ERROR: Format tidak valid atau rusak. Detail: {str(e)}"
def encrypt_file(password: str, file_data: bytes) -> bytes:
    """Mengenkripsi byte berkas dengan AES-256-GCM."""
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, file_data, None)
    
    return salt + nonce + ciphertext

def decrypt_file(password: str, encrypted_data: bytes) -> bytes:
    """Mendekripsi byte berkas kembali ke aslinya."""
    try:
        salt = encrypted_data[:16]
        nonce = encrypted_data[16:28]
        ciphertext = encrypted_data[28:]
        
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        
        return aesgcm.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        return b"ERROR_TAG"
    except Exception:
        return b"ERROR_FORMAT"