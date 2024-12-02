for messages_count in range(6):
    if messages_count > 0:
        print('Новых сообщений: ' + str(messages_count))
    elif messages_count == 0:
        print('У вас нет сообщений')