from collections import defaultdict
from nltk.corpus import wordnet as wn

k = 0
for i in open('../data/frequent200_words_of_two_group_authors.txt', 'r'):
    if k == 0:
        ws_author0 = i[8:len(i) - 2].split(', ')
        ws_author0 = ''.join(ws_author0)
        ws_author0 = ws_author0[1:len(ws_author0) - 1].split("''")
    else:
        ws_author1 = i[8:len(i) - 2].split(', ')
        ws_author1 = ''.join(ws_author1)
        ws_author1 = ws_author1[1:len(ws_author1) - 1].split("''")
    k = k + 1

ss_author0 = ()
for w in ws_author0:
    for ss in wn.synsets(w):
        ss_author0 = ss_author0 + (ss,)
ss_author0 = set(ss_author0)

ss_author1 = ()
for w in ws_author1:
    for ss in wn.synsets(w):
        ss_author1 = ss_author1 + (ss,)
ss_author1 = set(ss_author1)

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

domains = set(getDomainsGivenSynsets(ss_author0))
print('\nDistinct domains:\n')
doms = ''
for d in domains:
    doms = doms + d + ' '
print(doms)

domains = set(getDomainsGivenSynsets(ss_author1))
print('\nDistinct domains:\n')
doms = ''
for d in domains:
    doms = doms + d + ' '
print(doms)
