#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import csv
import nltk
import collections
import os

acentos_regex = re.compile(r"('[aeiou]|\"u|'n)")
recupera_acento = re.compile(r'[AEIOUNW]')
suspensivos_duda_remarcado_regex = re.compile(
                    r'\.\.+|'# puntos suspensivos
                    r'\?+|' # duda
                    r'\?_\?|'
                    r'\!+' # remarcado
                )

molestia_regex = re.compile(
                    r'\s+:@\s*|'
                    r'\bfail\b',
                    re.IGNORECASE
                 )

tristeza_regex = re.compile(
                    r"\s+:'\(+\s*|"
                    r'\s+:\(+\s*|'
                    r'\s+:\s?\/\s*|'
                    r'\s+:c\s*|'
                    r'\s+=\(\s*|'
                    r'\s+\=\s*|'
                    r'\s+-[_\.]-\s*|'
                    r'\s+u[_\.]u\s+|'
                    r'\s+--\s*',
                    re.IGNORECASE
                 )

alegria_regex = re.compile(
                    r'\s*:-?\)+\s*|'
                    r'\s*;\)\s*|'
                    r'\s*\*-\*\s*|'
                    r'\s*:b\s*|'
                    r'\s*c:\s*|'
                    r'\s*:d+\s*|'
                    r'\s*=\)\s*\|'
                    r'\s*<;3\s*|'
                    r'\s*&lt;3\s*|'
                    r'\byay\b',
                    re.IGNORECASE
                )

sorpresa_regex = re.compile(
                    r'\s*:O\s*|'
                    r'\s*d:\*',
                    re.IGNORECASE
                 )

disgusto_regex = re.compile(
                    r'\s*:p\s*',
                    re.IGNORECASE
                 )

poco_disgusto_regex = re.compile(
                        r'\s*:s+\s*',
                        re.IGNORECASE
                      )

insulto_regex = re.compile(
                    r'\s*\.[l\|]\.\s*|'
                    r'\s+o.o\s*|'
                    r'\bfuck\b|'
                    r'\bchinguen\b|'
                    r'odio jarocho\s*',
                    re.IGNORECASE
                )

admiracion_regex = re.compile(
                    r'\^\^'
                   )

pensando_regex = re.compile(
                    r'\s*:\|\s*'
                 )

coma_regex = re.compile(
                r', '
             )

ironia_regex = re.compile(
                r'\!+\?+'
               )

mas_regex = re.compile(
                r'\+'
            )
def reemplaza_acentos(m):
    mapper = {"'a": 'A', "'e": 'E', "'i": 'I', "'o": 'O', "'u": 'U', '"u': 'W', "'n": 'N'}
    return mapper[m.group(0)]

def recupera_acentos(m):
    mapper = {'A': "'a", 'E': "'e", 'I': "'i", 'O': "'o", 'U': "'u", 'W': '"u', 'N': "'n"}
    return mapper[m.group(0)]

def reemplaza_suspensivos_duda_remarcado_2ps(m):
    mapper = {'.': ' <puntos_suspensivos> ', '?': ' <duda> ', '!': ' <remarcando> ', ':': ' <dos_puntos>'}
    return mapper[m.group(0)[0]]

def remplaza_caritas(s):
    s = suspensivos_duda_remarcado_regex.sub(
            reemplaza_suspensivos_duda_remarcado_2ps,
            s
        )
    s = molestia_regex.sub(' <molestia> ', s)
    s = tristeza_regex.sub(' <tristeza> ', s)
    s = alegria_regex.sub(' <alegria> ', s)
    s = sorpresa_regex.sub(' <sorpresa>', s)
    s = disgusto_regex.sub(' <disgusto> ', s)
    s = poco_disgusto_regex.sub(' <poco_disgusto> ', s)
    s = insulto_regex.sub(' <insulto> ', s)
    s = admiracion_regex.sub(' <admiracion> ', s)
    s = pensando_regex.sub(' <pensando> ', s)
    s = coma_regex.sub(' <coma> ', s)
    s = ironia_regex.sub(' <ironia> ', s)
    s = mas_regex.sub('mAs', s)

#    s = re.sub(":P ",' <disgusto> ',s) no creo que sea disgusto
#    s = re.sub(":P$",' <disgusto> ',s)
#    s = re.sub("\-\_\-",' <tristeza> ',s) no creo que sea tristeza
#    s = re.sub("\-\.\-",' <tristeza> ',s)
#    s = re.sub("\:[Pp]\s",' <molestia> ',s) no creo que sea molestia
#    s = re.sub("\:[Pp]$",' <molestia> ',s)
#    s = re.sub("\su\.u ",' <tristeza> ',s) no creo que sea tristeza
#    s = re.sub("\su\.u$",' <tristeza>',s)
#    s = re.sub("\su\_u ",' <tristeza> ',s)
#    s = re.sub("\su\_u$",' <tristeza> ',s)
#    s = re.sub("\s--'$",' <tristeza> ',s)
#    s = re.sub(" D: ",' <sorpresa> ',s) no creo que sea sorpresa
#    s = re.sub("^D: ",' <sorpresa> ',s)
#    s = re.sub("D:$",' <sorpresa> ',s)

    return s

