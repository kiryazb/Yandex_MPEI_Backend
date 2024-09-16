# Добавьте новые условия в elif и else
for messages_count in range(0, 21):
    if messages_count == 0:
        print('У вас нет новых сообщений')
    elif messages_count == 1:
        print('У вас 1 новое сообщение')
    elif messages_count == 2 or messages_count == 3 or messages_count == 4:
        print(f'У вас {messages_count} новых сообщения')
    else:
        print(f'У вас {messages_count} новых сообщений')