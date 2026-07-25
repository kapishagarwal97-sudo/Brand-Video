#!/usr/bin/env python3
"""Produce a self-contained copy of storyboard.html with media inlined as data URIs.

The repo copy of storyboard.html references the real files next to it. A published
Artifact can't reach those, so this bakes downscaled thumbnails and a 640x360
preview of the film into a single HTML file.
"""
import base64, io, os, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "edit-sheet.html")

SHOTS = ["01-hook-thumbnail.png", "01-hook-thumbnail3.png", "02-endless-scroll.png",
         "03-dead-group-chat.png", "04-couple-apart.png", "04-couple-apart.png1.png",
         "05-data-decline.png", "01-hook-thumbnail2.png", "06-tryb-reveal.png",
         "07-what-energizes-you.png", "08-real-experiences.png", "09-curated-matches.png",
         "10-invitation-gathering.png", "11-real-connection1.png", "11-real-connection.png",
         "12-endcard.png", "12-endcard1.png"]


def jpeg_uri(path, box=560, q=72):
    im = Image.open(path).convert("RGB")
    im.thumbnail((box, box), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def preview_uri():
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    tmp = os.path.join(ROOT, ".preview.mp4")
    subprocess.run([ff, "-y", "-i", os.path.join(ROOT, "tryb-vox-collage-90s.mp4"),
                    "-vf", "scale=640:360", "-c:v", "libx264", "-crf", "31",
                    "-preset", "veryslow", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", tmp],
                   check=True, capture_output=True)
    data = open(tmp, "rb").read()
    os.remove(tmp)
    return "data:video/mp4;base64," + base64.b64encode(data).decode()


def main():
    media = {f: jpeg_uri(os.path.join(ROOT, f)) for f in SHOTS}
    media["__poster__"] = jpeg_uri(os.path.join(ROOT, "poster.jpg"), box=960, q=70)
    media["__film__"] = preview_uri()

    html = open(os.path.join(ROOT, "storyboard.html"), encoding="utf-8").read()
    payload = "<script>window.MEDIA=" + __import__("json").dumps(media) + ";</script>\n"
    # inject before the first script that reads MEDIA
    html = html.replace("<script>\n/* MEDIA is empty", payload + "<script>\n/* MEDIA is empty", 1)
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"wrote {OUT}  ({os.path.getsize(OUT)/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