def remplaza_repeticiones(s):
    s = re.sub('AAAA+H+',' <queja> ',s)
    s = re.sub('aaaa+H+',' <queja> ',s)
    s = re.sub('aa+y+',' <queja> ',s)
    s = re.sub('AAAA+ ',' <queja> ',s)
    s = re.sub('aaaa+ ',' <queja> ',s)
    s = re.sub('AAAA+','A',s)
    s = re.sub('aaaa+','a',s)
    s = re.sub('a+','a',s)
    s = re.sub("\Aah!?\s",' <queja> ',s)
    s = re.sub("\sah!?\s",' <queja> ',s)
    s = re.sub("\Awau!\s",' <asombro> ',s)
    s = re.sub("\swau!\s",' <asombro> ',s)
    s = re.sub("\Awau\s",' <asombro> ',s)
    s = re.sub("\swau\s",' <asombro> ',s)
    s = re.sub('ah+s+ ',' <queja> ',s)
    s = re.sub('ah+s+$',' <queja> ',s)
    s = re.sub('as+h+ ',' <queja> ',s)
    s = re.sub('as+h+$',' <queja> ',s)
    s = re.sub('ah+!? ',' <queja> ',s)
    s = re.sub('ah+!?$',' <queja> ',s)
    s = re.sub('ag+h+ ',' <queja> ',s)
    s = re.sub('ag+h+$',' <queja> ',s)
    s = re.sub('\Ayay\s',' <alegria> ',s)
    s = re.sub('\syay\s',' <alegria> ',s)
    s = re.sub('\syay$',' <alegria> ',s)
    s = re.sub('pppp+','p',s)
    s = re.sub('ug+h+\s',' <queja> ',s)
    s = re.sub('ug+h+$',' <queja> ',s)
    s = re.sub('e{3,}','e',s)
    s = re.sub('EEEE+','E',s)
    s = re.sub('eeee+','e',s)
    s = re.sub('i+','i',s)
    s = re.sub('IIII+','I',s)
    s = re.sub('iiii+','i',s)
    s = re.sub('o{3,}','o',s)
    s = re.sub('OOO+','O',s)
    s = re.sub('ooo+','o',s)
    s = re.sub('u+','u',s)
    s = re.sub('UUU+','U',s)
    s = re.sub('uuu+','u',s)
    s = re.sub('\Ammm+\s',' <pensando> ',s)
    s = re.sub('\smmm+\s',' <pensando> ',s)
    s = re.sub('m{4,}','m',s)
    s = re.sub('y+','y',s)
    s = re.sub('[Jj]+','j',s)
    s = re.sub('r{3,}','r',s)
    s = re.sub('l{3,}','l',s)
    s = re.sub('s{3,}','s',s)
    s = re.sub('1ro.?','primero',s)
    s = re.sub('2do.?','segundo',s)
    s = re.sub('3ro.?','tercero',s)
    s = re.sub('4to.?','cuarto',s)
    s = re.sub('5to.?','quinto',s)
    s = re.sub('6to.?','sexto',s)
    s = re.sub('8vo.?','octavo',s)
    s = re.sub('n+','n',s)
    s = re.sub('h+','h',s)
    s = re.sub('R{3,}','R',s)
    s = re.sub('r{3,}','r',s)
    s = re.sub('L{3,}','L',s)
    s = re.sub('l{3,}','l',s)
    s = re.sub('Y+','Y',s)
    s = re.sub('y+','y',s)
    s = re.sub('S{3,}','S',s)
    s = re.sub('s{3,}','s',s)
    s = re.sub('N{3,}','N',s)
    s = re.sub('n{3,}','n',s)
    s = re.sub('HH+','HH',s)
    s = re.sub('hh+','hh',s)
    s = re.sub('(si)+','si',s)
    s = re.sub('[Jj]a(ja)+\w*',' <risa> ',s)
    s = re.sub('[Hh]a(ha)+\w*',' <risa> ',s)
    s = re.sub('[Jj]e(je)+\w*',' <risa> ',s)
    s = re.sub('[Jj]o(jo)+\w*',' <risa> ',s)
    s = re.sub('[Jj]i(ji)+\w*',' <risa> ',s)
    s = re.sub('[Jj]u(ju)+\w*',' <risa> ',s)
    s = re.sub('\Alol\s',' <risa> ',s)
    s = re.sub('\slol\s',' <risa> ',s)
    s = re.sub('www\.','w3.',s) # disfraza el wwww.
    s = re.sub('WWW\.','W3.',s) # disfraza el WWWW.
    s = re.sub('WWW\s','W3',s) # disfraza el wwww.
    s = re.sub('ww+','w',s)
    s = re.sub('WW+','W',s)
    s = re.sub('://','&2&',s) # disfraza el ://
    s = re.sub('w3\.','www.',s) # regresa el wwww.
    s = re.sub('WWW\.','W3.',s) # regresa el WWWW.
    s = re.sub('\('," <par_izq> ",s)
    s = re.sub('\)'," <par_der> ",s)
    return s

