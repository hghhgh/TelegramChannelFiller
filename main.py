# coding=utf-8
import json

__author__ = 'ghiassi'

# need to install Telegram Bot package by 'sudo pip install python-telegram-bot'

# from kivy.app import App
# from kivy.uix.button import Button

import numpy as np
import pickle
import telegram
import requests
import html2texthgh
from random import randint
from lxml import html
import csv
from BeautifulSoup import BeautifulSoup
import re
from datetime import datetime
import time
import random
from PIL import Image
import urllib, cStringIO
import uuid
import os
import Image
import ImageFont, ImageDraw
from bidi.algorithm import get_display
import arabic_reshaper
import ssl

state = {}


def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i


def get_bot():
    bot = telegram.Bot('300284060:AAG2uEoyvarn8-fmckiApm7iDLkjWS8JKwY')  # Telegram Bot Authorization Token
    return bot


def sendTitle():
    bot = get_bot()

    cap = ''
    cap += 'هر روز با دانش جدید.' + '\n'
    cap += ' جملات روز را اینجا بخوانید :' + '\n'
    cap += 'تقویم روز' + '\n'
    cap += 'هر روز یک آیه' + '\n'
    cap += 'حدیث روز' + '\n'
    cap += 'یک بیت از حافظ' + '\n'
    cap += 'جملات بزرگان' + '\n'
    cap += 'دانستنی ها' + '\n'
    cap += 'طب اسلامی' + '\n'
    cap += 'و...' + '\n'
    # cap = '' + '\n'
    cap += 'اکنون عضو شوید' + '\n'
    cap += '@danesh_emrooz'
    addr = 'images/danem.png'
    # bot.sendPhoto(chat_id='@danesh_emrooz', photo=open(addr, 'rb'), caption=res)
    res = bot.sendPhoto(chat_id='@danesh_emrooz', photo=open(addr, 'rb'), caption=cap)
    # print res


def sendPicofDay():
    bot = get_bot()

    imnum = randint(0, 6)
    # res = requests.post('http://www.yooz.ir/today/image/', data={'d':imnum})
    res = requests.post('http://yooz.ir/today/image/', data={'d': 0})
    res = json.loads(res.content)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    file = cStringIO.StringIO(urllib.urlopen(res[u'src'], context=ctx).read())
    img = Image.open(file)
    # img = Image.open(res[u'src'])
    w = img.size[0]
    h = img.size[1]
    img = img.crop((0, 0, w, h - 80))
    img.save('danesh_emrooz.jpg')
    try:
        img.save('imgbk/' + res[u'description'] + '_' + str(uuid.getnode()) + '.jpg')
    except:
        pass

    title = ("#تصویر روز").decode("utf-8", "strict") + "\n"
    cap = (title + res[u'description']).encode("utf-8")
    cap += '\n@danesh_emrooz'

    res = bot.sendPhoto(chat_id='@danesh_emrooz', photo=open('danesh_emrooz.jpg', 'rb'), caption=cap)


def sendToday():
    bot = get_bot()

    url = 'http://time.ir/'
    content = requests.get(url).content
    tree = html.fromstring(content)
    titles = [e.text_content() for e in tree.xpath('//div[@class="dateTypeTitle"]')]
    bodies = [e.text_content() for e in tree.xpath('//div[@class="dateTypeBody"]')]

    res = ''
    for dt in range(0, len(titles) - 1):
        res += titles[dt]
        res += bodies[dt]

    res = res.replace('  ', '')
    res = res.replace('\r\n', '\n')
    res = res.replace('\n\n', '\n')

    title = ("تقویم").decode("utf-8", "strict") + "\n"

    res += '\n @danesh_emrooz'
    bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')


