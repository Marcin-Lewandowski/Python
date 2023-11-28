# Expense Tracker  - in polish at the moment  ;)

# Objectives :
# Create an app that allows the user to track expenses and income.
# Add transaction categorization functionality and generate financial summaries.
# Use a SQLite database to store transactional data.

import PySimpleGUI as sg
import sqlite3, csv
import datetime

width = 1800
height = 900

class ExpenseTrackerApp:
    def __init__(self):
        # Nawiązanie połączenia z bazą danych (utworzy nową, jeśli nie istnieje)
        self.connection = sqlite3.connect(r'c:\kodilla\Python\baza_danych.db')

        # Utworzenie obiektu kursora
        self.cursor = self.connection.cursor()

        # Stworzenie tabeli 'transakcje' (jeśli nie istnieje)
        self.create_transactions_table()

        # Pobranie nazw kolumn z bazy danych
        self.column_names = self.get_column_names()

        # Pobranie transakcji z bazy danych i zapisanie ich w liście transactions
        self.transactions = self.get_transactions_from_database()

        # Definicja interfejsu graficznego
        upper_left_frame = [
            [sg.Text("Witaj w Kalkulatorze Wydatków!")],
            [sg.Button("Dodaj Transakcję")],
        ]

        middle_left_frame = [
            [sg.Text("To jest środkowa część lewej kolumny")],
            [sg.Button("Zapisz do CSV")]
        ]

        lower_left_frame = [
            [sg.Text("To jest dolna część lewej kolumny")],
            [sg.Button("Przycisk w dolnej części")]
        ]


        frame_center = [
            [sg.Text("To jest srodkowa kolumna")],
            [sg.Button("Przycisk :)")]
        ]


        left_column = [
            [sg.Frame("Górna Część", upper_left_frame, size=(350, 360))],
            [sg.Frame("Srodkowa Część", middle_left_frame, size=(250, 200))],
            [sg.Frame("Dolna Część", lower_left_frame, size=(250, 360))]
        ]

        # Dynamiczne tworzenie kolumny dla danych transakcyjnych
        transactions_column = []
        for transaction in self.transactions:
            transactions_column.append(list(transaction))

        header_list = self.column_names
        data_list = transactions_column


        middle_column = [
            [sg.Frame("Środkowa kolumna z uśmiechem :)", frame_center, size = (250, 660))]
            
        ]
        
        
        right_column = [
            [sg.Column([
                [sg.Table(values=data_list, headings=header_list,auto_size_columns = False, 
                                justification='center', 
                                col_widths=[5, None, None, 20, None, None, 40], 
                                font=('Helvetica', 12),
                                #size = (1200, None),
                                num_rows=min(80, 100), key='-TABLE-', enable_events=True)]],
                        )  # Ustawienie wysokości kolumny na 500 pikseli: size=(width, height)
            ]
            
        ]
        
        
        self.main_layout = [
            [
                sg.Column(left_column, justification='top'),  # Lewa kolumna
                sg.Column(middle_column, justification='top'),  # środkowa kolumna
                sg.Column(right_column, justification='top')  # Prawa kolumna
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

    def get_column_names(self):
        # Pobranie nazw kolumn z tabeli 'transakcje'
        self.cursor.execute('PRAGMA table_info(transakcje)')
        columns_info = self.cursor.fetchall()
        column_names = [info[1] for info in columns_info]
        return column_names

    def get_transactions_from_database(self):
        # Pobranie transakcji z bazy danych
        self.cursor.execute('SELECT * FROM transakcje')
        transactions = self.cursor.fetchall()
        return transactions
    
    def save_to_csv(self):
        # Ustanów połączenie z bazą danych
        conn = sqlite3.connect(r'c:\kodilla\Python\baza_danych.db')  # Zmień 'twoja_baza_danych.db' na nazwę twojej bazy danych

        # Uzyskaj kursor do wykonania poleceń SQL
        cursor = conn.cursor()
        # Wykonaj zapytanie SQL, aby pobrać dane z tabeli
        cursor.execute("SELECT * FROM transakcje")  # Zmień 'nazwa_tabeli' na nazwę twojej tabeli
        rows = cursor.fetchall()

        # Ścieżka do pliku CSV, który chcesz utworzyć
        path = (r'c:\kodilla\Python\transakcje.csv')

        # Zapisz wyniki do pliku CSV
        with open(path, mode='w', newline='', encoding='utf-8') as plik_csv: 
            writer = csv.writer(plik_csv)
            # Zapisz nagłówki kolumn
            writer.writerow([i[0] for i in cursor.description])
            # Zapisz dane
            writer.writerows(rows)

        print(f'Dane zostały zapisane do pliku CSV: {path}')

        # Zamknij połączenie z bazą danych
        conn.close()
        
    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Dodaj Transakcję":
                self.open_add_transaction_window()
                
            elif event == "Zapisz do CSV":
                self.save_to_csv()

        self.window.close()

    def open_add_transaction_window(self):
        # Okno dodawania transakcji
        add_transaction_layout = [
            [sg.Text("Dodaj Transakcję")],
            [sg.Text("Data"), sg.CalendarButton("Wybierz datę", target="data", format="%d-%m-%Y", button_color=('black', 'white'), key="cal_button"), sg.Input(key="data", visible=True)],
            [sg.Text("Kwota"), sg.Input(key="kwota")],
            [sg.Text("Opis"), sg.Input(key="opis")],
            [sg.Text("Kategoria"), sg.Combo(['Jedzenie', 'Opłaty', 'Dom', 'Samochód', 'Ubrania', 'Inne'], key="kategoria", default_value='Jedzenie')],
            [sg.Text("Typ transakcji"), sg.Combo(['Karta', 'Gotówka', 'Direct Debit', 'PayPal'], key="typ_transakcji", default_value='Karta')],
            [sg.Text("Tagi"), sg.Input(key="tagi")],
            [sg.Button("Dodaj"), sg.Button("Anuluj")]
        ]

        add_transaction_window = sg.Window("Dodaj Transakcję", add_transaction_layout)

        while True:
            event, values = add_transaction_window.read()

            if event == sg.WINDOW_CLOSED: 
                break
            elif event == "Anuluj":
                add_transaction_window.close()
                
            elif event == "Dodaj":
                self.add_transaction(values)
                self.transactions = self.get_transactions_from_database()
                
                
                data_list = [list(transaction) for transaction in self.transactions]
                self.window['-TABLE-'].update(values=data_list)
                
                
                add_transaction_window.close()             

    def add_transaction(self, values):
        # Pobierz dane od użytkownika
        data = values["data"]
        kwota = values["kwota"]
        opis = values["opis"]
        kategoria = values["kategoria"]
        typ_transakcji = values["typ_transakcji"]
        tagi = values["tagi"]

        try:
        # Sprawdź, czy wprowadzone dane to liczba
            kwota = float(kwota)

            # Sprawdź, czy wprowadzona kwota to liczba zmiennoprzecinkowa większa od zera
            if kwota <= 0:
                sg.popup_error("Kwota musi być liczbą większą od zera.")
                return

        except ValueError:
            # Kod do wykonania, gdy wprowadzone dane to liczba typu int lub float większa od zera
            sg.popup_error("ValueError")
            return

        else:
            # Kod do wykonania, gdy wprowadzone dane to liczba float lub int
            kwota = float(kwota)
            

        # Dodaj transakcję do bazy danych
        self.cursor.execute('''
            INSERT INTO transakcje (data, kwota, opis, kategoria, typ_transakcji, tagi)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data, kwota, opis, kategoria, typ_transakcji, tagi))

        # Zatwierdzenie zmian
        self.connection.commit()

        sg.popup("Dodano transakcję do bazy danych!")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()
