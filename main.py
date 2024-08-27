from tkinter import *

# Définis les bases du jeudefaut_theme = 'white'grille = 8balles = 4class Game:
    def __init__(self):
        # Initialisation de la racine du jeu        self.root = Tk()
        self.root.title("BlackBox Game")
        self.root.geometry("1080x720")
        self.root.resizable = False        self.root.configure(bg='white')

        self.traversed_buttons = []
        self.buttons = []
        self.balles_positions = set()  # Stocker les positions des balles        self.score = 0        self.start = True  # Indicateur pour savoir si on est en mode de placement des balles        # Affichage des 2 espaces du jeu        self.side_board()
        self.game_space()

    def side_board(self):
        self.board = Frame(self.root, bg='lightgray', width=360, height=720)
        self.board.pack(side=RIGHT, fill=Y)
        self.board.pack_propagate(False)

        title = Label(self.board, text='𝘽𝙡𝙖𝙘𝙠𝘽𝙤𝙭 -𝙂𝙖𝙢𝙚', font=('Arial', 23), bg='lightgrey')
        title.pack(side=TOP, pady=35)

        self.balles_restantes = balles
        self.balles_stock = Label(self.board, text=f'Balles restantes : {self.balles_restantes}', font=('Lato', 25),                                  bg='lightgray')
        self.balles_stock.place(x=50, y=220)

        self.score_label = Label(self.board, text=f'Score : {self.score}', font=('Lato', 25), bg='lightgray')
        self.score_label.place(x=50, y=280)

        start_button = Button(self.board, text='Start', bg='lightgreen', font=('Lato', 23), width=13, height=2,                              command=self.start_game)
        start_button.place(x=50, y=350)

        reset_button = Button(self.board, text='Reset', bg='blue', font=('Lato', 23), width=13, height=2,                              command=self.reset_game)
        reset_button.place(x=50, y=450)

    def poser_balles(self, row, col):
        if self.start and self.balles_restantes > 0:
            button = self.buttons[row][col]
            if button.cget('bg') == 'white':
                button.config(bg='black')
                self.balles_positions.add((row, col))  # Ajouter la position à l'ensemble des balles                self.balles_restantes -= 1                self.balles_stock.config(text=f'Balles restantes : {self.balles_restantes}')

    def start_game(self):
        if self.start:
            self.start = False            # Cacher les balles (les rendre à nouveau invisibles)            for row, col in self.balles_positions:
                button = self.buttons[row][col]
                button.config(bg=defaut_theme)

    def reset_game(self):
        self.balles_restantes = balles
        self.start = True        self.balles_positions.clear()  # Vider les positions des balles        self.traversed_buttons.clear()
        self.score = 0        self.balles_stock.config(text=f'Balles restantes : {self.score}')

    def faisseau(self, start_row, start_col):
        if self.start:  # Si on est en mode de placement, on ne lance pas de faisceau            return        # Détermine la direction        global direction
        if start_row == 0:
            direction = (1, 0)  # bas        elif start_row == grille + 1:
            direction = (-1, 0)  # haut        elif start_col == 0:
            direction = (0, 1)  # droite        elif start_col == grille + 1:
            direction = (0, -1)  # gauche        current_row, current_col = start_row, start_col
        self.traversed_buttons.clear()

        while 0 <= current_row <= grille + 1 and 0 <= current_col <= grille + 1:
            current_row += direction[0]
            current_col += direction[1]

            # Vérifier si le faisceau touche une balle            if (current_row, current_col) in self.balles_positions:
                self.score += 1                self.score_label.config(text=f'Score : {self.score}')
                self.balles_positions.remove((current_row, current_col))  # Supprimer la balle                button = self.buttons[current_row][current_col]
                button.config(bg='black')  # Afficher la case en noir                break  # Le faisceau est arrêté s'il touche une balle            # Check si il est sorti du plateau            if current_row == 0 or current_row == grille + 1 or current_col == 0 or current_col == grille + 1:
                break            if 0 <= current_row <= grille + 1 and 0 <= current_col <= grille + 1:
                button = self.buttons[current_row][current_col]
                button.config(bg='blue')
                self.traversed_buttons.append(button)

        self.root.after(1000, self.reset_faisceau)  

    def reset_faisceau(self):
        for button in self.traversed_buttons:
            if button.cget('bg') != 'black':  # Ne pas réinitialiser si la case est noire (contient une balle)                button.config(bg=defaut_theme)  # Remet la couleur des boutons à la couleur par défaut        self.traversed_buttons.clear()

    def game_space(self):
        field = Frame(self.root, bg=defaut_theme, width=624, height=720)
        field.pack(side=LEFT, padx=40)

        for i in range(grille+2):
            row = []
            for ii in range(grille+2):
                if (i == 0 or i == grille+1 or ii == 0 or ii == grille+1) and not ((i == 0 and ii == 0) or (i == 0 and ii == grille + 1) or (i == grille + 1 and ii == 0) or (i == grille + 1 and ii == grille + 1)):
                    case = Button(field, width=4, height=2, bg='red', command=lambda i=i, ii=ii: self.faisseau(i, ii))
                elif not (i == 0 or i == grille + 1 or ii == 0 or ii == grille + 1):
                    case = Button(field, borderwidth=1, width=4, height=2, bg='white', command=lambda i=i, ii=ii: self.poser_balles(i, ii))
                else:
                    continue                case.grid(row=i, column=ii, padx=2, pady=2)
                row.append(case)
            self.buttons.append(row)


if __name__ == '__main__':
    blackbox = Game()
    blackbox.root.mainloop()
