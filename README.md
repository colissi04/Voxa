# Voxa - Transcrição e Tradução em Tempo Real

Voxa é uma aplicação desktop desenvolvida em Python que permite capturar áudio em tempo real, transcrever o conteúdo e opcionalmente traduzir para outro idioma.

## Funcionalidades

### Captura de Áudio
- Captura de áudio em tempo real através do VB-Cable
- Interface intuitiva com botão para iniciar/parar a gravação
- Indicador de status da conexão com o dispositivo de áudio

### Transcrição
- Transcrição em tempo real do áudio capturado
- Suporte para múltiplos idiomas:
  - Português
  - English (Inglês)
  - Español (Espanhol)
- Visualização instantânea do texto transcrito
- Opção para limpar o texto transcrito

### Tradução
- Tradução em tempo real do texto transcrito
- Seleção flexível de idiomas de origem e destino
- Ativação/desativação da tradução através de checkbox
- Visualização lado a lado da transcrição e tradução
- Interface adaptativa que maximiza a área de transcrição quando a tradução está desativada

### Gerenciamento de Texto
- Botão para limpar todo o conteúdo transcrito/traduzido
- Funcionalidade de salvamento com opções personalizáveis:
  - Seleção do que salvar (transcrição e/ou tradução)
  - Escolha do diretório de destino
  - Arquivos salvos com timestamp para fácil organização
  - Suporte a caracteres especiais (UTF-8)

## Requisitos

### Software
- Python 3.11
- VB-Cable (necessário para captura de áudio)

### Bibliotecas Python
- customtkinter
- sounddevice
- numpy
- torch
- torchaudio
- faster-whisper
- deep-translator
- python-dotenv

## Configuração do VB-Cable

1. Faça o download e instale o VB-Cable em seu sistema
2. Configure a saída de áudio do aplicativo que deseja capturar para "CABLE Input"
3. O Voxa automaticamente detectará e utilizará o VB-Cable como fonte de entrada

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
```
3. Ative o ambiente virtual:
```bash
# Windows
.\venv\Scripts\activate
```
4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Ative o ambiente virtual (se ainda não estiver ativo)
2. Execute o aplicativo:
```bash
python main.py
```
3. Selecione o idioma de origem da transcrição
4. Se desejar tradução, marque a opção "Traduzir" e selecione o idioma de destino
5. Clique em "Start Recording" para iniciar a captura
6. Use os botões "Limpar" e "Salvar" para gerenciar o texto conforme necessário

## Salvando o Conteúdo

Para salvar o conteúdo transcrito/traduzido:

1. Clique no botão "Salvar"
2. Selecione o que deseja salvar:
   - Transcrição
   - Tradução (se estiver ativa)
3. Escolha o diretório de destino
4. Os arquivos serão salvos com o formato:
   - `transcript_YYYYMMDD_HHMMSS.txt` para transcrição
   - `translation_YYYYMMDD_HHMMSS.txt` para tradução

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