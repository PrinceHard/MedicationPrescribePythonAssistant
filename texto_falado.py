import pyttsx3
import lista_conversacao

def texto_falado(linha_texto):
    engine = pyttsx3.init()
    engine.say(linha_texto)
    engine.runAndWait()

texto_falado(lista_conversacao.conversation_list[0])