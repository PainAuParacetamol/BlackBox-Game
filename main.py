from tkinter import *

# Définis les bases du jeudefaut_theme = 'white'grille = 8balles = 4class Game:
    def __init__(self):
        self.root = Tk()
        self.root.title("BlackBox Game")
        self.root.geometry("1080x720")
        self.root.resizable(False, False)
        self.root.configure(bg='white')

        self.traversed_buttons = []
        self.buttons = []
        self.balles_positions = set()
        self.balles_touchees = set()
        self.score = 0        self.start = True  # Mode de placement des balles        self.phase = 1  # Phase 1 : Placement des balles, Phase 2 : Envoi de faisceaux        self.side_board()
        self.game_space()

    def side_board(self):
        self.board = Frame(self.root, bg='lightgray', width=360, height=720)
        self.board.pack(side=RIGHT, fill=Y)
        self.board.pack_propagate(False)

        title = Label(self.board, text='𝘽𝙡𝙖𝙘𝙠𝘽𝙤𝙭 -𝙂𝙖𝙢𝙚', font=('Arial', 23), bg='lightgrey')
        title.pack(side=TOP, pady=35)

        self.balles_restantes = balles
        self.info_label = Label(self.board, text=f'Balles restantes : {self.balles_restantes}', font=('Lato', 25),                                bg='lightgray')
        self.info_label.place(x=50, y=220)

        self.start_button = Button(self.board, text='Start', bg='lightgreen', font=('Lato', 23), width=13, height=2,                                   command=self.start_game)
        self.start_button.place(x=50, y=350)

        reset_button = Button(self.board, text='Reset', bg='blue', font=('Lato', 23), width=13, height=2,                              command=self.reset_game)
        reset_button.place(x=50, y=450)

        self.info_square = Label(self.board, width=2, height=1, text="", bg='Darkgray', font=('Arial', 50), fg='Blue')
        self.info_square.place(x=132, y=590)
        self.info_square.pack_propagate(False)

    def poser_balles(self, row, col):
        if self.start and self.balles_restantes > 0:
            button = self.buttons[row][col]
            if button.cget('bg') == 'white':
                button.config(bg='black')
                self.balles_positions.add((row, col))
                self.balles_restantes -= 1                self.info_label.config(text=f'Balles restantes : {self.balles_restantes}')

    def start_game(self):
        if self.start:
            if self.balles_restantes > 0:
                self.info_label.config(text="Placez toutes les balles!")
                return            self.start = False            self.phase = 2            self.info_label.config(text=f'Score : {self.score}')
            self.start_button.config(state=DISABLED)

            # Cacher les balles (les rendre à nouveau invisibles)            for row, col in self.balles_positions:
                button = self.buttons[row][col]
                button.config(bg=defaut_theme)

    def reset_game(self):
        self.balles_restantes = balles
        self.start = True        self.phase = 1        self.balles_positions.clear()
        self.balles_touchees.clear()
        self.traversed_buttons.clear()
        self.score = 0        self.start_button.config(state=NORMAL)

        self.info_label.config(text=f'Balles restantes : {self.balles_restantes}')

        for i, row in enumerate(self.buttons):
            for j, button in enumerate(row):
                if i == 0 or i == grille + 1 or j == 0 or j == grille + 1:
                    button.config(bg='red')  # Garder les bordures rouges                else:
                    button.config(bg=defaut_theme)  # Rendre les cases internes blanches    def faisseau(self, start_row, start_col):
        if self.phase != 2:
            return        # Définir la direction du faisceau en fonction de la position de départ        if start_row == 0:
            direction = (1, 0)  # bas        elif start_row == grille + 1:
            direction = (-1, 0)  # haut        elif start_col == 0:
            direction = (0, 1)  # droite        elif start_col == grille + 1:
            direction = (0, -1)  # gauche        current_row, current_col = start_row, start_col
        absorbed = False        reflection_occurred = False        beam_terminated = False        while not beam_terminated:
            next_row = current_row + direction[0]
            next_col = current_col + direction[1]

            # Arrêter si le faisceau sort du plateau            if next_row < 0 or next_row > grille + 1 or next_col < 0 or next_col > grille + 1:
                beam_terminated = True                break            # Vérifier pour l'absorption immédiate (collision directe avec une balle)            if (next_row, next_col) in self.balles_positions:
                absorbed = True                self.info_square.config(text='H')
                self.root.after(1000, lambda: self.info_square.config(text=''))
                break            # Vérifier la réflexion immédiate (balle adjacente sur le bord)            if (current_row in [0, grille + 1] or current_col in [0, grille + 1]):
                # Détecter si le faisceau doit réfléchir à cause d'une balle adjacente                diag_left = (current_row + (-direction[1]), current_col + (-direction[0]))
                diag_right = (current_row + direction[1], current_col + direction[0])

                if diag_left in self.balles_positions and diag_right in self.balles_positions:
                    # Double déviation                    reflection_occurred = True                    break                elif diag_left in self.balles_positions or diag_right in self.balles_positions:
                    # Réflexion simple (rebondir en arrière)                    reflection_occurred = True                    break            # Mettre à jour la position du faisceau s'il n'y a ni absorption ni réflexion            current_row, current_col = next_row, next_col

        # Si le faisceau a été absorbé, on arrête ici        if absorbed:
            return        # Si une réflexion a eu lieu        if reflection_occurred:
            self.info_square.config(text='R')
            self.show_faisseau_result(start_row, start_col)
            self.root.after(1000, lambda: self.info_square.config(text=''))
        else:
            # Si aucune réflexion n'a eu lieu, montrer la position finale            self.show_faisseau_result(current_row, current_col)

        self.score += 1        self.info_label.config(text=f'Score : {self.score}')

    def show_faisseau_result(self, row, col):
        button = self.buttons[row][col]
        button.config(bg='yellow')
        # Revenir à la couleur rouge après 1 seconde        self.root.after(1000, lambda: button.config(bg='red'))

    def game_space(self):
        field = Frame(self.root, bg=defaut_theme, width=624, height=720)
        field.pack(side=LEFT, padx=40)

        for i in range(grille + 2):
            row = []
            for ii in range(grille + 2):
                if (i == 0 or i == grille + 1 or ii == 0 or ii == grille + 1) and not (
                        (i == 0 and ii == 0) or (i == 0 and ii == grille + 1) or (i == grille + 1 and ii == 0) or (
                        i == grille + 1 and ii == grille + 1)):
                    case = Button(field, width=4, height=2, bg='red', command=lambda i=i, ii=ii: self.faisseau(i, ii))
                elif not (i == 0 or i == grille + 1 or ii == 0 or ii == grille + 1):
                    case = Button(field, borderwidth=1, width=4, height=2, bg='white',                                  command=lambda i=i, ii=ii: self.poser_balles(i, ii))
                else:
                    case = Label(field, width=4, height=2, bg='white')
                case.grid(row=i, column=ii, padx=2, pady=2)
                row.append(case)
            self.buttons.append(row)

    def run(self):
        self.root.mainloop()


# Lancer le jeugame = Game()
game.run()
