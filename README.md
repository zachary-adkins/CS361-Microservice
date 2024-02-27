How to Request Data utilizing my Microservice
    Make sure zmq is installed in your environment and imported in your program.
    Have a file in the same directory as the server titled "decks.json"
    Create a socket that is connected to "tcp://localhost:5555".
    Make sure that the server file provided is running in the background.

    The full call to request data will look something like this:
        SOCKET_NAME.send_json(example_deck_name)
    Format your data to be sent to the server.
        Send your data as a JSON object. The server will be waiting to receive a JSON object. I sent python dictionaries as JSON objects in my testing.

        For example:
            example_deck_name = {deck_name: cards_list}
            deck_name is a STRING to be used for deck naming purposes
                For example: 
                    "dragon", "burn", "xyz", etc.
            cards_list is an ARRAY (I used Python Lists)
                For example: 
                    ["Blue Eyes White Dragon", "Red Eyes Black Dragon", "Dark Magician"]

        Some things to know when requesting data:
            Passing a filled array as the cards_list with a deck_name that has not been added to the system yet will add the {deck_name: cards_list} to "decks.json".

            Passing a filled array as the cards_list with a deck_name that is already in the JSON file will overwrite the contents paired with deck_name.
            For example:
                IN "decks.json" before call: {"dragon": ["Blue Eyes White Dragon", "Red Eyes Black Dragon"]}

                deck_name = "dragon"
                cards_list = ["Cyber Dragon", "Blue Eyes White Dragon"]
                example_deck = {deck_name: cards_list}
                socket.send_json(example_deck)

                IN "decks.json" after call: {"dragon": ["Cyber Dragon", "Blue Eyes White Dragon"]}

            Passing an empty array as the cards_list will retrieve all cards for the given deck_name.
            For example (continuing from previous example):
                deck_name = "dragon"
                cards_list = []
                example_deck = {deck_name: cards_list}
                socket.send_json(example_deck)
                This will return: 
                    "dragon": ["Cyber Dragon", "Blue Eyes White Dragon"]

            Passing an empty array as the cards_list when "decks.json" is empty will not work! You will receive an error message.

How to Receive Data utilizing my Microservice
    The full call to receive data will look something like this:
        data = SOCKET_NAME.recv()
        This will return a byte object to the user.
        For example:
            When a deck is added or updated, the server will send a message saying b"Deck saved" or b"Deck overwritten" respectively

            When the user attempts to retrieve from an empty "decks.json", the server will send a message saying b"No decks in saved decks"

            When the user asks to retrieve a deck from "decks.json" by passing an empty list with a recognizable deck_name, the server will send the array of the cards for that deck. The response will look something like this:
                b"{"dragon": ["Cyber Dragon", "Blue Eyes White Dragon"]}"

UML Diagram