#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
post_20nen_no_jibun.py
20年後の幸せな自分から、今日の婚活へのメッセージ - Wix投稿スクリプト
カテゴリ: お見合い
"""

import os
import re
import time
import uuid
import requests

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"
CATEGORY_ID = "5089ac63-e2ce-4de1-b472-3512a77401af"  # お見合い

RELATED_POST_IDS = [
    "58079daf-693b-48bd-b4e0-9bfcc0ae918d",
    "03c53a37-76a8-4c0c-8320-8adbc613a7c7",
    "1e95a04e-83c1-4f80-a204-cacc6c740c35",
]

EXCERPT = "婚活がうまくいかないとき、問題を掘り続けてしんどくなっていませんか。20年後の幸せな自分を先に生きる未来思考の婚活で、心が軽くなるアプローチをご紹介します。"

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts", "images")


# ── ノードヘルパー ───────────────────────────────────────────────────────────────

def nid():
    return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {
        "lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"
    }}

def make_text_nodes(text):
    result, pos = [], 0
    for m in re.compile(r'https?://\S+').finditer(text):
        if m.start() > pos:
            result.append({"type": "TEXT", "id": nid(), "nodes": [],
                           "textData": {"text": text[pos:m.start()], "decorations": []}})
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": m.group(0), "decorations": [
                           {"type": "LINK", "linkData": {"link": {"url": m.group(0), "target": "BLANK"}}}
                       ]}})
        pos = m.end()
    if pos < len(text):
        result.append({"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": text[pos:], "decorations": []}})
    return result or [{"type": "TEXT", "id": nid(), "nodes": [],
                       "textData": {"text": "", "decorations": []}}]

def p(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": make_text_nodes(text), "paragraphData": {}}

def h(text, level=2):
    return {"type": "HEADING", "id": nid(),
            "nodes": [{"type": "TEXT", "id": nid(), "nodes": [],
                        "textData": {"text": text, "decorations": []}}],
            "headingData": {"level": level}}

def heading_block(text, level=2):
    return [sp(), divider_node(), sp(), h(text, level)]

def img_node(file_info, caption=""):
    url = file_info["url"]
    m = re.search(r"/media/([^?#\s]+)", url)
    wix_uri = f"wix:image://v1/{m.group(1)}/img.png" if m else url
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {"image": {"src": {"url": wix_uri}}, "caption": caption}}


# ── Wixヘッダー ─────────────────────────────────────────────────────────────────

def wix_headers():
    return {
        "Authorization": WIX_API_KEY,
        "wix-site-id":   WIX_SITE_ID,
        "Content-Type":  "application/json",
    }


# ── ローカル画像 → Wix Media アップロード ──────────────────────────────────────

def upload_local_image(local_path, display_name):
    print(f"  アップロード中: {display_name}")

    # アップロードURL取得
    resp = requests.post(
        f"{WIX_BASE}/site-media/v1/files/generate-upload-url",
        headers=wix_headers(),
        json={"mimeType": "image/png", "fileName": display_name},
        timeout=30,
    )
    if not resp.ok:
        print(f"  アップロードURL生成失敗: {resp.status_code} {resp.text[:200]}")
        return None

    data = resp.json()
    upload_url   = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token", "")

    if not upload_url:
        print(f"  uploadUrl取得失敗: {data}")
        return None

    # ファイルをPUT
    with open(local_path, "rb") as f:
        file_bytes = f.read()

    params = {"filename": display_name}
    if upload_token:
        params["uploadToken"] = upload_token

    put_resp = requests.put(
        upload_url,
        headers={"Content-Type": "image/png"},
        params=params,
        data=file_bytes,
        timeout=120,
    )
    if not put_resp.ok:
        print(f"  PUT失敗: {put_resp.status_code} {put_resp.text[:200]}")
        return None

    # レスポンスからfile_idを取得
    try:
        put_data = put_resp.json()
    except Exception:
        put_data = {}

    file_id = (
        (put_data.get("file") or {}).get("id")
        or put_data.get("fileId")
        or put_data.get("id")
    )

    if not file_id:
        print(f"  file_id取得失敗: {put_data}")
        return None

    # READY になるまで待機
    for i in range(20):
        time.sleep(3)
        chk = requests.get(f"{WIX_BASE}/site-media/v1/files/{file_id}",
                           headers=wix_headers(), timeout=15)
        if chk.ok:
            fd = chk.json().get("file", {})
            state = fd.get("state", "")
            if state in ("READY", "OK"):
                url = fd.get("url", "")
                m = re.search(r"/media/([^?#\s]+)", url)
                print(f"  完了: {url[:70]}...")
                return {"url": url, "id": m.group(1) if m else file_id,
                        "height": 1024, "width": 1792, "filename": display_name}
            print(f"  待機中... ({state}, {i+1}/20)")
        else:
            print(f"  確認失敗: {chk.status_code}")

    print("  タイムアウト")
    return None


# ── richContent 構築 ───────────────────────────────────────────────────────────

def build_nodes(img2=None, img3=None):
    nodes = []

    # 冒頭挨拶（2段落）
    nodes.append(p("こんにちは！松山市駅から徒歩3分。あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("婚活をしていると、こんな気持ちになること、ありませんか？"))
    nodes.append(sp())

    # イントロ
    nodes.append(p("「お見合いがうまくいかなかった」"))
    nodes.append(p("「また断られた」"))
    nodes.append(p("「どうして私だけこんなに時間がかかるんだろう」"))
    nodes.append(sp())
    nodes.append(p("そういうとき、多くの人が「自分の何がダメなんだろう」と原因を探し始めます。"))
    nodes.append(sp())
    nodes.append(p("もっと条件を緩めるべき？もっと笑顔を増やすべき？もっと話題を準備するべき？"))
    nodes.append(sp())
    nodes.append(p("掘れば掘るほど、なんだかどんどん重くなっていく。婚活が楽しくなくなる瞬間は、たいていここにあります。"))

    # Section 1
    nodes.extend(heading_block("不安は性格ではなく、反応パターンです"))
    nodes.append(p("「うまくいかないとき自分を責める」——これは、あなたの性格が暗いのでも、ネガティブなのでもありません。"))
    nodes.append(sp())
    nodes.append(p("幼いころから「うまくいかないのは自分のせい」と感じるように、無意識にパターンが作られてきただけのことです。"))
    nodes.append(sp())
    nodes.append(p("右利きの人が左手でお箸を持つとうまく使えないように、これまでの反応パターンのまま婚活をすると、なんとなくしっくりこない。それだけのことです。"))

    # Section 2
    nodes.extend(heading_block("今日は逆の方向から考えてみましょう"))
    nodes.append(p("問題を掘るのをいったん止めて、こんな問いを自分に投げかけてみてください。"))
    nodes.append(sp())
    nodes.append(p("「もし20年後、幸せなパートナーシップを築いている自分がいるとしたら、その自分は今日の私に何を言いたいだろう？」"))
    nodes.append(sp())
    nodes.append(p("少し目を閉じて、想像してみてください。"))

    # 画像2（本文差し込み）
    if img2:
        nodes.append(sp())
        nodes.append(img_node(img2, "20年後、一緒に歩いている"))
        nodes.append(sp())

    # Section 3
    nodes.extend(heading_block("ミニワーク：未来の自分からのメッセージを受け取る"))
    nodes.append(p("以下の問いに、思いついたままに答えてみてください。正解はありません。"))
    nodes.append(sp())
    nodes.append(p("① 20年後の幸せなあなたは、どんな朝を迎えていますか？"))
    nodes.append(p("（例：好きなコーヒーを飲みながら、パートナーと今日の話をしている）"))
    nodes.append(sp())
    nodes.append(p("② その自分は、今日の婚活中のあなたに、何と声をかけてくれますか？"))
    nodes.append(p("（思い浮かぶ言葉を、そのまま心の中で受け取ってみてください）"))
    nodes.append(sp())
    nodes.append(p("③ 焦らなくていい、と言われたとしたら、今日どんな行動が変わりますか？"))

    # Section 4
    nodes.extend(heading_block("あなたはもう、素敵なパートナーです"))
    nodes.append(p("私が最近、会員さんに伝えているアプローチがあります。それは「なりたい自分を先に生きてみる」というものです。"))
    nodes.append(sp())
    nodes.append(p("幸せなパートナーシップを築いている未来の自分だったら、今日のお見合いにどんな心持ちで臨むだろう？今日の断りをどんなふうに受け取るだろう？次の出会いに、どんな期待を持つだろう？"))
    nodes.append(sp())
    nodes.append(p("答えを出すことより、問いを持って過ごすことが、婚活の質を変えていきます。"))

    # 画像3（本文差し込み）
    if img3:
        nodes.append(sp())
        nodes.append(img_node(img3, "未来の自分に問いかけるワーク"))
        nodes.append(sp())

    # Section 5
    nodes.extend(heading_block("じんわり、でも確かに変わります"))
    nodes.append(p("婚活がうまくいかない理由を探し続けていたあなたが、「20年後の幸せな自分はどんな人だろう」と想像し始める。その小さな視点の転換が、出会いへの向き合い方を変えます。"))
    nodes.append(sp())
    nodes.append(p("相手を評価する目より、自分が幸せでいられる場所を見つける目になる。「どうせ私なんて」という声より、「この人と一緒にいたら楽しいかな」という問いが先に立つ。"))
    nodes.append(sp())
    nodes.append(p("疲れて帰った夜に、ただいまと言える人がいる。そんな日常の温かさを、一緒に描いていきましょう。"))
    nodes.append(sp())
    nodes.append(p("婚活は、なりたい自分になる旅です。"))

    # CTA
    nodes.append(sp())
    nodes.append(p("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️ https://www.asunaru.jp/soudan"))

    return nodes


# ── メイン ────────────────────────────────────────────────────────────────────

def main():
    today  = "2026-05-02"
    title  = "20年後の幸せな自分から、今日の婚活へのメッセージ"

    print("\n[1/3] ローカル画像をWix Mediaにアップロード中...")
    img1 = upload_local_image(
        os.path.join(IMAGES_DIR, f"{today}_img1.png"),
        f"{today}_eyecatch.png",
    )
    img2 = upload_local_image(
        os.path.join(IMAGES_DIR, f"{today}_img2.png"),
        f"{today}_img2.png",
    )
    img3 = upload_local_image(
        os.path.join(IMAGES_DIR, f"{today}_img3.png"),
        f"{today}_img3.png",
    )

    print("\n[2/3] richContentを構築中...")
    nodes = build_nodes(img2=img2, img3=img3)
    print(f"  ノード数: {len(nodes)}")

    draft_post = {
        "title":          title,
        "memberId":       MEMBER_ID,
        "richContent":    {"nodes": nodes},
        "categoryIds":    [CATEGORY_ID],
        "excerpt":        EXCERPT,
        "relatedPostIds": RELATED_POST_IDS,
    }

    # カバー画像
    if img1:
        m = re.search(r"/media/([^?#\s]+)", img1["url"])
        draft_post["media"] = {
            "custom": True,
            "wixMedia": {"image": {
                "id":       m.group(1) if m else img1["id"],
                "url":      img1["url"],
                "height":   img1["height"],
                "width":    img1["width"],
                "filename": img1["filename"],
            }},
        }

    # SEOデータ
    draft_post["seoData"] = {
        "tags": [
            {"type": "title",  "children": title},
            {"type": "meta",   "props": {"name": "description", "content": EXCERPT}},
        ]
    }

    print("\n[3/3] Wix Blog 下書き作成中...")
    resp = requests.post(
        f"{WIX_BASE}/blog/v3/draft-posts",
        headers=wix_headers(),
        json={"draftPost": draft_post},
        timeout=30,
    )

    if not resp.ok:
        print(f"Wix投稿失敗: {resp.status_code}\n{resp.text[:500]}")
        return

    draft_id = resp.json().get("draftPost", {}).get("id")
    print(f"\n完了！")
    print(f"  Wix下書きID: {draft_id}")
    print(f"  管理画面: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog")


if __name__ == "__main__":
    main()
