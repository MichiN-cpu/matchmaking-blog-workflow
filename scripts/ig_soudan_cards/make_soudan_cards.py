import re, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from breaks import B
from PIL import Image, ImageDraw, ImageFont
D=os.path.expanduser('~/Desktop')
OUT=os.path.join(D,'インスタ画像_こんな相談がありました'); os.makedirs(OUT,exist_ok=True)
F='/System/Library/Fonts/'
def font(w,s): return ImageFont.truetype(F+f'ヒラギノ角ゴシック W{w}.ttc',s)
MARU=ImageFont.truetype(F+'ヒラギノ丸ゴ ProN W4.ttc',40)
W,H=1080,1440
ACC={'女性':(226,140,165),'男性':(110,145,190)}
PALE={'女性':(252,238,242),'男性':(234,241,250)}
NG='、。，．」』）！？ー…'
BRK='、。？！』」）はがをにでともてのよねなかへ'
def wrap(t,f,maxw,d):
    lines=[];i=0
    while i<len(t):
        j=i;last=-1
        while j<len(t) and d.textlength(t[i:j+1],font=f)<=maxw:
            if t[j] in BRK and (j+1>=len(t) or t[j+1] not in NG): last=j
            j+=1
        if j>=len(t): lines.append(t[i:]);break
        cut = last+1 if last>=i+2 else j
        while cut<len(t) and t[cut] in NG: cut+=1
        lines.append(t[i:cut]);i=cut
    return lines
def card(quote,gender,path):
    img=Image.new('RGB',(W,H),(255,255,255));d=ImageDraw.Draw(img)
    a,p=ACC[gender],PALE[gender]
    d.rectangle([0,0,W,H],fill=p)
    d.rounded_rectangle([60,60,W-60,H-60],radius=48,fill=(255,255,255))
    lab='こんな相談がありました'; lw=d.textlength(lab,font=MARU)
    d.rounded_rectangle([(W-lw)/2-44,130,(W+lw)/2+44,214],radius=42,fill=a)
    d.text((W/2,172),lab,font=MARU,fill=(255,255,255),anchor='mm')
    q=quote.strip().strip('「」')
    if q not in B: raise SystemExit('no breaks: '+q)
    lines=B[q].split('/')
    for size in ((66,62,58,54) if len(lines)>=5 else (78,72,66,60,56,52,48)):
        qf=font(6,size)
        if max(d.textlength(l,font=qf) for l in lines)<=820: break
    lh=int(size*1.65); total=lh*len(lines)
    top=max(300,690-total/2)
    big=font(3,150)
    d.text((150,top-40),'「',font=big,fill=a,anchor='lm')
    d.text((W-150,top+total+30),'」',font=big,fill=a,anchor='rm')
    for i,l in enumerate(lines):
        d.text((W/2,top+lh*i+lh/2),l,font=qf,fill=(60,60,60),anchor='mm')
    y=min(top+total+130,H-360)
    d.line([(W/2-80,y),(W/2+80,y)],fill=a,width=3)
    d.text((W/2,y+60),'公認心理師の仲人が、お答えします',font=font(4,36),fill=(110,110,110),anchor='mm')
    d.text((W/2,H-210),'あすなる愛媛 結婚相談所',font=font(6,40),fill=a,anchor='mm')
    d.text((W/2,H-155),'松山市駅から徒歩3分',font=font(3,30),fill=(130,130,130),anchor='mm')
    img.save(path)
items=[]
items.append(('1110','我慢グセ','女性','「素直になれない私のままで、婚活していいのかな」'))
items.append(('1113','週末婚','女性','「結婚しても、お財布も住まいも別々。そんな形は、ありですか？」'))
t=open(os.path.join(D,'インスタ_こんな相談がありました_まとめ.txt'),encoding='utf-8').read()
sched={}
for m in re.finditer(r'\|\s*(\d+)/(\d+)\S*\s*\|\s*(P\d+)',t): sched[m.group(3)]=f'{int(m.group(1)):02d}{int(m.group(2)):02d}'
for m in re.finditer(r'――――――――――（(P\d+)・(.+?)・(女性|男性)向け.*?）[\s\S]*?【こんな相談がありました】\s*\n(「.+」)',t):
    pid,theme,g,q=m.groups()
    items.append((sched.get(pid,'0000'),f'{pid}_{theme}',g,q))
for date,name,g,q in items:
    safe=re.sub(r'[\\/:*?"<>|「」]','',name)
    card(q,g,os.path.join(OUT,f'{date}_{safe}.png'))
print(len(items)); print('\n'.join(sorted(os.listdir(OUT))))
