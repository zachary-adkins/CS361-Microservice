import zmq
import time
import json

def main():
    # Setting up the socket: server-side
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:

        # Receiving a message from the client
        message = socket.recv_json()
        for key, value in message.items():
            message_key = key
            message_value = value

        time.sleep(1)

        # Initially reading the JSON file containing decks
        with open("decks.json", 'r') as f:
            try:
                decks = json.load(f)
            except ValueError:
                decks = {}
            finally:
                f.close()

        # No decks in the JSON file
        if len(decks) == 0:
            # Adding first deck with array of cards
            if len(message_value) > 0:
                with open("decks.json", 'w') as f2:
                    json.dump(message, f2)
                    socket.send_string("Deck saved")
                    f2.close()
            # Invalid request - attempting to retrieve from empty "decks.json"
            else:
                socket.send_string("No decks in saved decks")
                return

        # There are decks in the JSON file and a deck being sent by the client
        elif len(message_value) != 0:
            # Deck already exists in "decks.json" - overwrite
            if message_key in decks:
                decks[message_key] = message_value
                with open("decks.json", 'w') as f3:
                    json.dump(decks, f3)
                    socket.send_string("Deck overwritten")
                    f3.close()
            # Deck doesn't exist - append
            else:
                with open("decks.json", 'r+') as f4:
                    decks = json.load(f4)
                    decks[message_key] = message_value
                    f4.seek(0)
                    json.dump(decks, f4)
                    socket.send_string("Deck saved")
                    f4.close()
        # There are decks in the JSON file and an empty array being sent by the client - retrieve
        else:
            socket.send_json({message_key: decks[message_key]})

                
if __name__ == '__main__':
    main()
