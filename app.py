#!/usr/bin/python3.4

'''
/*******************************************************************************
* Copyright 2016-2018 Exactpro (Exactpro Systems Limited)
* 
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* 
*     http://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
******************************************************************************/
'''


from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import numpy
import pandas
import datetime
import calendar
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text 
from nltk.stem.snowball import SnowballStemmer
import pickle
from sklearn.feature_selection import (chi2, SelectKBest)
from sklearn import feature_selection
import matplotlib as plt
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import configparser
import os

#from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, KFold
#from sklearn import cross_validation
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.svm import SVC
from werkzeug.utils import secure_filename
import json
import scipy.stats as stats
from collections import OrderedDict
from datetime import datetime as dt
from lxml import objectify
import re
import csv
import traceback
import logging
from flask import send_from_directory
from multiprocessing import cpu_count, Pool

global origFrame
global newData
global murkup
global SignificanceTop
global origFreqTop
global asigneeReporterFin
global statInfo
global categoricDict
global clearDictionary
global tempFiles
global description1
global path
global columns
columns = []
path = 'SingleMod.ini'

config = configparser.ConfigParser()    

config.read('myconf.ini')
mymodel=config['Path']['models']
myvocab=config['Path']['vocab']

class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: (stemmer.stem(w) for w in analyzer(doc))

p00 = r'<((th)|(li)|(span)|p|(td)|(tr)|(pre)|(tbody)|(div)|(p)|(b)|(thead))>.*'
p000 = r'.*((\/th)|(\/li)|(\/p)|(\/span)|(span\/)|(p\/)|(td\/)|(tr\/)|(pre\/)|(tbody\/)|(div\/)|(p\/)|(br\/)|(thead\/))>'
p0000 = r'.*New'
p0 = r'<table'
p1 = r'&lt;p&gt;'
p2 = r'</?p>'
p3 = r'&amp;'
p4 = r'&gt;'
p5 = r'&lt;'
p7 = ('Original Message.*\\n(>\\s)?Subject:.*\\n(>\\s)?Date:.*\\n(>\\s)?From:.*\\n(>\\s)?To:.*')
p8 = (
    '\\n(>\\s)?Service Level:.*\\n(>\\s)?Product:.*\\n(>\\s)?Response Time:.*\\n(>\\s)?Time of Expiration:.*\\n(>\\s)?Created:.*\\n(>\\s)?URL:.*\\n(>\\s)?Subject:.*')
p9 = ('[[(][0-9][0-9]:[0-9][0-9].*(?:(PM)|(AM)).*:')

p10 = (
    '\\n(>\\s)?Resolving.*\\n(>\\s)?Connecting.*\\n(>\\s)?HTTP.*\\n(>\\s)?(\\s)+HTTP.*\\n(>\\s)?(\\s)+Date:.*\\n(>\\s)?(\\s)+Server:.*(?:(\\n(>\\s)?(\\s)+Location:.*\\n(>\\s)?(\\s)+Content-Length:.*\\n(>\\s)?(\\s)+Keep-Alive:.*\\n(>\\s)?(\\s)+Connection:.*\\n(>\\s)?(\\s)+Content-Type:.*(\\n(>\\s)?(\\s)+Location:.*)?)|(\\n(>\\s)?(\\s)+X-Powered-By:.*\\n(>\\s)?(\\s)+Content-Type:.*\\n(>\\s)?(\\s)+(?:(Content-Language:)|(Content-Length:)).*(\\n(>\\s)?(\\s)+Set-Cookie:.*)?(\\n(>\\s)?(\\s)+Via:.*)?(\\n(>\\s)?(\\s)+Connection:.*)?))(.*Length:.*)?')
p11 = (
    '(?:(.*ALERT.*)|(?:(.*ERROR.*)|(?:.*ERROR.*|(?:.*INFO.*|(?:.*WARN.*|(?:.*CLOSE_WAIT.*|(?:.*BLOCKED.*|(?:.*DEBUG.*|.*WAITING.*))))))))')
p12 = (
    '(?:(((\\n.*ERROR.*)+)?((.*ERROR.*\\n)+)?((.*[a-zA-Z]Exception.*\\n)+)?((.*[a-zA-Z]Error.*\\n)+)?((.*at .*[(].*(?:java|(?:Unknown Source|Native Method)).*[)].*)+))|((((?:((\\n.*ERROR.*)+)|((.*ERROR.*\\n)+)))+)((((.*[a-zA-Z]Exception.*\\n)+)))))')
p13 = ('.*(?:waiting|locked).*0x.*[(].*[)].*')
p14 = ('.*0x.*0x.*')
p15 = ('.*(?:(".*ActiveMQ.*")|(".*Thread-7.*")).*')
p16 = (
    '([a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+[(](?:.*java.*|(?:.*Native Method.*|.*No such file or directory.*))[)])')
p17 = ('.*[Cc]aused by.*java.*\\n(.*[Cc]aused by.*java.*\\n)+')
p18 = ('.*at line.*\\n.*at line.*\\n((.*at line.*\\n)+)')
p19 = ('((.*[0-9][0-9]:[0-9][0-9]:[0-9][0-9].*[[]error[]].*client.*)+)')
p20 = ('.*java.*[(].*[)].*\\n.*java.*[(].*[)].*\\n')
p21 = ('.*[(].*".*".*=>.*".*".*[)].*')

p22 = ('[/][^\\s]*=[^\\s]*[/][^\\s]*=[^\\s]*')
p23 = ('[^\\s]+[.][^\\s"]+')
p24 = ('{{.*}}')  #
p25 = ('[^\\s]+[/][^\\s]+')
p26 = ('.*Event.*receive.*from remote server.*\\nInternal Server Error.*')

p27 = ('(?:({panel})|(?:({code[^\\s]*})|(?:({noformat})|({quote}))))')

p28 = ('[A-Z][a-z]+[A-Z][a-z]+[(].*[)]')

p29 = ('[^\\s]*@[^\\s]*')
p30 = ('[A-Z]+?[a-z]+[A-Z][a-z]+[^\\s]*')
p31 = ('[0-9]+.*has been deprecated')

p32 = ('@[^\\s]*')
p33 = ('[.][a-z]+[^\\s]*')
p34 = ('<[^\\s]*>')
p35 = ('<[[].*[]]>')
p36 = ('[[]disconnected.*[/][]]')
p37 = ('[-][-][a-z]*')
p38 = ('try.*{.*}')
p39 = ('catch.*{.*}')
p40 = ('{.*throw.*}')
p41 = ('check.*{.*}')
p42 = ('public void')
p43 = ('private void')
p44 = ('[[][[].*[]][]]')
p45 = ('<.*[/]>')
p46 = (
    '(?:a2p|ac|addgroup|adduser|agrep|alias|apropos|apt-cache|apt-get|aptitude|ar|arch|arp|as|aspell|at|awk|basename|bash|bc|bdiff|bfs|bg|biff|break|bs|bye|cal|calendar|cancel|cat|cc|cd|cfdisk|chdir|checkeq|checknr|chfn|chgrp|chkey|chmod|chown|chroot|chsh|cksum|clear|cmp|col|comm|compress|continue|cp|cpio|crontab|csh|csplit|ctags|cu|curl|cut|date|dc|dd|delgroup|deluser|depmod|deroff|df|dhclient|diff|dig|dircmp|dirname|dmesg|dos2unix|dpkg|dpost|du|echo|ed|edit|egrep|eject|elm|emacs|enable|env|eqn|ex|exit|expand|expr|fc|fdisk|fg|fgrep|file|find|findsmb|finger|fmt|fold|for|foreach|free|fsck|ftp|fuser|gawk|getfacl|gpasswd|gprof|grep|groupadd|groupdel|groupmod|gunzip|gview|gvim|gzip|halt|hash|hashstat|head|help|history|host|hostid|hostname|id|ifconfig|ifdown|ifquery|ifup|info|init|insmod|iostat|ip|isalist|iwconfig|jobs|join|keylogin|kill|killall|ksh|last|ld|ldd|less|lex|link|ln|lo|locate|login|logname|logout|losetup|lp|lpadmin|lpc|lpq|lpr|lprm|lpstat|ls|lsmod|lsof|lzcat|lzma|mach|mail|mailcompat|mailx|make|man|merge|mesg|mii-tool|mkdir|mkfs|mkswap|modinfo|modprobe|more|mount|mt|mv|myisamchk|mysql|mysqldump|nc|neqn|netstat|newalias|newform|newgrp|nice|niscat|nischmod|nischown|nischttl|nisdefaults|nisgrep|nismatch|nispasswd|nistbladm|nl|nmap|nohup|nroff|nslookup|od|on|onintr|optisa|pack|pagesize|parted|partprobe|passwd|paste|pax|pcat|perl|pg|pgrep|pico|pine|ping|pkill|poweroff|pr|printenv|printf|priocntl|ps|pstree|pvs|pwd|quit|rcp|readlink|reboot|red|rehash|rename|renice|repeat|replace|rgview rgvim|rlogin|rm|rmdir|rmmod|rn|route|rpcinfo|rsh|rsync|rview|rvim|s2p|sag|sar|scp|screen|script|sdiff|sed|sendmail|service|set|setenv|setfacl|sfdisk|sftp|sh|shred|shutdown|sleep|slogin|smbclient|sort|spell|split|startx|stat|stop|strftime|strip|stty|su|sudo|swapoff|swapon|sysklogd|tabs|tac|tail|talk|tar|tbl|tcopy|tcpdump|tcsh|tee|telinit|telnet|test|time|timex|todos|top|touch|tput|tr|traceroute|trap|tree|troff|tty|ul|umask|umount|unalias|uname|uncompress|unhash|uniq|unlink|unlzma|unpack|until|unxz|unzip|uptime|useradd|userdel|usermod|vacation|vgrind|vi|view|vim|vipw|visudo|vmstat|w|wait|wall|wc|wget|whatis|whereis|which|while|who|whoami|whois|write|X|Xorg|xargs|xfd|xhost|xinit|xlsfonts|xrdb|xset|xterm|xz|xzcat|yacc|yes|yppasswd|yum|zcat|zip|zipcloak|zipinfo|zipnote|zipsplit) -{1,2}\w+ \w*')

