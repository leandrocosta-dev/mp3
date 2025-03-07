import os
import streamlit as st
import yt_dlp
from pathlib import Path

def criar_pasta_mp3():
    # Verificar se a pasta MP3 existe, senão criar
    if not os.path.exists("MP3"):
        os.makedirs("MP3")
        return "Pasta MP3 criada com sucesso!"
    else:
        return "A pasta MP3 já existe."

def baixar_mp3(url):
    if not url:
        return "Por favor, insira uma URL válida do YouTube."
    
    # Configuração das opções de download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'MP3/%(title)s.%(ext)s',
        'restrictfilenames': True,  # Evita caracteres especiais nos nomes de arquivo
        'noplaylist': True,  # Não baixa playlists, apenas o vídeo
    }
    
    try:
        # Baixar o áudio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', None)
            
            # Gerar o caminho para o arquivo baixado
            filename = f"{title}.mp3"
            filepath = os.path.join("MP3", filename)
            
            # Verificar se o arquivo existe para download
            if os.path.exists(filepath):
                return {
                    "status": "success",
                    "message": f"Download concluído com sucesso! '{title}' foi salvo na pasta MP3",
                    "filepath": filepath,
                    "filename": filename
                }
            else:
                # Tentar encontrar o arquivo com nome limpo (devido ao restrictfilenames=True)
                mp3_dir = Path("MP3")
                possible_files = list(mp3_dir.glob("*.mp3"))
                # Ordenar por data de modificação para pegar o arquivo mais recente
                if possible_files:
                    newest_file = max(possible_files, key=lambda p: p.stat().st_mtime)
                    return {
                        "status": "success",
                        "message": f"Download concluído com sucesso! '{title}' foi salvo na pasta MP3",
                        "filepath": str(newest_file),
                        "filename": newest_file.name
                    }
                
                return {
                    "status": "warning",
                    "message": f"Download concluído, mas não foi possível localizar o arquivo para download."
                }
    except Exception as e:
        return {"status": "error", "message": f"Erro ao baixar o vídeo: {str(e)}"}

# Configuração da página Streamlit
st.set_page_config(
    page_title="YouTube para MP3 Downloader",
    page_icon="🎵",
    layout="centered"
)

# Título e descrição do aplicativo
st.title("YouTube para MP3 Downloader")
st.markdown("Baixe áudios de vídeos do YouTube em formato MP3 rapidamente.")

# Inicialização da pasta MP3
status_pasta = criar_pasta_mp3()
st.info(status_pasta)

# Campo para entrada da URL
url = st.text_input("Digite a URL do vídeo do YouTube:", placeholder="https://www.youtube.com/watch?v=...")

# Botão de download
if st.button("Baixar MP3"):
    if url:
        # Mostrar mensagem de progresso
        with st.spinner("Baixando o áudio... Por favor, aguarde."):
            resultado = baixar_mp3(url)
            
            if isinstance(resultado, dict):
                if resultado["status"] == "success":
                    st.success(resultado["message"])
                    
                    # Oferecer o arquivo para download no navegador
                    with open(resultado["filepath"], "rb") as file:
                        st.download_button(
                            label="Baixar o arquivo MP3",
                            data=file,
                            file_name=resultado["filename"],
                            mime="audio/mpeg"
                        )
                elif resultado["status"] == "warning":
                    st.warning(resultado["message"])
                else:
                    st.error(resultado["message"])
            else:
                st.warning(resultado)
    else:
        st.warning("Por favor, insira uma URL do YouTube válida.")

# Rodapé com informações adicionais
st.markdown("---")
st.caption("Este aplicativo usa yt-dlp para baixar áudios do YouTube. Utilize apenas para conteúdo livre de direitos autorais ou para uso pessoal conforme permitido pela lei.")
st.caption("Desenvolvido com Streamlit e Python")
