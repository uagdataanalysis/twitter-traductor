import re
import csv
import os

ruta = os.path.dirname(__file__)          
c = csv.writer(open(ruta + '/entradas/twitter_muestra_01min.csv', 'wb'))          
with open(ruta + '/entradas/sentiment_spanish.csv', 'rU') as lineas:
        index = 1
        for row in csv.reader(lineas, delimiter=','):
            # print "I-" + str(index) +": " + row[0] #row[<index>]
            s1 = re.sub(' +',' ',row[0]) # deja un solo blanco entre cada palabra
            
            # Repeticiones
            s1 = re.sub('a+','a',s1)
            s1 = re.sub('e{3,}','e',s1)
            s1 = re.sub('i+','i',s1)
            s1 = re.sub('o{3,}','o',s1)
            s1 = re.sub('u+','u',s1)
            s1 = re.sub('y+','y',s1)
            s1 = re.sub('[Jj]+','j',s1)
            s1 = re.sub('r{3,}','r',s1)
            s1 = re.sub('l{3,}','l',s1)
            s1 = re.sub('s{3,}','s',s1)
            s1 = re.sub('n+','n',s1)
            s1 = re.sub('h+','h',s1)
            s1 = re.sub('R{3,}','R',s1)
            s1 = re.sub('L{3,}','l',s1)
            s1 = re.sub('Y+','Y',s1)
            s1 = re.sub('S{3,}','S',s1)
            s1 = re.sub('N{3,}','N',s1)
            s1 = re.sub('HH+','HH',s1)
            s1 = re.sub('hh+','hh',s1)
            s1 = re.sub('(si)+','si',s1)
            s1 = re.sub('[Jj]a(ja)+\w*','<risa>',s1)
            s1 = re.sub('[Hh]a(ha)+\w*','<risa>',s1)
            s1 = re.sub('[Jj]e(je)+\w*','<risa>',s1)
            s1 = re.sub('[Jj]o(jo)+\w*','<risa>',s1)
            s1 = re.sub('[Jj]i(ji)+\w*','<risa>',s1)
            s1 = re.sub('[Jj]u(ju)+\w*','<risa>',s1)
            s1 = re.sub('www\.','w3.',s1)
            s1 = re.sub('WWW\.','W3.',s1)
            s1 = re.sub('WWW\b','W3',s1)
            s1 = re.sub('ww+','w',s1)
            s1 = re.sub('WW+','W',s1)
            s1 = re.sub('://','&2&',s1)
            s1 = re.sub('w3\.','www.',s1)
            s1 = re.sub('WWW\.','W3.',s1)
            s1 = re.sub('!+','!',s1)
            s1 = re.sub('\?+','?',s1)
            s1 = re.sub(' \+[\b\s] '," m'as ",s1)
            
            # Reglas
            reglas = open(ruta + '/datos/Reglas-traduccion2mej.csv','rU')
            for regla in csv.reader(reglas):
                s1 = re.sub(regla[0]," "+regla[1]+" ",s1)
            s1 = re.sub(' +',' ',s1) # deja un solo blanco entre cada palabra
            s1 = re.sub('&2&','://',s1)
            # print "F-" + str(index) +": " + s1
            row[0]=s1
            c.writerow(row)
            index = index + 1
            # print
        
lineas.closed
reglas.closed      
