# -*- coding: utf-8 -*-
"""APPARATUS IMMORTALIS — сатирический мануал-журнал, 13 полос 200x280мм.
HTML+CSS -> Playwright Chromium -> PDF. Шрифты и картинки: base64 data-URI."""
import base64, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
IMG  = os.path.join(BASE, 'img')
FNT  = os.path.join(BASE, 'fonts')
OUT_HTML = os.path.join(BASE, 'magazine.html')
OUT_PDF  = os.path.join(BASE, 'APPARATUS_IMMORTALIS.pdf')

def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path,'rb').read()).decode()

fonts = {k: b64(os.path.join(FNT,v), 'font/ttf') for k,v in {
    'UNB':'Unbounded.ttf','OXA':'Oxanium.ttf','RUB':'Rubik.ttf','JBM':'JetBrainsMono.ttf'}.items()}

SCENES = {n: os.path.join(IMG, f) for n,f in {
    1:'01_cover.png', 2:'02_genesis.png', 3:'03_schema.png', 4:'04_assemblatio.png',
    5:'05_protocolum.png', 6:'06_usus.png', 7:'07_testimonia.png', 8:'08_finis.png',
    9:'09_societas.png', 10:'10_via_tertia.png', 11:'11_bracculum.png', 12:'12_finale.png', 13:'13_omnidollar.png', 14:'14_badges.png', 15:'15_indifferens.png', 16:'16_badge_chest.png', 17:'17_gate.png'}.items()}
PREVIEW = '--preview' in sys.argv
missing = [f for f in SCENES.values() if not os.path.exists(f)]
if missing and not PREVIEW:
    print('НЕТ ФАЙЛОВ:', *missing, sep='\n  '); sys.exit(1)
if missing:
    from PIL import Image, ImageDraw
    ph = os.path.join(BASE, '_placeholder.png')
    im = Image.new('RGB',(1792,2400),(225,227,230))
    d = ImageDraw.Draw(im)
    for gx in range(0,1792,120): d.line([(gx,0),(gx,2400)],fill=(210,212,216),width=2)
    for gy in range(0,2400,120): d.line([(0,gy),(1792,gy)],fill=(210,212,216),width=2)
    d.rectangle([60,1100,1732,1300],outline=(13,15,18),width=6)
    d.text((200,1160),'SCENE LOADING...',fill=(13,15,18))
    im.save(ph)
    OUT_PDF = OUT_PDF.replace('.pdf','_PREVIEW.pdf')
def img_b64(path):
    """resize до 1600px по большей стороне + JPEG q86 — печатных 200 dpi хватает"""
    from PIL import Image
    import io
    im = Image.open(path).convert('RGB')
    im.thumbnail((1600,1600), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf,'JPEG',quality=86)
    return 'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()

QR_PROC = b64(os.path.join(BASE,'logo_qr_site.png'),'image/png')
img = {n: img_b64(p if os.path.exists(p) else os.path.join(BASE,'_placeholder.png')) for n,p in SCENES.items()}

TOTAL = 17
def hud_frame(n, pars):
    return f'''
  <div class="frame"></div>
  <div class="corner c-tl"></div><div class="corner c-tr"></div>
  <div class="corner c-bl"></div><div class="corner c-br"></div>
  <div class="cross x1">+</div><div class="cross x2">+</div>
  <div class="edge-l">GAUSSE HOLLER CUSTOM LAB</div>
  <div class="edge-r">[{pars}] · MORS OPTIONALIS</div>
  <div class="folio">{n:02d} / {TOTAL}</div>
  <div class="brandline">APPARATUS IMMORTALIS · MANUALIS TECHNICUS</div>'''

def annos(items):
    out=''
    for (top,left,txt,side) in items:
        line = 'anno-line-l' if side=='l' else 'anno-line-r'
        out+=f'<div class="anno" style="top:{top}mm;left:{left}mm"><span class="{line}"></span>{txt}</div>'
    return out

pages=[]

# ── 01 ОБЛОЖКА ──────────────────────────────────────────────
pages.append(f'''<section class="page cover">
  <img class="cover-img" src="{img[1]}">
  <div class="cover-shade"></div>
  <div class="logo-plate">GAUSSE HOLLER CUSTOM LAB</div>
  <h1 class="cover-title">APPARATUS<br>IMMORTALIS</h1>
  <div class="cover-mono">MANUALIS TECHNICUS · EDITIO PRIMA · VER. ∞.0</div>
  <div class="cover-bottom">
    <div class="cover-slogan">«MORS OPTIONALIS»<span> — смерть теперь по желанию</span></div>
    <div class="cover-dek">Научно-технический доклад о том, как перестать заканчиваться. С чертежами, счётчиком и лёгким чувством, что вы опоздали записаться.</div>
    <div class="cover-credit">ИНИЦИАТОР — INCEPTOR PRIMARIS · GAUSSE HOLLER CUSTOM LAB</div>
  </div>
  {hud_frame(1,'COVER')}
</section>''')

