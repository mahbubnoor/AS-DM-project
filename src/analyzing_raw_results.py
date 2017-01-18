import sys

def getDomains(raw_results_file_path):
    line = 0
    domains = ()
    for i in open(raw_results_file_path, 'r'):
        line = line + 1
        if -1 != i.find('Distinct domains:'):
            break
    line = line + 2
    l = 0
    for i in open(raw_results_file_path, 'r'):
        l = l + 1
        if l >= line:
            for domain in i.split(' '):
                if -1 != domain.find('\n'):
                    domain = domain[:len(domain) - 1]
                domains = domains + (domain,)
    return domains

if len(sys.argv) == 2:
    normal = getDomains('../results/' + sys.argv[1] + '_words_normal.txt')
    addictive = getDomains(
        '../results/frequent' + sys.argv[1] + '_words_addictive.txt')

    print(sys.argv[1] + ': Common domains:')
    common = [d for d in addictive if d in normal]
    res = ''
    for c in common:
        res = res + c + ' '
    print('\n' + res)

    print('\n' + sys.argv[1] + ': Domains unique to normal:')
    normal_unique = [d for d in normal if d not in addictive]
    res = ''
    for n_u in normal_unique:
        res = res + n_u + ' '
    print('\n' + res)

    print('\n' + sys.argv[1] + ': Domains unique to addictive:')
    addictive_unique = [d for d in addictive if d not in normal]
    res = ''
    for a_u in addictive_unique:
        res = res + a_u + ' '
    print('\n' + res)
else:
    print('\nusage: py analyzing_raw_results.py 2500|5000|10000|20000|40000')