def remplaza_contracciones(s):
    s = re.sub("\b[Pp]/ ?k\b",'para que ',s)
    s = re.sub("\b[Bb]n\b",'bien ',s)
    s = re.sub("\b[Bb]b\b",'black_berry ',s)
    s = re.sub("\b[Bb]uska\b",'busca ',s)
    s = re.sub("\A[Dd]\s",'de ',s)
    s = re.sub("\s[Dd]\s",' de ',s)
    s = re.sub("\A[Dd]ike\s",'dice ',s)
    s = re.sub("\s[Dd]ike\s",' dice ',s)
    s = re.sub("\A[Dd]nde\s",'donde ',s)
    s = re.sub("\s[Dd]nde\s",' donde ',s)
    s = re.sub("\A[Ee]zperare\s","esperarE ",s)
    s = re.sub("\s[Ee]zperare\s"," esperarE ",s)
    s = re.sub("\sfb\s",' facebook ',s)
    s = re.sub("\A[Gg]oor\s",'gordo ',s)
    s = re.sub("\s[Gg]oor\s",' gordo ',s)
    s = re.sub("\A[Hh]oygan\s",'oigan ',s)
    s = re.sub("\s[Hh]oygan\s",' oigan ',s)
    s = re.sub("\A[Hh]y\s",'hoy ',s)
    s = re.sub("\s[Hh]y\s",' hoy ',s)
    s = re.sub("\A[Oo]h sorpresa\s",' <sorpresa> ',s)
    s = re.sub("\s[Oo]h sorpresa\s",' <sorpresa> ',s)
    s = re.sub("\A[Oo]h\s",'  <sorpresa> ',s)
    s = re.sub("\s[Oo]h\s",' <sorpresa> ',s)
    s = re.sub("\A[Jj]a\s",' <risa> ',s)
    s = re.sub("\A[Kk]sa",'casa',s)
    s = re.sub("\s[Jj]a\s",' <risa> ',s)
    s = re.sub("\Art\s",' <retwitter> ',s)
    s = re.sub("\srt\s",' <retwitter> ',s)
    s = re.sub("\Art$",' <retwitter> ',s)
    s = re.sub("\srt$",' <retwitter> ',s)
    s = re.sub("\A[Kk]e\s",'que ',s)
    s = re.sub("\s[Kk]e\s",' que ',s)
    s = re.sub("\A[Kk]ie",'quie',s)
    s = re.sub("\s[Kk]ie",' quie',s)
    s = re.sub("\A[Oo]ign\s",'oigan ',s)
    s = re.sub("\s[Oo]ign\s",' oigan ',s)
    s = re.sub("\A[Oo]la\s",'hola ',s)
    s = re.sub("\s[Oo]la\s",' hola ',s)
    s = re.sub("\A[Pp]q\s","por quE ",s)
    s = re.sub("\s[Pp]q\s"," por quE ",s)
    s = re.sub("\A[Qq]\s",'que ',s)
    s = re.sub("\s[Qq]\s",' que ',s)
    s = re.sub("\A[Tt]a\s",' <afecto> ',s)
    s = re.sub("\s[Tt]a\s",' <afecto> ',s)
    s = re.sub("\A[Tt]qm\s",'te quiero mucho ',s)
    s = re.sub("\s[Tt]qm\s",' te quiero mucho ',s)
    s = re.sub("\A[Xx] fas\s",'por favor ',s)
    s = re.sub("\s[Xx] fas\s",' por favor ',s)
    s = re.sub("\A[Pp]orfas?\s",'por favor ',s)
    s = re.sub("\s[Pp]orfas?\s",' por favor ',s)
    s = re.sub("\A[Pp]orfis\s",'por favor ',s)
    s = re.sub("\s[Pp]orfis\s",' por favor ',s)
    s = re.sub("\A[Pp]orfis$",'por favor ',s)
    s = re.sub("\s[Pp]orfis$",' por favor ',s)
    s = re.sub("\A[Pp]orfitas\s",'por favor ',s)
    s = re.sub("\s[Pp]orfitas\s",' por favor ',s)
    s = re.sub("\A[Pp]orfitas$",'por favor ',s)
    s = re.sub("\s[Pp]orfitas$",' por favor ',s)
    s = re.sub("\A[Kk]re",'cre',s)
    s = re.sub("\s[Kk]re",' cre',s)
    s = re.sub("\Aase\s",'hace ',s)
    s = re.sub("\sase\s",' hace ',s)
    s = re.sub("\Aaser\s",'hace ',s)
    s = re.sub("\saser\s",' hace ',s)
    s = re.sub("\Aazta\s",'hasta ',s)
    s = re.sub("\sazta\s",' hasta ',s)
    s = re.sub("\Ablackberry\s",'black_berry ',s)
    s = re.sub("\sblackberry\s",' black_berry ',s)
    s = re.sub("\Ac\s",'se ',s)
    s = re.sub("\sc\s",' se ',s)
    s = re.sub("\Acdt\s","cuIdate ",s)
    s = re.sub("\scdt\s"," cuIdate ",s)
    s = re.sub("\Acel\s",'celular ',s)
    s = re.sub("\scel\s",' celular ',s)
    s = re.sub("\Acel\s",'celular ',s)
    s = re.sub("\scel\s",' celular ',s)
    s = re.sub("\Acelu\s",'celular ',s)
    s = re.sub("\scelu\s",' celular ',s)
    s = re.sub("\Achambeo\s",'trabajo ',s)
    s = re.sub("\schambeo\s",' trabajo ',s)
    s = re.sub("\Achelas\s",'cervezas ',s)
    s = re.sub("\schelas\s",' cervezas ',s)
    s = re.sub("\Achelita\s",'cerveza ',s)
    s = re.sub("\schelita\s",' cerveza ',s)
    s = re.sub("\Acheves\s",'cervezas ',s)
    s = re.sub("\scheves\s",' cervezas ',s)
    s = re.sub("\Achikita\s",'chiquita ',s)
    s = re.sub("\schikita\s",' chiquita ',s)
    s = re.sub("\Achulis\s",'linda ',s)
    s = re.sub("\schulis\s",' linda ',s)
    s = re.sub("\Acred\s","crEdito ",s)
    s = re.sub("\scred\s"," crEdito ",s)
    s = re.sub("\scred$"," crEdito",s)
    s = re.sub("\Acl\s",'cliente ',s)
    s = re.sub("\scl\s",' cliente ',s)
    s = re.sub("\Aclient\s",'cliente ',s)
    s = re.sub("\sclient\s",' cliente ',s)
    s = re.sub("\Acn\s",'con ',s)
    s = re.sub("\scn\s",' con ',s)
    s = re.sub("\Acomidita\s",'comida ',s)
    s = re.sub("\scomidita\s",' comida ',s)
    s = re.sub("\Acsada\s",'casada ',s)
    s = re.sub("\scsada\s",' casada ',s)
    s = re.sub("\A[Dd]sd\s",'desde ',s)
    s = re.sub("\s[Dd]sd\s",' desde ',s)
    s = re.sub("\Adivis\s",'divina ',s)
    s = re.sub("\sdivis\s",' divina ',s)
    s = re.sub("\Aekis\s",' <indiferencia> ',s)
    s = re.sub("\sekis\s",' <indiferencia> ',s)
    s = re.sub("\Afuck u\s",' <insulto> ',s)
    s = re.sub("\sfuck u\s",' <insulto> ',s)
    s = re.sub("\Afuck\s",' <insulto> ',s)
    s = re.sub("\sfuck\s",' <insulto> ',s)
    s = re.sub("\Aflaka\s",'flaca ',s)
    s = re.sub("\sflaka\s",' flaca ',s)
    s = re.sub("\Afut\s",'futbol ',s)
    s = re.sub("\sfut\s",' futbol ',s)
    s = re.sub("\Agrx\s",'gracias ',s)
    s = re.sub("\sgrx\s",' gracias ',s)
    s = re.sub("\Aidita\s",'ida ',s)
    s = re.sub("\sidita\s",' ida ',s)
    s = re.sub("\Ainter\s",'internet ',s)
    s = re.sub("\sinter\s",' internet ',s)
    s = re.sub("\Aizq\s",'izquierda ',s)
    s = re.sub("\sizq\s",' izquierda ',s)
    s = re.sub("\AIZQ\s",'izquierda ',s)
    s = re.sub("\sIZQ\s",' izquierda ',s)
    s = re.sub("\Akie",'quie',s)
    s = re.sub("\skie",' quie',s)
    s = re.sub("\A[Kk]pm\s",'que poca madre',s)
    s = re.sub("\s[Kk]pm\s",' que poca madre',s)
    s = re.sub("\Aksa\s",'casa ',s)
    s = re.sub("\sksa\s",' casa ',s)
    s = re.sub("\Aksita\s",'casa ',s)
    s = re.sub("\sksita\s",' casa ',s)
    s = re.sub("\Amam\s",'mamada',s)
    s = re.sub("\smam\s",' mamada ',s)
    s = re.sub("\Amamad\s",'mamada ',s)
    s = re.sub("\smamad\s",' mamada ',s)
    s = re.sub("\Amejo\s",'mi hijo ',s)
    s = re.sub("\smejo\s",' mi hijo ',s)
    s = re.sub("\Amez\s",'mes ',s)
    s = re.sub("\smez\s",' mes ',s)
    s = re.sub("\Ami shihiiis\s",'muchachita ',s)
    s = re.sub("\smi shihiiis\s",' muchachita ',s)
    s = re.sub("\Amsj\s",'mensaje ',s)
    s = re.sub("\smsj\s",' mensaje ',s)
    s = re.sub("\Amb\s",'megabytes ',s)
    s = re.sub("\smb\s",' megabytes ',s)
    s = re.sub("\Asms\s",'mensaje ',s)
    s = re.sub("\ssms\s",' mensaje ',s)
    s = re.sub("\Anah\s",'no ',s)
    s = re.sub("\snah\s",' no ',s)
    s = re.sub("\Anav\s",'navegar ',s)
    s = re.sub("\snav\s",' navegar ',s)
    s = re.sub("\snav$",' navegar',s)
    s = re.sub("\And\s",'nada ',s)
    s = re.sub("\snd\s",' nada ',s)
    s = re.sub("\Ahp\s",'hewlett_packard ',s)
    s = re.sub("\shp\s",' hewlett_packard ',s)
    s = re.sub("\Aclub movistar\s",'club_movistar ',s)
    s = re.sub("\sclub movistar\s",' club_movistar ',s)
    s = re.sub("\A[Oo] k\s","o qu'e ",s)
    s = re.sub("\s[Oo] k\s"," o qu'e ",s)
    s = re.sub("\Aof\s","oficina ",s)
    s = re.sub("\sof\s"," oficina ",s)
    s = re.sub("\Aonde\s",'donde ',s)
    s = re.sub("\sonde\s",' donde ',s)
    s = re.sub("\Adnd\s",'donde ',s)
    s = re.sub("\sdnd\s",' donde ',s)
    s = re.sub("\Akomo\s",'como ',s)
    s = re.sub("\skomo\s",' como ',s)
    s = re.sub("\Atng\s",'tenga ',s)
    s = re.sub("\stng\s",' tenga ',s)
    s = re.sub("\Ata\s",'esta ',s)
    s = re.sub("\sta\s",' esta ',s)
    s = re.sub("\A[Kk]\s",'que ',s)
    s = re.sub("\s[Kk]\s",' que ',s)
    s = re.sub("\Apedlla\s",'borrachera ',s)
    s = re.sub("\spedlla\s",' borrachera ',s)
    s = re.sub("\Apeo\s",'pedo ',s)
    s = re.sub("\speo\s",' pedo ',s)
    s = re.sub("\Aperece\s","esp'erece ",s)
    s = re.sub("\sperece\s"," esp'erece ",s)
    s = re.sub("\Aplis\s","por favor ",s)
    s = re.sub("\splis\s"," por favor ",s)
    s = re.sub("\Apolis\s","policIa ",s)
    s = re.sub("\spolis\s"," policIa ",s)
    s = re.sub("\Apin\'s\s",'pinches ',s)
    s = re.sub("\spin\'s\s",' pinches ',s)
    s = re.sub("\Apin\'\s",'pinche ',s)
    s = re.sub("\spin\'\s",' pinche ',s)
    s = re.sub("\Apqe\s","por quE ",s)
    s = re.sub("\spqe\s"," por quE ",s)
    s = re.sub("\Aporq\s","por quE ",s)
    s = re.sub("\sporq\s"," por quE ",s)
    s = re.sub("\Aporq\s",'porque ',s)
    s = re.sub("\sporq\s",' porque ',s)
    s = re.sub("\Apqe\s","porque ",s)
    s = re.sub("\spqe\s"," porque ",s)
    s = re.sub("\Aprdr\s",'perder ',s)
    s = re.sub("\sprdr\s",' perder ',s)
    s = re.sub("\Apro\s",'pero ',s)
    s = re.sub("\spro\s",' pero ',s)
    s = re.sub("\Apront\s",'pronto ',s)
    s = re.sub("\spront\s",' pronto ',s)
    s = re.sub("\Aps\s",'pues ',s)
    s = re.sub("\sps\s",' pues ',s)
    s = re.sub("\Apsas\s",'pasas ',s)
    s = re.sub("\spsas\s",' pasas ',s)
    s = re.sub("\Aqueles\s",'quieres ',s)
    s = re.sub("\squeles\s",' quieres ',s)
    s = re.sub("\ARe\s",'muy ',s)
    s = re.sub("\sRe\s",' muy ',s)
    s = re.sub("\Are\s",'muy ',s)
    s = re.sub("\sre\s",' muy ',s)
    s = re.sub("\Aserv\s",'servicio ',s)
    s = re.sub("\sserv\s",' servicio ',s)
    s = re.sub("\Ashi\s",'si ',s)
    s = re.sub("\sshi\s",' si ',s)
    s = re.sub("\Ashisotas\s",'chichis ',s)
    s = re.sub("\sshisotas\s",'chichis ',s)
    s = re.sub("\Asn\s",'son ',s)
    s = re.sub("\ssn\s",' son ',s)
    s = re.sub("\Asoluc\s","soluciOn ",s)
    s = re.sub("\ssoluc\s"," soluciOn ",s)
    s = re.sub("\Aspr",'super ',s)
    s = re.sub("\sspr",'super ',s)
    s = re.sub("\Astas\s",'estas ',s)
    s = re.sub("\sstas\s",' estas ',s)
    s = re.sub("\Asttus\s",'estatus ',s)
    s = re.sub("\ssttus\s",' estatus ',s)
    s = re.sub("\A[Tt]\s",'te ',s)
    s = re.sub("\s[Tt]\s",' te ',s)
    s = re.sub("\Atlf\s","telEfono ",s)
    s = re.sub("\stlf\s"," telEfono ",s)
    s = re.sub("\Atn\s",'tan ',s)
    s = re.sub("\stn\s",' tan ',s)
    s = re.sub("\Atns\s",'entonces ',s)
    s = re.sub("\stns\s",' entonces ',s)
    s = re.sub("\Auni\s",'universidad ',s)
    s = re.sub("\suni\s",'universidad ',s)
    s = re.sub("\Aunis\s",'universitarias ',s)
    s = re.sub("\sunis\s",'universitarias ',s)
    s = re.sub("\Auns\s",'unas ',s)
    s = re.sub("\suns\s",'unas ',s)
    s = re.sub("\Avd\s",'verdad ',s)
    s = re.sub("\svd\s",' verdad ',s)
    s = re.sub("\Avieji\s",'vieja ',s)
    s = re.sub("\svieji\s",' vieja ',s)
    s = re.sub("\Avms\s",'vamos ',s)
    s = re.sub("\svms\s",' vamos ',s)
    s = re.sub("\Avy\s",'voy ',s)
    s = re.sub("\svy\s",' voy ',s)
    s = re.sub("\Awei\s",'wey ',s)
    s = re.sub("\swei\s",' wey ',s)
    s = re.sub("\Axuxa\s",'puta ',s)
    s = re.sub("\sxuxa\s",' puta ',s)
    s = re.sub("\Acu%&amp;",'culo',s)
    s = re.sub("\scu%&amp;",' culo',s)
    s = re.sub("\A[Kk]ike\s",'enrique ',s)
    s = re.sub("\s[Kk]ike\s",' enrique ',s)
    s = re.sub("\A[Tt]qm\s",'te quiero mucho ',s)
    s = re.sub("\s[Tt]qm\s",' te quiero mucho ',s)
    s = re.sub("\ATQM\s",'te quiero mucho ',s)
    s = re.sub("\sTQM\s",' te quiero mucho ',s)
    s = re.sub("\Abuska\s",'busca ',s)
    s = re.sub("\sbuska\s",' busca ',s)
    s = re.sub("\Achikita\s",'chiquita ',s)
    s = re.sub("\schikita\s",' chiquita ',s)
    s = re.sub("\Adf\s",'Distrito_Federal ',s)
    s = re.sub("\sdf\s",' Distrito_Federal ',s)
    s = re.sub("\Ahd\s",'high_definition ',s)
    s = re.sub("\shd\s",' high_definition ',s)
    s = re.sub("najillos\s","najes ",s)
    s = re.sub("\A[Pp]qe\s",'porque ',s)
    s = re.sub("\s[Pp]qe\s",' porque ',s)
    s = re.sub("\A[Qq]e\s",'que ',s)
    s = re.sub("\s[Qq]e\s",' que ',s)
    s = re.sub("\A[Qq]ro\s",'quiero ',s)
    s = re.sub("\s[Qq]ro\s",' quiero ',s)
    s = re.sub("\A[Cc]erk\s",'cerca ',s)
    s = re.sub("\s[Cc]erk\s",' cerca ',s)
    s = re.sub("\A[Xx]\s",'por ',s)
    s = re.sub("\s[Xx]\s",' por ',s)
    s = re.sub("\A[Xx]q\s","porque ",s)
    s = re.sub("\s[Xx]q\s"," porque ",s)
    s = re.sub("\A[Aa]ssholes","culos ",s)
    s = re.sub("\s[Aa]ssholes"," culos ",s)
    s = re.sub("\A[Aa]sshole","culo ",s)
    s = re.sub("\s[Aa]sshole"," culo ",s)
    s = re.sub("\A[Ww]ebos\s","wevos ",s)
    s = re.sub("\A[Ww]evo\s","wevo ",s)
    s = re.sub("\A[Ww]evos\s","wevos ",s)
    s = re.sub("\s[Ww]evos\s"," wevos ",s)
    s = re.sub("\A[Cc]he\s","pinche ",s)
    s = re.sub("\s[Cc]he\s"," pinche ",s)
    s = re.sub("\A[Cc]nd\s","cuando ",s)
    s = re.sub("\s[Cc]nd\s"," cuando ",s)
    s = re.sub("\A[Cc]ndo\s","cuando ",s)
    s = re.sub("\s[Cc]ndo\s","cuando ",s)
    s = re.sub("\A[Kk]ga\s","caga ",s)
    s = re.sub("\s[Kk]ga\s"," caga ",s)
    s = re.sub("\A[Kk]gas\s","cagas ",s)
    s = re.sub("\s[Kk]gas\s"," cagas ",s)
    s = re.sub("\A[Kk]gn\s","cagOn ",s)
    s = re.sub("\s[Kk]gn\s"," cagOn ",s)
    s = re.sub("\A[Mm]\s","me ",s)
    s = re.sub("\s[Mm]\s"," me ",s)
    s = re.sub("\A[Mm]ex\s","mExico ",s)
    s = re.sub("\s[Mm]ex\s"," mExico ",s)
    s = re.sub("\Aa la c\s","a la chingada ",s)
    s = re.sub("\sa\sla\sc\s"," a la chingada ",s)
    s = re.sub("\Acbrn\s","cabrOn ",s)
    s = re.sub("\scbrn\s"," cabrOn ",s)
    s = re.sub("\Aagusto\s","a gusto ",s)
    s = re.sub("\sagusto\s"," a gusto ",s)
    s = re.sub("\Amamado\s","mamado ",s)
    s = re.sub("\smamado\s"," mamado ",s)
    s = re.sub("\Asmierdero\s","mierdero ",s)
    s = re.sub("\smierdero\s"," mierdero ",s)
    s = re.sub("\Ano chinguen\s"," <insulto> ",s)
    s = re.sub("\sno chinguen\s"," <insulto> ",s)
    s = re.sub("\Aodio jarocho\s"," <insulto> ",s)
    s = re.sub("\sodio\sjarocho[\s\s]"," <insulto> ",s)
    s = re.sub("\Aosea\s","o sea ",s)
    s = re.sub("\sosea\s"," o sea ",s)
    s = re.sub("\Aqpm\s","que puta madre ",s)
    s = re.sub("\sqpm\s"," que puta madre ",s)
    s = re.sub("\Aweno\s",'bueno ',s)
    s = re.sub("\sweno\s",' bueno ',s)
    s = re.sub("\Awena\s",'buena ',s)
    s = re.sub("\swena\s",' buena ',s)
    s = re.sub("\Awei\s",'wey ',s)
    s = re.sub("\swei\s",' wey ',s)
    s = re.sub("\A[Cc]hingatumadre\s",'chinga tu madre ',s)
    s = re.sub("\s[Cc]hingatumadre\s",' chinga tu madre ',s)
    s = re.sub("\A[Mm]njs?\s",'mensajes ',s)
    s = re.sub("\s[Mm]njs?\s",' mensajes ',s)
    s = re.sub("\A[Pp]\'\s",'para ',s)
    s = re.sub("\s[Pp]\'\s",' para ',s)
    s = re.sub("\A[Pp]a\'\s",'para ',s)
    s = re.sub("\s[Pp]a\'\s",' para ',s)
    s = re.sub("\A[Pp]a\s",'para ',s)
    s = re.sub("\s[Pp]a\s",' para ',s)
    s = re.sub("\Anot bad quality\s",' <comentario-positivo> ',s)
    s = re.sub("\snot bad quality\s",' <comentario-positivo> ',s)
    s = re.sub("\A[Bb]ye\s",'adios ',s)
    s = re.sub("\s[Bb]ye\s",' adios ',s)
    s = re.sub("\Afriend\s",'amigo ',s)
    s = re.sub("\sfriend\s",' amigo ',s)
    s = re.sub("\Anot bad\s",' <comentario-positivo> ',s)
    s = re.sub("\snot bad\s",' <comentario-positivo> ',s)
    s = re.sub("\Afriend\s",'por favor ',s)
    s = re.sub("\sfriend\s",' por favor ',s)
    s = re.sub("\A[Dd]\s","por dios ",s)
    s = re.sub("\s[Dd]\s"," por dios ",s)
    s = re.sub("\Ax[Dd]$","por dios ",s)
    s = re.sub("\sx[Dd]$"," por dios ",s)
    s = re.sub("\Abad quality\s",'mala calidad ',s)
    s = re.sub("\sbad quality\s",' mala calidad ',s)
    s = re.sub("\Abad quality$",'mala calidad ',s)
    s = re.sub("\sbad quality$",' mala calidad ',s)
    s = re.sub("\ABB\.?\s",'black_berry ',s)
    s = re.sub("\sBB\.?\s",' black_berry ',s)
    s = re.sub("\Abb\.?\s",'black_berry ',s)
    s = re.sub("\sbb\.?\s",' black_berry ',s)
    s = re.sub("\Azaz\s",' <sorpresa> ',s)
    s = re.sub("\szaz\s",' <sorpresa> ',s)
    s = re.sub("\Ac.c.p.\s",'con_copia_para ',s)
    s = re.sub("\sc.c.p.\s",' con_copia_para ',s)
    s = re.sub("\Accp\s",'con_copia_para ',s)
    s = re.sub("\sccp\s",' con_copia_para ',s)
    s = re.sub('&2&','://',s)  # regresa el ://
    return s