def text_page(n, pars, kicker, title, img_n, img_side, body_html, quote, anno_items):
    im_cls = 'ph-r' if img_side=='r' else 'ph-l'
    tx_cls = 'tx-l' if img_side=='r' else 'tx-r'
    return f'''<section class="page">
  <div class="photo {im_cls}"><img src="{img[img_n]}">{annos(anno_items)}</div>
  <div class="txt {tx_cls}">
    <div class="kicker">[{pars}] {kicker}</div>
    <h2>{title}</h2>
    {body_html}
  </div>
  <div class="pull">{quote}</div>
  {hud_frame(n,pars)}
</section>'''

# ── 02 GENESIS ──────────────────────────────────────────────
pages.append(text_page(2,'PARS I','GENESIS','Мне надоело, что&nbsp;люди кончаются',2,'r','''
  <p>Не в философском смысле. В бытовом. Ты годами настраиваешь человека под себя — как он молчит, как варит кофе, как смеётся не вовремя — а потом приходит счёт. Гарантия истекла. Спасибо за покупку.</p>
  <p>Я посмотрел на это как инженер. И увидел плохой продукт.</p>
  <p>Смерть подавали как фичу: «придаёт жизни смысл». Гениально — взять дефект и приклеить ценник духовности. Ту же схему крутят в спортзалах, в церквях и в подписке на медитацию: сначала внушают, что ты сломан, потом продают починку в рассрочку. Смерть — просто самая старая компания на этом рынке. Монополист. Ни одного возврата за всю историю.</p>
  <p>Так появился APPARATUS IMMORTALIS. Он работает — конец больше не входит в комплектацию. И это первый в истории случай, когда слово «вечная» в гарантии стоит буквально, а не для красоты.</p>
  <p><b>VITA AETERNA.</b> «Пожить подольше» — это про витамины. Мы про другое: право не заканчиваться и дорогу, у которой нет последней остановки. Смертному выдают отрезок и просят уложиться, будто жизнь — парковка на два часа. Мы сняли шлагбаум. За ним, выяснилось, нет таблички «выход» — там вообще нет табличек, там звёзды.</p>''',
  '«Смерть — не трагедия. Смерть — это подписка, которую оформили без твоего согласия и списывают ровно один раз. Зато навсегда.»',
  [(107,6,'FIG.01 · MOMENTUM GENESIS','l'),(100,64,'MORS: DEPRECATED','l')]))

# ── 03 SCHEMA (картинка сверху, ТТХ-таблица) ────────────────
rows = [('REACTOR CORDIS','Двигатель работает на твоём «дальше». Пока есть куда дальше — не глохнет. Топливо возобновляемое.'),
        ('ANNULUS VIAE','Держит курс на горизонт, даже когда ты спишь. Спать теперь можно — торопиться некуда.'),
        ('MASCA DIAMANTIS','Фильтрует страх конца на подходе. Паника больше не подкрадётся.'),
        ('NULLIFICATOR MORTIS','Глушитель смерти. Единственный блок без кнопки «выкл».'),
        ('РЕСУРС','∞ циклов. Счётчик сломался на слове «конец».'),
        ('ДЕДЛАЙН','Снят с производства. Первый и последний раз.'),
        ('ГАРАНТИЯ','Вечная. В данном случае — издёвка.'),
        ('ПИТАНИЕ','Желание не заканчиваться + один доллар. Оба возобновляемы.')]
trs=''.join(f'<tr><td class="tk">{a}</td><td>{b}</td></tr>' for a,b in rows)
pages.append(f'''<section class="page">
  <div class="photo ph-top"><img src="{img[3]}">
    {annos([(10,14,'FIG.02 · EXPLOSIO MODULORUM','l'),(96,146,'CORE: BIO-GREEN','r')])}
  </div>
  <div class="txt tx-under">
    <div class="kicker">[PARS II] SCHEMA TECHNICA</div>
    <h2>Внутри всё просто</h2>
    <p class="lead">Простота — это то, что остаётся, когда убираешь враньё.</p>
    <table class="ttx">{trs}</table>
  </div>
  <div class="pull">«Каждый блок по отдельности звучит как чудо. Собери в цепь — и, кажется, весь мир помещается в одну руку. Красиво.»</div>
  {hud_frame(3,'PARS II')}
</section>''')

# ── 04 ASSEMBLATIO ──────────────────────────────────────────
pages.append(text_page(4,'PARS III','ASSEMBLATIO','Его собирают не&nbsp;на&nbsp;заводе',4,'l','''
  <p>Заводы делают вещи, которые ломаются по расписанию, — это их бизнес-модель, а не досадная случайность. Наш рецепт для завода не годится: в нём нет ни одной детали, которую можно взвесить.</p>
  <p>Берётся немного денег. Ровно один доллар: столько, чтобы человек почувствовал, что вложился, и ни центом больше — чтобы не почувствовал, что его развели.</p>
  <p>Дальше — щепотка того единственного, что отличает нас от свиней у корыта: способность иногда оторвать голову от кормушки и посмотреть вверх. У свиньи не выходит по анатомии, у человека — по лени. С ленью мы и работаем: рынок огромный, конкурентов ноль.</p>
  <p>Смешать. Настаивать не надо — оно само. Обратной инструкции нет: разложить это обратно на доллар и звёзды ещё никому не удавалось. Пробовали. Получались только революции.</p>''',
  '«Свинья от человека отличается одним: человек иногда смотрит вверх. Мы не продаём этот момент — мы его открываем. Инициация стоит доллар.»',
  [(107,6,'FIG.03 · MANUFACTURA SACRA','l'),(100,60,'SPARKS: AURO-VIRIDIS','l')]))