p47 = (
    r'\b(a2p|ac|addgroup|adduser|agrep|alias|apropos|apt-cache|apt-get|aptitude|ar|arch|arp|as|aspell|at|awk|basename|bash|bc|bdiff|bfs|bg|biff|break|bs|bye|cal|calendar|cat|cc|cd|cfdisk|chdir|checkeq|checknr|chfn|chgrp|chkey|chmod|chown|chroot|chsh|cksum|cmp|col|comm|compress|cp|cpio|crontab|csh|csplit|ctags|cu|curl|date|dc|dd|delgroup|deluser|depmod|deroff|df|dhclient|diff|dig|dircmp|dirname|dmesg|dos2unix|dpkg|dpost|du|echo|ed|egrep|eject|elm|emacs|env|eqn|ex|expr|fc|fdisk|fg|fgrep|findsmb|finger|fmt|foreach|fsck|ftp|fuser|gawk|getfacl|gpasswd|gprof|grep|groupadd|groupdel|groupmod|gunzip|gview|gvim|gzip|halt|hash|hashstat|hostid|ifconfig|ifdown|ifquery|ifup|init|insmod|iostat|ip|isalist|iwconfig|keylogin|kill|killall|ksh|last|ld|ldd|less|lex|link|ln|lo|logname|logout|losetup|lp|lpadmin|lpc|lpq|lpr|lprm|lpstat|ls|lsmod|lsof|lzcat|lzma|mach|mailcompat|mailx|mesg|miitool|mkdir|mkfs|mkswap|modinfo|modprobe|mount|mt|mv|myisamchk|mysqldump|nc|neqn|netstat|newalias|newform|newgrp|niscat|nischmod|nischown|nischttl|nisdefaults|nisgrep|nismatch|nispasswd|nistbladm|nl|nmap|nohup|nroff|nslookup|od|on|onintr|optisa|pack|pagesize|parted|partprobe|passwd|pax|pcat|perl|pg|pgrep|pico|pine|pkill|poweroff|pr|printenv|printf|priocntl|ps|pstree|pvs|pwd|rcp|readlink|red|rehash|renice|repeat|rgview|rgvim|rlogin|rm|rmdir|rmmod|rn|route|rpcinfo|rsh|rsync|rview|rvim|s2p|sag|sar|scp|sdiff|sed|sendmail|setenv|setfacl|sfdisk|sftp|sh|shred|slogin|smbclient|sort|spell|split|startx|stat|strftime|strip|stty|su|sudo|swapoff|swapon|sysklogd|tac|tar|tbl|tcopy|tcpdump|tcsh|tee|telinit|telnet|timex|todos|tput|tr|traceroute|trap|tree|troff|tty|ul|umask|umount|unalias|uname|uncompress|unhash|uniq|unlink|unlzma|unpack|until|unxz|unzip|uptime|useradd|userdel|usermod|vacation|vgrind|vi|vim|vipw|visudo|vmstat|w|wall|wc|wget|whatis|whereis|which|while|who|whoami|whois|X|Xorg|xargs|xfd|xhost|xinit|xlsfonts|xrdb|xset|xterm|xz|xzcat|yacc|yppasswd|yum|zcat|zip|zipcloak|zipinfo|zipnote|zipsplit)\b')
p48 = ('[^\\s]*[0-9][^\\s]*')

p49 = ('[^a-zA-Z\\s]+')
p50 = ('\\sPM\\s')
p51 = ('\\sAM\\s')


p52 = ('(?:(\\sabstract\\s)|(\\sassert\\s))')
p53 = ('(?:(\\sboolean\\s)|(\\sbreak\\s))')
p54 = ('(?:(\\sbyte\\s)|(\\scase\\s))')
p55 = ('(?:(\\scatch\\s)|(\\schar\\s))')
p56 = ('(?:(\\sclass\\s)|(\\sconst\\s))')
p57 = ('(?:(\\scontinue\\s)|(\\sdefault\\s))')
p58 = ('(?:(\\sdo\\s)|(\\sdouble\\s))')
p59 = ('(?:(\\selse\\s)|(\\senum\\s))')
p60 = ('(?:(\\sfor\\s)|(\\sfloat\\s))')
p61 = ('(?:(\\sgoto\\s)|(\\sif\\s))')
p62 = ('(?:(\\sinstanceof\\s)|(\\sint\\s))')
p63 = ('(?:(\\snew\\s)|(\\sprivate\\s))')
p64 = ('(?:(\\sprotected\\s)|(\\spublic\\s))')
p65 = ('(?:(\\sreturn\\s)|(\\sstatic\\s))')
p66 = ('(?:(\\sstrictfp\\s)|(\\sswitch\\s))')
p67 = ('(?:(\\sthis\\s)|(\\sthrow\\s))')
p68 = ('(?:(\\sthrows\\s)|(\\stransient\\s))')
p69 = ('(?:(\\stry\\s)|(\\svoid\\s))')
p70 = ('(?:(\\svolatile\\s)|(\\swhile\\s))')
p71 = ('(?:(\\strue\\s)|(\\sfalse\\s))')
p72 = ('\\snull\\s')
p73 = ('[a-zA-Z]+\'[a-zA-Z]+')
p74 = ('\\s[a-zA-Z]\\s')
p75 = ('\\s[A-Z]+\\s')
p76 = ('.*undefined.*\\n.*undefined.*\\n.*undefined.*\\n.*undefined.*\\n.*undefined.*\\n')
p77 = ('relay.*undefined.*\\n.*transport.*\\n.*undefined.*\\n.*undefined')
p78 = ('drwxr xr.*')
p79 = ('\\t\\t\\t\\t\\t\\soption.*\\n\\t\\t\\t\\t\\t\\soption.*\\n\\t\\t\\t\\t\\t\\soption.*\\n')
p80 = ('\\t\\smodule option.*\\n\\t\\smodule option.*\\n\\t\\smodule option.*\\n')
p81 = (
    '\\s\\sFailed to load module\\s\\s\\sextension.*\\n.*\\n\\s\\sFailed to load module\\s\\s\\sextension.*\\n.*\\n')
p82 = ('\\sdoes\\s')
p83 = ('\\sdoesnt\\s')
p84 = ('\\sive\\s')
p85 = ('\\sdont\\s')
p86 = ('\\shes\\s')
p87 = ('\\sill\\s')
p88 = ('\\sdid\\s')
p89 = ('\\syoull\\s')
p90 = ('\\sdoesn\\s')
p91 = ('\\shaven\\s')
p92 = ('\\sdon\\s')
p93 = ('\\sisnt\\s')

pattern0 = re.compile(r'({{.*?}})', re.DOTALL)
pattern1 = re.compile(r'({code.*?{code})', re.DOTALL)
pattern2 = re.compile(r'({noformat.*?{noformat})', re.DOTALL)
pattern3 = re.compile(r'({panel.*?{panel})', re.DOTALL)
pattern4 = re.compile(r'({quote.*?{quote})', re.DOTALL)
pattern5 = re.compile(r'\\nmysql>.* sec[)]', re.DOTALL)
pattern6 = re.compile(r'failure description:.*[{].*[}]', re.DOTALL)
pattern7 = re.compile(r'[\\s][{][\\s].*[\\s][}][\\s]', re.DOTALL)
pattern8 = re.compile(r'(?:https|http)://\w*\S*\d*', re.DOTALL)
pattern9 = re.compile(r'\(\d{2}:.*?\n', re.DOTALL)

p124 = r' fghfgh | cebd | jcmd | tx | seq | ute |fsvlmdsfvfn| trc | SLL |addToBATSG| cf | fw | Sl | id | cmd | pre '
p126 = r'gzaa'
p125 = r'(&lt.*)|(&lt.*&gt)|(.*&gt)'
p00000 = r'<((li)|(span)|p|(td)|(tr)|(pre)|(tbody)|(div)|(p)|(b)|(thead)).*'

remove_pat = [p126, p125, p00, p000, p00000, p0000, p0, p1, p2, p3, p4, p5, p7, p8, p9, p10, p11, p12, p13, p14, p15,
         p16, p17, p18, p19, p20, p21,
         p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, p39, p40, p41,
         p42, p43, p44, p45, p46, p47
    , p48, p49, p50, p51, p52, p53, p54, p55, p56, p57, p58, p59, p60, p61, p62, p63, p64, p65, p66, p67, p68,
         p69, p70, p71, p72, p73,
         p74, p75, p76, p77, p78, p79, p80, p81, p82, p83, p84, p85, p86, p87, p88, p89, p90, p91, p92, p93,
         pattern0, pattern1,
         pattern2, pattern3, pattern4, pattern5, pattern6, pattern7, pattern8, pattern9, p124]

stemmer = SnowballStemmer("english")

myStopWords = ['monday', 'mon', 'tuesday', 'tue', 'wednesday', 'wed', 'thursday', 'thu', 'friday', 'fri', 'saturday', 'sat',
               'sunday', 'sun', 'january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'may', 'june', 'july', 'august',
               'aug', 'september', 'sep', 'octomber', 'oct', 'november', 'nov', 'december', 'dec']

def proc_text(text, col_class, name_model):
    test_pro=text
    for i in range(len(remove_pat)):
        test_pro=re.sub(remove_pat[i],'', test_pro)
    proba={}
    load_model_test=pickle.load(open(mymodel+name_model+'.sav', 'rb'))
    proba_=list(numpy.array(numpy.around(load_model_test.predict_proba([test_pro])[0],3), dtype=float).flatten())
    proba_dic=dict(zip(col_class, proba_))
    return proba_dic

def build_prob_bar(dic, angle):    
    plt.figure() 
    ax = plt.axes() 
    plt.tight_layout()
    plt.ylabel('probability', fontsize=8, rotation_mode='anchor')
    ax.yaxis.grid(which="major", color='r', linestyle='-')
    plt.xticks(range(len(dic)), dic.keys(),rotation=angle, rotation_mode='anchor')    
    plt.bar(range(len(dic)), dic.values(), align='center')
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  
    figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8').replace('\n', '')
    figfile.close()
    return figdata_png

