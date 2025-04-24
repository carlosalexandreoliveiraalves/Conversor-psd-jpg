import os
from tkinter import Tk, Label, Entry, Button, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from psd_tools import PSDImage
from PIL import Image
import re

def converter_psd_para_jpg(caminho_psd, caminho_saida_jpg):
    try:
        psd = PSDImage.open(caminho_psd)
        imagem = psd.composite()
        imagem_rgb = imagem.convert("RGB")
        imagem_rgb.save(caminho_saida_jpg, "JPEG")
        print(f"Imagem convertida e salva em: {caminho_saida_jpg}")
    except Exception as e:
        print(f"Erro ao converter {caminho_psd}: {e}")

def on_drop(event):
    # Remove as chaves { e } e divide com base no padrão de caminhos
    data = event.data.strip()
    
    # Se tiver apenas uma chave de abertura e fechamento, limpa e trata como um só
    if data.startswith("{") and data.endswith("}"):
        data = data[1:-1]  # remove as chaves

    # Se vários arquivos forem arrastados, eles ainda podem estar entre chaves, separados por } {
    arquivos = re.findall(r'[^{}]+', data)

    for caminho_completo in arquivos:
        caminho_completo = caminho_completo.strip()

        if not caminho_completo:  # ← ignora strings vazias
            continue


        if caminho_completo.lower().endswith('.psd'):
            nome_base = os.path.splitext(os.path.basename(caminho_completo))[0]
            destino = os.path.join(pasta_saida.get(), f"{nome_base} - {ator.get()}.jpg")
            converter_psd_para_jpg(caminho_completo, destino)
        else:
            print(f"Arquivo ignorado (não é PSD): {caminho_completo}")

# GUI
root = TkinterDnD.Tk()
root.title("Conversor PSD para JPG")
root.geometry("500x250")

Label(root, text="Nome do ator:").pack()
ator = Entry(root, width=50)
ator.pack()

Label(root, text="Pasta de saída:").pack()
pasta_saida = Entry(root, width=50)
pasta_saida.pack()

def selecionar_pasta():
    caminho = filedialog.askdirectory()
    if caminho:
        pasta_saida.delete(0, "end")
        pasta_saida.insert(0, caminho)

Button(root, text="Selecionar pasta de saída", command=selecionar_pasta).pack(pady=5)

drop_area = Label(root, text="Arraste arquivos .PSD aqui", relief="ridge", borderwidth=2, width=60, height=5)
drop_area.pack(pady=20)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
