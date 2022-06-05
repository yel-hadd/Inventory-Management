import re

str = 'Python is a programming language'
#search using regex
x = re.search('language$', str)

if(x!=None):
	print('The line ends with \'language\'.')
else:
	print('The line does not end with \'language\'.')
 

def search_charge(self, month, year):
    charges = self.charges
    
    if month != '':
        reg = f'{month}-{year}$'
    else:
        reg = f'{year}$'
    
    _charges = {}
    _charges['Ref'] = {}
    _charges['montant'] = {}
    _charges['motif'] = {}
    _charges['date'] = {}
    
    ref = []
    motifs = []
    montants = []
    dates = []
    for user in charges.find():
        if re.search(reg, user['date']) != None:
            ref.append(user['Ref'])
            motifs.append(user['motif'])
            montants.append(user['montant'])
            dates.append(user['date'])
    
    for c, v in enumerate(ref):
        _charges['Ref'][c] = ref[c]
        _charges['motif'][c] = motifs[c]
        _charges['montant'][c] = montants[c]
        _charges['date'][c] = dates[c]
    
    return _charges