# ── 05 PROTOCOLUM ───────────────────────────────────────────
pages.append(text_page(5,'PARS IV','PROTOCOLUM','Первый запуск — на&nbsp;себе',5,'r','''
  <p>Разумеется на себе. Кто ещё подпишет договор, где мелкий шрифт длиннее самого договора. Свет пошёл по венам — и горизонт, который всю жизнь нагло приближался, впервые сделал шаг назад.</p>
  <p>Первая мысль трезвого бессмертного до обидного бытовая: больше не надо торопиться. Вся человеческая спешка, все «успеть до сорока», «купить до кризиса», «пожить для себя на пенсии» — оказались очередью в кассу, которая закрывается. Касса больше не закрывается. Спешить теперь — просто дурной тон.</p>
  <p>Смерть всегда подавали как драматичный финал. На деле это обрыв плёнки на середине хорошего фильма — и никто не вернёт деньги за билет. Я склеил плёнку. <b>VIA AETERNA.</b> Дальше сценарий не написан: его пишет тот, кто досидел до конца. А конца нет.</p>''',
  '«Смертному объясняют, как прожить отпущенное. Мы сообщаем, что отпущенное закончилось. За сообщение денег не берём — берём за инициацию.»',
  [(107,6,'FIG.04 · ACTIVATIO PRIMA','l'),(100,64,'STATUS: AWAKE','l')]))

# ── 06 USUS (двое, шаги) ────────────────────────────────────
steps=[('I · IGNIS','Скажи «я в деле». Один доллар — и искра пошла. Звать её не надо, сама разгорится.'),
       ('II · CORONA','Точка невозврата. Вокруг тебя загорается корона света — не украшение, а индикатор: назад уже нельзя.'),
       ('III · ITER','Выбери направление. Земля маленькая — начни с неё, разгонишься по пути.'),
       ('IV · VIVE','Живи. И живи. И живи. Пункт четвёртый не заканчивается — это не опечатка.')]
cards=''.join(f'<div class="step"><div class="step-n">{a}</div><div>{b}</div></div>' for a,b in steps)
pages.append(f'''<section class="page">
  <div class="photo ph-top45"><img src="{img[6]}">
    {annos([(88,14,'FIG.05 · INVENTOR + SOCIUS','l'),(84,148,'DUO OPERATORES','r')])}
  </div>
  <div class="txt tx-under45">
    <div class="kicker">[PARS V] USUS</div>
    <h2>Пользоваться просто</h2>
    <p class="lead">Всё гениальное просто. Всё простое потом оказывается необратимым.</p>
    <div class="steps">{cards}</div>
    <div class="contra"><div class="contra-t">CONTRAINDICATIONES</div>
      <p>· Не рекомендуется тем, кому нравился финал.</p>
      <p>· Не совместим с фразой «доживу до пенсии» — доживёшь до чего угодно, пенсия просто потеряет смысл.</p>
      <p>· При желании «а можно я всё-таки закончусь» блок NULLIFICATOR MORTIS вежливо сделает вид, что не расслышал.</p>
    </div>
  </div>
  <div class="pull">«Инструкция к бессмертию помещается на одной строке: продолжай. Проблема всегда была в том, чтобы её прекратить.»</div>
  {hud_frame(6,'PARS V')}
</section>''')

# ── 07 TESTIMONIA ───────────────────────────────────────────
revs=[('«Живу с вторника. Какого именно вторника — уже не помню. Их было много.»','★★★★★ · Клиент №0001'),
      ('«Пережил три ипотеки, две империи и один тренд на осознанность. Аппарат работает.»','★★★★★ · Anonymus Aeternus'),
      ('«Хотел вечную жизнь. Получил вечную жизнь. Внимательнее читайте, чего хотите.»','★★★★☆ · снял звезду за честность'),
      ('«Смерть больше не звонит. Иногда скучаю по её звонкам.»','★★★★★ · Vir Insomnis')]
rc=''.join(f'<div class="rev"><p>{a}</p><div class="rev-s">{b}</div></div>' for a,b in revs)
pages.append(f'''<section class="page">
  <div class="photo ph-l"><img src="{img[7]}">
    {annos([(107,6,'FIG.06 · TEMPLUM MERCATUS','l'),(100,56,'RATING: ETERNAL','l')])}
  </div>
  <div class="txt tx-r">
    <div class="kicker">[PARS VI] TESTIMONIA</div>
    <h2>Клиенты довольны</h2>
    <p class="lead">У них теперь очень много времени быть довольными.</p>
    {rc}
  </div>
  <div class="pull">«Я думал, что раздаю вечную жизнь. Я раздаю невозможность выйти. Проходят инициацию одинаково охотно.»</div>
  {hud_frame(7,'PARS VI')}
</section>''')

