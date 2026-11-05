# 「よくあるご相談」インスタ画像（2026-11-05新デザイン：明朝・余白多め・ピンク/ブルーを使わない）
import os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from breaks import B
from PIL import Image, ImageDraw, ImageFont
A='/System/Library/AssetsV2/com_apple_MobileAsset_Font8/'
MIN=A+'a35803b18dea500ee1e426f403635efbe5a84bd4.asset/AssetData/ToppanBunkyuMinchoPr6N-Regular.otf'
MID=A+'36a81f2dad2ef266c50802d85839e0201fcf4e57.asset/AssetData/ToppanBunkyuMidashiMinchoStdN-ExtraBold.otf'
GOM=A+'ee89e7987a76cc8cfdff36c96bd7bc77655b343e.asset/AssetData/YuGothic-Medium.otf'
f=lambda p,s: ImageFont.truetype(p,s)
W,H=1080,1440
THEMES={
 'A':dict(bg=(243,242,237),ink=(38,66,56),acc=(168,138,92),sub=(110,118,112)),   # 深緑×アイボリー×金
 'B':dict(bg=(236,234,231),ink=(52,52,56),acc=(176,104,78),sub=(118,114,110)),   # チャコール×グレージュ×テラコッタ
}
def spaced(d,xy,t,fo,fill,sp):
    w=sum(d.textlength(c,font=fo) for c in t)+sp*(len(t)-1); x=xy[0]-w/2
    for c in t: d.text((x,xy[1]),c,font=fo,fill=fill,anchor='lm'); x+=d.textlength(c,font=fo)+sp
def card(quote,gender,path,th='A'):
    c=THEMES[th]; img=Image.new('RGB',(W,H),c['bg']); d=ImageDraw.Draw(img)
    d.rectangle([48,48,W-48,H-48],outline=c['acc'],width=2)
    d.rectangle([62,62,W-62,H-62],outline=c['acc'],width=1)
    spaced(d,(W/2,190),'よくあるご相談',f(MIN,44),c['ink'],14)
    d.line([(W/2-40,250),(W/2+40,250)],fill=c['acc'],width=2)
    spaced(d,(W/2,292),f'{gender}に多いお悩み',f(GOM,28),c['sub'],6)
    d.text((W/2,410),'Q',font=f(MID,170),fill=c['acc'],anchor='mm')
    q=quote.strip().strip('「」'); lines=B[q].split('/')
    for size in ((70,66,62,58,54,50) if len(lines)<4 else (62,58,54,50)):
        qf=f(MID,size)
        if max(d.textlength(l,font=qf) for l in lines)<=820: break
    lh=int(size*1.75); total=lh*len(lines); top=max(560,810-total/2)
    for i,l in enumerate(lines): d.text((W/2,top+lh*i+lh/2),l,font=qf,fill=c['ink'],anchor='mm')
    y=min(top+total+90,H-330)
    d.text((W/2,y),'— 公認心理師の仲人が、お答えします —',font=f(MIN,34),fill=c['sub'],anchor='mm')
    d.line([(160,H-250),(W-160,H-250)],fill=c['acc'],width=1)
    spaced(d,(W/2,H-190),'あすなる愛媛 結婚相談所',f(MIN,40),c['ink'],6)
    d.text((W/2,H-135),'松山市駅から徒歩3分',font=f(GOM,28),fill=c['sub'],anchor='mm')
    img.save(path)
if __name__=='__main__':
    O=os.path.expanduser('~/Desktop/インスタ画像_よくあるご相談')
    for th in 'AB':
        card('いい人ほど、好きになれないんです','女性',f'{O}/見本{th}_女性.png',th)
        card('自分なんか、モテるわけないですよ','男性',f'{O}/見本{th}_男性.png',th)
    print(sorted(os.listdir(O)))