def build_prob_pie(mydict):  
    plt.figure()
    mypie=plt.pie([float(v) for v in mydict.values()], labels=[k for k in mydict.keys()],autopct=None)
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  
    figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8').replace('\n', '')
    figfile.close()
    return figdata_png

app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
bootstrap = Bootstrap(app)

@app.route('/',methods = ['POST', 'GET'])
def enterlog():
    global description1
    global tempFiles
    description1 = ''
    tempFiles = []
    return render_template('filterPage.html', json=json.dumps({'message':'please choose file'}))

UPLOAD_FOLDER = os.path.abspath(os.curdir)+'/files'
ALLOWED_EXTENSIONS = set(['xml'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def open_file(file, markup):
    filename, file_extension = os.path.splitext(file.filename)
    if(file_extension == '.csv'):
        if(markup == 1):
            data = pandas.read_csv(file)
        else:
            data = pandas.read_csv(file)
    else:
        if(isinstance(parseXML(file, markup, app.config['UPLOAD_FOLDER']+'/'+secure_filename(file.filename+'.csv')), str)):
            os.remove(app.config['UPLOAD_FOLDER']+'/'+secure_filename(file.filename)+'.csv')
            return 'incorrect format for xml'
        data = pandas.read_csv(open(app.config['UPLOAD_FOLDER']+'/'+secure_filename(file.filename)+'.csv', 'r'))
        os.remove(app.config['UPLOAD_FOLDER']+'/'+secure_filename(file.filename)+'.csv')
    return data

def get_attributes(data, murkup):
    mas = []
    area = []
    if(murkup == 0):
        for el in list(data.keys()):
            if el not in area:
                mas.append(el)
    else:
        mas = list(data.keys())
    return mas

def prepare_categorical(date, murkup):
    if(document_verification(date, murkup)):
        fields = {'Status': date['Status'].fillna('null').unique().tolist(), 'Project_name': date['Project_name'].fillna('null').unique().tolist(), 'Priority': date['Priority'].fillna('null').unique().tolist(), 'Resolution': date['Resolution'].fillna('null').unique().tolist(), 'DEV_resolution': date['DEV_resolution'].fillna('null').unique().tolist(), 'ReferringTo': add_prefix(origFrame['Priority'].fillna('null').unique().tolist(), 'Priority ')+add_prefix(origFrame['Resolution'].fillna('null').unique().tolist(), 'Resolution ')}
        return fields
    else:
        if(murkup == 1):
            return 'document is not valid. Please check that document have following fields:' + '\n' + '\'Issue_key\', \'Summary\', \'Status\', \'Project_name\', \'Priority\', \'Resolution\', \'Components\', \'Labels\', \'Description\', \'Comments\', \'Attachments\', \'Version\', \'DEV_resolution\', \'Created\', \'Resolved\''
        else:
            return 'document is not valid. Please check that document have following fields:' + '\n' + '\'Issue_key\', \'Summary\', \'Status\', \'Project_name\', \'Priority\', \'Resolution\', \'Components\', \'Labels\', \'Description\', \'Comments\', \'Attachments\', \'Version\', \'DEV_resolution\', \'Created\', \'Resolved\''

def categorical_json(date, murkup):
    dictionary = prepare_categorical(date, murkup)
    if(isinstance(dictionary, str)):
        return dictionary
    for listName in dictionary:
        for el in dictionary[listName]:
            el = str(el)
    return dictionary

def document_verification(date, murkup):
    required_fields = ['Issue_key','Summary','Status','Project_name','Priority','Resolution','Components','Labels','Description','Comments','Attachments','DEV_resolution','Created','Resolved','Version']
    required_fields_murkup = ['Issue_key','Summary','Status','Project_name','Priority','Resolution','Components','Labels','Description','Comments','Attachments','DEV_resolution','Created','Resolved','Version']
    trigger = False
    if(murkup == 0):
        for field in required_fields_murkup:
            for el in get_attributes(date, murkup):
                if(field.lower() == el.lower()):
                    trigger = True
            if(trigger == False):
                return False
            trigger = False
        return True
    else:
        for field in required_fields:
            for el in get_attributes(date, murkup):
                if(field.lower() == el.lower()):
                    trigger = True
            if(trigger == False):
                return False
            trigger = False
        return True

def add_prefix(list, prefix):
    return [prefix+el for el in list]

def transform_fields(data):
    try:
        global origFrame
        global newData
        data['summary'] = data['Summary'].fillna(value='?')
        data['summary'] = data['summary'].str.lower()
        data['descr'] = data['Description'].fillna(value='default_descr_value')
        data['descr'] = data['descr'].str.lower()
        data['labels'] = data['Labels'].fillna(value='?')
        data['labels'] = data['labels'].str.lower()
        data['components'] = data['Components'].fillna(value='?')
        data['components'] = data['components'].str.lower()
        data['date_created'] = pandas.to_datetime(data['Created'],dayfirst=True)
        data['date_resolved'] = pandas.to_datetime(data['Resolved'],dayfirst=True)
        data['date_resolved_td'] = data['date_resolved'].fillna(value=datetime.date.today())
        data['ttr'] = (data['date_resolved_td']-data['date_created']).dt.days
        newData = data
        origFrame = data
        return data
    except KeyError:
            return 'document is not valid. Please check that document have following fields:' + '\n' + '\'Comments\', \'Summary\' ,\'Components\', \'Labels\', \'Description\', \'Comments\', \'Attachments\', \'Created\', \'Resolved\''
    except ValueError: return 'invalid value for date field please use format dd-mm-yyyy'

def nonetozero(val):
    if(val == 'None'):
        return '0'
    else: return val

def get_statInfo(data):
    return {'total': str(origFrame['Issue_key'].count()),
            'filtered': str(data['Issue_key'].count()),
            'commentStat': {'max': str(data['Comments'].max()),
                            'min': str(data['Comments'].min()),
                            'mean': str(round(data['Comments'].mean(), 3)),
                            'std': str(round(data['Comments'].std(), 3))
                            },
            'attachmentStat': {
                                'max': str(data['Attachments'].max()),
                                'min': str(data['Attachments'].min()),
                                'mean': str(round(data['Attachments'].mean(), 3)),
                                'std': str(round(data['Attachments'].std(), 3))
                                },
            'ttrStat': {
                        'max': str(data['ttr'].max()),
                        'min': str(data['ttr'].min()),
                        'mean': str(round(data['ttr'].mean(), 3)),
                        'std': str(round(data['ttr'].std(), 3))
                        }
            }

def parse_to_int(var):
    try:
        intVar = int(var)
        return intVar
    except ValueError:
        return 'incorrect value for \'' + var + '\'.Please enter correct type of data'

def parse_to_date(var):
    try:
        varDate =pandas.to_datetime(dt.strptime(var, '%d-%m-%Y'))
        return varDate
    except ValueError:
        return 'incorrect value for \'' + var + '\'.Please use type of data like \'dd-mm-yyyy\''

def fields_for_filtration(dictionary):
    newDictionary = {}
    for key in dictionary:
        if(dictionary[key] != '' and dictionary[key] != []):
            newDictionary[key] = dictionary[key]
    return newDictionary

def checkNumeric(dictionary, key):
    if key in dictionary:
        el = parse_to_int(dictionary[key])
        return isinstance(el, str)
    else:
        return False

def checkDate(dictionary, key):
    if key in dictionary:
        el = parse_to_date(dictionary[key])
        return isinstance(el, str)
    else: return False

def parseToIntFinal(dictionary):
    newDictionary = {}
    for key in dictionary:
        newDictionary[key] = parse_to_int(dictionary[key])
    return newDictionary

def parseToDateFinal(dictionary):
    newDictionary ={}
    for key in dictionary:
        newDictionary[key] = parse_to_date(dictionary[key])
    return newDictionary

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def special_character_escaping(val):
        newVal = val.replace('[', '\[')
        newVal1 = newVal.replace(']', '\]')
        newVal2 = newVal1.replace('*', '\*')
        newVal3 = newVal2.replace('(', '\(')
        newVal4 = newVal3.replace(')', '\)')
        newVal5 = newVal4.replace('{', '\{')
        newVal6 = newVal5.replace('}', '\}')
        newVal7 = newVal6.replace('-', '\-')
        newVal8 = newVal7.replace('+', '\+')
        newVal9 = newVal8.replace('?', '\?')
        newVal10 = newVal9.replace('.', '\.')
        newVal11 = newVal10.replace('|', '\|')
        newVal12 = newVal11.replace('$', '\&')
        newVal13 = newVal12.replace('^', '\^')
        newVal14 = newVal13.replace(r'\n', '')
        newVal15 = newVal14.replace(r' ', '')
        return newVal15

def filtration(key, value, data):
        global newData
        if key.lower()=='issue_key':
            newData = data[data['Issue_key'].str.lower() == value.lower()]
            return newData
        if key.lower()=='summary':
            newData = data[data['summary'].str.replace(r'\n', ' ').str.contains(value, case=False, na=False, regex=False) == True]
            return newData
        if key.lower() == 'status':
            newData = data[data["Status"].isin(value) == True]
            #for val in value:
            #    newData = newData[newData['Status'].str.replace(r'\n', ' ').str.contains(val, case=False, na=False, regex=False) == True]
            return newData
        if key.lower()=='project_name':
            newData = data[data["Project_name"].isin(value) == True]
            return newData
        if key.lower()=='priority':
            newData = data[data["Priority"].isin(value) == True]
            return newData
        if key.lower()=='resolution':
            newData = data[data["Resolution"].isin(value) == True]
            return newData
        if key.lower()=='components':
            newData = data
            newData['components'] = newData['Components'].astype(str)
            for pattern in value.split(','):
                newData = contains(newData, 'components', pattern.strip())
            return newData
        if key.lower()=='labels':
            newData = data
            newData['labels'] = newData['Labels'].astype(str)
            for pattern in value.split(','):
                newData = contains(newData, 'labels', pattern.strip())
            return newData
        if key.lower()=='description':
            newData = data[data['descr'].str.replace(r'\n', ' ').str.replace(' ', '').str.contains(value.replace(r'\n', ' ').replace(' ', ''), case=False, na=False, regex=False) == True]
            return newData
        if key.lower()=='version':
            newData = data
            newData['version'] = newData['Version'].astype(str)
            for pattern in value.split(','):
                newData = contains(newData, 'version', pattern.strip())
            return newData
        if key.lower()=='comments2':
            newData = data[data['Comments'] >= value]
            return newData
        if key.lower()=='comments4':
            newData = data[data['Comments'] <= value]
            return newData
        if key.lower()=='attachments2':
            newData = data[data['Attachments'] >= value]
            return newData
        if key.lower()=='attachments4':
            newData = data[data['Attachments'] <= value]
            return newData
        if key.lower()=='date_created2':
            data['date_created'] = pandas.to_datetime(data['date_created'])
            newData = data[data['date_created'] >= value]
            return newData
        if key.lower()=='date_created4':
            data['date_created'] = pandas.to_datetime(data['date_created'])
            newData = data[data['date_created'] <= value]
            return newData
        if key.lower()=='date_resolved2':
            data['date_resolved_td'] = pandas.to_datetime(data['date_resolved_td'])
            newData = data[data['date_resolved_td'] >= value]
            return newData
        if key.lower()=='date_resolved4':
            data['date_resolved_td'] = pandas.to_datetime(data['date_resolved_td'])
            newData = data[data['date_resolved_td'] <= value]
            return newData
        if key.lower()=='ttr2':
            newData = data[data['ttr'] >= value]
            return newData
        if key.lower()=='ttr4':
            newData = data[data['ttr'] <= value]
            return newData
        if key.lower()=='DEV_resolution':
            newData = data[data["DEV_resolution"].isin(value) == True]
            return newData

def find(value, pattern):
    pattern = re.compile(r'\b' + re.sub(r'[%;"\\.^:\/$​–•\|!#<~&@>*\-+=◾\'\?╙“”‘’]*', '', pattern) + r'\b')
    if (re.findall(pattern, re.sub(r'[%;"\\.^:\/$​–•\|!#<~&@>*\-+=◾\'\?╙“”‘’]*', '', value))):
        return True
    else:
        return False

def contains(df, field, pattern):
    newDf = df[df[field].str.replace(r'\n', ' ').apply(find, args=(pattern,)) == True]
    return newDf[newDf[field].str.contains(pattern, case=False, na=False, regex=False) == True]

def check_fileName(fileName):
    if not re.match(r'.*\.csv', fileName):
        return False
    else: return True

def save_file(data, fileName, murkup):
    if(murkup == 0):
        data.to_csv(os.path.join(UPLOAD_FOLDER, fileName), columns=['Issue_key', 'Summary', 'Status', 'Project_name', 'Priority', 'Resolution', 'Components', 'Labels', 'Description', 'Comments', 'Attachments', 'DEV_resolution', 'Created', 'Resolved', 'Affects_Ver', 'Version'], index=False)
    else:
        data.to_csv(os.path.join(UPLOAD_FOLDER, fileName), columns=['Issue_key', 'Summary', 'Status', 'Project_name', 'Priority', 'Resolution', 'Components', 'Labels', 'Description', 'Comments', 'Attachments', 'DEV_resolution', 'Created', 'Resolved', 'Affects_Ver', 'Version'], index=False)

def drop_filter():
    global origFrame
    global newData
    global statInfo
    global categoricDict
    global clearDictionary
    newData = origFrame
    categoricDict = categorical_json(newData, murkup)
    statInfo = get_statInfo(newData)
    clearDictionary = {'SignificanceTop': SignificanceTop[categoricDict['ReferringTo'][0]], 'ReferringTo': 'Priority '+categoricDict['Priority'][0], 'freqTop': origFreqTop}
    return statInfo

def drop_newData():
    global origFrame
    global newData
    newData = origFrame
    return newData

def prepareToFiltering(dictionary, key, val1, val2, val3, val4):
    dictionary[key] = {'operation': [ifExist(dictionary, val1), ifExist(dictionary, val3)], 'left': ifExist(dictionary, val2), 'rigth': ifExist(dictionary, val4)}
    return dictionary

def ifExist(dictionary, val):
    if val not in dictionary:
        dictionary[val] = ''
    return dictionary[val]

def checkLeftRigth(dictionary):
    newDict = {}
    for key in dictionary:
        if(key in ['Date_created', 'Comments', 'TTR', 'Date_resolved', 'Attachments']):
            innerDict = dictionary[key]
            if(str(innerDict['left']) != ''):
                    newDict[key] = dictionary[key]
            else:
                if(str(innerDict['rigth']) != ''):
                    newDict[key] = dictionary[key]

        if(key in ['Issue_key']):
            if(str(dictionary[key]) != ''):
                newDict[key] = str(dictionary[key])

        if(key in ['Summary', 'Status', 'Project_name', 'priority', 'Resolution', 'Components', 'Labels', 'Description', 'DEV_resolution']):
            if(str(dictionary[key]) != ''):
                newDict[key] = dictionary[key]
    return newDict

def checkLeftRigthWithoutSings(dictionary):
    newDict = {}
    for key in dictionary:
        if(key in ['Comments2', 'Comments4', 'Attachments2', 'Attachments4', 'Date_created2', 'Date_created4', 'Date_resolved2', 'Date_resolved4', 'TTR2', 'TTR4']):
            newDict[key] = dictionary[key]
        if(key in ['Issue_key', 'Version']):
            if(str(dictionary[key]) != ''):
                newDict[key] = str(dictionary[key])
        if(key in ['Summary', 'Components', 'Labels', 'Description']):
            if(str(dictionary[key]) != ''):
                newDict[key] = dictionary[key]
        if(key in ['Status', 'Project_name', 'Priority', 'Resolution', 'DEV_resolution']):
            if dictionary[key]:
                newDict[key] = dictionary[key]
    return newDict

def checkEmptyElInList(dictionary):
    for el in dictionary:
        if(el == ''):
            return False
    return True

def toBool(val):
    if(val == 'Yes'):
        return True
    else: return False

def to_0_1(val):
    if(val == 'yes'):
        return 1
    else: return 0

def  rel_freq(ser, _bins):
    btt=numpy.array(list(ser))
    y_, x_, bars = plt.hist(btt, weights=numpy.zeros_like(btt) + 1. / btt.size, bins=_bins)
    return x_, y_

def  den_rel_freq(ser, _bins):
    btt=numpy.array(list(ser))
    y_, x_, bars = plt.hist(btt, bins=_bins, density=True)
    return x_, y_

def  den_rel_freq_gauss(ser):
    try:
        btt=numpy.array(list(ser))
        density = stats.kde.gaussian_kde(list(ser))
        x_den = numpy.linspace(0, ser.max(), ser.count())
        density = density(x_den)
        return x_den, density
    except numpy.linalg.linalg.LinAlgError: return [-1], [-1]

def data_for_plot(data):
    listFinal = []
    for list in data:
        listFinal.append(array_to_List(list))
    return listFinal

def array_to_List(array):
    myList = []
    for el in array:
        myList.append(el)
    return myList

def prepare_XY(data, x, y, scale, stepSize):
        dict = {}
        rezDict = {}
        valDict = {}
        if(y == 'Relative Frequency'):
            rezDict['Relative Frequency'] = data_for_plot(rel_freq(data[x].dropna().apply(int), 10))
            rezDict['scale'] = scale
            rezDict['stepSize'] = stepSize
            valDict['x'] = x
            valDict['y'] = y
            rezDict['fieldsVal'] = valDict
            return rezDict
        if(y == 'Frequency density'):
            dict['histogram'] = data_for_plot(den_rel_freq(data[x].dropna().apply(int), 'fd'))
            dict['line'] = data_for_plot(den_rel_freq_gauss(data[x].dropna().apply(int)))
            rezDict['Frequency density'] = dict
            rezDict['scale'] = scale
            rezDict['stepSize'] = stepSize
            valDict['x'] = x
            valDict['y'] = y
            rezDict['fieldsVal'] = valDict
            return rezDict

def add_0(dict):
    for key in dict:
        if(key == 'Relative Frequency'):
            masHist = dict[key]
            masHistY = masHist[1]
            masHistY.append(float(0))
            return dict
        if(key == 'Frequency density'):
            dictFr = dict['Frequency density']
            masHist = dictFr['histogram']
            masHistY = masHist[1]
            masHistY.append(float(0))
            return dict

class MyException(Exception):
    pass

def parseXML(xmlFile, markup, path):
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.WARNING, filename = u'mylog.log')
    global asigneeReporterFin
    try:
        xml = xmlFile.read()
        root = objectify.fromstring(xml)

        file = open(path, 'w')
        csvwriter = csv.writer(file)
        head = ["Issue_key", "Issue_id", "Summary", "Status", "Project_name", "Priority", "Resolution", "Created", "Resolved", "Affects_Ver", "Fix_Ver", "Components", "Labels", "Description", "is related to", "blocks", "is blocked by", "is duplicated by", "incorporates", "is incorporated by", "is dependant on", "has a dependency of", "resolves", "is resolved by", "DEV_Target_Fix_ver", "Reported_In", "Reported_In_Env", "Root_Cause_Analysis", "System", "Test_Name", "DEV_resolution", "Comments", "Attachments", "Version"]
        headMark = ["Issue_key", "Issue_id", "Summary", "Status", "Project_name", "Priority", "Resolution", "Created", "Resolved", "Affects_Ver", "Fix_Ver", "Components", "Labels", "Description", "is related to", "blocks", "is blocked by", "is duplicated by", "incorporates", "is incorporated by", "is dependant on", "has a dependency of", "resolves", "is resolved by", "DEV_Target_Fix_ver", "Reported_In", "Reported_In_Env", "Root_Cause_Analysis", "System", "Test_Name", "DEV_resolution", "Comments", "Attachments", "Version"]
        row = {"Issue_key": None, "Issue_id": None, "Summary": None, "Status": None, "Project_name": None, "Priority": None, "Resolution": None, "Created": None, "Resolved": None, "Affects_Ver": None, "Fix_Ver": None, "Components": None, "Labels": None, "Description": None, "is related to": None, "blocks": None, "is blocked by": None, "is duplicated by": None, "incorporates": None, "is incorporated by": None, "is dependant on": None, "has a dependency of": None, "resolves": None, "is resolved by": None, "DEV_Target_Fix_ver": None, "Reported_In": None, "Reported_In_Env": None, "Root_Cause_Analysis": None, "System": None, "Test_Name": None, "DEV_resolution": None, "Comments": None, "Attachments": None, "Version": None}
        if(markup == 1):
            csvwriter.writerow(headMark)
        else: csvwriter.writerow(head)
        countVersion = 0
        countComment = 0
        countAttachments = 0
        countComponent = ''
        countLabels = ''
        issuelinks = []
        fixVersion = ''
        countItem = 0
        version = ''
        asigneeReporter = []
        customFields = {"DEV target fix version": None, "reported in": None, "reported in\ environment": None, "root cause analysis": None, "system": None, "test name": None, "DEV resolution": None}

        tags = []
        #for rssChilds in root.getchildren():
        #    for channelChilds in rssChilds.getchildren():
        #        tags.append(channelChilds.tag)

        for rssChilds in root.getchildren():
            for channelChilds in rssChilds.getchildren():
                if(channelChilds.tag == 'item'):
                    countItem = countItem + 1
                    tags.append(channelChilds.tag)
                    try:
                        for chield in channelChilds.getchildren():
                            if(chield.tag == 'key'):
                                row["Issue_key"] = chield.text
                                row["Issue_id"] = chield.attrib['id']
                            if(chield.tag == 'status'):
                                row["Status"] = chield.text
                            if(chield.tag == 'summary'):
                                row["Summary"] = chield.text
                            if(chield.tag == 'project'):
                                row["Project_name"] = chield.text
                            if(chield.tag == 'priority'):
                                row["Priority"] = chield.text
                            if(chield.tag == 'resolution'):
                                row["Resolution"] = chield.text
                            if(chield.tag == 'created'):
                                row["Created"] = getDate(chield.text)
                            if(chield.tag == 'resolved'):
                                row["Resolved"] = getDate(chield.text)
                            if(chield.tag == 'description'):
                                row["Description"] = clean(chield.text)
                            if(chield.tag == 'version'):
                                countVersion = countVersion + 1
                                if(version != ''):
                                    version = version + ',' + chield.text
                                else: version = chield.text
                            if(chield.tag == 'component'):
                                if(countComponent != ''):
                                    countComponent = countComponent + ',' + chield.text
                                else:countComponent = chield.text
                            if(chield.tag == 'labels'):
                                for chieldLab in chield.getchildren():
                                    if(chieldLab.text != None):
                                        if(countLabels != ''):
                                            countLabels = countLabels + ',' + chieldLab.text
                                        else:countLabels = chieldLab.text
                            if(chield.tag == 'fixVersion'):
                                fixVersion = chield.text
                            if(chield.tag == 'issuelinks'):
                                try:
                                    issuelinks.append(chield.issuelinktype.name.text)
                                except AttributeError: logging.warning( u'In '+ xmlFile + ' for block \'Item\' № ' + countItem.__str__() + ':\n' + traceback.format_exc().splitlines()[traceback.format_exc().splitlines().__len__()-1])
                            if(chield.tag == 'customfields'):
                                for chieldCust in chield.getchildren():
                                    try:
                                        if(chieldCust.customfieldname.text.lower() in list(customFields.keys())):
                                            customFields[chieldCust.customfieldname.text.lower()] = chieldCust.customfieldvalues.customfieldvalue.text
                                    except AttributeError: logging.warning( u'In '+ xmlFile + ' for block \'Item\' № ' + countItem.__str__() + ':\n' + traceback.format_exc().splitlines()[traceback.format_exc().splitlines().__len__()-1])
                            if(chield.tag == 'comments'):
                                for comment in chield.getchildren():
                                    countComment = countComment + 1
                            if(chield.tag == 'attachments'):
                                for attachment in chield.getchildren():
                                    countAttachments = countAttachments + 1
                            if (chield.tag == 'assignee'):
                                asigneeReporter = asigneeReporter + chield.text.lower().split()
                            if (chield.tag == 'reporter'):
                                asigneeReporter = asigneeReporter + chield.text.lower().split()

                        row["Comments"] = countComment
                        row["Attachments"] = countAttachments
                        row["Version"] = version
                        row["Affects_Ver"] = countVersion
                        row["Fix_Ver"] = fixVersion
                        row["Components"] = countComponent
                        row["Labels"] = countLabels
                        row = issuelinksF(row, issuelinks)
                        row["DEV_Target_Fix_ver"] = customFields["DEV target fix version"]
                        row["Reported_In"] = customFields["reported in"]
                        row["Reported_In_Env"] = customFields["reported in\ environment"]
                        row["Root_Cause_Analysis"] = customFields["root cause analysis"]
                        row["System"] = customFields["system"]
                        if(customFields["test name"] == None):
                            row["Test_Name"] = 0
                        else: row["Test_Name"] = 1
                        row["DEV_resolution"] = customFields["DEV resolution"]

                        if(markup == 1):
                            csvwriter.writerow(dictionaryToList(row, markup))
                        else:
                            csvwriter.writerow(dictionaryToList(row, markup))

                        countVersion = 0
                        countComponent = ''
                        countLabels = ''
                        issuelinks = []
                        cleanDictionary(customFields)
                        cleanDictionary(row)
                        countAttachments = 0
                        countComment = 0
                        fixVersion = ''
                        version = ''
                    except AttributeError:
                        logging.warning( u'In '+ xmlFile + ' for block \'Item\' № ' + countItem.__str__() + ':\n' + traceback.format_exc().splitlines()[traceback.format_exc().splitlines().__len__()-1])
            if 'item' not in tags:
                return 'incorrect format for xml'
        asigneeReporterFin = list(set(asigneeReporter))
    except Exception:
        return 'incorrect format for xml'

def getDate(date):
    if(date == None):
        return ''
    d = dt.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
    day = d.day.__str__()
    month = d.month.__str__()
    if(d.day.__str__().__len__()==1):
        day = '0'+day
    if(d.month.__str__().__len__()==1):
        month = '0'+month

    date =day +'-'+month+'-'+d.year.__str__()
    return date

def clean(text):
    if text is None:
        return None
    else:
        p1 = r'&lt;p&gt;'
        p2 = r'</?p>'
        p3 = r'&amp;'
        p4 = r'&gt;'
        p5 = r'&lt;'
        remove_pat = [p1, p2, p3, p4, p5]
        test_clean=text
        for el in remove_pat:
            test_clean=re.sub(el, ' ', test_clean)
        return test_clean

def dictionaryToList(dictionary, markup):

    listForWrite = []

    listForWrite.append(dictionary["Issue_key"])
    listForWrite.append(dictionary["Issue_id"])
    listForWrite.append(dictionary["Summary"])
    listForWrite.append(dictionary["Status"])
    listForWrite.append(dictionary["Project_name"])
    listForWrite.append(dictionary["Priority"])
    listForWrite.append(dictionary["Resolution"])
    listForWrite.append(dictionary["Created"])
    listForWrite.append(dictionary["Resolved"])
    listForWrite.append(dictionary["Affects_Ver"])
    listForWrite.append(dictionary["Fix_Ver"])
    listForWrite.append(dictionary["Components"])
    listForWrite.append(dictionary["Labels"])
    listForWrite.append(dictionary["Description"])
    listForWrite.append(dictionary["is related to"])
    listForWrite.append(dictionary["blocks"])
    listForWrite.append(dictionary["is blocked by"])
    listForWrite.append(dictionary["is duplicated by"])
    listForWrite.append(dictionary["incorporates"])
    listForWrite.append(dictionary["is incorporated by"])
    listForWrite.append(dictionary["is dependant on"])
    listForWrite.append(dictionary["has a dependency of"])
    listForWrite.append(dictionary["resolves"])
    listForWrite.append(dictionary["is resolved by"])
    listForWrite.append(dictionary["DEV_Target_Fix_ver"])
    listForWrite.append(dictionary["Reported_In"])
    listForWrite.append(dictionary["Reported_In_Env"])
    listForWrite.append(dictionary["Root_Cause_Analysis"])
    listForWrite.append(dictionary["System"])
    listForWrite.append(dictionary["Test_Name"])
    listForWrite.append(dictionary["DEV_resolution"])
    listForWrite.append(dictionary["Comments"])
    listForWrite.append(dictionary["Attachments"])
    listForWrite.append(dictionary["Version"])
    return listForWrite

def issuelinksF(dictionary, issuelinks):
    dictionary["is related to"] = 0
    dictionary["blocks"] = 0
    dictionary["is blocked by"] = 0
    dictionary["is duplicated by"] = 0
    dictionary["incorporates"] = 0
    dictionary["is incorporated by"] = 0
    dictionary["is dependant on"] = 0
    dictionary["has a dependency of"] = 0
    dictionary["resolves"] = 0
    dictionary["is resolved by"] = 0

    for el in issuelinks:
        if(el.lower() == "is related to"):
            dictionary["is related to"] = 1
        if(el.lower() == "blocks"):
            dictionary["blocks"] = 1
        if(el.lower() == "is blocked by"):
            dictionary["is blocked by"] = 1
        if(el.lower() == "is duplicated by"):
            dictionary["is duplicated by"] = 1
        if(el.lower() == "incorporates"):
            dictionary["incorporates"] = 1
        if(el.lower() == "is incorporated by"):
            dictionary["is incorporated by"] = 1
        if(el.lower() == "is dependant on"):
            dictionary["is dependant on"] = 1
        if(el.lower() == "has a dependency of"):
            dictionary["has a dependency of"] = 1
        if(el.lower() == "resolves"):
            dictionary["resolves"] = 1
        if(el.lower() == "is resolved by"):
            dictionary["is resolved by"] = 1

    return dictionary

def cleanDictionary(dictionary):
    for el in dictionary:
        dictionary[el] = None

def check_scale_step(scale, stepSize, x, statInfo):
    if(scale == '' and stepSize == ''):
        return True
    elif(scale != '' and stepSize == ''):
        if(isinstance(string_to_float(scale), float)):
            return validate_step_scale(string_to_float(scale), x, statInfo)
        else: return 'incorrect value'
    elif(stepSize != '' and scale ==''):
        if(isinstance(string_to_float(stepSize), float)):
            return validate_step_scale(string_to_float(stepSize), x, statInfo)
        else: return 'incorrect value'
    elif(scale != '' and stepSize != ''):
        if(isinstance(string_to_float(stepSize), float) and isinstance(string_to_float(scale), float)):
            return validate_step_scale(string_to_float(scale), x, statInfo) and validate_step_scale(string_to_float(stepSize), x, statInfo)
        else: 'incorrect value'
    else: return False

def validate_step_scale(param, x, statInfo):
    if(x == 'ttr' and param >= 0 and param <= float(statInfo['ttrStat']['max'])):
        return True
    if(x == 'Comments' and param >= 0 and param <= float(statInfo['commentStat']['max'])):
        return True
    if(x == 'Attachments' and param >= 0 and param <= float(statInfo['attachmentStat']['max'])):
        return True
    return False

def string_to_float(val):
    if check_float(val):
        return float(val)
    elif try_convert_float(val):
        return float(val.replace(',', '.'))
    else: return False

def check_float(val):
    try:
        float(val)
        return True
    except:
        return False

def try_convert_float(val):
    try:
        float(val.replace(',', '.'))
        return True
    except:
        return False

def dynamic_bug_chart(frame, stepSize):
    plot = {}
    dynamic_bugs = []
    x = []
    y = []
    plot['period'] = stepSize
    if(stepSize == 'W-SUN'):
        periods = get_periods(frame, stepSize)
        if(len(periods) == 0):
            return 'error'
        cumulative = 0
        for period in periods:
            if(pandas.to_datetime(period[0]) < pandas.to_datetime(frame['date_created']).min()):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(frame['date_created']).min()) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(period[1]))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(datetime.datetime.date(pandas.to_datetime(frame['date_created'], format='%Y-%m-%d').min())))
                y.append(cumulative)
            else:
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(period[0])) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(period[1]))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str((period[0])))
                y.append(cumulative)
        if(pandas.to_datetime(frame['date_created']).max() > pandas.to_datetime(periods[-1][1])):
            newFrame = frame[(pandas.to_datetime(frame['date_created']) > pandas.to_datetime(periods[-1][1])) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(frame['date_created']).max())]
            cumulative = cumulative + int(newFrame['Issue_key'].count())
            x.append(str(datetime.datetime.date(pandas.to_datetime(periods[-1][1], format='%Y-%m-%d'))+datetime.timedelta(days=1)))
            y.append(cumulative)
        dynamic_bugs.append(x)
        dynamic_bugs.append(y)
        plot['dynamic bugs'] = dynamic_bugs
        cumulative = 0
        return plot
    if(stepSize in ['7D', '10D', '3M', '6M', 'A-DEC']):
        count0 = 0
        count1 = 1
        periods = get_periods(frame, stepSize)
        if(len(periods) == 0):
            return 'error'
        cumulative = 0
        countPeriodsList = len(periods)
        count = 1
        if(countPeriodsList == 1):
            if(stepSize == '7D'):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(frame['date_created']).min()) & (pandas.to_datetime(frame['date_created']) < pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=7)))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(frame['date_created'], format='%Y-%m-%d').min()), stepSize)))
                y.append(cumulative)
                if(pandas.to_datetime(frame['date_created']).max() > pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=7))):
                    newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=7))) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(frame['date_created']).max())]
                    cumulative = cumulative + int(newFrame['Issue_key'].count())
                    x.append(str(getDateForDynamicMY((datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=7)), stepSize)))
                    y.append(cumulative)
                cumulative = 0
            if(stepSize == '10D'):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(frame['date_created']).min()) & (pandas.to_datetime(frame['date_created']) < pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=10)))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(frame['date_created'], format='%Y-%m-%d').min()), stepSize)))
                y.append(cumulative)
                if(pandas.to_datetime(frame['date_created']).max() > pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=10))):
                    newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=10))) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(frame['date_created']).max())]
                    cumulative = cumulative + int(newFrame['Issue_key'].count())
                    x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min())+datetime.timedelta(days=10), stepSize)))
                    y.append(cumulative)
                cumulative = 0
            if(stepSize == '3M'):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(frame['date_created']).min()) & (pandas.to_datetime(frame['date_created']) < pandas.to_datetime(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 3)))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(frame['date_created'], format='%Y-%m-%d').min()), stepSize)))
                y.append(cumulative)
                if(pandas.to_datetime(frame['date_created']).max() > pandas.to_datetime(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 3))):
                    newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 3))) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(frame['date_created']).max())]
                    cumulative = cumulative + int(newFrame['Issue_key'].count())
                    x.append(str(getDateForDynamicMY(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 3), stepSize)))
                    y.append(cumulative)
                cumulative = 0
            if(stepSize == '6M'):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(frame['date_created']).min()) & (pandas.to_datetime(frame['date_created']) < pandas.to_datetime(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 6)))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(frame['date_created'], format='%Y-%m-%d').min()), stepSize)))
                y.append(cumulative)
                if(pandas.to_datetime(frame['date_created']).max() > pandas.to_datetime(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 6))):
                    newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 6))) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(frame['date_created']).max())]
                    cumulative = cumulative + int(newFrame['Issue_key'].count())
                    x.append(str(getDateForDynamicMY(add_months(datetime.datetime.date(pandas.to_datetime(frame['date_created']).min()), 6), stepSize)))
                    y.append(cumulative)
                cumulative = 0
            if(stepSize == 'A-DEC'):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(frame['date_created']).min()) & (pandas.to_datetime(frame['date_created']) < pandas.to_datetime(str(int(periods[0])+1)))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(frame['date_created'], format='%Y-%m-%d').min()), stepSize)))
                y.append(cumulative)
                if(pandas.to_datetime(frame['date_created']).max() > pandas.to_datetime(str(int(periods[0])+1))):
                    newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(str(int(periods[0])+1))) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(frame['date_created']).max())]
                    cumulative = cumulative + int(newFrame['Issue_key'].count())
                    x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(str(int(periods[0])+1))), stepSize)))
                    y.append(cumulative)
                cumulative = 0
        else:
            while(count < countPeriodsList):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(periods[count0])) & (pandas.to_datetime(frame['date_created']) < pandas.to_datetime(periods[count1]))]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(periods[count0], format='%Y-%m-%d')), stepSize)))
                y.append(cumulative)
                count0 = count0 +1
                count1 = count1 +1
                count = count +1
            if(pandas.to_datetime(frame['date_created']).max() >= pandas.to_datetime(periods[-1])):
                newFrame = frame[(pandas.to_datetime(frame['date_created']) >= pandas.to_datetime(periods[-1])) & (pandas.to_datetime(frame['date_created']) <= pandas.to_datetime(frame['date_created']).max())]
                cumulative = cumulative + int(newFrame['Issue_key'].count())
                x.append(str(getDateForDynamicMY(datetime.datetime.date(pandas.to_datetime(periods[-1], format='%Y-%m-%d')), stepSize)))
                y.append(cumulative)
            cumulative = 0
        dynamic_bugs.append(x)
        dynamic_bugs.append(y)
        plot['dynamic bugs'] = dynamic_bugs
        return plot

