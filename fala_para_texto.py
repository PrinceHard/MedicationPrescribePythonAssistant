from email.mime import audio
import speech_recognition as sr

def texto_falado():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Escutando...")
        audio = r.listen(source)
    
    try:
        texto = r.recognize_google(audio)
        print(texto)
    except Exception as e:
        print(e)
        texto = "Ocorreu um erro durante o PLN do audio"
    return texto

texto_falado()
