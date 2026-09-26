from PIL import Image, ImageDraw, ImageFont
W,H=1080,1350
B='/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'; R='/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'
M='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc'
BG=(244,248,251); CARD=(255,255,255); ACC=(92,140,170); TXT=(52,58,64); SUB=(120,130,140)
NG_HEAD=set('、。，．」』）！？ー…っゃゅょぁぃぅぇぉッャュョ')
def wrap(d,text,font,maxw):
    lines=[];cur=''
    for ch in text:
        if d.textlength(cur+ch,font=font)>maxw:
            if ch in NG_HEAD: cur+=ch; lines.append(cur); cur=''; continue
            lines.append(cur); cur=ch
        else: cur+=ch
    if cur: lines.append(cur)
    return lines
def emoji(ch,size):
    f=ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc',160)
    im=Image.new('RGBA',(180,180),(0,0,0,0)); ImageDraw.Draw(im).text((0,0),ch,font=f,embedded_color=True)
    return im.crop(im.getbbox()).resize((size,size),Image.LANCZOS)
def make(no,paras,out,size,tail_emoji=None):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rounded_rectangle((50,50,W-50,H-50),radius=36,fill=CARD)
    fh=ImageFont.truetype(B,30); ft=ImageFont.truetype(B,46); fq=ImageFont.truetype(M,150); fb=ImageFont.truetype(R,size)
    d.text((110,110),"MORNING JOURNAL",font=fh,fill=ACC)
    d.text((110,158),f"参加者さんの声　{no}/2",font=ft,fill=TXT)
    d.line((110,232,300,232),fill=ACC,width=4)
    d.text((W-230,95),"“",font=fq,fill=(214,228,237))
    y=285; lh=int(size*1.75); maxw=W-220
    last=None
    for i,p in enumerate(paras):
        for ln in wrap(d,p,fb,maxw):
            d.text((110,y),ln,font=fb,fill=TXT); last=(110+d.textlength(ln,font=fb),y); y+=lh
        y+=int(size*0.7)
    if tail_emoji and last:
        e=emoji(tail_emoji,size+4); im.paste(e,(int(last[0])+6,last[1]-2),e)
    fs=ImageFont.truetype(R,30)
    d.text((110,H-150),"モーニングジャーナル第11期　10月5日（月）スタート",font=fs,fill=SUB)
    d.text((110,H-108),"いつからでも始められます",font=fs,fill=SUB)
    print(out,'bottom y =',y)
    im.save(out)
v1=["最初に『モーニングジャーナルを始める』と知ったときは、『すごいなぁ』と思いました。でも同時に、『私には無理だろうなぁ』とも感じていました。",
"そんな私が、あるときふと、『モーニングジャーナルをやってみよう』と思ったんです。なぜそう思ったのかは、自分でもよく分かりませんが、何かの直感が働いたのでしょう。",
"続けている人を見て『すごいなぁ、私とは違うなぁ』と思っていたのに、気がつけば私も自然と続けられていました。あと一カ月でモーニングジャーナルも一年になります。ノートも2冊目です。朝の夢や、昨日の出来事、今浮かんだことなどを、いろいろ書いています。",
"『私には無理だなぁ』と思っている方もいるかもしれませんが、最初から完璧にやろうとしなくても大丈夫です。ゆるりと一緒にやりましょう！"]
v2=["毎朝、メンバーに会える楽しみと、休んでも普通に受け入れてくれる安心感で、いつの間にか続いていました。",
"起床時間が決まると、生活が整う。朝の書き出しで、自分の位置が見える。人の書き出しを聞いて、視野が広がる。",
"参加したり休んだり、ゆるゆると11期目。人生が主体的になりました。直感で動いたり、面白いご縁に気づいたり、やらかしても、まあ平気だったり。毎日のゆるーい積み重ねのおかげです。そこに居場所があるって、根っこができました。ありがとうございます"]
make(1,v1,'ig_voice_1.png',33)
make(2,v2,'ig_voice_2.png',36,tail_emoji='🙌')
