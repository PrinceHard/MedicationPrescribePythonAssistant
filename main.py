import speech_recognition as sr
import pyttsx3

conversation_list = [
    "Como posso te ajudar?...",
    "Você quer começar com {medication}. \
    A dose padrão é {dosing}mg {numb_day} vezes ao dia . Isso é o que você quer prescrever?",
    "Baseado em uma função renal de {GFR} e um peso de {weight} kg, \
    Eu calculei a dosagem necessária de {dosing}mg {numb_day} vezes ao dia. Isso é o que você quer prescrever?",
    "Você deseja mudar ou cancelar a dose prescrita ?",
    "Quantas miligramas você deseja prescrever?",
    "Quantas vezes ao dia você quer que o paciente tome isso?",
    "Ok, você deseja mudar a dosagem de {dosing}mg {numb_day} vezes ao dia?",
    "Ok, vamos começar novamente",
    "Ok, Eu vou prescrever {medication} em uma dosagem de {dosing}",
    "A lista de medicamentos do paciente consiste de {medication_list} e eu vou adicionar: {new_drug} \
    em uma dosagem de {dosing}mg {numb_day} vezes ao dia. Está correto?",
    "Eu não entendi você corretamente, ou o remédio não está no meu dicionário, por favor me diga novamente qual medicamento você quer \
    prescrever"]

def text_speech(text_line):
    engine = pyttsx3.init()  
    engine.say(text_line)  
    engine.runAndWait()  
    
text_speech(conversation_list[0])

def speech_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escutando...")
        audio = r.listen(source)
    try:
        string = r.recognize_google(audio)
        print(string)
    except Exception as e:
        print(e)
        string = "Erro gerado durante PLN do audio"
    return string

medication_dictionary = {
    "Diazepam": [6,5],
    "Dipirona":  [4,500],
    "Paracetamol": [4,500],
    "Midazolam": [2,2],
    "Clozapina": [3,100],
    "Ácido Acetilsalicílico": [3,500],
}