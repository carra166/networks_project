import socket
import threading

# Error Message List
error_messages = ['Subject Not Found',
                  'Subscription Failed - Subject Not Found',
                  'Invalid action',
                  'Already subscribed']

# Lists for checking validity
valid_subjects = ('WEATHER', 'NEWS')
weather_subscribers = []
weather_messages = []
news_subscribers = []
news_messages = []
associated_lists = {
    valid_subjects[0] : weather_subscribers,
    valid_subjects[1] : news_subscribers
}


# Checks client sent valid format + action
def is_valid_message(msg_items, num_items):
    content_type = 'Not Valid'
    action_valid = False
    if num_items == 1:      # Could be <DISC> or invalid
        if msg_items[0] == 'DISC':
            content_type = 'DISC'
            action_valid = True

    elif num_items == 2:    # Could be <CLIENT_NAME, CONN> or invalid
        if msg_items[1] == 'CONN':
            content_type = 'CONN'
            action_valid = True

    elif num_items == 3:    # Could be <CLIENT_NAME, SUB, SUBJECT> or invalid
        if msg_items[1] == 'SUB':
            content_type = 'SUB'
            action_valid = True

    elif num_items == 4:    # Could be <CLIENT_NAME, PUB, SUBJECT, MSG> or invalid
        if msg_items[1] == 'PUB':
            content_type = 'PUB'
            action_valid = True

    return content_type, action_valid


# Checks if a client is subscribed to a subject
def is_subscribed(subj, client):
    is_sub = False

    if ((subj == valid_subjects[0]) and (client in associated_lists.get(valid_subjects[0]))) or ((subj == valid_subjects[1]) and (client in associated_lists.get(valid_subjects[1]))):
        is_sub = True

    return is_sub


# Handles each client connection
def handle_client(client_socket, client_address):
    client_info = (client_socket, client_address)
    print(f"[INFO] Connected to {client_address}")
    try:
        while True:
            # Receive message
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break

            print(f"[MESSAGE from {client_address}]: {message}")

            # Check message for client type, validity
            message_content = [i.strip() for i in message.split(',')]
            message_item_count = len(message_content)
            msg_type, msg_valid = is_valid_message(message_content, message_item_count)

            if msg_valid:
                if msg_type == 'DISC':
                    client_socket.sendall("DISC_ACK".encode("utf-8"))
                    break

                elif msg_type == 'CONN':
                    client_socket.sendall("CONN_ACK".encode("utf-8"))
                    continue

                elif msg_type == 'SUB':
                    subject = message_content[2]

                    # Is client attempting to subscribe to non-existent subject?
                    if subject not in valid_subjects:
                        client_socket.sendall(f"ERROR: {error_messages[1]}".encode("utf-8"))
                        continue

                    # Is client already subscribed?
                    elif is_subscribed(subject, client_info):
                        client_socket.sendall(f"ERROR: {error_messages[3]}".encode("utf-8"))

                    else:
                        client_socket.sendall("SUB_ACK".encode("utf-8"))
                        # TODO: add to list
                        continue

                elif msg_type == 'PUB':
                    # TODO: See below for errors to check
                    # Is publisher subscribed to the subject they are publishing?
                    # Is publisher attempting to publish to a non-existent subject?
                    pass

            # This case covers clients that have been subscribed, but attempted an invalid action
            elif (client_info in weather_subscribers) or (client_info in news_subscribers):
                client_socket.sendall(f"ERROR: {error_messages[2]}".encode("utf-8"))
                continue

            # This case covers a client that is not listed at all, forces it to disconnect
            else:
                break

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        # Close connection
        client_socket.close()
        print(f"[INFO] Connection closed {client_address}")


# Start the server
def start_server():
    server_port = 12000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", server_port))
    server_socket.listen(5)
    print(f"[INFO] Server listening on port {server_port}")

    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()

        # Create threads
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"[INFO] Started thread for {client_address}")


if __name__ == "__main__":
    start_server()