def get_periods(frame, period):
    periods = []
    periodsFrame = pandas.period_range(start=pandas.to_datetime(frame['date_created']).min(), end=pandas.to_datetime(frame['date_created']).max(), freq=period)
    if(period == 'W-SUN'):
        for period in periodsFrame:
            periods.append(str(period).split('/'))
    if(period in ['7D', '10D', '3M', '6M', 'A-DEC']):
        for period in periodsFrame:
            periods.append(str(period))
    return periods

def add_months(sourcedate, months):
     month = sourcedate.month - 1 + months
     year = sourcedate.year + month // 12
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year, month)[1])
     return year.__str__() + '-' + month.__str__()

def parse_period(period):
    if(period == '1 week'):
        return 'W-SUN'
    if(period == '10 days'):
        return '10D'
    if(period == '3 months'):
        return '3M'
    if(period == '6 months'):
        return '6M'
    if(period == '1 year'):
        return 'A-DEC'

def combine_charts(distr, dynamic):
    distr['dynamic bugs'] = dynamic
    return distr

def getDateForDynamicMY(date, stepSize):
    if(date == None):
        return ''
    if(stepSize == '10D'):
        day = date.day.__str__()
        month = date.month.__str__()
        if(date.day.__str__().__len__()==1):
            day = '0'+day
        if(date.month.__str__().__len__()==1):
            month = '0'+month
        date =day +'-'+month+'-'+date.year.__str__()
        return date
    if(stepSize in ['3M', '6M']):
        month = date.month.__str__()
        if(date.month.__str__().__len__()==1):
            month = '0'+month
        date = date.year.__str__() + '-' + month
        return date
    if(stepSize == 'A-DEC'):
        return date.year.__str__()

