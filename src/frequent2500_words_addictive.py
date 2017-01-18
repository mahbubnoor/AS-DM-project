from collections import defaultdict
from nltk.corpus import wordnet as wn

for i in open('../data/frequent2500_words_addictive.txt', 'r'):
    ws_author = i.split(' ')

ss_author = ()
for w in ws_author:
    for ss in wn.synsets(w):
        ss_author = ss_author + (ss,)
ss_author = set(ss_author)

# Loading the Wordnet domains.
domain2synsets = defaultdict(list)
synset2domains = defaultdict(list)
for i in open('../docs/wn-domains-3.2/wn-domains-3.2-20070223', 'r'):
    ssid, doms = i.strip().split('\t')
    doms = doms.split()
    synset2domains[ssid] = doms
    for d in doms:
        domain2synsets[d].append(ssid)

def getDomainsGivenSynsets(synsets):
    domains = ()
    print(str(len(synsets)) + ' synsets\n\nDomains found:\n')
    for ss in synsets:
        ssid = str(ss.offset()).zfill(8) + "-" + ss.pos()
        if synset2domains[ssid]: # not all synsets are in WordNet Domain.
            doms = ''
            for s2d in synset2domains[ssid]:
                domains = domains + (s2d,)
                doms = doms + s2d + ' '
            print('(' + ssid + ')\t' + str(ss) + '\t', doms)
    return domains

domains = set(getDomainsGivenSynsets(ss_author))
print('\nDistinct domains:\n')
doms = ''
for d in domains:
    doms = doms + d + ' '
print(doms)
