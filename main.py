from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QListWidget, QTextEdit, QHBoxLayout

import json

# Funciones para escribir y leer notas
def write_notas():
    namefile = 0
    print(1,notes)
    for name in notes:
        filename = str(namefile) + '.txt'
        with open(filename, "w", encoding='utf-8') as file:
            file.write(name + '\n')
            file.write(notes[name]['texto'] + '\n')
            tags = notes[name]['etiquetas']
            for tag in tags:
                file.write(tag+' ')
            #tags = ' '.join(tags)
        namefile += 1

def read_notes():
    global notes
    namefile = 0
    while True:
        filename = str(namefile) + '.txt'
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                name = file.readline().strip()
                text = file.readline().strip()
                tags = file.readline().split()
                notes[name] = {'texto': text, 'etiquetas': tags}
            namefile += 1
            print(notes)
        except FileNotFoundError:
            break



# Inicializar notas
init_file=False
if init_file:
    with open("0.txt", "w", encoding='utf-8') as file:
            file.write("nota_inicial_0"+'\n')
            file.write("Texto de la nota 0"+'\n')
            file.write("eti00 eti01")
            
            
    

notes = {}
read_notes()

# Crear ventana principal
app = QApplication([])
win = QWidget()
win.setWindowTitle('Smart Notes')
win.resize(900, 600)

# Estilos
win.setStyleSheet("background-color: #f0f0f0;")
button_style = "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; border-radius: 5px;"
label_style = "font-weight: bold; font-size: 14px;"
text_edit_style = "background-color: #ffffff; border: 1px solid #ccc; border-radius: 5px; padding: 5px;"

# Layouts
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()
field_text = QTextEdit()
field_text.setStyleSheet(text_edit_style)
col_1.addWidget(field_text)

# Columna 2
list_note_label = QLabel('Lista de Notas')
list_note_label.setStyleSheet(label_style)
list_notes = QListWidget()
col_2.addWidget(list_note_label)
col_2.addWidget(list_notes)

# Botones para notas
button_note_create = QPushButton('Crear Nota')
button_note_create.setStyleSheet(button_style)
button_note_del = QPushButton('Eliminar Nota')
button_note_del.setStyleSheet(button_style)
button_note_save = QPushButton('Guardar Nota')
button_note_save.setStyleSheet(button_style)

# Layout de botones
row1 = QHBoxLayout()
row2 = QHBoxLayout()

row1.addWidget(button_note_create)
row1.addWidget(button_note_del)
col_2.addLayout(row1)

row2.addWidget(button_note_save)
col_2.addLayout(row2)

# Etiquetas
list_tags_label = QLabel('Lista de Etiquetas')
list_tags_label.setStyleSheet(label_style)
list_tags = QListWidget()
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Ingresar etiqueta...')
field_tag.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")

button_add_tag = QPushButton('Añadir Etiqueta')
button_add_tag.setStyleSheet(button_style)
button_del_tag = QPushButton('Remover Etiqueta')
button_del_tag.setStyleSheet(button_style)
button_search_tag = QPushButton('Buscar por Etiqueta')
button_search_tag.setStyleSheet(button_style)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

# Botones de etiquetas
row3 = QHBoxLayout()
row3.addWidget(button_add_tag)
row3.addWidget(button_del_tag)
col_2.addLayout(row3)

row4 = QHBoxLayout()
row4.addWidget(button_search_tag)
col_2.addLayout(row4)

# Organizar layouts
layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
win.setLayout(layout_notes)

#Cargar las keys enla lista de notas
list_notes.addItems(notes)

# Funciones para interacción
def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["texto"])
        list_tags.clear()
        list_tags.addItems(notes[key]["etiquetas"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        text = field_text.toPlainText()
        notes[key]['texto'] = text
        write_notas()

def create_note():
    note_name, result = QInputDialog.getText(win, 'Añadir Nota', 'Nombre de la nueva nota:')
    if result and note_name != '':
        notes[note_name] = {'texto': '', 'etiquetas': []}
        list_notes.addItem(note_name)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag and tag not in notes[key]['etiquetas']:
            notes[key]['etiquetas'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            write_notas()

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['etiquetas'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['etiquetas'])
        write_notas()

def sh_tag():
    tag = field_tag.text()
    if button_search_tag.text() == 'Buscar por Etiqueta' and tag != '':
        notes_filtered = {note: notes[note] for note in notes if tag in notes[note]["etiquetas"]}
        button_search_tag.setText('Restablecer Búsqueda')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_search_tag.text() == 'Restablecer Búsqueda':
        list_notes.clear()
        list_tags.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        button_search_tag.setText('Buscar por Etiqueta')

# Conectar eventos
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_create.clicked.connect(create_note)
button_note_del.clicked.connect(del_note)
button_add_tag.clicked.connect(add_tag)
button_search_tag.clicked.connect(sh_tag)
button_del_tag.clicked.connect(del_tag)

# Mostrar ventana
win.show()
app.exec()
