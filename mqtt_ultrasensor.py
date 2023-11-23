from machine import Pin
import utime
from umqtt.simple import MQTTClient
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SHARE-RESIDENTE", "Share@residente23")

print("Conectando à rede", end="")

# Loop até que a conexão seja estabelecida
while not wlan.isconnected():
    utime.sleep(2)  # Espera 1 segundo antes de tentar novamente
    print(".", end="")

print("\nConectado!")

utime.sleep_us(5)

mqtt_server = 'broker.hivemq.com'
client_id = 'cerjon'
client = MQTTClient(client_id, mqtt_server, keepalive=3600)

Trig = Pin(2, Pin.OUT) # Pino de Saida, Escrita
Echo = Pin(3, Pin.IN) # Pino de Entrada, Leitura

def ultrassonicRead():
    total_distance = 0 # Distância total
    
    iterations = 5 # Iterações para obter média
    
    while iterations > 0: # Loop de medição de distâncias
        
        # Impulsos para o sensor
        Trig.high()
        utime.sleep_us(5)
        Trig.low()

        # Aguardando sinal de eco
        while Echo.value() == 0:
            off = utime.ticks_us()
        while Echo.value() == 1:
            on = utime.ticks_us()
        
        # Medição de distância
        time = on - off
        distance = (time * 0.0343) / 2
        total_distance += distance
        iterations -= 1
        
    average_distance = total_distance / 5
    message = f"A distancia média do objeto mais próximo é de {average_distance} cm"
    return message

while True:
    
    try:
        client.connect()
        print(f"Conexão com broker {mqtt_server} estabelecida.")
        utime.sleep_us(2000)
        message = ultrassonicRead()
        print(message)
        client.publish("CerjaoMQTT", message)
        utime.sleep(2)
    except OSError as e:
        print('Falha ao conectar ao broker MQTT. Tentando novamente...')
        client.disconnect()
        utime.sleep(5)
    
