def nombre_en_lettres(n):
    """Convertit un nombre en lettres (français)"""
    if not isinstance(n, int) or n < 0:
        return str(n)
        
    unite = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf']
    dizaine = ['', 'dix', 'vingt', 'trente', 'quarante', 'cinquante', 
              'soixante', 'soixante-dix', 'quatre-vingt', 'quatre-vingt-dix']
    exceptions = {
        0: 'zéro',
        11: 'onze',
        12: 'douze',
        13: 'treize',
        14: 'quatorze',
        15: 'quinze',
        16: 'seize',
        71: 'soixante-et-onze',
        72: 'soixante-douze',
        73: 'soixante-treize',
        74: 'soixante-quatorze',
        75: 'soixante-quinze',
        76: 'soixante-seize',
        80: 'quatre-vingts',
        81: 'quatre-vingt-un',
        91: 'quatre-vingt-onze',
        92: 'quatre-vingt-douze',
        93: 'quatre-vingt-treize',
        94: 'quatre-vingt-quatorze',
        95: 'quatre-vingt-quinze',
        96: 'quatre-vingt-seize'
    }
    
    if n in exceptions:
        return exceptions[n]
    
    if n < 100:
        if n < 10:
            return unite[n]
        elif 10 <= n < 20:
            return dizaine[n//10-1] + ('-'+unite[n%10] if n%10 else '')
        elif 20 <= n < 100:
            if n%10 == 1 and n//10 not in [7, 9]:
                return dizaine[n//10] + '-et-un'
            return dizaine[n//10] + ('-' + unite[n%10] if n%10 else '')
    elif n < 1000:
        centaines = n // 100
        reste = n % 100
        if centaines == 1:
            texte = 'cent'
        else:
            texte = unite[centaines] + ' cent'
        
        if reste == 0:
            return texte + ('s' if centaines > 1 else '')
        else:
            return texte + ' ' + nombre_en_lettres(reste)
    elif n < 1000000:
        mille = n // 1000
        reste = n % 1000
        if mille == 1:
            texte_mille = "mille"
        else:
            texte_mille = nombre_en_lettres(mille) + " mille"
        if reste == 0:
            return texte_mille
        else:
            return texte_mille + " " + nombre_en_lettres(reste)
    else:
        return str(n)