def sendVaqaye():
    bot = get_bot()

    url = 'http://time.ir/'
    content = requests.get(url).content
    tree = html.fromstring(content)
    bodies = [e.text_content() for e in tree.xpath('//span[@class="show numeral"]')]
    todaynumera = bodies[0]
    t2i = todaynumera.split('/')
    tnum = ''
    for v in t2i:
        tnum += '/' + str(int(v.encode("utf-8", "strict").decode("utf-8", "strict"))).zfill(2)

    url = 'http://www.time.ir/fa/event/list/0' + tnum
    # url = 'http://www.time.ir/fa/event/list/0/1396/02/22'
    content = requests.get(url).content
    tree = html.fromstring(content)
    tdevents = [e.text_content() for e in tree.xpath('//ul[@class="list-unstyled"]')]

    res = ''
    for dt in range(0, len(tdevents)):
        res += tdevents[dt].replace('  ', '').replace('\r\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace(
            '\n\n', '\n')

    if len(res) < 10:
        # return
        res = '--'

    title = ("مناسبت های امروز").decode("utf-8", "strict") + "\n"

    res += '\n @danesh_emrooz'
    bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')


def sendAye():
    bot = get_bot()

    qurandata = []
    with open('quran/qurandata.csv', 'r') as f:
        reader = csv.reader(f)
        qurandata = map(tuple, reader)

    soore = randint(1, 114)
    sooretitle = qurandata[soore][1]
    totalaye = int((qurandata[soore][2]).decode("utf-8", "strict"))
    aye = randint(2, totalaye)

    url = 'http://www.parsquran.com/data/show.php?sura=' + str(soore) + '&ayat=' + str(
        aye) + '&user=far&lang=far&tran=2'
    content = requests.get(url).content
    tree = html.fromstring(content)
    randomQuote = [e.text_content() for e in tree.xpath('//div[@class="DA"]')]
    resAr = randomQuote[0]
    resAr = resAr.replace('\t', '').replace('\n', '')

    randomQuote = [e.text_content() for e in tree.xpath('//div[@class="DF"]')]
    resFa = randomQuote[0]
    resFa = resFa.replace('\t', '').replace('\n', '')

    url = 'http://www.parsquran.com/data/show.php?sura=' + str(soore) + '&ayat=' + str(
        aye) + '&user=far&lang=eng&tran=1'
    content = requests.get(url).content
    tree = html.fromstring(content)
    randomQuote = [e.text_content() for e in tree.xpath('//div[@class="DE"]')]
    resEn = randomQuote[0]
    resEn = resEn.replace('\t', '').replace('\n', '')

    name = ("سوره ").decode("utf-8", "strict") + sooretitle.decode("utf-8", "strict")
    res = name + '\n' + resAr + '\n' + resFa + '\n' + resEn
    title = ("هر روز یک #آیه").decode("utf-8", "strict") + "\n" + "\n"

    res += '\n @danesh_emrooz'
    bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')

    soup = BeautifulSoup(content)
    for tag in soup.findAll('script'):
        # Use extract to remove the tag
        st = tag.string.replace('\n', ' ').replace('\r', ' ')
        m = re.findall(r'files\s\=\s(.*?);', st)
        if (m):
            ad = json.loads(m[0])
            bot.send_audio(chat_id='@danesh_emrooz', audio=ad[0], title='danesh_emrooz',
                           caption=name + '\n' + resAr + '\n @danesh_emrooz')
            break


def sendHadith():
    bot = get_bot()

    hadithurl = 'http://daily.hadith.net/dailyscript/v1/20170407074136961-panel-1.js'
    data = requests.get(hadithurl).content
    hs = data[data.index("innerHTML"):]
    hs = hs[hs.index("'") + 1:]
    # hadith= '<p>' + hs[0:hs.index("'")] + '</p>'
    hadithhtml = hs[0:hs.index("'")]

    tree = html.fromstring(hadithhtml.decode("utf-8", "strict"))
    randomQuote = [e.text_content() for e in tree.xpath('//div')]
    text = randomQuote[0]

    text = text.replace('\\n', '')
    text = text.replace('\t', '\n')
    text = text.replace('\n\n', '\n')

    res = text
    # txl = [x for x in text.split('\n') if x]
    # res = txl[0] + '\n' + '<b>' + txl[1] + '</b> \n' + '<b>' + txl[2] + '</b> \n' + txl[3]
    # res = txl[0] + '\n' + txl[1] + '\n' + txl[2] + '\n' + txl[3]


    title = ("#حدیث روز").decode("utf-8", "strict") + "\n"

    res += '\n @danesh_emrooz'

    bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')


