#!/usr/bin/env python3
import tkinter 
import re
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import scrolledtext
import webvtt
  

  
# Criar uma função para abrir a caixa de diálogo
def tela_splitter(notebook):
    def gerar_splitter(textarea, result): 
        """
        Esta função pega o texto de um widget de texto tkinter chamado 'textarea', divide o texto em linhas e realiza as seguintes operações:

        1. Encontra todas as ocorrências de ". " e as substitui por ".\n", exceto nas linhas onde há apenas um ponto.
        2. Se o número de caracteres entre duas vírgulas exceder 40, quebra a linha na próxima vírgula.
        3. Remove todos os espaços em branco iniciais de cada linha.
        
        O texto resultante é então exibido em um widget de texto tkinter chamado 'result'.
        """
        

        texto = textarea.get("1.0", "end-1c")

        # Substitui todos os "? " por "?\n\n"
        texto = texto.replace("? ", "?\n\n")

        # Substitui todos os "! " por "!\n\n"
        texto = texto.replace("! ", "!\n\n")

        # Procurar todas as ocorrências de ". " e substituir por ".\n", exceto nas linhas em que só houver um ponto
        new_text = ""
        for line in texto.split("\n"):
            if line.count(".") > 1:
                new_text += line.replace(". ", ".\n\n") + "\n"
            else:
                new_text += line + "\n\n"
        texto = new_text.strip()


        # Se a quantidade de caracteres entre duas vírgulas passar de 40, quebrar a linha na próxima vírgula
        new_text = ""
        for line in texto.split("\n"):
            if len(line) > 40:
                new_line = ""
                words = line.split(",")
                for i in range(len(words)):
                    if i == 0:
                        new_line += words[i]
                    elif len(new_line.split(",")[-1]) + len(words[i]) + 1 > 40:
                        new_line += ",\n\n\n" + words[i]
                    else:
                        new_line += "," + words[i]
                new_text += new_line + "\n"
            else:
                new_text += line + "\n"
        texto = new_text.strip()

        # Remove todos os espaços em branco no início das linhas
        new_text = ""
        for line in texto.split("\n"):
            new_text += line.strip() + "\n"
        texto = new_text.strip()

        print(texto)

        # Define o valor da textarea result com o da variável texto
        result.delete("1.0", "end")
        result.insert("1.0", texto)
    
    # Criar um frame para conter os widgets
    frame = tkinter.Frame(notebook)
    notebook.add(frame, text="Splitter")

    # Criar um label para mostrar o título da caixa de diálogo
    label = tkinter.Label(frame, text="Coloque o texto abaixo")

    # Criar um textarea para digitar o texto
    textarea = tkinter.Text(frame)

    # Criar um outro textarea para mostrar o resultado
    result = tkinter.Text(frame)

    # Criar um botão para fechar a caixa de diálogo
    button = tkinter.Button(frame, text="Gerar", command= lambda: gerar_splitter(textarea, result))

    # Empacotar os widgets no frame
    label.pack()
    textarea.pack()
    button.pack()
    result.pack()

def tela_sbv(notebook):
    # Função para abrir o arquivo
    def abrir_sbv(result):
        # Abrir a caixa de diálogo para selecionar o arquivo
        filename = filedialog.askopenfilename(initialdir = "/",title = "Selecione o arquivo",filetypes = (("arquivos de legendas sbv","*.sbv"),("todos os arquivos","*.*")))

        captions = webvtt.from_sbv(filename)

        indice = "Índice\n0:00 Introdução"

        for caption in captions:
            if re.match('^\d+\.', caption.text):
                # Obtém os minutos e segundos do início do caption no formato (mm:ss)
                parts = caption.start.split(":")

                # Pegue a segunda e terceira partes e faça o padding de zeros à esquerda
                minute = parts[1].lstrip('0')
                second = parts[2].split(".")[0].zfill(2)

                minute_second = f"{minute}:{second}"

                # Remove os números do inicio da caption
                caption.text = re.sub('^\d+\.', '', caption.text)

                # Mantenha somente a primeira linha na caption
                caption.text = caption.text.split("\n")[0]

                indice += f"\n{minute_second}{caption.text}"
        
        print(indice)

        result.delete("1.0", "end")
        result.insert("1.0", indice)
        
    # Criar um frame para conter os widgets
    frame2 = tkinter.Frame(notebook)
    notebook.add(frame2, text="Leitor SBV para Índice YouTube")

    # Criar um label para mostrar o título da caixa de diálogo
    label2 = tkinter.Label(frame2, text="Escolha o arquivo SBV")

    # Botão para abrir um arquivo de extensão sbv
    button2 = tkinter.Button(frame2, text="Abrir", command= lambda: abrir_sbv(result))

    # Criar um outro textarea para mostrar o resultado
    result = tkinter.Text(frame2)


    label2.pack()
    button2.pack()
    result.pack()


# Criar uma janela principal
root = tkinter.Tk()

notebook = ttk.Notebook(root)

tela_splitter(notebook)
tela_sbv(notebook)

# Empcotar o notebook
notebook.pack(expand=True, fill='both')

# Iniciar o loop principal da janela
root.mainloop()