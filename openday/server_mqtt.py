import paho.mqtt.client as mqtt
import json
import os

BROKER = "mqtt.ssh.edu.it" 
PORT = 1883
TOPICS = [("Atrio/T", 0), ("Atrio/H", 0), ("Atrio/P", 0), ("Lab/T", 0), ("Lab/H", 0), ("Lab/P", 0)] 

# Salva il file JSON nella stessa cartella dello script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_JSON = os.path.join(BASE_DIR, "dati.json")

DATI = {}

# Carica eventuali dati precedenti all'avvio per non perderli al riavvio
if os.path.exists(FILE_JSON):
    try:
        with open(FILE_JSON, "r", encoding="utf-8") as f:
            DATI = json.load(f)
    except Exception as e:
        print(f"Avviso: impossibile leggere i dati precedenti ({e})")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connesso con successo al broker!")
        client.subscribe(TOPICS)
        print(f"Iscritto ai topic: {[t[0] for t in TOPICS]}")
    else:
        print(f"Errore di connessione, codice: {rc}")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        
        # Prova a convertire il dato in numero (float) se possibile, altrimenti lo lascia come testo
        try:
            valore = float(payload)
        except ValueError:
            valore = payload

        DATI[topic] = valore
        print(f"Ricevuto -> {topic}: {valore}")

        with open(FILE_JSON, "w", encoding="utf-8") as f:
            json.dump(DATI, f, indent=4)
            
    except Exception as e:
        print(f"Errore durante l'elaborazione del messaggio: {e}")

# Compatibilità per le versioni recenti di paho-mqtt (v2.0+)
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