# ── 08 SOCIETAS ($1) ────────────────────────────────────────
pages.append(text_page(8,'PARS VII','SOCIETAS','Доллар — чтобы не ждать инвайт',9,'r','''
  <p>Можно было бы назвать цену квартиры. Но мы не назначаем цен — мы не продавцы. Есть только инициация, и она стоит один доллар. Не потому что дёшево, а потому что доллар есть у всех — и на этом заканчиваются отговорки.</p>
  <table class="ttx"><tr><td class="tk">ИНИЦИАЦИЯ</td><td>Один доллар. Разово. «В месяц» — для тех, кому нравится ритуал.</td></tr><tr><td class="tk">ЧТО ДАЁТ</td><td>Инвайт перестаёт зависеть от чужого настроения. Дальше — сам.</td></tr><tr><td class="tk">ПРОШЛИ</td><td>1 204 880. Счётчик растёт каждую секунду. Секунды здесь длинные.</td></tr><tr><td class="tk">ПЕРЕДУМАЛИ</td><td>0 человек. Подумай, что это говорит. Об инициации. Или о нас.</td></tr><tr><td class="tk">ВЫГОДА ДЛЯ НАС</td><td>Ноль. Мы честные — это написано прямо здесь.</td></tr></table>''',
  '«Я ничего не продаю. Я всего лишь убираю слово „никогда“ из твоего приглашения. Один доллар — и оно исчезает.»',
  [(107,6,'FIG.07 · PROGRAMMA CO-AUCTORIS','l'),(100,62,'RITUS · $1','l')]))

# ── 09 ОДИН ДОЛЛАР ──────────────────────────────────────────
pages.append(text_page(9,'PARS VIII','UNUS DOLLARUS','Все скидываются по&nbsp;доллару. Всё.',13,'r','''
  <p>Доллар — не деньги. Доллар — подпись под фразой «я тоже». Мы собрали миллион подписей и забрали под них кусок неба. Попробуй оспорь.</p>
  <table class="ttx"><tr><td class="tk">МОДЕЛЬ</td><td>Никакая. В этом её сила.</td></tr><tr><td class="tk">ТВОЙ ВЗНОС</td><td>$1. Столько же, сколько у миллиардера. Он в бешенстве.</td></tr><tr><td class="tk">ТЫ ПОЛУЧАЕШЬ</td><td>Ничего. Заметь: ты всё ещё читаешь.</td></tr><tr><td class="tk">РАЗДЕЛ ПЛАНЕТОИДА</td><td>Так, как хотим мы. Враньё бережём для важных случаев.</td></tr><tr><td class="tk">ЗАЯВКИ «ПО ДВА»</td><td>Отклонены. Двое миллиардеров подписались от обиды.</td></tr></table>''',
  '«Люди веками платили за землю, которую никогда не увидят. Мы просто убрали землю. Стало честнее и легче доставлять.»',
  [(107,6,'FIG.08 · DIVISIO PLANETOIDIS','l'),(100,60,'1 $ = 1 VOX','l')]))

# ── 10 ORDO PRETIORUM (тарифы + значки) ─────────────────────
tarifs=[('$1 · CIVIS','Один агент, одна функция: троллить тех, кто не в теме. Экран показывает твой доллар и место в очереди. Место шестизначное. Зато светится.'),
        ('$10 · SOCIUS','Показывает твоё место в очереди друзьям. Друзья делают вид, что рады.'),
        ('$100 · PATRONUS','Лазерный резак в аренду на церемонии распила. Резать медленно. Быстро — дороже. Медленно, но с чувством — ещё дороже.'),
        ('$1000 · ARCHITECTUS','Резать быстрее, влиять раньше, не думать, что делать с бессмертием уже завтра, — за тебя подумает тариф.'),
        ('$1 000 000 · DEUS MINOR','Значок размером с нагрудную плиту, собственный сектор планетоида и право стоять рядом с нами на всех фотографиях. Стоять — не говорить.')]
trows=''.join(f'<tr><td class="tk">{a}</td><td>{b}</td></tr>' for a,b in tarifs)
pages.append(f'''<section class="page">
  <div class="photo ph-half-l"><img src="{img[14]}">
    {annos([(54,6,'FIG.09a · ORDO INSIGNIUM','l')])}
  </div>
  <div class="photo ph-half-r"><img src="{img[16]}">
    {annos([(54,6,'FIG.09b · IN PECTORE','l')])}
  </div>
  <div class="txt tx-under-tarif">
    <div class="kicker">[PARS IX] ORDO INITIATIONUM</div>
    <h2>Очередь к вечности — через&nbsp;инициацию</h2>
    <p class="lead">Очередь одна на всех — так честнее. Но стоять в ней необязательно: чем сильнее хочешь вперёд, тем ты ближе. Каждому — кибер-значок на левую грудь: LED снизу, на экране твой шаг и место в очереди. Значки различаются глубиной. Как и их владельцы.</p>
    <table class="ttx">{trows}</table>
  </div>
  <div class="pull">«Вечность одна на всех. Кто хочет пройти быстрее — проходит быстрее. Не за деньги. За желание не стоять.»</div>
  {hud_frame(10,'PARS IX')}
</section>''')

# ── 11 INITIATORIUM (слот под QR — код вставляет издатель вручную) ─
payrows=[('ИНИЦИАЦИЯ','Один доллар. Не цена — жест. Способ сказать «я не жду приглашения, я уже иду».'),
         ('ИНВАЙТ','Приходит всем. Срок — от недели до «никогда». Инициация вычёркивает слово «никогда».'),
         ('УРОВЕНЬ 2','Что за воротами — узнают прошедшие. Спойлер обесценивает инициацию.'),
         ('ОЧЕРЕДЬ','Отсутствует. Все стоят перед воротами и думают. Ворота, между тем, открыты.'),
         ('ПРОХОД','100%. Ворота ещё никого не остановили. Они, строго говоря, и не закрываются.'),
         ('ОТКАТ','Предусмотрен. В следующей жизни. Как раз туда мы и держим дверь.')]