def friquency_stat(data):
    SW = text.ENGLISH_STOP_WORDS.union(asigneeReporterFin, myStopWords)
    tfidf = StemmedTfidfVectorizer(norm='l2', sublinear_tf=True, min_df=1, stop_words=SW, analyzer='word', max_features=1000)

    tfs = tfidf.fit_transform(parallelize(data['descr'], cleanDescr))

    idf = tfidf.idf_
    voc_feat = dict(zip(tfidf.get_feature_names(), idf))

    voc_feat_s = OrderedDict((k, v) for k, v in sorted(voc_feat.items(), key=lambda x: x[1], reverse=True))
    return list(voc_feat_s.keys())[:100]

def defaultsCleanForTop(text, remove_pat):
    if text is None:
        return None
    else:
        test_clean = text
        for el in remove_pat:
            test_clean = re.sub(el, ' ', test_clean)
        return test_clean

def top_terms(data, metric, field):
    chi2 = feature_selection.chi2
    SW = text.ENGLISH_STOP_WORDS.union(asigneeReporterFin, myStopWords)
    tfidf = StemmedTfidfVectorizer(norm='l2', sublinear_tf=True, min_df=1, stop_words=SW, analyzer='word', max_features=1000)

    bidata = pandas.get_dummies(data, prefix=[field], columns=[field])

    tfs = tfidf.fit_transform(parallelize(bidata['descr'], cleanDescr))

    y = bidata[metric]
    selector = SelectKBest(score_func=chi2, k='all')
    selector.fit_transform(tfs, y)
    X_new = dict(zip(tfidf.get_feature_names(), selector.scores_))

    temp_dict = OrderedDict((k, v) for k, v in sorted(X_new.items(), key=lambda x: x[1], reverse=True))
    return list(temp_dict.keys())[:20]

