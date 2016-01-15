'Linkipedia system'
import json
import urllib
import urllib2
import re
import string

def find_json(query):
    # Linkipedia does't support non-ascii
    query = filter(lambda x: x in string.printable, query)
    query = query.replace('"', '')
    query = query.replace(',', '')
    query = urllib.quote_plus(query)
    url = 'http://blender05.cs.rpi.edu:3301/linking?query=%s'
    url = url % query
    request = urllib2.Request(url)
    result = urllib2.urlopen(request).read()
    return result

def find_candidates(json_input, score=False, raw=False):
    candidates = list()
    try:
        result = json.loads(json_input)
    except ValueError:
        print 'Unexpected input.'
        return list()
    for i in result['results']:
        for j in i['annotations']:
            if j['url'] != 'NIL':
                if raw:
                    candidate = j['url'].encode('utf-8')
                else:
                    dburl = '\<http\:\/\/dbpedia\.org\/resource\/(.+)\>'
                    try:
                        candidate = re.search(dburl, j['url']).group(1)
                        candidate = candidate.encode('utf-8')
                    except:
                        candidate = j['url'].encode('utf-8')
                if score == True:
                    candidates.append((candidate, float(j['score'])))
                else:
                    candidates.append(candidate)
    return candidates

def linking(query, score=False, raw=False):
    candidates = find_candidates(find_json(query), score)
    return candidates

if __name__ == '__main__':
    for i in linking('carashnikov'):
        print i
