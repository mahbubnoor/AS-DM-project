import sys
from collections import defaultdict
from nltk.corpus import wordnet as wn

def getDomains(first_analysis_results_file_path):
    should_line_increment = True
    line = 0
    line2 = 0
    n_domains = ()
    for i in open(first_analysis_results_file_path, 'r'):
        line2 = line2 + 1
        if should_line_increment == True:
            line = line + 1
        if -1 != i.find(': Domains unique to normal:'):
            should_line_increment = False
        if -1 != i.find(': Domains unique to addictive:'):
            break
    line = line + 2
    line2 = line2 - 2
    l = 0
    for i in open(first_analysis_results_file_path, 'r'):
        l = l + 1
        if l >= line and l <= line2:
            for domain in i.split(' '):
                if -1 != domain.find('\n'):
                    domain = domain[:len(domain) - 1]
                n_domains = n_domains + (domain,)

    line = 0
    a_domains = ()
    for i in open(first_analysis_results_file_path, 'r'):
        line = line + 1
        if -1 != i.find(': Domains unique to addictive:'):
            break
    line = line + 2
    l = 0
    for i in open(first_analysis_results_file_path, 'r'):
        l = l + 1
        if l >= line:
            for domain in i.split(' '):
                if -1 != domain.find('\n'):
                    domain = domain[:len(domain) - 1]
                a_domains = a_domains + (domain,)
    return (n_domains, a_domains)

if len(sys.argv) == 2:
    domains = getDomains('../results/' + sys.argv[1] + '_stats.txt')

    n_d_synsets = ()
    for d in domains[0]:
        for ss in wn.synsets(d):
            n_d_synsets = n_d_synsets + (ss,)
    n_d_synsets = set(n_d_synsets)

    a_d_synsets = ()
    for d in domains[1]:
        for ss in wn.synsets(d):
            a_d_synsets = a_d_synsets + (ss,)
    a_d_synsets = set(a_d_synsets)

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

    n_d_domains = set(getDomainsGivenSynsets(n_d_synsets))
    a_d_domains = set(getDomainsGivenSynsets(a_d_synsets))

    print(n_d_domains)
    print(a_d_domains)
else:
    print('\nusage: py second_analysis.py 2500|5000|10000|20000|40000')