def get_topPriority(frame, field):
    if(field.split()[0] == 'Priority'):
        return top_terms(frame, 'Priority_' + ' '.join(e for e in field.split()[1:]), 'Priority')
    if(field.split()[0] == 'Resolution'):
        return top_terms(frame, 'Resolution_' + ' '.join(e for e in field.split()[1:]), 'Resolution')

def save_significanceTop(referenceTo, significanceTop):
    global SignificanceTop
    if referenceTo in significanceTop.keys():
        return significanceTop[referenceTo]
    else:
        significanceTop[referenceTo] = get_topPriority(origFrame, referenceTo)
        return significanceTop[referenceTo]

def parallelize(data, func):
    cores = cpu_count()
    split = numpy.array_split(data, cores)
    pool = Pool(cores)
    data = pandas.concat(pool.map(func, split))
    pool.close()
    pool.join()
    return data

def cleanDescr(data):
    return data.apply(defaultsCleanForTop, args=(remove_pat,)).fillna(value='aftercleaning')

def categorical(dict, field):
    if field not in dict.keys():
        return []
    else: return dict[field]

def collabels(data,list_pat, list_aot, colname, field):
    global columns
    columns.append(list_aot+colname)
    data[list_aot+colname] = data[field].str.contains(list_pat.strip(), case=False, na=False, regex=True).astype(int)
    return data

