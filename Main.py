# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:42:04 2020

@author: Mauro
"""

import os
from flask import Flask, render_template
 
# costruisco il percorso alla cartella "static" basandomi sul path dell'applicazione corrente
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
 
# creo la app passando il percorso della cartella con le risorse statiche
app = Flask(__name__, static_url_path="/static", static_folder=static_file_dir) 

db = [
      {"id": '0', "title": "Home", "html_page":"home.html"},
      {"id": '1', "title": "Results", "html_page":"results.html", "data":{}}
     ]

# metodo per recuperare la pagina singola
def get(id):
    for item in db:
        if item["id"] == id:
            return item
    return None

# metodo per recuperare il menu in base alle pagine presenti nel db
def menu():
    items = []
    return items

# definisco un metodo che si occupa di caricare la pagina dal DB
# se non la trova mostra la pagina di errore 404
def get_page(id):
    page = get(id)
    if page == None:
        # se non trovo la pagina errore 404
        return page_not_found(None)
    # recupero il menu
    menu_ = menu()
    html_page = page["html_page"]
    # faccio il render
    return render_template(html_page, menu=menu_, page=page) 
 
# definisco la prima route, home, caricherà la pagina con id=0
@app.route("/")
def main():
    return get_page('0')

@app.route("/results")
def results():
	application_path = os.getcwd()
    chromedrv_path = application_path + "\chromedriver.exe"
    driver = webdriver.Chrome(chromedrv_path)
    #driver.set_window_position(-5000, 0)
    print('Connessione a sisal.it...')
    driver.get("https://www.sisal.it/scommesse-live?disciplina=1&streaming=false")
	db[1]['data'] = driver.find_element_by_class_name("sc-gPEVay.emAhFN").text
	driver.quit()
    return get_page('1')

# pagina di errore
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

# verifica se è il programma principale
# e manda in esecuzione il web server su http://localhost:5000
if __name__ == "__main__":
    app.run(debug=False, port=5000)