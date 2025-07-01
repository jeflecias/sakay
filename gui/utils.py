# nilipat ko dito para hindi mag importerror
def cursor_hovering(e):
    e.widget['background'] = '#e2eb3d'  # shiny effect
    e.widget['fg'] = 'black'
    e.widget['relief'] = 'raised'
    e.widget['bd'] = '3'

def cursor_not_hovering(e):
    e.widget['bg'] = '#D2B48C' #default na itsura nong button
    e.widget['fg'] = '#643602'
    e.widget['relief'] = 'flat'
    e.widget['bd'] = '1'