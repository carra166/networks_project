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
#weather_publishers = []
news_subscribers = []
#news_publishers = []


'''
:param msg_items: list of items received from client message

'''
def is_valid_message(msg_items, num_items):
    content_type = 'Not Valid'
    action_valid = False
    subject_exists = False
    if num_items == 1:      # Could be <DISC> or invalid
        if msg_items[0] == 'DISC':
            content_type = 'DISC'
            action_valid = True

    elif num_items == 2:    # Could be <CLIENT_NAME, CONN> or invalid
        if msg_items[1] == 'CONN':
            content_type = 'CONN'
            action_valid = True

    elif num_items == 3:    # Could be <CLIENT_NAME, SUB, SUBJECT> or invalid
        if (msg_items[1] == 'SUB') and (msg_items[2] in valid_subjects):
            content_type = 'SUB'
            action_valid = True
            subject_exists = True

    elif num_items == 4:    # Could be <CLIENT_NAME, PUB, SUBJECT, MSG> or invalid
        if (msg_items[1] == 'PUB') and (msg_items[2] in valid_subjects):
            content_type = 'PUB'
            action_valid = True
            subject_exists = True

    return content_type, action_valid, subject_exists


# Handles each client connection
def handle_client(client_socket, client_address):
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
            msg_type, msg_valid, action_subject = is_valid_message(message_content, message_item_count)

            if msg_valid:
                if msg_type == 'DISC':
                    pass
                elif msg_type == 'CONN':
                    pass
                elif msg_type == 'SUB':
                    # TODO: See errors below to be checked
                    # Is client already subscribed?
                    # Is client attempting to subscribe to non existent subject?
                    pass
                elif msg_type == 'PUB':
                    # TODO: See below for errors to check
                    # Is publisher subscribed to the subject they are publishing?
                    # Is publisher attempting to publish to a non0existent subject?
                    pass

            elif () or () or () or ():      # This case covers clients that have been subscribed, but attempted an invalid action
                client_socket.sendall(f"ERROR: {error_messages[2]}".encode("utf-8"))

            else:       # This case covers a client that is not listed at all, forces it to disconnect
                break

            # TODO: Change this accordingly after testing basic functionality
            # Echo message back
            client_socket.sendall(f"Server received: {message}".encode("utf-8"))

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