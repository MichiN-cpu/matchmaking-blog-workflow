"""
【特別編】結婚報告その3 57歳から婚活→59歳で再婚（2026-12-05(土) 9:00 想定）。Wixには下書き保存のみ（publish:false）。
みっちゃん口述→ジェイ下書き→みっちゃん加筆（11/10朝）。写真は本人提供の実写（その1と共通・公開前に差し替え可）。
ロジックは post_kekkon_houkoku_1_2026_11.py を再利用（設定だけ差し替え）。
使い方: python3 post_kekkon_houkoku_3_2026_12.py     検証のみ: --verify <DRAFT_ID>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_kekkon_houkoku_1_2026_11 as k

k.MD = os.path.join(k.D, "kekkon3_57sai.md")
k.SLUG = "2026-12-05_kekkon-houkoku_3"
k.SEO_SLUG = "57sai-konkatsu-59sai-saikon"
k.CTA_URL = "https://www.asunaru.jp/soudan?utm_source=blog&utm_medium=cta&utm_campaign=2026-12-05-kekkon-houkoku-3"
k.EXCERPT = ("「彼氏がほしい」と言いながら20年。57歳の春にやっと婚活を始めた仲人・中嶋美知が、59歳の秋に再婚しました。"
             "「1年でも早ければ」と何度も思ったまわり道の2年間と、今いちばん大切にしている小さな毎日のこと。結婚報告、その3です。")
k.FOCUS = "57歳 婚活 再婚"
k.TAGS = ["婚活", "再婚", "シニア婚活", "50代婚活", "結婚報告", "別居婚", "57歳仲人婚活始めました", "パートナーシップ"]
k.RELATED = ["771006c5-5963-457e-b7c9-cdf514e0a0ac",   # 57歳仲人、婚活始めました。（第１話）
             "1e4d8345-f803-4522-b7d8-37cf8dbbb1dc",   # 同（第2話）
             "02c1c45f-9569-4010-9371-93e93447abb5"]   # 一緒に暮らせない結婚なんて…（別居婚）
k.LINKS = {}
k.PHOTOS = [
    ("57歳で婚活を始めた私は、59歳の秋に、再婚しました。", "p_sunset.jpg"),
    ("最終的には、このタイミングで、この人と出会えたことが、私にとって最善で、最適で、最高だったと、今は心から思っています。", "p_bouquet2.jpg"),
    ("そんな小さな毎日が、今、とっても心強い安心感になっています。", "p_ferry.jpg"),
]
k.COVER = "cover3_composed.png"

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        k.base.verify(sys.argv[2], k.CTA_URL)
    else:
        k.run()