def other_lab(frame, columns):
    other = pandas.Series([])
    for count in range(len(frame.index)):
        other[count] = 1
        for column in columns:
            if(frame[column].iloc[count] == 1):
                other[count] = 0
                break
            else: continue
    return other

def training_imbalance_kf (X_, Y_, TFIDF_, IMB_, FS_,pers_,CLF_, name_):
    transform = feature_selection.SelectPercentile(FS_)
    clf_model = Pipeline([('tfidf', TFIDF_),('imba', IMB_),('fs', transform), ('clf', CLF_)])
    kf = KFold(n_splits=10)
    kf.get_n_splits(X_)
    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X_,Y_,train_size=.8, stratify=Y_)
    for train_index, test_index in kf.split(X_):
        X_train, X_test = X_[train_index], X_[test_index]
        y_train, y_test = Y_[train_index], Y_[test_index]

    clf_model.set_params(fs__percentile=pers_).fit(X_train, y_train)
    pickle.dump(clf_model, open(mymodel+name_+'.sav', 'wb'))
    #y_pred = clf_model.predict(X_test)
    #print(classification_report(y_test, y_pred))
    return

def ifZero(val):
    if val<0:
        return 0
    else: return val

def sortIntervals(list):
    print(list)
    list.sort()
    print(list.sort())
    newList = list.sort()
    return [str(newList[0])+'-'+str(newList[1]), str(newList[1])+'-'+str(newList[2]), str(newList[2])+'-'+str(newList[3]), '>'+str(newList[3])]

def create_config(path):
    config = configparser.ConfigParser()
    config.add_section("SingleMod")
    with open(path, "w") as config_file:
        config.write(config_file)

def update_setting(path, section, setting, value):
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)

def get_config(path):
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config

def get_setting(path, section, setting):
    config = get_config(path)
    value = config.get(section, setting)
    return value

def checkSingle():
    try:
        get_config(path)
        if(get_setting(path, 'SingleMod', 'prior_col_class') and get_setting(path, 'SingleMod', 'ttr_col_class') and get_setting(path, 'SingleMod', 'fix_col_class') and get_setting(path, 'SingleMod', 'rej_col_class') and get_setting(path, 'SingleMod', 'columns') and get_setting(path, 'SingleMod', 'binary_col_class')):
            return True
        else: False
    except Exception: return False

@app.route('/trainingModel', methods = ['GET', 'POST'])
def trainingModel():
    SW = text.ENGLISH_STOP_WORDS.union(asigneeReporterFin, myStopWords)
    smt = SMOTE(ratio='minority', random_state=0, kind='borderline1')
    svm_imb = SVC(gamma=2, C=1, probability=True, class_weight='balanced')
    tfidf_imb = StemmedTfidfVectorizer(norm='l2',sublinear_tf=True, stop_words=SW, analyzer='word', max_df=0.5, max_features=500)
    anova=feature_selection.f_classif
    chi2=feature_selection.chi2
    if not os.path.exists('../model'):
        os.makedirs('../model')

    for col in columns:
        training_imbalance_kf(newData['descr'], newData[col], tfidf_imb, smt, chi2, 50, svm_imb, col+'_svmImb_chi2_smt_timb')

    newData['Priority_ord'] = newData['Priority'].astype("category")
    training_imbalance_kf(newData['descr'], newData['Priority_ord'], tfidf_imb, smt, chi2, 50, svm_imb, 'priority_svmImb_chi250_smt_timb')

    bins = 4
    ldis=[i for i in range(1, bins+1)]
    newData['temp_ttr_class'] = pandas.qcut(newData['ttr'], bins, labels=ldis, duplicates='drop')
    training_imbalance_kf(newData['descr'], newData['temp_ttr_class'], tfidf_imb, smt, chi2, 50, svm_imb, 'ttr_svmImb_chi250_smt_timb')

    bin_data = pandas.get_dummies(newData, prefix=['Resolution'], columns=['Resolution'])
    training_imbalance_kf(bin_data['descr'], bin_data['Resolution_Out of Date'], tfidf_imb, smt, chi2, 50, svm_imb, 'Resolution_Out of Date_svmImb_chi250_smt_timb')
    training_imbalance_kf(bin_data['descr'], bin_data['Resolution_Rejected'], tfidf_imb, smt, chi2, 50, svm_imb, 'Resolution_Rejected_svmImb_chi250_smt_timb')
    training_imbalance_kf(bin_data['descr'], bin_data["Resolution_Won't Fix"], tfidf_imb, smt, chi2, 50, svm_imb, "Resolution_Won't Fix_svmImb_chi250_smt_timb")

    create_config(path)
    update_setting(path, 'SingleMod', 'prior_col_class', ','.join(newData['Priority'].fillna('null').unique().tolist()))
    update_setting(path, 'SingleMod', 'binary_col_class', ','.join(['0', '1']))
    update_setting(path, 'SingleMod', 'fix_col_class', ','.join(['Fix', 'Wont Fix']))
    update_setting(path, 'SingleMod', 'rej_col_class', ','.join(['Not reject', 'Reject']))
    ttr_col_classTemp = pandas.qcut(newData['ttr'], 4,duplicates='drop').unique()
    update_setting(path, 'SingleMod', 'ttr_col_class', ','.join([str(ifZero(ttr_col_classTemp[0].left))+'-'+str(ifZero(ttr_col_classTemp[0].right)), str(ifZero(ttr_col_classTemp[1].left))+'-'+str(ifZero(ttr_col_classTemp[1].right)), str(ifZero(ttr_col_classTemp[2].left))+'-'+str(ifZero(ttr_col_classTemp[2].right)), '>'+str(ifZero(ttr_col_classTemp[2].right))]))
    update_setting(path, 'SingleMod', 'columns', ','.join(columns))

    return jsonify({'message': 'model trained', 'statInfo': statInfo, 'categoric': categoricDict, 'attributes': clearDictionary, 'plot': combine_charts(add_0(prepare_XY(newData, 'ttr', 'Relative Frequency', '', '')), dynamic_bug_chart(newData, 'W-SUN')), 'markup': str(murkup), 'singleMod': checkSingle()})

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    global origFrame
    global murkup
    global SignificanceTop
    global origFreqTop
    global asigneeReporterFin
    global statInfo
    global categoricDict
    global clearDictionary
    global columns
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            murkup = 0#to_0_1(request.form['murkup'])
            asigneeReporterFin = []
            newFile = open_file(file, murkup)
            if(isinstance(newFile, str)):
                return render_template('filterPage.html', json=json.dumps({'message': newFile}))
            origFrame = newFile
            categoricDict = categorical_json(origFrame, murkup)
            if(isinstance(categoricDict, str)):
                return render_template('filterPage.html', json = json.dumps({'message': categoricDict}))
            if(isinstance(transform_fields(origFrame), str)):
                return render_template('filterPage.html', json = json.dumps({'message': transform_fields(origFrame)}))
            trFrame = transform_fields(origFrame)
            columns = []
            if request.form['areas']:
                for pattern in request.form['areas'].split(','):
                    trFrame = collabels(trFrame, pattern.split('=')[1], pattern.split('=')[0], '_lab', 'components')
                trFrame['Other_lab'] = other_lab(trFrame, columns)
                columns.append('Other_lab')
            statInfo = get_statInfo(trFrame)
            period = 'W-SUN'
            origFreqTop = friquency_stat(trFrame)
            SignificanceTop = {categoricDict['ReferringTo'][0]: top_terms(origFrame, 'Priority_' + categoricDict['Priority'][0], 'Priority')}
            clearDictionary = {'SignificanceTop': SignificanceTop[categoricDict['ReferringTo'][0]], 'ReferringTo': 'Priority '+categoricDict['Priority'][0], 'freqTop': origFreqTop}
            return render_template('filterPage.html', json=json.dumps({'message': 'file uploaded successfully', 'statInfo': statInfo, 'categoric': categoricDict, 'plot': combine_charts(add_0(prepare_XY(trFrame, 'ttr', 'Relative Frequency', '', '')), dynamic_bug_chart(trFrame, period)), 'markup': str(murkup), 'attributes': {'SignificanceTop': SignificanceTop[categoricDict['ReferringTo'][0]], 'ReferringTo': 'Priority '+categoricDict['Priority'][0], 'freqTop': origFreqTop}, 'singleMod': checkSingle()}))
        else: return render_template('filterPage.html', json=json.dumps({'message': 'incorrect file format. Please use only xml'}))