def sendPoem():
    bot = get_bot()

    # state['poem'] = {}
    cst = state['poem']

    # load hafez
    hf = open('poem/taghafez.html', 'r')
    haf = html2texthgh.html2text(hf.read().decode("utf-8", "strict"))
    haf = haf.replace('\n\n', '\n')
    haf = haf.replace('*', '')
    hafl = [x for x in haf.split('~') if x]
    qazcnt = len(hafl) - 1
    qaznum = randint(0, qazcnt / 2)
    qaz = hafl[qaznum * 2 + 2]
    mesrl = [x for x in qaz.split('\n') if x]

    sqn = mesrl[0]
    mesrcnt = len(mesrl) - 1
    msr = randint(0, mesrcnt / 2 - 1)
    beyt = mesrl[msr * 2 + 1] + '\n' + mesrl[msr * 2 + 2]

    cst['qazcnt'] = qazcnt
    cst['qaznum'] = qaznum
    cst['mesrcnt'] = mesrcnt
    cst['msr'] = msr

    # ---------------------- draw on image ------------------
    hbg = Image.open('assets/hadithframe2.jpg')
    draw = ImageDraw.Draw(hbg)
    font = ImageFont.truetype("assets/font/BDavat.ttf", 70)
    DejaVuSans = ImageFont.truetype("DejaVuSans.ttf", 40)
    configuration = {
        'delete_harakat': False,
        'support_ligatures': True,
        'RIAL SIGN': True,  # Replace ريال with ﷼
    }
    reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)

    draw.text((922, 290), get_display(reshaper.reshape(('حافظ').decode("utf-8", "strict"))), font=font, fill="#000000")
    draw.text((904, 355), get_display(reshaper.reshape(('غزل').decode("utf-8", "strict") + sqn.strip())), font=font,
              fill="#000000")
    ub1 = get_display(reshaper.reshape(mesrl[msr * 2 + 1]))
    x = font.getsize(ub1)
    draw.text((1620 - x[0], 503), ub1, font=font, fill="#000000")
    draw.text((309, 627), get_display(reshaper.reshape(mesrl[msr * 2 + 2])), font=font, fill="#000000")
    # draw.text((790, 827), '@danesh_emrooz', font=DejaVuSans, fill="#000000")
    hbg.save("poem.jpg")  # , "JPEG", quality=80, optimize=True, progressive=True)

    res = '\n' + beyt + '\n' + ('#حافظ (غزل').decode("utf-8", "strict") + sqn + (')').decode("utf-8", "strict")
    # res = ''
    res += '\n @danesh_emrooz'
    # bot.sendMessage(chat_id='@danesh_emrooz', text=res, parse_mode='html')
    bot.sendPhoto(chat_id='@danesh_emrooz', photo=open("poem.jpg", 'rb'), caption=res.encode("utf-8"))


def sendSentence():
    bot = get_bot()

    url = 'http://time.ir/'
    content = requests.get(url).content
    tree = html.fromstring(content)
    randomQuote = [e.text_content() for e in tree.xpath('//div[@class="randomQuote"]')]
    res = randomQuote[0]

    res = res.replace('\t', '\n')
    res = res.replace('\r\n', '\n')
    res = res.replace('  ', ' ')
    res = res.replace('  ', ' ')
    res = res.replace('\n ', '\n')
    res = res.replace('\n ', '\n')
    res = res.replace('\n\n', '\n')
    res = res.replace('\n\n', '\n')

    nlen = len(res)
    res = res.replace('\n\n', '\n')
    while nlen != len(res):
        nlen = len(res)
        res = res.replace('\n\n', '\n')

    title = ("#جملات بزرگان").decode("utf-8", "strict") + "\n"
    res += '\n @danesh_emrooz'
    bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')


