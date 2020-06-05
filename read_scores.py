def read_scores():
    """
    Renvoie une liste avec les trois meilleurs scores et le score produit par le joueur sur sa dernière partie

    Parametres:
    ----------
    Aucun

    Renvoi:
    -------
    D : list

    """
    try:
        f = open('scores.txt', 'r')
    except:
        return ['    Aucun record']
    L = f.read().splitlines()
    f.close()

    S = []
    for i in range(len(L)//2):
        S.append((int(L[2*i]), int(L[2*i+1])))
    if len(S) == 0:
        return ['    Aucun record']

    current_score = S[-1]
    S.sort(reverse=True)

    if len(S) >= 3:
        S = S[:3]
    else:
        while len(S) < 3:
            S.append((0, 0))

    D = ['***Meileurs scores***']
    for s in S:
        D.append('Etage : ' + str(s[0]) + ' - XP : ' + str(s[1]))
    D.append('')
    D.append('  ***Ton score***')
    D.append('Etage : ' + str(current_score[0]) + ' - XP : ' + str(current_score[1]))
    if current_score == S[0]:
        D.append('    New record !')
    return D
