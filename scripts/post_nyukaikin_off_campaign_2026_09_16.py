"""
月間お見合い成立10万組突破を記念して。あすなる愛媛も入会金11,000円OFFの応援キャンペーンをはじめます
カテゴリ: お知らせ
2026-09-16
"""
import os, sys, uuid, requests

sys.path.insert(0, os.path.dirname(__file__))
from eyecatch_composer import compose_eyecatch

WIX_API_KEY = os.environ.get("WIX_API_KEY", "")
WIX_SITE_ID = "d01daac5-b796-4bd3-b09b-6d9bbcc37573"
WIX_BASE    = "https://www.wixapis.com"
MEMBER_ID   = "69e25236-d316-4da8-92e4-f500aca1fe37"

CATEGORY_IDS = [
    "fc247847-d52b-438c-ab23-95bae771dc0a",  # お知らせ
]
TAG_IDS = [
    "32413ff0-17fc-455e-93e1-3add76e9eb46",  # キャンペーン
    "4e730deb-5ff8-414c-a0ea-7fcde43eb113",  # 新規ご入会
    "61acc4f3-6c16-4653-995b-dd6d9136c1d3",  # IBJ
    "870be40e-713f-4c96-936c-75deb5ce8ddf",  # 婚活
    "01cf27f1-8406-473d-83d5-6b5f78950218",  # NLP
    "a1cddd3a-c52b-47f4-b1bf-3c8ce905ebc5",  # コミュニケーション心理学
    "8e779610-2acc-448e-b6b0-ad65dbb418d1",  # 無料相談
]
RELATED_POST_IDS = [
    "2a152014-7369-4a0c-b10d-ecaa654d19da",  # 会員11万名突破キャンペーンのお知らせ（前回同種）
    "c3d17505-356c-419e-9e6f-496bd4f04b1d",  # IBJ AWARD受賞
    "43d9ae43-938c-47a0-b889-e5aa397b6e07",  # AI美知仲人コーチ誕生
]

TITLE = "月間お見合い成立10万組突破を記念して。あすなる愛媛も入会金11,000円OFFの応援キャンペーンをはじめます"
EXCERPT = "IBJの月間お見合い成立数が10万組を突破したことを記念して、あすなる愛媛では期間限定で入会金を11,000円OFFにします。20代割引との併用も可能。年末年始に向けて動き出すのにちょうどいいタイミングです。"
FOCUS_KEYWORD = "愛媛 結婚相談所 入会金 割引"

REAL_PHOTO_URL = "https://static.wixstatic.com/media/a4e52d_cf3f0f8fec8d40e4ac0e0bb6dfc4771d~mv2.png"

CAMPAIGN_LP_URL = "https://michin-cpu.github.io/asunaru-shindan/campaign/nyukaikin-off-2026-09/?utm_source=blog&utm_medium=cta&utm_campaign=2026-09-nyukaikin-off"

ASSETS_DIR = os.path.expanduser("~/asunaru-shindan/campaign/nyukaikin-off-2026-09/assets")
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "drafts", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

def wix_headers():
    return {"Authorization": WIX_API_KEY, "wix-site-id": WIX_SITE_ID, "Content-Type": "application/json"}

def nid():
    return str(uuid.uuid4())[:8]

def sp():
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": "", "decorations": []}}
    ], "paragraphData": {}}

def p(text):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "paragraphData": {}}

def heading(text):
    return {"type": "HEADING", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": []}}
    ], "headingData": {"level": 2}}

def divider_node():
    return {"type": "DIVIDER", "id": nid(), "nodes": [], "dividerData": {"lineStyle": "SINGLE", "width": "LARGE", "alignment": "CENTER"}}

def section_heading(text):
    return [sp(), divider_node(), sp(), heading(text)]

def link_node_centered(text, url, underline=False):
    decos = [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]
    if underline:
        decos.append({"type": "UNDERLINE"})
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": text, "decorations": decos}}
    ], "paragraphData": {"textStyle": {"textAlignment": "CENTER"}}}

def p_with_link(prefix, link_text, suffix, url):
    return {"type": "PARAGRAPH", "id": nid(), "nodes": [
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": prefix, "decorations": []}},
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": link_text, "decorations": [{"type": "LINK", "linkData": {"link": {"url": url, "target": "BLANK"}}}]}},
        {"type": "TEXT", "id": nid(), "nodes": [], "textData": {"text": suffix, "decorations": []}},
    ], "paragraphData": {}}

