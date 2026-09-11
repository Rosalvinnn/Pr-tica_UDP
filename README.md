# Chat via UDP

Projeto desenvolvido para a disciplina de Redes de Computadores.

## Descrição

Este projeto consiste em um sistema simples de chat utilizando o protocolo UDP.

Como o UDP não garante a entrega dos pacotes, foi implementado um sistema de confirmação na camada de aplicação. Cada mensagem enviada possui um ID e permanece pendente até receber uma confirmação do servidor.

O servidor também simula uma perda de 40% dos pacotes para demonstrar o funcionamento do sistema de reenvio.

## Arquivos

* `chat_sender.py` - Cliente responsável por enviar mensagens.
* `chat_receiver.py` - Servidor responsável por receber mensagens e enviar confirmações.

## Funcionamento

As mensagens são enviadas no formato:

```text
MSG|ID|CONTEUDO
```

Exemplo:

```text
MSG|1|Olá
```

Quando a mensagem é recebida corretamente, o servidor responde:

```text
DELIVERED|ID
```

Exemplo:

```text
DELIVERED|1
```

## Comandos

### `/status`

Mostra as mensagens que ainda estão pendentes de confirmação.

### `/reenviar`

Reenvia todas as mensagens que continuam pendentes.

## Como executar

Primeiro, execute o servidor:

```bash
python chat_receiver.py
```

Em outro terminal, execute o cliente:

```bash
python chat_sender.py
```

Depois disso, basta digitar as mensagens no terminal do cliente.

## Tecnologias utilizadas

* Python
* Socket UDP
* Threading
