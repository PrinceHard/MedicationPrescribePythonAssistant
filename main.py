import speech_recognition as sr
from nltk import word_tokenize, corpus
import json

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "config.json"


def iniciar():
    global reconhecedor
    global palavras_de_parada
    global nome_assistente
    global acoes
    global lista_prescricoes
    global dosagem
    global tempo
    global dose
    global quantidade

    lista_prescricoes = []
    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))

    with open(CAMINHO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)

        nome_assistente = configuracao["nome"]
        acoes = configuracao["acoes"]

        arquivo_configuracao.close()


def escutar_comando(texto):
    global reconhecedor

    comando = None

    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)

        print(texto)
        fala = reconhecedor.listen(fonte_audio, timeout=5, phrase_time_limit=5)
        try:
            comando = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        except sr.UnknownValueError:
            pass

    return comando


def eliminar_palavras_de_parada(tokens):
    global palavras_de_parada

    tokens_filtrados = []
    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)

    return tokens_filtrados


def tokenizar_comando(comando):
    global nome_assistente

    acao = None
    item = None

    tokens = word_tokenize(comando, IDIOMA_CORPUS)
    if tokens:
        tokens = eliminar_palavras_de_parada(tokens)

        if len(tokens) >= 3:
            if nome_assistente == tokens[0].lower():
                acao = tokens[1].lower()
                item = tokens[2].lower()

    return acao, item


def validar_comando(acao, item):
    global acoes

    valido = False

    if acao and item:
        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                if item in acaoCadastrada["itens"]:
                    valido = True

                break

    return valido

def confirmar_prescricao(prescricao):
    global lista_prescricoes
    continuar = True
    while continuar:
        try:
            comando = escutar_comando("Você confirma essa prescrição?")
            print(f"processando o comando: {comando}")

            if comando == "sim":
                lista_prescricoes.append(prescricao)
                print(f"A prescrição {prescricao} foi adicionada na lista de prescrições")
                continuar = False
            if comando == "não":
                print("Sua prescricao não foi adicionada na listas de prescrições")
                continuar = False
        except KeyboardInterrupt:
            print("Saindo!")
            continuar = False

def executar_comando(acao, item):
    if(acao == "prescrever"):
        with open("dosagem_remedios.json", "r") as dosagem_remedios:
            configuracao = json.load(dosagem_remedios)
            for rem in configuracao:
                if rem["nome"].lower() == item:
                    dosagem = rem["dosagem"]
                    tempo = rem["tempo"]
                    break
        dosagem_remedios.close()
        with open("info_paciente.json", "r") as info_paciente:
            configuracao = json.load(info_paciente)
            peso = configuracao["peso"]
            dose = dosagem * peso
            quantidade = 24 / tempo
        info_paciente.close()
        print(f"A prescrição para {item} é de {dose}mg {quantidade} vezes ao dia")
        prescricao = {"nome": item, "dose": dose, "quantidade": quantidade}
        confirmar_prescricao(prescricao)

    if(acao == "listar"):
        if(item == "prescrições"):
            print(f"A lista de prescricoes é: {lista_prescricoes}")
        if(item == "remédios"):
            with open("dosagem_remedios.json", "r") as dosagem_remedios:
                configuracao = json.load(dosagem_remedios)
                print(f"A lista de remédios é:")
                for rem in configuracao:
                    remedio = rem["nome"]
                    print(remedio)
            dosagem_remedios.close()

if __name__ == '__main__':
    iniciar()

    continuar = True
    while continuar:
        try:
            comando = escutar_comando("Escutando...")
            print(f"processando o comando: {comando}")

            if comando:
                if comando == "sair":
                    continuar = False
                    break
                acao, item = tokenizar_comando(comando)
                valido = validar_comando(acao, item)
                if valido:
                    executar_comando(acao, item)
                else:
                    print("Não entendi o comando. Repita, por favor!")
        except KeyboardInterrupt:
            print("Saindo!")

            continuar = False
