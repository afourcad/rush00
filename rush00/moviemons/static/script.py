with open('player_position.css', 'w') as css:
    x = range(0, 10)
    for i in x:
        y = range(0, 10)
        for j in y:
            css.write('.player[data-x="'+ str(i) + '"][data-y="' + str(j) + '"]{\n')
            css.write('     left: ' + str(i * 10) + '%;\n')
            css.write('     top: ' + str(j * 10) + '%;\n')
            css.write('}\n\n')