ptr=''.join(f'<tr><td class="tk">{a}</td><td>{b}</td></tr>' for a,b in payrows)
pages.append(f'''<section class="page">
  <div class="txt" style="position:absolute; top:16mm; left:12mm; right:12mm">
    <div class="kicker">[PARS X] INITIATORIUM · GRADUS SECUNDUS</div>
    <h2>Инициация перехода на&nbsp;второй уровень</h2>
    <p class="lead">Никто ничего не продаёт и не покупает. Инвайт приходит сам — рано или поздно. Обычно поздно. Инициация — это способ не выяснять, насколько поздно.</p>
  </div>
  <div class="gate"><img src="{img[17]}"></div>
  <div class="qr-slot" style="border:none;padding:0;background:none"><img src="{QR_PROC}" style="width:100%;height:100%;object-fit:contain"></div>
  <div class="qr-cap">СКАНИРУЙ — КАНАЛ ОТКРОЕТСЯ.<br>ОЧЕРЕДЬ ОСТАНЕТСЯ СНАРУЖИ. <b>ВМЕСТЕ С ТОБОЙ ВЧЕРАШНИМ.</b><br>GAUSSE HOLLER CUSTOM LAB<br>SCAN · AGE · ASCENDE</div>
  <div class="txt tx-pay"><table class="ttx">{ptr}</table></div>
  <div class="pull">«Мы ничего не продаём. Мы проводим инициации. Разница в том, что инициацию не отменить задним числом.»</div>
  {hud_frame(11,'PARS X')}
</section>''')

# ── 09 REGULA AETERNA (браслет) ─────────────────────────────
pages.append(f'''<section class="page">
  <div class="photo ph-top"><img src="{img[11]}">
    {annos([(10,14,'FIG.09 · REGULA AETERNA','l'),(96,140,'AETERNUS COUNTER','r')])}
  </div>
  <div class="txt tx-under">
    <div class="kicker">[PARS XI] REGULA AETERNA</div>
    <h2>Каждому третьему — часы до&nbsp;вечности</h2>
    <p>Каждый третий прошедший участник получает <b>REGULA AETERNA</b> — наручный отсчёт до бессмертия. У остальных дата тоже идёт. Просто они её не видят. Так спокойнее. Им, не нам.</p>
    <table class="ttx"><tr><td class="tk">ЭКРАН</td><td>TEMPUS AD IMMORTALITATEM. Тикает в твою пользу. Впервые в жизни.</td></tr><tr><td class="tk">ПОЧЕМУ ТРЕТИЙ</td><td>Первый завидует, второй платит за двоих. Мы просто перестали стесняться этой математики.</td></tr><tr><td class="tk">ТОЧНОСТЬ</td><td>До секунды. Секунд у владельца теперь больше, чем было.</td></tr><tr><td class="tk">СНЯТЬ БРАСЛЕТ</td><td>Можно. Отсчёт — нельзя.</td></tr></table>
  </div>
  <div class="pull">«Люди боятся не смерти. Люди боятся цифр. Уберите табло — и вечность становится уютной.»</div>
  {hud_frame(12,'PARS XI')}
</section>''')

# ── 10 VIA TERTIA ───────────────────────────────────────────
pages.append(text_page(13,'PARS XII','VIA TERTIA','Есть два пути. Оба — по&nbsp;кругу.',10,'r','''
  <p>Раз в четыре года тебе выдают бюллетень: одни фашики, другие — фашики с человеческим лицом на плакате. Спор, чьи хуже, называется «гражданская позиция». На него уходит жизнь. Удобно: она как раз одна.</p>
  <p>Мы выбрали третье: <b>героические страдания тысячелетиями на кораблях поколений</b>. Написали «страдания» прямо на плакате — нас назвали сектой. Значит, работает.</p>
  <table class="ttx"><tr><td class="tk">ТВОЙ МАРШРУТ</td><td>Работа → выборы → работа. По кругу.</td></tr><tr><td class="tk">НАШ МАРШРУТ</td><td>По прямой. Из иллюминатора — звёзды, а не экзитполы.</td></tr><tr><td class="tk">В КОНЦЕ У НИХ</td><td>Пенсия. Не у всех.</td></tr><tr><td class="tk">В КОНЦЕ У НАС</td><td>Не скажем — сами не знаем. Программа без спойлеров.</td></tr><tr><td class="tk">ПЕНСИОННЫЙ ВОЗРАСТ</td><td>Отменён. Вместе с пенсией. Взаимозачёт.</td></tr></table>''',
  '«Политика предлагает выбрать, кто будет виноват. Мы предлагаем выбрать, куда лететь. Почувствуй разницу масштаба.»',
  [(107,6,'FIG.10 · ASCENSIO','l'),(100,60,'DEAD END / TERMINATED / ↑','l')]))

