'''
 Wrap raw AMR
'''

import re
import os
import urllib

'''
 Input:  raw AMR from ISI AMR release file
         type: str
 Output: convert '( )' to '%28 %29'
         remove unnecessary information
         type: str
'''
def wrap(raw_amr):
    raw_amr = raw_amr.split('\n')
    output = list()
    for line in raw_amr:
        ### file title
        if re.match('# AMR release .+', line) != None:
            continue
        ### save-date
        if re.match('# ::save-date .+', line) != None:
            continue
        ### lpp Chinese translation
        if re.match('# ::zh .+', line) != None:
            continue

        ### convert '( )' to '%28 %29' in wiki title
        m = re.search(':wiki\s\"(.+?)\"', line)
        if m != None:
            line = line.replace(m.group(1),
                                urllib.quote_plus(m.group(1)))
        ### convert '( )' to '%28 %29' in :name
        m = re.findall('\"(\S+)\"', line)
        for i in m:
            if '(' in i or ')' in i:
                line = line.replace(i, urllib.quote_plus(i))

        output.append(line)
    return '\n'.join(output)



# '''
#  Input: raw AMR from ISI AMR release files
#  Output:
#         # ::id
#         # ::snt
#         ( ...
#              AMR
#                 ... )
# '''
# def read(path, file_name, output):
#     f = open(path + file_name)
#     for line in f:
#         m = re.search('#\s::id\s(\S+)', line)
#         if m != None:
#             senid = m.group(1)
#             # print senid
#             output.append('# ::id %s\n' % senid)
#             sen = re.search('#\s::snt\s(.+)', next(f)).group(1)
#             output.append('# ::snt %s\n' % sen)
#             next(f)
#             line = next(f)
#             while line != '\n':
#                 ### convert '( )' to '%28 %29' in wiki title
#                 m = re.search(':wiki\s\"(.+?)\"', line)
#                 if m != None:
#                     line = line.replace(m.group(1),
#                                         urllib.quote_plus(m.group(1)))
#                 ### convert '( )' to '%28 %29' in :name
#                 m = re.search('\"(\w*\(\S+\)\w*)\"', line)
#                 if m != None:
#                     line = line.replace(m.group(1),
#                     urllib.quote_plus(m.group(1)))
#                 output.append(line)

#                 try:
#                     line = next(f)
#                 except StopIteration:
#                     print 'END OF FILE: %s' % file_name
#                     break
#             output.append('\n')

# '''
#  Input: raw AMR from ISI AMR release files
#  Output: keep everthing
#          only convert '( )' to '%28 %29'
# '''
# def read_all(path, file_name, output):
#     f = open(path + file_name)
#     for line in f:
#         ### file title
#         if re.match('# AMR release .+', line) != None:
#             continue
#         ### lpp Chinese translation
#         if re.match('# ::zh .+', line) != None:
#             continue

#         ### convert '( )' to '%28 %29' in wiki title
#         m = re.search(':wiki\s\"(.+?)\"', line)
#         if m != None:
#             line = line.replace(m.group(1),
#                                 urllib.quote_plus(m.group(1)))
#         ### convert '( )' to '%28 %29' in :name
#         m = re.findall('\"(\S+)\"', line)
#         for i in m:
#             if '(' in i or ')' in i:
#                 line = line.replace(i, urllib.quote_plus(i))
#         output.append(line)
#     print 'END OF FILE: %s' % file_name

# '''
#  Input: raw AMR from ISI AMR release files
#  Output: plain docs
# '''
# def generate_raw_docs(path, file_name, output_path):
#     output_path += 'raw_docs/'
#     try: os.mkdir(output_path)
#     except OSError: pass

#     f = open(path + file_name)
#     for line in f:
#         m = re.search('#\s::id\s(\S+)', line)
#         if m != None:
#             senid = m.group(1)
#             docid = senid[:senid.rfind('.')]

#             out = open(output_path + docid, 'aw')
#             print senid
#             sen = re.search('#\s::snt\s(.+)', next(f)).group(1)
#             out.write('%s\t%s\n' % (senid, sen))
#             next(f)
#             line = next(f)
#             while line != '\n':
#                 pass
#                 try:
#                     line = next(f)
#                 except StopIteration:
#                     print 'END OF FILE %s' % file_name
#                     break