def sendBG():
    bot = get_bot()

    if 'bgs' not in state:
        state['bgs'] = {}
        state['bgs']['bgi'] = 0
    cst = state['bgs']
    bgi = cst['bgi'] + 1

    Bgs = []
    # for file in os.listdir("bgs"):
    #     Bgs.append(file)
    # shuffle(Bgs)
    # with open('Bgs.pickle', 'wb') as handle:
    #     pickle.dump(Bgs, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('Bgs.pickle', 'rb') as handle:
        Bgs = pickle.load(handle)

    cst['bgi'] = bgi

    title = ("تصویر #زمینه").decode("utf-8", "strict") + "\n"
    cap = (title + '\n@danesh_emrooz').encode("utf-8")

    res = bot.sendPhoto(chat_id='@danesh_emrooz', photo=open('bgs/' + Bgs[bgi], 'rb'), caption=cap)


def sendEngWord():
    bot = get_bot()

    # state['engword'] = {}
    cst = state['engword']
    wlmax = cst['wlmax'] + 1
    wlnum = cst['wlnum'] + 1

    words = []
    with open('eng/504.txt', 'r') as f:
        words = f.read()

    wl = words.split('\n')
    word = wl[wlnum].decode("utf-8", "strict")

    cst['wlmax'] = wlmax
    cst['wlnum'] = wlnum

    # sentence example
    sen =''
    try:
        senurl = 'http://sentence.yourdictionary.com/' + word
        senp = requests.get(senurl).content
        tree = html.fromstring(senp)
        sens = [e.text_content() for e in tree.xpath('//div[@class="li_content"]')]
        sen = sens[0]
    except:
        pass

    # Translation
    transurl = 'http://bestdic.ir/Function/wordsAutoCompelete.aspx?lang=en&baseLang=persian&term=' + word
    trans = requests.get(transurl).content
    pk = (json.loads(trans))[0]

    res = pk['label'] + '\n' + pk['value'] + u'\n مثال :\n' + sen

    # pronounciation
    prourl = 'https://www.merriam-webster.com/dictionary/' + word
    propage = requests.get(prourl).content
    tree = html.fromstring(propage)
    randomQuote = [e for e in tree.xpath('//a[@class="play-pron"]')]
    PrL = randomQuote[0].attrib
    Pfile = PrL['data-file']
    Pdir = PrL['data-dir']
    Plink = 'http://media.merriam-webster.com/audio/prons/en/us/mp3/' + Pdir + '/' + Pfile + '.mp3'

    title = ("هر روز یک #کلمه از ").decode("utf-8", "strict") + "504:\n" + "\n"

    res += '\n\n @danesh_emrooz'
    try:
        bot.send_audio(chat_id='@danesh_emrooz', audio=Plink, title='danesh_emrooz', caption=title + res)
    except:
        try:
            bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')
        except:
            pass
    # bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')


def doUKnow():
    bot = get_bot()

    # state['douknow'] = {}
    cst = state['douknow']
    dukmax = cst['dukmax'] + 1
    duknum = cst['duknum'] + 1

    duk = []
    with open('douknow/douknow.txt', 'r') as f:
        duk = f.read()

    dukl = duk.split('\n')
    dukt = dukl[duknum].decode("utf-8", "strict")

    cst['dukmax'] = dukmax
    cst['duknum'] = duknum

    title = ("#آیامیدانید که :").decode("utf-8", "strict") + "\n" + "\n"

    dukt += '\n @danesh_emrooz'
    bot.sendMessage(chat_id='@danesh_emrooz', text=title + dukt, parse_mode='html')