# ── 11 OBJECTIONES (текстовая) ──────────────────────────────
objs=[('«А что мне даст мой доллар?»','Тебе — почти ничего. Мне — миллион таких вопросов, помноженных на доллар. Ты спрашиваешь, что даёт доллар, у тех, кто отменил смерть. Смерть ты почему-то принял без единого вопроса. А из-за доллара вдруг стал жаться.'),
      ('«Какие гарантии?»','Гарантия — вечная. Это единственное слово в документе, которое буквально. Ты просишь гарантию у бессмертия. У ипотеки не просил, у брака не просил, у собственного сердца не просил — а тут вдруг стал аудитором.'),
      ('«А вдруг не сработает?»','Тогда ты умрёшь. Ровно как в плане, который у тебя был и без меня. Риск в том, что всё останется как есть. Странно бояться именно этого.'),
      ('«Звучит как секта.»','В секте берут всё и обещают рай. Я беру доллар и обещаю вторник. Бесконечный, но вторник. Чувствуешь разницу в честности?')]
qa=''.join(f'<div class="obj"><div class="obj-q">{q}</div><p>{a}</p></div>' for q,a in objs)
pages.append(f'''<section class="page">
  <div class="txt tx-full">
    <div class="kicker">[PARS XIII] OBJECTIONES</div>
    <h2>Вопросы задают выжившие</h2>
    <p class="lead">Раздел для тех, кто дочитал и всё ещё сомневается. Сомнение — здоровый рефлекс. У здоровых. У остальных — симптом смертности.</p>
    {qa}
  </div>
  <div class="pull">«Не бывает глупых вопросов. Бывают вопросы, которые задаёт тот, кто всё ещё планирует умереть.»</div>
  {hud_frame(14,'PARS XIII')}
</section>''')

# фикс: страница 12 через text_page с корректной сигнатурой
# ── 14 INDIFFERENS ──────────────────────────────────────────
pages.append(text_page(15,'PARS XIV','ПОКУПАТЕЛЬ ЗАВТРАШНЕГО ДНЯ','EMPTOR CRASTINUS',15,'l','''
  <p>Значки — для тех, кто уже вошёл. Над значками есть кольца: их носят инвесторы такого порядка, что вслух о них не говорят. Как выглядит кольцо, не знает никто — включая тех, кому оно якобы прислано. В этом и статус: значок показывают, кольцо подразумевают.</p>
  <p>Наш герой пока не носит ни того, ни другого. Не потому что против — он «за». Просто зайдёт завтра.</p>
  <p>Он тоже хочет узнать: может ли жизнь надоесть <i>на самом деле</i>? Отличный вопрос. Научный. Единственный способ проверить — жить дальше и записывать. У смертных эксперимент обрывается на самом интересном месте: данные кончаются вместе с исследователем. Наши клиенты доводят исследование до конца. Точнее — без конца. Это и есть методика.</p>
  <p>Пока же он — <b>EMPTOR CRASTINUS</b>, покупатель завтрашнего дня. Самая многочисленная цивилизация во вселенной. Девиз: «с понедельника». Понедельник передвижной.</p>
  <p>Отдел лора его обожает: самый лояльный участник из всех. Пройдёт инициацию сразу на сто долларов — через двадцать лет. Посмертно. Завещание уже готово и лежит у нашего кибер-агента. Участник его ещё не писал — но кибер-агент никуда не торопится. В этом их главное различие.</p>
  <p>Мы держим для него место. И счётчик. Наше «завтра» длиннее его — на этом стоит весь бизнес-план.</p>''',
  '«Он придёт завтра. Мы работаем всегда. Где-то эти два графика пересекутся.»',
  [(107,6,'FIG.11 · EMPTOR CRASTINUS','l'),(100,56,'STATUS: MOX (СКОРО)','l')]))

pages.append(text_page(16,'PARS XV','FINIS · БУДУЩЕЕ, КОТОРОЕ ОБЯЗАНО СЛУЧИТЬСЯ','FUTURUM DEBITUM',8,'l','''
  <p>Всё большое начиналось одинаково: кто-то переставал спорить и просто строил. Пирамиды не выиграли ни одних дебатов. Они стоят.</p>
  <p>Спорить — бесплатно, поэтому спор ничего и не стоит. Очередь — другое дело. Очередь голосует ногами, кошельком и молчанием. Самая честная форма выборов: результат невозможно подделать — в ней стоят добровольно.</p>
  <p>Где-то сейчас гремит парад. Он будет греметь и завтра: парадам больше нечем заняться. А за углом, со двора, открыта дверь, и за ней тихо. Там не обещают. Там записывают.</p>
  <p>Инициация входа — один доллар. Не потому что дёшево, а потому что доллар есть у всех. Отговорки конструкцией не предусмотрены.</p>
  <div class="finis-lines"><div>«Парад пройдёт. Очередь останется.»</div><div>«Доллар — и ты в ней.»</div></div>''',
  '«MORS OPTIONALIS · VIA SINE FINE · VITA AETERNA»',
  [(107,6,'FIG.12 · THRONUS LUCIS','l'),(100,58,'04:00 · SEMPER','l')]))

