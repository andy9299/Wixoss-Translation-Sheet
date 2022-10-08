import utilities

# default assumes files are in the same directory
db_location = "Wixoss TCG.xml"
deck_location = "test_deck.cod"
pdf_file_name = "test_deck.pdf"

db = utilities.open_db(db_location)

decks = utilities.open_decks(deck_location)
decks = utilities.parse_decks(decks, db)

utilities.create_deck(decks, pdf_file_name)