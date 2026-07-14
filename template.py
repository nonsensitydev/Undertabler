"""
HTML/CSS template for the schedule graphic.
This is a direct, flattened translation of the original SCSS module into a
standalone stylesheet (no build step / no Next.js required), so a headless
browser can render it exactly like the production Puppeteer screenshot does.
"""

CSS = """
@font-face {
  font-family: "IBM Plex Sans Thai";
  src: url("fonts/IBMPlexSansThai-Regular.ttf") format("truetype");
  font-weight: 400;
}
@font-face {
  font-family: "IBM Plex Sans Thai";
  src: url("fonts/IBMPlexSansThai-Medium.ttf") format("truetype");
  font-weight: 500;
}
@font-face {
  font-family: "IBM Plex Sans Thai";
  src: url("fonts/IBMPlexSansThai-SemiBold.ttf") format("truetype");
  font-weight: 600;
}

* { box-sizing: border-box; }

body, html {
  margin: 0;
  padding: 0;
  font-family: "IBM Plex Sans Thai", sans-serif;
  font-size: 16px;
  background-color: transparent !important;
}

.wrapper {
  border: 0px solid #ffffff;
  width: 2388px;
  height: 1768px;
  background-color: transparent !important; /* OVERRIDDEN FOR TRANSPARENCY */
  position: relative;
  margin: 0 auto;
  overflow: hidden;
}

.logo {
  position: relative;
  width: 75px;
  height: 59px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  font-weight: 600;
  font-size: 40px;
  line-height: 59px;
}

.wrapper > .header {
  display: flex;
  width: calc(2388px - 302px);
  padding-top: 340px;
  margin: 0 auto;
  justify-content: space-between;
  align-items: center;
}

.wrapper > .header > .left {
  display: flex;
  align-items: center;
}

.wrapper > .header > .left > .title-container {
  display: inline-block;
}
.wrapper > .header > .left > .title-container > .title {
  font-size: 88px;
  line-height: 1.15;
  font-weight: 600;
  margin: 0;
}
.wrapper > .header > .left > .title-container > .subtitle {
  font-size: 36px;
  font-weight: 500;
  margin: 0;
}

.wrapper > .header > .right {
  text-align: right;
}
.wrapper > .header > .right > .room {
  font-size: 42px;
  margin-bottom: 16px;
  margin-top: 0;
  font-weight: 500;
}
.wrapper > .header > .right > .teacher > .text {
  font-size: 32px;
  margin: 0;
}

.wrapper > .main {
  margin: 115px auto 0 auto;
  position: relative;
}

.wrapper > .main > .days {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 90%;
  margin-left: 30px;
}

.wrapper > .main > .days > .day {
  width: 100%;
  position: relative;
  margin-bottom: 106px;
}
.wrapper > .main > .days > .day:last-child {
  margin-bottom: 0;
}

.wrapper > .main > .days > .day > .button {
  position: relative;
  display: inline-block;
  border-radius: 36px;
  padding: 23px 0;
  font-size: 36px;
  z-index: 2;
  width: 238.7px;
  text-align: center;
  /* OVERRIDDEN FOR TRANSPARENCY */
  background-color: transparent !important; 
  box-shadow: none !important;
}

.wrapper > .main > .days > .day > .line {
  height: 28px;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  /* OVERRIDDEN FOR TRANSPARENCY */
  background-color: transparent !important; 
  box-shadow: none !important;
}

.schedules {
  position: absolute;
  top: -16px;
  left: 300px;
  z-index: 3;
}

.schedules > .mon-to-thurs {
  display: flex;
  flex-direction: row;
}

.schedules > .mon-to-thurs > .col {
  position: relative;
  display: flex;
  flex-direction: column;
}

.schedules > .mon-to-thurs > .col > .time {
  font-family: "Roboto", "IBM Plex Sans Thai", sans-serif;
  position: absolute;
  top: -48px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  font-size: 24px;
  width: 100%;
  margin-right: 15px;
}

.schedules > .mon-to-thurs > .col > .button {
  position: relative;
  display: inline-block;
  border-radius: 20px;
  font-size: 36px;
  width: 197.5px;
  height: 162px;
  margin-bottom: 42px;
  margin-left: 15px;
  z-index: 2;
  /* OVERRIDDEN FOR TRANSPARENCY */
  background-color: transparent !important; 
  box-shadow: none !important;
}
.schedules > .mon-to-thurs > .col > .button:last-child {
  margin-bottom: 0;
}

.schedules > .mon-to-thurs > .col > .blank {
  position: relative;
  display: inline-block;
  width: 225px;
  height: 162px;
  margin-bottom: 42px;
}
.schedules > .mon-to-thurs > .col > .blank:last-child {
  margin-bottom: 0;
}

.schedules > .mon-to-thurs > .col > .break10-button {
  position: relative;
  display: inline-block;
  border-radius: 17px;
  width: 76px;
  height: 100%;
  margin-bottom: 0;
  padding-top: 250px;
  margin-right: 0;
  margin-left: 15px;
  z-index: 2;
  /* OVERRIDDEN FOR TRANSPARENCY */
  background-color: transparent !important; 
  box-shadow: none !important;
}
.schedules > .mon-to-thurs > .col > .break10-button.no-afternoon {
  height: 79%;
}
.schedules > .mon-to-thurs > .col > .break10-button > .text {
  text-align: center;
  color: #a6a8ab;
  font-size: 24px;
  width: 100%;
  margin-top: 48px;
  margin-bottom: 64px;
}

.schedules > .mon-to-thurs > .col > .lunch-button {
  position: relative;
  display: inline-block;
  border-radius: 17px;
  width: 130px;
  height: 100%;
  margin-bottom: 0;
  padding-top: 245px;
  margin-left: 15px;
  /* OVERRIDDEN FOR TRANSPARENCY */
  background-color: transparent !important; 
  box-shadow: none !important;
}
.schedules > .mon-to-thurs > .col > .lunch-button.no-afternoon {
  height: 79%;
}
.schedules > .mon-to-thurs > .col > .lunch-button > .text {
  text-align: center;
  color: #a6a8ab;
  font-size: 24px;
  width: 100%;
  margin-top: 48px;
  margin-bottom: 64px;
}

.schedules > .mon-to-thurs > .col > .button > .text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
  padding: 0 10px;
}
.schedules > .mon-to-thurs > .col > .button > .text > .subject {
  width: 100%;
  font-size: 24px;
  display: block;
  line-height: 1.2;
  margin-bottom: 10px;
  color: #000;
  font-weight: 400;
  white-space: break-spaces;
  word-wrap: break-word;
}
.schedules > .mon-to-thurs > .col > .button > .text > .teacher {
  width: 100%;
  font-size: 18px;
  color: #a6a8ab;
  word-wrap: break-word;
  margin: 0;
}
"""