# ── 13 FINALE (двое к звездолёту, full-bleed) ───────────────
pages.append(f'''<section class="page cover">
  <img class="cover-img" src="{img[12]}">
  <div class="finale-bottom">
    <div class="finale-line">VIA TERTIA — К ЗВЁЗДАМ. ВМЕСТЕ.</div>
    <div class="colophon">MORS OPTIONALIS · VIA SINE FINE · VITA AETERNA<br>
    GAUSSE HOLLER CUSTOM LAB · VER. ∞.0 · MMXXVI</div>
  </div>
  {hud_frame(17,'FINALE')}
</section>''')

CSS = f'''
@font-face {{font-family:UNB; src:url({fonts['UNB']}); font-weight:200 900}}
@font-face {{font-family:OXA; src:url({fonts['OXA']}); font-weight:200 800}}
@font-face {{font-family:RUB; src:url({fonts['RUB']}); font-weight:300 900}}
@font-face {{font-family:JBM; src:url({fonts['JBM']}); font-weight:100 800}}
:root {{--ink:#0D0F12; --mut:#8A8F98; --grn:#2ECC40; --neon:#39FF6A; --bg:#EDEEF0}}
* {{margin:0; padding:0; box-sizing:border-box}}
@page {{size:200mm 280mm; margin:0}}
body {{font-family:RUB; color:var(--ink); -webkit-print-color-adjust:exact; print-color-adjust:exact}}
.page {{position:relative; width:200mm; height:280mm; background:var(--bg); overflow:hidden; page-break-after:always}}
/* HUD-рамка */
.frame {{position:absolute; inset:7mm; border:.35mm solid var(--ink); pointer-events:none}}
.corner {{position:absolute; width:6mm; height:6mm; border:.8mm solid var(--ink)}}
.c-tl {{top:5mm; left:5mm; border-right:none; border-bottom:none}}
.c-tr {{top:5mm; right:5mm; border-left:none; border-bottom:none}}
.c-bl {{bottom:5mm; left:5mm; border-right:none; border-top:none}}
.c-br {{bottom:5mm; right:5mm; border-left:none; border-top:none}}
.cross {{position:absolute; font-family:JBM; font-size:4mm; color:var(--ink)}}
.x1 {{top:6.2mm; left:50%; transform:translateX(-50%)}}
.x2 {{bottom:6.2mm; left:50%; transform:translateX(-50%)}}
.edge-l {{position:absolute; left:2.2mm; top:50%; transform:rotate(-90deg) translateX(50%); transform-origin:left center; font-family:JBM; font-size:2.4mm; letter-spacing:.8mm; color:var(--mut); white-space:nowrap}}
.edge-r {{position:absolute; right:2.2mm; top:50%; transform:rotate(90deg) translateX(-50%); transform-origin:right center; font-family:JBM; font-size:2.4mm; letter-spacing:.8mm; color:var(--mut); white-space:nowrap}}
.folio {{position:absolute; bottom:2.4mm; right:8mm; font-family:JBM; font-size:2.8mm; color:var(--ink)}}
.brandline {{position:absolute; bottom:2.4mm; left:8mm; font-family:JBM; font-size:2.4mm; letter-spacing:.5mm; color:var(--mut)}}
/* фото-блоки */
.photo {{position:absolute; overflow:hidden; border:.35mm solid var(--ink)}}
.photo img {{width:100%; height:100%; object-fit:cover; display:block}}
.ph-r {{top:12mm; right:12mm; width:88mm; height:117mm}}
.ph-l {{top:12mm; left:12mm; width:88mm; height:117mm}}
.ph-top {{top:12mm; left:21mm; right:21mm; height:118mm}}
.ph-top45 {{top:12mm; left:33mm; right:33mm; height:100mm}}
.ph-half-l {{top:12mm; left:12mm; width:86mm; height:64mm}}
.ph-half-r {{top:12mm; right:12mm; width:86mm; height:64mm}}
.anno {{position:absolute; font-family:JBM; font-size:2.5mm; background:var(--bg); border:.3mm solid var(--ink); padding:.8mm 1.6mm; white-space:nowrap}}
/* текст */
.txt {{position:absolute; font-size:3.45mm; line-height:1.5}}
.tx-l {{top:14mm; left:12mm; width:82mm}}
.tx-r {{top:14mm; right:12mm; width:82mm}}
.tx-under {{top:136mm; left:12mm; right:12mm}}
.tx-under45 {{top:117mm; left:12mm; right:12mm}}
.tx-under-tarif {{top:84mm; left:12mm; right:12mm}}
.tx-full {{top:16mm; left:14mm; right:14mm}}
.kicker {{font-family:JBM; font-size:2.9mm; letter-spacing:.6mm; color:var(--grn); font-weight:700; margin-bottom:3mm}}
h2 {{font-family:UNB; font-weight:800; font-size:8.2mm; line-height:1.08; letter-spacing:-.1mm; margin-bottom:4.5mm; text-transform:uppercase}}
.txt p {{margin-bottom:2.8mm}}
.lead {{font-weight:600; font-size:3.7mm}}
.grn {{color:var(--grn)}}
.pull {{position:absolute; bottom:9mm; left:12mm; right:12mm; border-top:.6mm solid var(--ink); padding:2.6mm 0 0 22mm; font-family:OXA; font-weight:700; font-size:3.9mm; line-height:1.3}}
.pull::before {{content:'❞'; position:absolute; left:2mm; top:1mm; font-size:12mm; color:var(--grn); font-family:RUB; line-height:1}}
/* таблица ТТХ */
.ttx {{width:100%; border-collapse:collapse; font-size:3.1mm; margin-top:2mm}}
.ttx td {{border:.3mm solid var(--ink); padding:1.7mm 2.4mm; vertical-align:top}}
.ttx .tk {{font-family:JBM; font-weight:700; width:52mm; background:#fff}}
.tx-l .ttx td, .tx-r .ttx td {{font-size:2.85mm; padding:1.5mm 2mm}}
.tx-l .ttx .tk, .tx-r .ttx .tk {{width:23mm}}
/* шаги */
.steps {{display:grid; grid-template-columns:1fr 1fr; gap:2.6mm; margin:2mm 0 3mm}}
.step {{border:.35mm solid var(--ink); background:#fff; padding:2.4mm 3mm; font-size:3.05mm; line-height:1.4}}
.step-n {{font-family:OXA; font-weight:800; color:var(--grn); font-size:3.6mm; margin-bottom:1mm}}
.contra {{border:.6mm solid var(--ink); background:#fff; padding:2.6mm 3.2mm; font-size:3mm}}
.contra-t {{font-family:JBM; font-weight:800; letter-spacing:.5mm; margin-bottom:1.4mm; border-bottom:.3mm solid var(--ink); padding-bottom:1mm}}
.contra p {{margin-bottom:1mm}}
/* отзывы */
.rev {{border:.35mm solid var(--ink); background:#fff; padding:2.6mm 3mm; margin-bottom:2.6mm; font-size:3.15mm; line-height:1.42}}
.rev-s {{font-family:JBM; font-size:2.7mm; color:var(--grn); margin-top:1.4mm; font-weight:700}}
/* возражения */
.obj {{border-left:1.1mm solid var(--grn); padding:1.6mm 0 1.6mm 4mm; margin-bottom:4mm}}
.obj-q {{font-family:OXA; font-weight:800; font-size:4.6mm; margin-bottom:1.6mm}}
.finis-lines {{margin-top:5mm; font-family:UNB; font-weight:800; font-size:4.6mm; line-height:1.5}}
/* оплата */
.qr-slot {{position:absolute; top:64mm; left:16mm; width:78mm; height:78mm; border:.8mm dashed var(--grn); background:#fff; display:flex; align-items:center; justify-content:center; font-family:JBM; font-size:3mm; color:var(--mut); text-align:center}}
.qr-cap {{position:absolute; top:148mm; left:16mm; width:78mm; font-family:JBM; font-size:2.6mm; line-height:1.7; letter-spacing:.3mm}}
.qr-cap b {{color:var(--grn)}}
.tx-pay {{position:absolute; top:186mm; left:12mm; right:12mm}}
.gate {{position:absolute; top:62mm; right:12mm; width:88mm; height:117mm; border:.35mm solid var(--ink); overflow:hidden}}
.gate img {{width:100%; height:100%; object-fit:cover}}
/* обложка/финал */
.cover-img {{position:absolute; inset:0; width:100%; height:100%; object-fit:cover}}
.cover-shade {{position:absolute; inset:0; background:linear-gradient(180deg, rgba(237,238,240,.06) 40%, rgba(237,238,240,.94) 72%, #EDEEF0 88%)}}
.logo-plate {{position:absolute; top:11mm; left:50%; transform:translateX(-50%); background:var(--ink); color:#fff; font-family:JBM; font-size:3mm; letter-spacing:1mm; padding:1.6mm 4mm}}
.cover-title {{position:absolute; top:176mm; left:12mm; right:12mm; font-family:UNB; font-weight:900; font-size:17.5mm; line-height:1.0; letter-spacing:-.4mm; text-transform:uppercase}}
.cover-mono {{position:absolute; top:218mm; left:12.4mm; font-family:JBM; font-size:3.1mm; letter-spacing:.55mm; color:var(--ink)}}
.cover-bottom {{position:absolute; bottom:12mm; left:12mm; right:12mm}}
.cover-slogan {{font-family:OXA; font-weight:800; font-size:5.6mm; margin-bottom:2mm}}
.cover-slogan span {{font-family:RUB; font-weight:600; font-size:3.8mm; color:var(--ink)}}
.cover-dek {{font-size:3.5mm; max-width:150mm; margin-bottom:2.4mm}}
.cover-credit {{font-family:JBM; font-size:2.6mm; letter-spacing:.4mm; color:#5a616b}}
.finale-bottom {{position:absolute; bottom:11mm; left:12mm; right:12mm; text-align:center; background:rgba(237,238,240,.86); border:.35mm solid var(--ink); padding:4mm 6mm}}
.finale-line {{font-family:UNB; font-weight:900; font-size:6.4mm; margin-bottom:2.4mm}}
.colophon {{font-family:JBM; font-size:2.7mm; letter-spacing:.5mm; color:#5a616b; line-height:1.7}}
'''

html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
open(OUT_HTML,'w').write(html)
print('HTML:', len(html)//1024, 'KB')

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = b.new_page()
    pg.goto('file://'+OUT_HTML, wait_until='networkidle', timeout=120000)
    pg.pdf(path=OUT_PDF, width='200mm', height='280mm', print_background=True,
           prefer_css_page_size=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
    b.close()
print('Готово:', OUT_PDF, round(os.path.getsize(OUT_PDF)/1e6,1), 'MB')
