import re
import os
import urllib



'''
 generate raw amr from isi amr release files
'''
def read(path, file_name, output):
    f = open(path + file_name)
    for line in f:
        m = re.search('#\s::id\s(\S+)', line)
        if m != None:
            sen_id = m.group(1)
            print sen_id
            output.write('# ::id %s\n' %sen_id)
            sen = re.search('#\s::snt\s(.+)', next(f)).group(1)
            output.write('%s\n' %sen)
            next(f)
            line = next(f)
            while line != '\n':
                # deal with '()' in wiki title
                m = re.search(':wiki\s\"(.+?)\"', line)
                if m != None:
                    line = line.replace(m.group(1),
                                        urllib.quote_plus(m.group(1)))
                # deal with '()' in :name
                m = re.search('\"(\w*\(\S+\)\w*)\"', line)
                if m != None:
                    line = line.replace(m.group(1),
                    urllib.quote_plus(m.group(1)))

                output.write(line)

                try:
                    line = next(f)
                except StopIteration:
                    print 'END OF FILE'
                    break
            output.write('\n')

'''
 generate plain docs from isi amr release files
'''
def generate_raw_docs(path, file_name):
    f = open(path + file_name)
    for line in f:
        m = re.search('#\s::id\s(\S+)', line)
        if m != None:
            sen_id = m.group(1)
            doc_id = sen_id[:sen_id.rfind('.')]
            try: os.mkdir('../output/raw_docs/')
            except OSError: pass
            out = open('../output/raw_docs/%s' % doc_id, 'aw')
            print sen_id
            sen = re.search('#\s::snt\s(.+)', next(f)).group(1)
            out.write('%s\t%s\n' % (sen_id, sen))
            next(f)
            line = next(f)
            while line != '\n':
                pass
                try:
                    line = next(f)
                except StopIteration:
                    print 'END OF FILE'
                    break


                
if __name__ == '__main__':
    path = '../doc/amr/Dec23/'
    file_list = os.listdir(path)
    # output = open('../output/test', 'w')
    output = open('../output/banked_amr', 'w')
    for i in file_list:
        # if i != 'amr-internal-release-guidelines.txt': continue
        read(path, i, output)
        # generate_raw_docs(path, i)