def tebeslami():
    bot = get_bot()

    # state['tebeslami'] = {}
    cst = state['tebeslami']
    hnum = cst['hnum'] + 1

    with open('tebeslami/hadiths.pickle', 'rb') as handle:
        allhad = pickle.load(handle)

    # duk = []
    # with open('tebeslami/ap.txt', 'r') as f:
    #     duk = f.read()
    #
    # text = duk.decode("utf-8", "strict").replace('\n\n', '\n')
    # section = text.split('~')
    # sc = len(section)
    # hads = []
    # htitles = []
    # htp = []
    # j = 0
    # for i in range(0, sc):
    #     if (len(section[i]) > 10):
    #         hads.append([x for x in section[i].split('=') if x])
    #         htitles.append(hads[j][0])
    #         del hads[j][0]
    #         htp.append(len(hads[j]))
    #         j += 1
    #
    #
    # allhad = []
    # for i in range(len(htitles)):
    #     for j in range(len(hads[i])):
    #         allhad.append({'title':htitles[i], 'text': hads[i][j]})
    #
    # random.shuffle(allhad)
    # with open('tebeslami/hadiths.pickle', 'wb') as handle:
    #     pickle.dump(allhad, handle, protocol=pickle.HIGHEST_PROTOCOL)


    # denom = sum(htp)
    # for i in range(0, len(htp)):
    #     htp[i] = float(htp[i]) / denom
    # snum = weighted_choice(htp)

    # hc = len(hads[snum])
    # hnum = randint(0, hc)

    # htitle = htitles[snum]
    # hadith = hads[snum][hnum]

    htitle = allhad[hnum]['title']
    hadith = allhad[hnum]['text']

    cst['hnum'] = hnum

    title = ("#طب اسلامی (").decode("utf-8", "strict") + htitle.replace('\n', '') + ("):").decode("utf-8",
                                                                                                  "strict") + "\n\n"

    res = hadith[hadith.index('\n') + 1:]
    res += '\n @danesh_emrooz'
    bot.sendMessage(chat_id='@danesh_emrooz', text=title + res, parse_mode='html')


def runChannelUpdate():
    #
    # loadState()
    # for v in state :
    #     for i in state[v]:
    #         state[v][i] = 0
    # saveState()

    print 'loading state ...'
    loadState()

    # for test

    saveState()


    print 'start ...'
    sendTitle()
    print '1. title sent'
    sendToday()
    print '2. today sent.'
    saveState()
    print 'state saved.'
    sendVaqaye()
    print '3. Vaqaye sent.'
    saveState()
    print 'state saved.'
    sendPicofDay()
    print '4. pic sent'
    saveState()
    print 'state saved.'
    sendAye()
    print '5. Aye sent'
    saveState()
    print 'state saved.'
    sendHadith()
    print '6. hadith sent.'
    saveState()
    print 'state saved.'
    sendPoem()
    print '7. poem sent.'
    saveState()
    print 'state saved.'
    try:
        sendSentence()
    except:
        pass
    print '8. sentence sent.'
    saveState()
    print 'state saved.'
    tebeslami()
    print '9. tebeslami sent'
    saveState()
    print 'state saved.'
    doUKnow()
    print '10. doUKnow sent'
    saveState()
    print 'state saved.'
    sendBG()
    print '11. BG sent.'
    saveState()
    print 'state saved.'
    try:
        sendEngWord()
        print '12. eng word sent.'
    except:
        pass
    saveState()
    print 'state saved.'
    print 'done.'


def loadState():
    global state
    with open('state.pickle', 'rb') as handle:
        state = pickle.load(handle)


def saveState():
    with open('state.pickle', 'wb') as handle:
        pickle.dump(state, handle, protocol=pickle.HIGHEST_PROTOCOL)


def every24():
    lasttime = datetime.now()
    runChannelUpdate()
    while True:
        now = datetime.now()
        print 'checking on : ' + str(now) + ' ...'
        seconds = (now - lasttime).total_seconds()
        hours = seconds // 3600
        if (hours >= 24):
            runChannelUpdate()
            lasttime = now
        print 'waiting ...'
        time.sleep(3600)


def on5to8():
    did = False
    while True:
        now = datetime.now()
        print 'checking on : ' + str(now) + ' ...'
        if (now.hour >= 5 and now.hour < 8):
            if not did:
                runChannelUpdate()
                did = True
        else:
            did = False
        print 'waiting ...'
        time.sleep(3600 / 2)


def on8to11():
    did = False
    while True:
        now = datetime.now()
        print 'checking on : ' + str(now) + ' ...'
        if (now.hour >= 8 and now.hour < 11):
            if not did:
                runChannelUpdate()
                did = True
        else:
            did = False
        print 'waiting ...'
        time.sleep(3600 / 2)


# class TestApp(App):
#     def build(self):
#         runChannelUpdate()
#         return

# if __name__ == '__main__':
# on8to11()
every24()