def carga_tabla(filename):
    tablename = nltk.defaultdict(lambda: 1)
    with open(filename, 'rU') as lineas:
            for row in csv.reader(lineas, delimiter=','):
                tablename[row[0]]= row[1]
    return tablename

def isword(s):
    if re.match(r'\w+',s):
        return True
    return False

def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if
len(b)>1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if
b]
    inserts =[a+c+b for a,b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if dic[e2]>1)

def known(words): return set(w for w in words if dic[w]>1)

def candidatos_validos(lista_palabras):
    return set(e1 for e1 in lista_palabras if dic[e1]>1)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    #cvs = candidatos_validos(candidates)
    #print candidates
    #print cvs
    has_accent = re.search('\|('+word+')\|', '|'+'|'.join(candidates)+'|', re.IGNORECASE)
    if has_accent:
        return has_accent.group(1)
    return max(candidates, key=lambda w: dic[w])

def clasifica_palabra(word):
    if int(insts[word])>1 :
        w2 = 'institucion('+word+')'
    else:
        if int(servs[word])>1 :
            w2 = 'servicio('+word+')'
        else:
            if int(marcs[word])>1 :
                w2 = 'marca('+word+')'
            else:
                if int(sigls[word])>1 :
                    w2 = 'siglas('+word+')'
                else:
                    if int(emprs[word])>1 :
                        w2 = 'empresa('+word+')'
                    else:
                        if int(locs[word])>1 :
                            w2 = 'locacion('+word+')'
                        else:
                            if int(dic[word])<2:
                                w2 = correct(word)
                                if int(dic[w2])>2:
                                    w2=w2    # linea falsa
                                    # print 'Found: %s'%w2
                                else:
                                    w2 = 'pal_desconocida('+word+')'
                            else:
                                w2 = word
    return w2

