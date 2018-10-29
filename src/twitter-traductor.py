import re
import csv
import os

ruta = os.path.dirname(__file__)
with open(ruta + '/entradas/twitter-muestra-01min.csv', 'rU') as lineas:
        index = 1
        for row in csv.reader(lineas, delimiter=','):
            print 'I-' + str(index) +": " + row[0] #row[<index>]
            s1 = re.sub(' +',' ',row[0]) # deja un solo blanco entre cada palabra
            # Acentos
            s1 = re.sub('\xed\xe7',"'a",s1)
            s1 = re.sub('\xed\xa9',"'e",s1)
            s1 = re.sub('\xed_',"'i",s1)
            s1 = re.sub('\xed\xa9',"'a",s1)
            s1 = re.sub('\xed\xa9',"'a",s1)
            s1 = re.sub('\xed\xb1',"'n",s1)
            
            # Repeticiones
            s1 = re.sub('a+','a',s1)
            s1 = re.sub('e{3,}','e',s1)
            s1 = re.sub('i+','i',s1)
            s1 = re.sub('o+','o',s1)
            s1 = re.sub('u+','u',s1)
            s1 = re.sub('y+','y',s1)
            s1 = re.sub('r{3,}','r',s1)
            s1 = re.sub('l{3,}','l',s1)
            s1 = re.sub('s+','s',s1)
            s1 = re.sub('n+','n',s1)
            s1 = re.sub('h+','h',s1)
            s1 = re.sub('A+','A',s1)
            s1 = re.sub('E{3,}','E',s1)
            s1 = re.sub('I+','I',s1)
            s1 = re.sub('O+','O',s1)
            s1 = re.sub('U+','U',s1)
            s1 = re.sub('R{3,}','R',s1)
            s1 = re.sub('L{3,}','l',s1)
            s1 = re.sub('Y+','Y',s1)
            s1 = re.sub('S+','S',s1)
            s1 = re.sub('N+','N',s1)
            s1 = re.sub('HH+','HH',s1)
            s1 = re.sub('hh+','hh',s1)
            s1 = re.sub('(si)+','si',s1)
            s1 = re.sub('ja(ja)+','<alegria>',s1)
            s1 = re.sub('ha(ha)+','<alegria>',s1)
            s1 = re.sub('je(je)+','<alegria>',s1)
            s1 = re.sub('ji(ji)+','<alegria>',s1)
            s1 = re.sub('www\.','w3.',s1)
            s1 = re.sub('WWW\.','W3.',s1)
            s1 = re.sub('WWW\b','W3',s1)
            s1 = re.sub('ww+','w',s1)
            s1 = re.sub('WW+','W',s1)
            s1 = re.sub('w3\.','www.',s1)
            s1 = re.sub('WWW\.','W3.',s1)
            s1 = re.sub('!+','!',s1)
            s1 = re.sub('\?+','?',s1)
            s1 = re.sub(' \+ '," m'as ",s1)
            s1 = re.sub(' \+$'," m'as ",s1)
            
            # Reglas
            reglas = open(ruta + '/datos/Reglas-traduccion2.csv','rU')
            for regla in csv.reader(reglas):
                s1 = re.sub(regla[0],regla[1],s1)
            print "F-" + str(index) +": " + s1
            index = index + 1
            print
        

lineas.closed
reglas.closed      
