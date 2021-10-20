from tkinter import *


def affichage_graphique(plateau, filename):
    fenetre = Tk()
    fenetre.resizable(False, False)
    t = 60
    largeur = t * plateau.dim[1]
    hauteur = t * plateau.dim[0]
    canvas = Canvas(fenetre, width=largeur, height=hauteur, background='#DFDFDF')
    for l in range(plateau.dim[0]):
        for c in range(plateau.dim[1]):
            coord = (c * t, l * t, ( c +1) * t, ( l +1) * t)
            v = plateau.tab[l][c]
            if v == -1:
                canvas.create_rectangle(coord)
            elif v in [0 ,1 ,2 ,3 ,4]:
                canvas.create_rectangle(coord, fill='black')
                canvas.create_text( t *(c + 1/ 2), t * (l + 1 / 2), font=('Arial', int(t * 0.40)), text=str(v),
                                   fill='white')
            elif v == 5:
                canvas.create_rectangle(coord, fill='black')
            elif v == 6:
                canvas.create_rectangle(coord, fill='yellow')
                canvas.create_oval(coord[0] + t / 4, coord[1] + t / 4, coord[2] - t / 4, coord[3] - t / 4, fill='white')
            elif v == 7:
                canvas.create_rectangle(coord, fill='yellow')
            canvas.pack()
    Button(fenetre, text="Quitter", command=fenetre.destroy).pack()
    canvas.update()
    canvas.postscript(file=filename, colormode='color')