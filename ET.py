# Expense Tracker  - in polish at the moment  ;)

# Objectives :
# Create an app that allows the user to track expenses and income.
# Add transaction categorization functionality and generate financial summaries.
# Use a SQLite database to store transactional data.

import PySimpleGUI as sg
import sqlite3
import datetime
width = 1200
height = 800
class ExpenseTrackerApp:
    def __init__(self):
        # Nawiązanie połączenia z bazą danych (utworzy nową, jeśli nie istnieje)
        self.connection = sqlite3.connect('c://kodilla/Python/baza_danych.db')

        # Utworzenie obiektu kursora
        self.cursor = self.connection.cursor()

        # Stworzenie tabeli 'transakcje' (jeśli nie istnieje)
        self.create_transactions_table()
        
        # Pobranie transakcji z bazy danych i zapisanie ich w liście transactions
        self.transactions = self.get_transactions_from_database()
        
    
        
        
        # Definicja interfejsu graficznego
        
        upper_left_frame = [
            [sg.Text("Witaj w Kalkulatorze Wydatków!")],
            [sg.Button("Dodaj Transakcję")]
        ]

        lower_left_frame = [
            [sg.Text("To jest dolna część lewej kolumny")],
            [sg.Button("Przycisk w dolnej części")]
        ]

        
        
        left_column = [
            [sg.Frame("Górna Część", upper_left_frame, size=(250, 360))],
            [sg.Frame("Dolna Część", lower_left_frame, size=(250, 360))]
            
        ]
        
        

        right_column = [
            [sg.Listbox( values=self.transactions, size=(int(width/2), int(height/2)), key="-TRANSACTIONS-" ,enable_events=True)]
            
        ]
       

        self.main_layout = [
            [
                sg.Column(left_column, justification='top'),  # Lewa kolumna
                sg.Column(right_column)  # Prawa kolumna
            ]
        ]


        # Utworzenie okna
        
        
        self.window = sg.Window("Expense Tracker", self.main_layout, size=(width, height), resizable=True)
       
        
        

    def create_transactions_table(self):
        # Stworzenie tabeli 'transakcje'
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transakcje (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                kwota REAL NOT NULL,
                opis TEXT,
                kategoria TEXT,
                typ_transakcji TEXT,
                tagi TEXT
            )
        ''')
        # Zatwierdzenie zmian
        self.connection.commit()

    def get_transactions_from_database(self):
        # Pobranie transakcji z bazy danych
        self.cursor.execute('SELECT * FROM transakcje')
        transactions = self.cursor.fetchall()
        return transactions
        
        
    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Dodaj Transakcję":
                self.open_add_transaction_window()

        self.window.close()




    def open_add_transaction_window(self):
        # Okno dodawania transakcji
        add_transaction_layout = [
            [sg.Text("Dodaj Transakcję")],
            [sg.Text("Kwota"), sg.Input(key="kwota")],
            [sg.Text("Opis"), sg.Input(key="opis")],
            
            
            [sg.Text("Kategoria"), sg.Combo(['Jedzenie', 'Opłaty', 'Dom', 'Samochód', 'Inne'], key="kategoria", default_value='Jedzenie')],
            
            
            
            [sg.Text("Typ transakcji"), sg.Combo(['Karta', 'Gotówka', 'Direct Debit', 'PayPal'], key = "typ_transakcji", default_value='Karta')],
            
            
            
            [sg.Text("Tagi"), sg.Input(key="tagi")],
            [sg.Button("Dodaj"), sg.Button("Anuluj")]
        ]

        add_transaction_window = sg.Window("Dodaj Transakcję", add_transaction_layout)

        while True:
            event, values = add_transaction_window.read()

            if event == sg.WINDOW_CLOSED or event == "Anuluj":
                break
            elif event == "Dodaj":
                self.add_transaction(values)
                self.transactions = self.get_transactions_from_database()  # błąd ???
                self.window["-TRANSACTIONS-"].update(values=self.transactions)
                add_transaction_window.close()

    def add_transaction(self, values):
        # Pobierz dane od użytkownika
        kwota = float(values["kwota"])
        opis = values["opis"]
        kategoria = values["kategoria"]
        typ_transakcji = values["typ_transakcji"]
        tagi = values["tagi"]

        # Data ustawiona automatycznie na aktualną datę
        data = str(datetime.date.today())

        # Dodaj transakcję do bazy danych
        self.cursor.execute('''
            INSERT INTO transakcje (data, kwota, opis, kategoria, typ_transakcji, tagi)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data, kwota, opis, kategoria, typ_transakcji, tagi))

        # Zatwierdzenie zmian
        self.connection.commit()
        ####

        sg.popup("Dodano transakcję do bazy danych!")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()