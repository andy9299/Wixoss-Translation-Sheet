import xmltodict
from textwrap import wrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from cgitb import text

def open_db(db_location):
    """given path to Wixoss TCG.xml create a dictionary"""
    with open(db_location) as db_file:
        db = xmltodict.parse(db_file.read())

    db = db["cockatrice_carddatabase"]["cards"]["card"]
    return db

def open_decks(deck_location):
    """given a path to a Wixoss cod deck file get the lrig and main deck data """
    with open(deck_location) as deck:
        deck= xmltodict.parse(deck.read())

    lrig_deck_data = deck['cockatrice_deck']['zone'][0]['card']
    main_deck_data = deck['cockatrice_deck']['zone'][1]['card']
    return (lrig_deck_data, main_deck_data)

def parse_decks(decks, db):
    """given a tuple of decks and the card db return a tuple of the cards and data"""
    lrig_deck_cards = []
    main_deck_cards = []

    for card in decks[0]:
        name = card['@name']
        db_card = next(item for item in db if item["name"] == name)
        lrig_deck_cards.append(db_card)

    for card in decks[1]:
        name = card['@name']
        db_card = next(item for item in db if item["name"] == name)
        main_deck_cards.append(db_card)

    return (lrig_deck_cards, main_deck_cards)

def write_deck_on_canvas(deck, canvas):
    """given deck data write the images and text onto a pdf"""
    document_width, document_height = letter
    for card in deck:
        try:
            image_url = card["set"]["@picURL"]
        except:
            image_url = card["set"][0]["@picURL"]
        name = card["name"]
        type = card["prop"]["type"]
        text = card["text"] or "N/A"
        wraped_text_list = text.split("\n")
        for i, string in enumerate(wraped_text_list):
            wraped_text_list[i] = "\n".join(wrap(string, 53)) + "\n"
        wraped_text = "".join(wraped_text_list)
        canvas.drawImage(image_url, 0, 0, width=document_width,
                        height=document_height)
        canvas.showPage()
        text_object = canvas.beginText()
        text_object.setTextOrigin(10, 3 * document_height/4)
        text_object.setFont('Times-Roman', 24)
        text_object.textLines(f"""Name: {name}
        Type: {type}
        Text: {wraped_text}
        """)
        canvas.drawText(text_object)
        canvas.showPage()

def create_pdf(decks, pdf_file_name):
    """create and write both decks onto a pdf"""
    canvas = Canvas(pdf_file_name, pagesize=letter)

    write_deck_on_canvas(decks[0], canvas)
    write_deck_on_canvas(decks[1], canvas)

    canvas.save()
