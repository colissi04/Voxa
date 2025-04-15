# Voxa - Transcrição e Tradução em Tempo Real

O Voxa é uma aplicação desktop desenvolvida em Python que permite capturar, transcrever e traduzir áudio em tempo real de qualquer aplicação no seu computador.

## Funcionalidades

- 🎤 Captura de áudio de qualquer aplicação Windows
- 📝 Transcrição em tempo real usando o modelo Whisper
- 🌐 Tradução automática do inglês para português
- 🎯 Interface gráfica moderna e intuitiva
- 💾 Histórico de conversas

## Pré-requisitos

- Python 3.11 ou superior
- Windows 10/11
- [VB-Cable Virtual Audio Device](https://vb-audio.com/Cable/)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/voxa.git
cd voxa
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale o VB-Cable:
   - Baixe o VB-Cable em [https://vb-audio.com/Cable/](https://vb-audio.com/Cable/)
   - Execute o instalador
   - Reinicie o computador

## Configuração do VB-Cable

1. Configure o VB-Cable para reproduzir o áudio:
   - Abra as configurações de som do Windows
   - Vá para a aba "Gravação"
   - Encontre "CABLE Output"
   - Clique com o botão direito e selecione "Propriedades"
   - Na aba "Ouvir", marque "Ouvir este dispositivo"
   - Selecione seu dispositivo de saída padrão
   - Clique em "Aplicar" e "OK"

2. Configure a aplicação que deseja transcrever:
   - Abra as configurações de som do Windows
   - Em "Configurações de som avançadas"
   - Encontre a aplicação desejada (ex: Chrome, Discord)
   - Mude a saída para "CABLE Input"

## Uso

1. Execute a aplicação:
```bash
python main.py
```

2. Na interface do Voxa:
   - Verifique se o VB-Cable foi detectado
   - Clique em "Start Recording" para iniciar a captura
   - O áudio será transcrito em inglês e traduzido para português em tempo real
   - Clique em "Stop Recording" para parar

## Estrutura do Projeto

```
voxa/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── src/
│   ├── core/              # Componentes principais
│   ├── services/          # Serviços (áudio, transcrição, tradução)
│   └── ui/                # Interface gráfica
└── README.md              # Este arquivo
```

## Serviços Utilizados

- **Whisper**: Modelo de reconhecimento de fala da OpenAI
- **Google Translate**: Serviço de tradução
- **VB-Cable**: Driver de áudio virtual
- **CustomTkinter**: Framework para interface gráfica moderna

## Solução de Problemas

1. **Não encontro o VB-Cable nas configurações de som**
   - Reinstale o VB-Cable e reinicie o computador
   - Verifique se não está sendo bloqueado pelo antivírus

2. **A aplicação não detecta o VB-Cable**
   - Verifique se o VB-Cable está instalado corretamente
   - Reinicie a aplicação Voxa

3. **Não ouço o áudio ao usar o VB-Cable**
   - Verifique se "Ouvir este dispositivo" está ativado
   - Confirme se o dispositivo de saída está correto

4. **Erros de transcrição**
   - Verifique se o áudio está sendo capturado corretamente
   - Ajuste o volume da aplicação fonte

## Contribuindo

Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## Licença

Este projeto está licenciado sob a MIT License. 