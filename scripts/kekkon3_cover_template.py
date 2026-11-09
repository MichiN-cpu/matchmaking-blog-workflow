"""結婚報告その3・IBJサムネ用：左に文字パネル、右に縦写真（576x1024）"""
import eyecatch_composer as e
TEMPLATE = """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{width}px;height:{height}px;font-family:'Hiragino Mincho ProN','Hiragino Sans',serif;position:relative;overflow:hidden;
background:linear-gradient(160deg,#2a2238 0%,#4a3046 55%,#8a5446 100%)}}
.bg{{position:absolute;right:0;top:0;width:576px;height:1024px;object-fit:cover}}
.textblock{{position:absolute;left:80px;width:820px;top:50%;transform:translateY(-50%)}}
.line{{color:#fff;font-size:{main_size}px;font-weight:700;line-height:1.45;letter-spacing:.02em}}
.accent{{color:#f6c79a}}
.sub{{margin-top:44px;color:rgba(255,255,255,.88);font-size:{sub_size}px;font-family:'Hiragino Sans',sans-serif;font-weight:500;letter-spacing:.04em;border-top:2px solid rgba(246,199,154,.6);padding-top:28px}}
</style></head><body><img class="bg" src="{bg_path}"><div class="textblock"><div class="line">{main_html}</div><div class="sub">{subtitle_text}</div></div></body></html>"""
e.TEMPLATE = TEMPLATE
compose = e.compose_eyecatch
