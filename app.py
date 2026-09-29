import streamlit as st
import crypto_engine

st.set_page_config(page_title="Brankas Kriptografi", page_icon="🔒", layout="centered")
st.title("🔒 Brankas Enkripsi AES-256-GCM")
st.markdown("Tugas Proyek Keamanan Informasi. Mendukung enkripsi teks dan berkas (PDF/Gambar).")

tab1, tab2, tab3, tab4 = st.tabs(["Enkripsi Teks", "Dekripsi Teks", "Enkripsi Berkas", "Dekripsi Berkas"])

# --- TAB 1 & 2: TEKS ---
with tab1:
    st.subheader("Enkripsi Pesan Rahasia")
    pesan = st.text_area("Masukkan teks asli:")
    pass_enc = st.text_input("Kata sandi:", type="password", key="p1")
    if st.button("Enkripsi Teks"):
        if pesan and pass_enc:
            st.success("Berhasil!")
            st.code(crypto_engine.encrypt_text(pass_enc, pesan), language="text")

with tab2:
    st.subheader("Dekripsi Pesan Rahasia")
    cipher = st.text_area("Masukkan cipherteks (Base64):")
    pass_dec = st.text_input("Kata sandi:", type="password", key="p2")
    if st.button("Dekripsi Teks"):
        if cipher and pass_dec:
            hasil = crypto_engine.decrypt_text(pass_dec, cipher)
            if "ERROR" in hasil:
                st.error(hasil)
            else:
                st.success("Berhasil!")
                st.code(hasil, language="text")

# --- TAB 3: ENKRIPSI BERKAS ---
with tab3:
    st.subheader("Enkripsi Berkas (PDF/Gambar)")
    file_upload = st.file_uploader("Pilih berkas asli", key="f1")
    pass_fenc = st.text_input("Kata sandi pengaman:", type="password", key="p3")
    
    if file_upload and pass_fenc:
        if st.button("Enkripsi Berkas"):
            file_bytes = file_upload.read()
            enc_bytes = crypto_engine.encrypt_file(pass_fenc, file_bytes)
            st.success("Berkas berhasil dienkripsi!")
            st.download_button(
                label="⬇️ Unduh Berkas Terenkripsi (.enc)",
                data=enc_bytes,
                file_name=file_upload.name + ".enc",
                mime="application/octet-stream"
            )

# --- TAB 4: DEKRIPSI BERKAS ---
with tab4:
    st.subheader("Dekripsi Berkas Terenkripsi")
    file_enc_upload = st.file_uploader("Pilih berkas terenkripsi (.enc)", key="f2")
    pass_fdec = st.text_input("Kata sandi pembuka:", type="password", key="p4")
    
    if file_enc_upload and pass_fdec:
        if st.button("Dekripsi Berkas"):
            enc_bytes = file_enc_upload.read()
            dec_bytes = crypto_engine.decrypt_file(pass_fdec, enc_bytes)
            
            if dec_bytes in [b"ERROR_TAG", b"ERROR_FORMAT"]:
                st.error("Gagal! Kata sandi salah atau berkas rusak.")
            else:
                st.success("Berkas berhasil didekripsi!")
                nama_asli = file_enc_upload.name.replace(".enc", "")
                st.download_button(
                    label=f"⬇️ Unduh Berkas Asli ({nama_asli})",
                    data=dec_bytes,
                    file_name=nama_asli,
                    mime="application/octet-stream"
                )