def esc(s):
  """Minimal HTML escaping for text content."""
  if s is None:
      return ""
  return (
      str(s)
      .replace("&", "&amp;")
      .replace("<", "&lt;")
      .replace(">", "&gt;")
  )


def render_html(ctx: dict) -> str:
  """
  ctx keys:
    title, subtitle          -> header left text
    room, branch             -> header right first line
    teachers: [str]          -> header right teacher list
    color: {bg,t1,t2,logo}   -> theme text colors (CSS color strings, e.g. '#D17474')
    days: [ {name, color, text_color, line_width, columns_html} ]
    periods_html: str        -> the full .schedules > .mon-to-thurs inner HTML
  """
  color = ctx["color"]

  days_html = ""
  for d in ctx["days"]:
      days_html += f"""
      <div class="day">
        <div class="button" style="color:{d['text_color']};">{esc(d['name'])}</div>
        <div class="line" style="width:{d['line_width']}px;"></div>
      </div>"""

  teachers_html = "".join(
      f'<p class="text">{esc(t)}</p>' for t in ctx.get("teachers", [])
  )

  return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <div class="left">
        <div class="title-container">
          <h1 class="title" style="color:{color['t1']};">{esc(ctx['title'])}</h1>
          <p class="subtitle" style="color:{color['t2']};">{esc(ctx['subtitle'])}</p>
        </div>
      </div>
      <div class="right">
        <h2 class="room" style="color:{color['t2']};">ห้อง {esc(ctx['room'])} | {esc(ctx['branch'])}</h2>
        <div class="teacher" style="color:{color['t2']};">{teachers_html}</div>
      </div>
    </div>
    <div class="main">
      <div class="days">{days_html}
      </div>
      <div class="schedules">
        <div class="mon-to-thurs">{ctx['periods_html']}
        </div>
      </div>
    </div>
    <div class="logo" style="color:{color['logo']};">กช.</div>
  </div>
</body>
</html>"""