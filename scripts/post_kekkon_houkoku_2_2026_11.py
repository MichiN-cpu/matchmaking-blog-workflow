"""
【特別編】結婚報告その2 母の訪問着（2026-11-28(土) 9:00 想定）。Wixには下書き保存のみ（publish:false）。
みっちゃん口述→ジェイ下書き→みっちゃん加除修正（11/9）。写真は本人提供の実写3枚。
ロジックは post_kekkon_houkoku_1_2026_11.py を再利用（設定だけ差し替え）。
使い方: python3 post_kekkon_houkoku_2_2026_11.py     検証のみ: --verify <DRAFT_ID>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_kekkon_houkoku_1_2026_11 as k

k.MD = os.path.join(k.D, "kekkon2_houmongi.md")
k.SLUG = "2026-11-28_kekkon-houkoku_2"
k.SEO_SLUG = "haha-no-houmongi"
k.CTA_URL = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-11-28-kekkon-houkoku-2"
k.EXCERPT = ("59歳の神前挙式で、花嫁衣装に選んだのは、20代のころ母が作ってくれたピンクの訪問着。"
             "「もう着る場所がない」としまっていた一枚に、大正ロマンの髪型と着物柄のネイルを合わせて。仲人・中嶋美知の結婚報告、その2です。")
k.FOCUS = "訪問着 結婚式 50代"
k.TAGS = ["婚活", "再婚", "シニア婚活", "結婚報告", "神前式", "訪問着", "着物", "57歳仲人婚活始めました"]
k.RELATED = ["771006c5-5963-457e-b7c9-cdf514e0a0ac",   # 57歳仲人、婚活始めました。（第１話）
             "1e4d8345-f803-4522-b7d8-37cf8dbbb1dc",   # 同（第2話）
             "54ddc242-fc91-4f71-8d4a-c5914805df56"]   # ネイルサロンの椅子から見えた、仲良し夫婦の共通点（junco*さん）
k.LINKS = {"junco*さん": ("junco*さん", "https://www.instagram.com/p/Dedtzv0kuaw/")}
k.PHOTOS = [
    ("今日は、その日に着た着物のお話です👘", "p2_walk.jpg"),
    ("山田先生と相談して、ヘアは大正ロマンの雰囲気にしていただきました。", "p2_shinzen.jpg"),
    ("当日は、サプライズで来てくれた友人たちが「きれい！」と言ってくれて💕", "p2_smile.jpg"),
]
k.COVER = "cover2_composed.png"

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        k.base.verify(sys.argv[2], k.CTA_URL)
    else:
        k.run()