def cta_nodes():
    return [
        link_node_centered("⬇️あなたに合った婚活を。無料相談はこちらから！⬇️", "https://www.asunaru.jp/soudan"),
        link_node_centered("https://www.asunaru.jp/soudan", "https://www.asunaru.jp/soudan", underline=True),
    ]

def real_photo_node():
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": REAL_PHOTO_URL}},
                "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
            }}

def image_node(file_obj, caption=""):
    return {"type": "IMAGE", "id": nid(), "nodes": [],
            "imageData": {
                "image": {"src": {"url": file_obj["url"]}}, "caption": caption,
                "containerData": {"width": {"size": "SMALL"}, "alignment": "CENTER"},
            }}

def build_nodes(moment_photo_file):
    nodes = []
    nodes.append(p("こんにちは！松山市駅から徒歩3分。"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛の結婚相談所、プロの心理カウンセラーで仲人の中嶋美知です😊"))
    nodes.append(sp())
    nodes.append(p("毎週水曜9時に女性向け、木曜9時に男性向け、日曜9時に男女皆様へのメッセージをお届けしています。"))
    nodes.append(sp())

    nodes.append(p("IBJ（全国100,000人ネットワーク）のお見合い成立数が、月間10万件を突破しました。"))
    nodes.append(sp())
    nodes.append(p("数字だけ見るとピンとこないかもしれないんですけど、これって「今この瞬間も、10万組近い人が誰かと出会って、次の一歩を踏み出している」ということなんですよね。そう考えると、なんだかじんわり嬉しくなりました。"))
    nodes.append(sp())

    nodes.extend(section_heading("あすなる愛媛でも応援キャンペーンをします"))
    nodes.append(sp())
    nodes.append(p("月間お見合い成立10万組を記念して、期間限定で入会金を11,000円OFFにすることにしました。"))
    nodes.append(sp())
    nodes.append(p("期間は2026年9月19日（土）〜10月18日（日）まで。20代割引（25歳まで5,500円／28歳まで8,250円）との併用もできます。"))
    nodes.append(sp())
    nodes.append(image_node(moment_photo_file, "喜びを渡すから、また喜びが返ってくる。"))
    nodes.append(sp())

    nodes.extend(section_heading("年末年始に向けて、今がちょうどいいタイミングです"))
    nodes.append(sp())
    nodes.append(p("実はこの時期って、年末年始に向けてお見合いやデートがぐっと活発になるシーズンでもあるんです。"))
    nodes.append(sp())
    nodes.append(p("今からプロフィールを整えてお相手探しをはじめておくと、一番出会いが動く年末年始のタイミングに、ちょうどいい形で臨めます。"))
    nodes.append(sp())
    nodes.append(p("私自身、お見合いから3ヶ月弱で成婚しています。動き出すタイミングって、本当に大事だなと実感しています。"))
    nodes.append(sp())

    nodes.extend(section_heading("我慢するのでも、遠回しに伝えるのでもなく"))
    nodes.append(sp())
    nodes.append(p("あすなる愛媛が大事にしているのは、\"素直婚\"という考え方です。"))
    nodes.append(sp())
    nodes.append(p("自分の望みや不安を、我慢せず、でも押し付けもせず、穏やかに素直に伝え合いながら、ふたりでちょうどいい着地点を見つけていく。そんなパートナーシップのことです。"))
    nodes.append(sp())
    nodes.append(p("婚活って、つい「正解」を探しがちになるんですけど、本当は「自分の望みに気づいて、それを素直に伝えられるようになること」の方が、ずっと大事だったりします。"))
    nodes.append(sp())
    nodes.append(p("コミュニケーション心理学NLPトレーナーとして、あなたの望む結婚生活を可能にするコミュニケーション法をお伝えします。"))
    nodes.append(sp())

    nodes.append(real_photo_node())
    nodes.append(sp())

    nodes.append(p("もし気になっていることがあれば、この機会にぜひ一度、お話ししてみませんか。Zoomで30分、売り込みは一切しません。"))
    nodes.append(sp())
    nodes.append(p_with_link("キャンペーンの詳しい内容は、", "こちらのページ", "にまとめています。", CAMPAIGN_LP_URL))
    nodes.append(sp())

    nodes.extend(cta_nodes())
    return nodes

def upload_image_file(local_path, filename, mime="image/jpeg"):
    with open(local_path, "rb") as f:
        image_bytes = f.read()
    r = requests.post(f"{WIX_BASE}/site-media/v1/files/generate-upload-url", headers=wix_headers(),
                       json={"mimeType": mime, "displayName": filename}, timeout=30)
    if not r.ok:
        print("  upload URL failed:", r.status_code, r.text[:200]); return None
    data = r.json()
    upload_url = data.get("uploadUrl") or data.get("upload_url")
    upload_token = data.get("uploadToken") or data.get("upload_token")
    sep = "&" if "?" in upload_url else "?"
    hdrs = {"Content-Type": mime, "Content-Disposition": f'attachment; filename="{filename}"'}
    if upload_token:
        hdrs["Authorization"] = upload_token
    ru = requests.put(f"{upload_url}{sep}filename={filename}", data=image_bytes, headers=hdrs, timeout=60)
    if not ru.ok:
        print("  upload failed:", ru.status_code, ru.text[:200]); return None
    file_obj = ru.json().get("file", {})
    if not file_obj.get("url"):
        print("  URL missing:", ru.json()); return None
    print(f"  -> {file_obj['url'][:80]}...")
    return file_obj

def create_draft():
    moment_photo_path = os.path.join(ASSETS_DIR, "moment-photo.jpg")
    moment_photo_file = upload_image_file(moment_photo_path, "2026-09-16_nyukaikin_off_moment.jpg")
    if not moment_photo_file:
        print("moment-photo.jpg のアップロードに失敗しました。"); return None

    body = {
        "draftPost": {
            "title": TITLE,
            "richContent": {"nodes": build_nodes(moment_photo_file), "metadata": {"version": 1}},
            "categoryIds": CATEGORY_IDS,
            "tagIds": TAG_IDS,
            "relatedPostIds": RELATED_POST_IDS,
            "excerpt": EXCERPT,
            "memberId": MEMBER_ID,
        },
        "publish": False,
    }
    r = requests.post(f"{WIX_BASE}/blog/v3/draft-posts", headers=wix_headers(), json=body, timeout=30)
    if not r.ok:
        print("下書き作成失敗:", r.status_code, r.text[:500])
        return None
    draft = r.json()["draftPost"]
    print("下書き作成完了 ID:", draft["id"])
    return draft["id"]

def set_seo(draft_id):
    seo_patch = {
        "draftPost": {
            "seoData": {
                "tags": [
                    {"type": "title", "children": TITLE},
                    {"type": "meta", "props": {"name": "description", "content": EXCERPT}},
                ],
                "settings": {"preventAutoRedirect": False, "keywords": [{"term": FOCUS_KEYWORD, "isMain": True}]},
            }
        },
        "fieldMask": "seoData",
    }
    rp = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=seo_patch, timeout=30)
    print("SEOメタ更新:", "完了" if rp.ok else f"失敗 {rp.status_code} {rp.text[:300]}")

def set_eyecatch(draft_id):
    hero_path = os.path.join(ASSETS_DIR, "hero-couple.jpg")
    composed_path = os.path.join(IMAGES_DIR, "2026-09-16_nyukaikin_off_eyecatch_composed.png")
    compose_eyecatch(
        bg_path=hero_path,
        main_html='月間お見合い成立<span class="accent">10万組</span>突破を記念して。<br>入会金<span class="accent">11,000円OFF</span>',
        subtitle_text="――あすなる愛媛、応援キャンペーンをはじめます",
        out_path=composed_path,
        main_size=50,
    )
    eyecatch_file = upload_image_file(composed_path, "2026-09-16_nyukaikin_off_eyecatch_composed.png", mime="image/png")
    if not eyecatch_file:
        print("アイキャッチのアップロードに失敗しました。"); return
    media_patch = {
        "draftPost": {"media": {"custom": True, "wixMedia": {"image": {
            "id": eyecatch_file.get("id", ""), "url": eyecatch_file["url"],
            "height": eyecatch_file.get("height", 1024), "width": eyecatch_file.get("width", 1536),
            "filename": eyecatch_file.get("displayName", "eyecatch.png"),
        }}, "displayed": True}},
        "fieldMask": "media",
    }
    rm = requests.patch(f"{WIX_BASE}/blog/v3/draft-posts/{draft_id}", headers=wix_headers(), json=media_patch, timeout=30)
    print("カバー画像設定:", "完了" if rm.ok else f"失敗 {rm.status_code} {rm.text[:300]}")

if __name__ == "__main__":
    draft_id = create_draft()
    if draft_id:
        set_seo(draft_id)
        set_eyecatch(draft_id)
        print("\nDRAFT_ID =", draft_id)
        print(f"編集URL: https://manage.wix.com/dashboard/{WIX_SITE_ID}/blog/post/{draft_id}")
