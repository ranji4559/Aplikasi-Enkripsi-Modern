import streamlit as st
import crypto_engine

# Konfigurasi Halaman
st.set_page_config(page_title="Brankas Kriptografi", page_icon="🔒", layout="centered")

st.title("🔒 Brankas Enkripsi AES-256-GCM")
st.markdown("Tugas Proyek Keamanan Informasi. Aplikasi ini menggunakan **AES-256-GCM** dengan *Key Derivation* **PBKDF2**.")

# Membuat Tab Navigasi
tab1, tab2 = st.tabs(["Enkripsi Teks", "Dekripsi Teks"])

# --- BAGIAN ENKRIPSI ---
with tab1:
    st.subheader("Enkripsi Pesan Rahasia")
    pesan = st.text_area("Masukkan teks asli (Plaintext):")
    password_enc = st.text_input("Masukkan kata sandi pengaman:", type="password", key="pass_enc")
    
    if st.button("Enkripsi Teks"):
        if pesan and password_enc:
            hasil_enkripsi = crypto_engine.encrypt_text(password_enc, pesan)
            st.success("Teks berhasil dienkripsi!")
            st.markdown("**Cipherteks (Base64):**")
            # st.code otomatis menyediakan tombol copy di pojok kanan atas
            st.code(hasil_enkripsi, language="text") 
            st.info("💡 Cipherteks di atas sudah menggabungkan Salt (16 byte), Nonce (12 byte), dan data terenkripsi.")
        else:
            st.warning("Harap isi teks dan kata sandi terlebih dahulu!")

# --- BAGIAN DEKRIPSI ---
with tab2:
    st.subheader("Dekripsi Pesan Rahasia")
    cipherteks = st.text_area("Masukkan cipherteks (format Base64):")
    password_dec = st.text_input("Masukkan kata sandi pengaman:", type="password", key="pass_dec")
    
    if st.button("Dekripsi Teks"):
        if cipherteks and password_dec:
            hasil_dekripsi = crypto_engine.decrypt_text(password_dec, cipherteks)
            
            # Pengecekan jika gagal dekripsi (sesuai syarat wajib UTS menolak tag salah)
            if "ERROR" in hasil_dekripsi:
                st.error(hasil_dekripsi)
            else:
                st.success("Teks berhasil didekripsi!")
                st.markdown("**Teks Asli (Plaintext):**")
                st.code(hasil_dekripsi, language="text")
        else:
            st.warning("Harap isi cipherteks dan kata sandi terlebih dahulu!")