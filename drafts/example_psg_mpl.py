# To be honest, I have no idea how this works, here is the source code:
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Embedded_Toolbar.py


import PySimpleGUI as sg

from AI_intro_project.State import State

"""
    Embedding the Matplotlib toolbar into your application
"""

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


# ------------------------------- PySimpleGUI CODE
col1 = [[
    sg.B('Initialize 4x4'),
    sg.B('Initialize 4x4 & Play 10 moves'),
    sg.B('4x4 Best solution'),
    sg.B('Exit'),
]]
col2 = [
    [
        sg.B('▲', key='U')],
    [
        sg.B('◄', key='L'), 
        sg.B('⟲', key='undo'),
        sg.B('►', key='R')],
    [
        sg.B('▼', key='D')],
]
layout = [
    [sg.Column(col1),
        sg.VerticalSeparator(),
        sg.Column(col2, element_justification='center')],
    [sg.Canvas(key='controls_cv')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(630, 630)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],

]

window = sg.Window('The Penniless Pilgrim Riddle | https://github.com/htnminh/AI-intro-project', layout)



while True:
    event, values = window.read()
    # print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break

    elif event == 'Initialize 4x4':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.plt_preparation()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
    
    elif event == 'Initialize 4x4 & Play 10 moves':
        # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
        plt.clf() 

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.random_play(number_of_moves=10, silent=True)
        s.plt_preparation()

        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
    
    elif event == '4x4 Best solution':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        for _ in range(3):
            s.move_to_direction('D')
        for _ in range(2):
            s.move_to_direction('R')
        for _ in range(3):
            s.move_to_direction('U')
        s.move_to_direction('L')
        s.move_to_direction('D')
        for _ in range(3):
            s.move_to_direction('L')
        for _ in range(3):
            s.move_to_direction('D')
        for _ in range(4):
            s.move_to_direction('R')
        

        s.plt_preparation()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event in ('L', 'R', 'U', 'D'):
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))
        
        # check if s is defined
        assert 's' in locals(), \
                    'THE GAME DOES NOT EXIST, INITIALIZE FIRST'
        s.move_to_direction(event[0])
        s.plt_preparation()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    elif event == 'undo':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))
        
        # check if s is defined
        assert 's' in locals(), \
                    'THE GAME DOES NOT EXIST, INITIALIZE FIRST'
        s.undo_last_move()
        s.plt_preparation()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

window.close()