ruta = os.path.dirname(__file__)   

alphabet = 'AEIOUNWabcdefghijklmnopqrstuvwxyz'

dic = carga_tabla(ruta + '/datos/rae_corpus_v03.csv')
sigls = carga_tabla(ruta + '/datos/esp_siglas.csv')
emprs = carga_tabla(ruta + '/datos/esp_empresas.csv')
servs = carga_tabla(ruta + '/datos/esp_servicios.csv')
marcs = carga_tabla(ruta + '/datos/esp_marcas.csv')
locs = carga_tabla(ruta + '/datos/esp_locaciones.csv')
insts = carga_tabla(ruta + '/datos/esp_instituciones.csv')
#print len(dic)
#count = 0
#for k in dic:
#    if int(dic[k]) < 2:
#        count += 1
#print count
#import sys
#sys.exit(0)

c = csv.writer(open(ruta + "/entradas/twitter_spanish_mejorado.csv", "wb"))

with open(ruta + '/entradas/sentiment_spanish.csv', 'rU') as lineas:
        index = 1
        for row in csv.reader(lineas, delimiter=','):
            s1 = row[0]

            s1 = re.sub(' +',' ',s1) # deja un solo blanco entre cada palabra
            print "I-" + str(index) +": " + s1 #row[<index>]
            s1 = remplaza_caritas(s1)
            s1 = s1.lower() # Cambia mayusculas a minusculas
            s1 = acentos_regex.sub(reemplaza_acentos, s1)
            s1 = remplaza_repeticiones(s1)
            s1 = remplaza_contracciones(s1)

            s1 = re.sub(' +',' ',s1) # deja un solo blanco entre cada palabra

            items = re.split(" +", s1)
            #print 'items'+str(items)
            i = 0
            for item in items:
                if re.match(r"\$[0-9,]+[0-9]+", item):     #re.match(r"\$?[0-9,]+[\.(0-9)+|?]", item):
                    s3 = re.split(',',item[1:])
                    s3 = ''.join(s3)
                    items[i] = re.sub('\\'+item,"dinero("+s3+")",items[i],1)
                else:
                    if re.match(r"[0-9]+%", item):
                        s3 = item[:len(item)-1]
                        items[i] = re.sub(item,"porcentaje("+s3+")",items[i],1)
                    else:
                        if item.isdigit():
                            s3 = re.split(',',item)
                            s3 = ''.join(s3)
                            items[i] = re.sub(item,"num("+s3+")",items[i],1)
                        else:
                            if  re.match(r"[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", item):
                                items[i] = re.sub(item,"mail("+item+")",items[i],1)
                            else:
                                if  re.match(r"(http://|www\.|w3\.)[A-Za-z0-9\.\+/_-]+$", item):
                                    items[i] = re.sub(item,"url("+item+")",items[i],1)
                                else:
                                    if re.match(r"[A-Za-z]+\.[A-Za-z]+$", item):
                                        w = re.match('(\w+)\.(\w+)', item)
                                        items[i] = clasifica_palabra(w.group(1)) +' <punto> '+ clasifica_palabra(w.group(2))
                                    else:
                                        if re.match(r"[A-Za-z]+\.", item):
                                            w = re.match('(\w+)\.', item)
                                            items[i] = clasifica_palabra(w.group(1))+' <punto> '
                                        else:
                                            if isword(item):
                                                items[i] = clasifica_palabra(item)
                                            else:
                                                if  re.match(r"\@[A-Za-z0-9\._-]+:?$", item):
                                                    items[i] = re.sub(item,"cuenta("+item+")",items[i],1)
                                                else:
                                                    if  re.match(r"#[A-Za-z0-9\._-]+:?$", item):
                                                        items[i] = re.sub(item,"hashtag("+item+")",items[i],1)
                                                    else:
                                                        if item.isalnum():
                                                            items[i] = re.sub(item,"clave("+item+")",items[i],1)
                                                        else:
                                                            if  re.match(r"[\d,]+\.[A-Za-z]+", item):
                                                                s3 = re.split('\.',item)
                                                                s4 = re.split(',',s3[0])
                                                                s4 = ''.join(s4)
                                                                s5 = clasifica_palabra(s3[1])
                                                                items[i] = re.sub(item,"num("+s4+") <punto> "+s5,items[i],1)
                                                            #else:

                i += 1

            s2 = ' '.join(items)

            s2 = recupera_acento.sub(recupera_acentos, s2)

            print "F-{0}: {1}".format(str(index), s2)
            # print
            index += 1
            row[0]=s2
            c.writerow(row)



print "Fin"