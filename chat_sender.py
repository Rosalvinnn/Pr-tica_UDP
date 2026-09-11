import socket
import threading

TARGET_IP = "127.0.0.1"
PORT = 5001

pending_messages = {}
msg_counter = 1
lock = threading.Lock()


def listen_receipts(sock):
  """Thread em background para receber recibos sem bloquear o terminal."""

  while True:
    try:
      data, _ = sock.recvfrom(1024)

      raw = data.decode("utf-8")

      # TODO 1: Fazer o parsing do recibo recebido
      parts = raw.split("|")

      # TODO 2: Verificar se o tipo é "DELIVERED"
      if parts[0] == "DELIVERED":

        # TODO 3: Extrair o ID confirmado
        message_id = int(parts[1])

        # TODO 4: Com o lock adquirido, remover a mensagem
        with lock:

          if message_id in pending_messages:

            text = pending_messages.pop(message_id)

            print(f"\n[✓✓ Entregue] ID {message_id}: {text}")

    except Exception:
      break


def run_chat_sender():
  global msg_counter

  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    # Inicia a thread que processa os ACKs recebidos em segundo plano
    listener = threading.Thread(
      target=listen_receipts,
      args=(s,),
      daemon=True
    )

    listener.start()

    print("=== Mini-Chat UDP ===")
    print("Comandos especiais:")
    print("  /status   -> Mostra mensagens ainda pendentes")
    print("  /reenviar -> Reenvia todas as mensagens pendentes\n")

    while True:
      try:
        user_input = input("Digite uma mensagem: ").strip()

        if not user_input:
          continue

        # TODO 5: STATUS
        if user_input == "/status":

          with lock:

            print("\n=== MENSAGENS PENDENTES ===")

            if len(pending_messages) == 0:
              print("Nenhuma mensagem pendente.")

            else:
              for message_id, text in pending_messages.items():
                print(f"[PENDENTE] ID {message_id}: {text}")

            print()

          continue


        # TODO 6: REENVIAR
        if user_input == "/reenviar":

          with lock:

            print("\n=== REENVIANDO MENSAGENS ===")

            if len(pending_messages) == 0:
              print("Nenhuma mensagem pendente.")

            else:

              for message_id, text in pending_messages.items():

                message = f"MSG|{message_id}|{text}"

                s.sendto(
                  message.encode("utf-8"),
                  (TARGET_IP, PORT)
                )

                print(f"[REENVIADA] ID {message_id}: {text}")

            print()

          continue


        # TODO 7: Associar mensagem ao ID e salvar como pendente
        message_id = msg_counter

        with lock:
          pending_messages[message_id] = user_input


        # TODO 8: Montar pacote
        message = f"MSG|{message_id}|{user_input}"


        # TODO 9: Enviar pacote UDP
        s.sendto(
          message.encode("utf-8"),
          (TARGET_IP, PORT)
        )


        # TODO 10: Incrementar contador e avisar que está pendente
        print(f"[PENDENTE] ID {message_id}: {user_input}")

        msg_counter += 1


      except KeyboardInterrupt:
        print("\nEncerrando cliente...")
        break


if __name__ == "__main__":
  run_chat_sender()