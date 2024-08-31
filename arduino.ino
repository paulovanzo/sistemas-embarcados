#include <Ethernet.h>
#include <PubSubClient.h>
#include <SPI.h>

// Configuração do servidor MQTT
const char* mqtt_server = "104.154.253.95";
const int mqtt_port = 80; // Porta padrão para MQTT
const char* mqtt_user = "embarcados"; // Adicione seu usuário MQTT
const char* mqtt_password = "embeddedSystems@2024"; // Adicione sua senha MQTT

// Configuração do módulo Ethernet W5100
byte mac[] = { 0xD2, 0x8A, 0xBE, 0xEF, 0xAE, 0xED };  // Endereço MAC do módulo Ethernet
IPAddress ip(10, 9, 99, 90);  // Endereço IP estático para o módulo Ethernet
IPAddress gateway(10, 9, 99, 1); // Gateway
IPAddress subnet(10, 9, 99, 91); // Máscara de sub-rede

EthernetClient ethClient;
PubSubClient client(ethClient);

// Define o pino de Leitura do Sensor
int SensorTurbidez = A1;

// Inicia as variáveis
int i;
float voltagem;
float NTU;

void setup() {
    Serial.begin(115200);
    int teste = Ethernet.begin(mac);
    // Inicia o módulo Ethernet
    if (teste == 0) {
        Serial.println("Falha ao configurar Ethernet com DHCP");
        Ethernet.begin(mac, ip, gateway, subnet);
    } else {
        Serial.println("Conexão Ethernet estabelecida com DHCP");
    }
    delay(1000); // Aguarde um pouco para a conexão estabilizar

    // Configure o servidor MQTT
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);

    // Conecte-se ao MQTT
    reconnect();
}

void reconnect() {
    // Loop até conseguir conectar ao MQTT
    delay(2000);
    while (!client.connected()) {
        Serial.print("Tentando conexão MQTT...");
        
        // Tente conectar ao MQTT com credenciais
        if (client.connect("ArduinoClient", mqtt_user, mqtt_password)) {
            Serial.println("Conectado ao MQTT");
            // Inscrever-se em qualquer tópico necessário após conectar
            client.subscribe("some/topic");
        } else {
            Serial.print("Falhou, rc=");
            Serial.print(client.state());
            Serial.println(" tentando novamente em 5 segundos");
            delay(5000);
        }
    }
}

void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Mensagem recebida em [");
    Serial.print(topic);
    Serial.print("]: ");
    
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    
    // Publicar uma mensagem no tópico metrics.turbidity
    publishTurbidity();

    delay(5000);  // Aguarde 15 segundos antes de enviar novamente
}

void publishTurbidity() {
    // Obtém a turbidez como float
    float turbidity = get_turbidity();
    
    // Cria um buffer para a mensagem em bytes (4 bytes para um float)
    byte buffer[4];
    
    // Copia os 4 bytes do float para o buffer
    memcpy(buffer, &turbidity, sizeof(turbidity));
    
    // Se necessário, converte para big-endian
    // O Arduino normalmente usa little-endian, então precisamos reverter a ordem dos bytes
    byte temp;
    temp = buffer[0];
    buffer[0] = buffer[3];
    buffer[3] = temp;
    temp = buffer[1];
    buffer[1] = buffer[2];
    buffer[2] = temp;
    
    // Publica a mensagem no tópico metrics.turbidity
    if (client.publish("metrics.turbidity", buffer, sizeof(buffer))) {
        Serial.println("Mensagem publicada com sucesso");
    } else {
        Serial.println("Falha ao publicar a mensagem");
    }
}

float get_turbidity() {
    // Inicia a leitura da voltagem em 0
    voltagem = 0;

    // Realiza a soma dos "i" valores de voltagem
    for (i = 0; i < 800; i++) {
        voltagem += ((float)analogRead(SensorTurbidez) / 1023) * 5;
    }

    // Realiza a média entre os valores lidos na função for acima
    voltagem = voltagem / 800;
    voltagem = ArredondarPara(voltagem, 1);


    // Se Voltagem menor que 2.5 fixa o valor de NTU
    if (voltagem < 2.5) {
        NTU = 3000;
    } else if (voltagem > 4.2) {
        NTU = 0;
        voltagem = 4.2;
    } else {
        // Senão calcula o valor de NTU através da fórmula
        NTU = -1120.4 * square(voltagem) + 5742.3 * voltagem - 4353.8;
    }
    return NTU;
}

// Sistema de arredondamento para Leitura
float ArredondarPara(float ValorEntrada, int CasaDecimal) {
    float multiplicador = powf(10.0f, CasaDecimal);
    ValorEntrada = roundf(ValorEntrada * multiplicador) / multiplicador;
    return ValorEntrada;
}