@app.route('/buildChart/onlyDynamic/', methods = ['GET', 'POST'])
def build_onlyDynamic_chart():
    if request.method == 'POST':
        period = parse_period(request.args.get('period', default='W-SUN', type=str))
        return jsonify({'message': 'chart builded', 'statInfo': statInfo, 'categoric': categoricDict, 'plot': dynamic_bug_chart(newData, period), 'attributes': clearDictionary, 'markup': str(murkup)})

@app.route('/buildChart/onlyDistribution/', methods = ['GET', 'POST'])
def build_onlyDistribution_chart():
    if request.method == 'POST':
        scale = request.form['scale']
        stepSize = request.form['stepSize']
        x = request.form['x']
        y = request.form['y']
        if(len(newData)<=1 and y=='Frequency density'):
            return jsonify({'message': 'you are cannot to build frequency density chart for data with one value', 'statInfo': statInfo, 'categoric': categoricDict, 'attributes': clearDictionary, 'plot': add_0(prepare_XY(newData, x, 'Relative Frequency', '', '')), 'markup': str(murkup)})
        if(check_scale_step(scale, stepSize, x, statInfo) == 'incorrect value'):
            return jsonify({'message': 'incorrect value for Xmax or StepSize', 'statInfo': statInfo, 'categoric': categoricDict, 'attributes': clearDictionary, 'plot': add_0(prepare_XY(newData, x, y, '', '')), 'markup': str(murkup)})
        elif(check_scale_step(scale, stepSize, x, statInfo)):
            return jsonify({'message': 'chart builded', 'statInfo': statInfo, 'categoric': categoricDict, 'plot': add_0(prepare_XY(newData, x, y, scale, stepSize)), 'attributes': clearDictionary, 'markup': str(murkup)})
        else:
            return jsonify({'message': 'please use Xmax and StepSize value in the array [0,maxValue from stat info]', 'statInfo': statInfo, 'categoric': categoricDict, 'attributes': clearDictionary, 'plot':add_0(prepare_XY(newData, x, y, '', '')), 'markup': str(murkup)})


@app.route('/filtering', methods = ['GET', 'POST'])
def filter():
    global newData
    global statInfo
    global categoricDict
    global clearDictionary
    if request.method == 'POST':
        varDictionary = {}
        varDictionary['Comments2'] = request.form['Comments2']
        varDictionary['Comments4'] = request.form['Comments4']
        varDictionary['Attachments2'] = request.form['Attachments2']
        varDictionary['Attachments4'] = request.form['Attachments4']
        varDictionary['Date_created2'] = request.form['Date_created2']
        varDictionary['Date_created4'] = request.form['Date_created4']
        varDictionary['Date_resolved2'] = request.form['Date_resolved2']
        varDictionary['Date_resolved4'] = request.form['Date_resolved4']
        varDictionary['TTR2'] = request.form['TTR2']
        varDictionary['TTR4'] = request.form['TTR4']
        varDictionary['Issue_key'] = request.form['Issue_key']
        varDictionary['Summary'] = request.form['summary']
        varDictionary['Status'] = categorical(request.form.to_dict(flat=False), 'Status')
        varDictionary['Project_name'] = categorical(request.form.to_dict(flat=False), 'Project_name')
        varDictionary['Priority'] = categorical(request.form.to_dict(flat=False), 'Priority')
        varDictionary['Resolution'] = categorical(request.form.to_dict(flat=False), 'Resolution')
        varDictionary['Components'] = request.form['Components']
        varDictionary['Labels'] = request.form['labels']
        varDictionary['Description'] = request.form['description']
        varDictionary['Version'] = request.form['Version']
        varDictionary['DEV_resolution'] = categorical(request.form.to_dict(flat=False), 'DEV_resolution')
        varDictionary['ReferringTo'] = request.args.get('ReferringTo', type=str)
        categoricDict = categorical_json(newData, murkup)
        clearDictionary = fields_for_filtration(varDictionary)

        dictForParseInt = {}
        dictForParseDate = {}
        for key in ['Comments2', 'Comments4', 'Attachments2', 'Attachments4', 'TTR2', 'TTR4']:
            if key in clearDictionary:
                dictForParseInt[key] = clearDictionary[key]
        for key in ['Date_created2', 'Date_created4', 'Date_resolved2', 'Date_resolved4']:
            if key in clearDictionary:
                dictForParseDate[key] = clearDictionary[key]
        result = merge_two_dicts(parseToIntFinal(dictForParseInt), parseToDateFinal(dictForParseDate))
        dictForFiltration = merge_two_dicts(clearDictionary, result)
        checkDict = checkLeftRigthWithoutSings(dictForFiltration)

        for key in checkDict:
            newData = filtration(key, checkDict[key], newData)
            if(newData.empty):
                clearDictionary = categorical_json(origFrame, murkup)
                return jsonify({'message': 'there are no rows corresponding to the condition', 'statInfo': drop_filter(), 'categoric': categoricDict, 'plot': combine_charts(add_0(prepare_XY(origFrame, 'ttr', 'Relative Frequency', '', '')), dynamic_bug_chart(origFrame, 'W-SUN')), 'markup': str(murkup), 'freqTop': friquency_stat(origFrame)})
        statInfo = get_statInfo(newData)
        categoricDict = categorical_json(newData, murkup)
        clearDictionary['freqTop'] = friquency_stat(newData)
        clearDictionary['SignificanceTop'] = save_significanceTop(varDictionary['ReferringTo'], SignificanceTop)
        return jsonify({'message': 'data filtered', 'statInfo': statInfo, 'categoric': categoricDict, 'attributes': clearDictionary, 'plot': combine_charts(add_0(prepare_XY(newData, 'ttr', 'Relative Frequency', '', '')), dynamic_bug_chart(newData, 'W-SUN')), 'markup': str(murkup)})

@app.route('/resetFilter', methods = ['GET', 'POST'])
def resetFilter():
    if request.method == 'POST':
        return jsonify({'message': 'filter dropped', 'statInfo': drop_filter(), 'categoric': categoricDict, 'plot': combine_charts(add_0(prepare_XY(origFrame, 'ttr', 'Relative Frequency', '', '')), dynamic_bug_chart(origFrame, 'W-SUN')), 'markup': str(murkup), 'attributes': {'SignificanceTop': SignificanceTop[categoricDict['ReferringTo'][0]], 'ReferringTo': categoricDict['ReferringTo'][0], 'freqTop': origFreqTop}})

@app.route('/saveSubset', methods = ['GET', 'POST'])
def saveSubset():
    global tempFiles
    if request.method == 'POST':
        fileName = request.form['fileName']
        save_file(newData, fileName, murkup)
        tempFiles.append(app.config['UPLOAD_FOLDER']+'/'+secure_filename(fileName))
        return send_from_directory(app.config['UPLOAD_FOLDER'], fileName, as_attachment=True)

@app.route('/delTempFiles', methods = ['GET', 'POST'])
def delTempFiles():
    global tempFiles
    if request.method == 'POST':
        for path in tempFiles:
            os.remove(path)
        tempFiles = []
        return 'done'

@app.route('/significanceTop', methods = ['GET', 'POST'])
def significanceTop():
    if request.method == 'POST':
        ReferringTo = request.form['ReferringTo']
        return jsonify({'SignificanceTop': save_significanceTop(ReferringTo, SignificanceTop)})

@app.route('/singleMod',methods = ['POST', 'GET'])
def singleMod():
    global description1
    return render_template('resultSinglePage.html', json=json.dumps({'description1': description1}))

@app.route('/result', methods = ['POST', 'GET'])
def result():
    '''
    prior_col_class = newData['Priority'].fillna('null').unique().tolist()
    binary_col_class = [0, 1]
    fix_col_class = ['Fix', 'Wont Fix']
    rej_col_class = ['Not reject', 'Reject']
    ttr_col_classTemp = pandas.qcut(newData['ttr'], 4,duplicates='drop').unique()
    ttr_col_class = [str(ifZero(ttr_col_classTemp[0].left))+'-'+str(ifZero(ttr_col_classTemp[0].right)), str(ifZero(ttr_col_classTemp[1].left))+'-'+str(ifZero(ttr_col_classTemp[1].right)), str(ifZero(ttr_col_classTemp[2].left))+'-'+str(ifZero(ttr_col_classTemp[2].right)), '>'+str(ifZero(ttr_col_classTemp[2].right))]
    '''
    '''
    descr = re.sub('/',' ', request.form['descr'])
    priority_prob = proc_text(descr, prior_col_class, 'priority_svmImb_chi250_smt_timb')
    ttr_prob = proc_text(descr, ttr_col_class, 'ttr_svmImb_chi250_smt_timb')
    wontfix_prob = proc_text(descr, fix_col_class, "Resolution_Won't Fix_svmImb_chi250_smt_timb")
    reject_prob = proc_text(descr, rej_col_class, 'Resolution_Rejected_svmImb_chi250_smt_timb')
    '''
    descr = re.sub('/',' ', request.form['descr'])
    priority_prob = proc_text(descr, get_setting(path, 'SingleMod', 'prior_col_class').split(','), 'priority_svmImb_chi250_smt_timb')
    ttr_prob = proc_text(descr, get_setting(path, 'SingleMod', 'ttr_col_class').split(','), 'ttr_svmImb_chi250_smt_timb')
    wontfix_prob = proc_text(descr, get_setting(path, 'SingleMod', 'fix_col_class').split(','), "Resolution_Won't Fix_svmImb_chi250_smt_timb")
    reject_prob = proc_text(descr, get_setting(path, 'SingleMod', 'rej_col_class').split(','), 'Resolution_Rejected_svmImb_chi250_smt_timb')

    area_prob = {}
    for column in get_setting(path, 'SingleMod', 'columns').split(','):
        tmp = proc_text(descr, get_setting(path, 'SingleMod', 'binary_col_class').split(','), column+'_svmImb_chi2_smt_timb')
        area_prob.update({column.split('_')[0]: float(tmp['1'])})

    t = tuple(key for key, value in area_prob.items() if value > 0.5)
    s = ''
    recom = ''
    for i in range(len(t)):
        s = s + t[i]+'    '
    if s=='':
        recom = "no idea"
    else:
        recom = s

    return jsonify({'descr': descr, 'recom': recom, 'prio': priority_prob, 'ttr': ttr_prob, 'wontfix': wontfix_prob, 'reject': reject_prob, 'areas': area_prob})

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False)
