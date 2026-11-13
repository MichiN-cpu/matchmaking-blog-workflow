"""12/3男性向けのアイキャッチ差し替え（撮影シーン・手はポケットに入れない）。11/13みっちゃん指示"""
import os, sys, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_omiai_josei_2026_10_14 as base
from eyecatch_composer import compose_eyecatch
c = base.c
DID = "53676df8-72e4-46bb-8bf8-46e141dc0411"
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "drafts", "omiai_kumenai_2026-12")
n = sys.argv[1] if len(sys.argv) > 1 else "v2"
slug = f"2026-12-03_omiai_kumenai_dansei_eyecatch_{n}"
prompt = (base.BASE_STYLE + ", behind-the-scenes of a professional profile photo shoot in a bright clean studio with a light-gray backdrop. "
          "In the foreground, a photographer seen from behind and slightly to the side, holding a DSLR camera up to the eye. "
          "In the background, a friendly-looking Japanese man in his early 40s, East Asian appearance, short neat black hair, clean-shaven, "
          "in a well-fitted navy suit and white shirt, standing in a relaxed friendly pose with a natural warm smile, "
          "both hands clearly visible and OUT of his pockets, arms relaxed at his sides with one hand lightly touching his jacket button, "
          "NO hands in pockets, softbox lights on stands, wide shot, the man on the right side of the frame, lower-left area calm and uncluttered")
bg = base.generate_image(prompt, os.path.join(D, f"{slug}.png"))
out = compose_eyecatch(bg_path=bg, main_html='お見合いが<br><span class="accent">なかなか決まらない？</span>',
                       subtitle_text="―女性がプロフィールで、本当に見ているもの",
                       out_path=os.path.join(D, f"{slug}_composed.png"), main_size=60)
print("COMPOSED", out)
if "--upload" in sys.argv:
    cov = c.upload_image_file(out, os.path.basename(out))
    mp = {"draftPost": {"media": {"custom": True, "wixMedia": {"image": {
          "id": cov.get("id", ""), "url": cov["url"], "height": cov.get("height", 1024),
          "width": cov.get("width", 1536), "filename": os.path.basename(out)}}, "displayed": True}}, "fieldMask": "media"}
    print("cover:", requests.patch(f"{c.WIX_BASE}/blog/v3/draft-posts/{DID}", headers=c.wix_headers(), json=mp, timeout=30).status_code)
