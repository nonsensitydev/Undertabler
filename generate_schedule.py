import json
import os
import sys
import glob
from playwright.sync_api import sync_playwright
 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import render_html
 
INPUT_DIR = "input"
OUTPUT_DIR = "output"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- Default theme (matches defaultColors in the original TSX) ----
DEFAULT_COLORS = {
    "bg": "#FFFFFF",
    "t1": "#D17474",
    "t2": "#E28B8B",
    "c1": "#EBB8B8",
    "c2": "#E49E9E",
    "c3": "#E08484",
    "c4": "#D17474",
    "c5": "#BA5757",
}

DAYS = [
    {"num": 1, "name": "จันทร์", "color_key": "c1"},
    {"num": 2, "name": "อังคาร", "color_key": "c2"},
    {"num": 3, "name": "พุธ", "color_key": "c3"},
    {"num": 4, "name": "พฤหัสฯ", "color_key": "c4"},
    {"num": 5, "name": "ศุกร์", "color_key": "c5"},
]

# time_cols mirrors the column order rendered in the original component:
# period columns interleaved with the two break columns and the lunch column.
TIME_COLS = [
    {"type": "p", "period": 1, "label": "07.50-08.40"},
    {"type": "p", "period": 2, "label": "08.40-09.30"},
    {"type": "break10"},
    {"type": "p", "period": 3, "label": "09.40-10.30"},
    {"type": "p", "period": 4, "label": "10.30-11.20"},
    {"type": "lunch"},
    {"type": "p", "period": 5, "label": "12.20-13.10"},
    {"type": "p", "period": 6, "label": "13.10-14.00"},
    {"type": "break10_pm"},  # second break10, gets the "no-afternoon" (79%) height
    {"type": "p", "period": 7, "label": "14.10-15.00"},
    {"type": "p", "period": 8, "label": "15.00-15.50"},
]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def is_dark_or_light(hex_color: str) -> str:
    """
    Approximates the project's isDarkOrLight util. Threshold tuned so the
    5 default pastel-pink day colors all resolve to white pill text, matching
    the reference screenshots.
    """
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "light" if luminance > 200 else "dark"


def build_periods_html(schedule: dict, colors: dict) -> str:
    """
    Builds the .schedules > .mon-to-thurs inner HTML, column by column,
    exactly matching the original component's period-major layout:
    each column is a vertical stack of day-cells (Mon..Fri for periods 1-3,
    Mon..Thu only for periods 4-8, since Friday has no afternoon classes).
    """
    html_parts = []

    for col in TIME_COLS:
        if col["type"] == "p":
            period = col["period"]
            day_count = 5 if period <= 3 else 4
            cells = []
            for day in DAYS[:day_count]:
                slot = schedule.get(str(day["num"]), {}).get(str(period))
                if slot and (slot[0] or slot[1]):
                    name = esc(slot[0])
                    teacher = esc(slot[1]).replace("+", " + ")
                    cells.append(
                        f'<div class="button"><div class="text">'
                        f'<strong class="subject">{name}</strong>'
                        f'<p class="teacher">{teacher}</p>'
                        f"</div></div>"
                    )
                else:
                    cells.append('<div class="blank"></div>')
            html_parts.append(
                f'<div class="col"><div class="time">{esc(col["label"])}</div>{"".join(cells)}</div>'
            )

        elif col["type"] == "break10":
            html_parts.append(
                '<div class="col"><div class="break10-button">'
                '<p class="text">พัก</p><p class="text">10</p><p class="text">นาที</p>'
                "</div></div>"
            )

        elif col["type"] == "break10_pm":
            html_parts.append(
                '<div class="col"><div class="break10-button no-afternoon">'
                '<p class="text">พัก</p><p class="text">10</p><p class="text">นาที</p>'
                "</div></div>"
            )

        elif col["type"] == "lunch":
            html_parts.append(
                '<div class="col"><div class="lunch-button no-afternoon">'
                '<p class="text">พัก</p><p class="text">กลาง</p><p class="text">วัน</p>'
                "</div></div>"
            )

    return "".join(html_parts)


def build_days_html_ctx(schedule: dict, colors: dict):
    days_ctx = []
    for day in DAYS:
        count = sum(
            1
            for p in range(1, 9)
            if schedule.get(str(day["num"]), {}).get(str(p))
            and (
                schedule[str(day["num"])][str(p)][0]
                or schedule[str(day["num"])][str(p)][1]
            )
        )
        color = colors[day["color_key"]]
        days_ctx.append(
            {
                "name": day["name"],
                "color": color,
                "text_color": "#fff" if is_dark_or_light(color) == "dark" else "#444",
                "line_width": 300 + 230 * count,
            }
        )
    return days_ctx


def normalize_slot(slot):
    """
    Normalizes a raw slot value from the "body" schedule into the internal
    [name, teacher] pair used throughout this script. Handles:
      - missing/empty ([] or None) -> None (blank cell)
      - single-item lists like ["แนะแนว"] -> ["แนะแนว", ""]
      - normal two-item lists like ["ฟิสิกส์", "ครูธนวัฒน์"] -> unchanged
    """
    if not slot:
        return None
    name = slot[0] if len(slot) > 0 else ""
    teacher = slot[1] if len(slot) > 1 else ""
    if not name and not teacher:
        return None
    return [name, teacher]


def normalize_schedule(body: dict) -> dict:
    """Converts the {"body": {day: {period: [name, teacher?]}}} shape into
    the internal schedule dict keyed the same way, but with every slot
    normalized to a 2-item [name, teacher] list (or omitted if blank)."""
    schedule = {}
    for day_num, periods in body.items():
        day_out = {}
        for period_num, slot in (periods or {}).items():
            norm = normalize_slot(slot)
            if norm is not None:
                day_out[str(period_num)] = norm
        schedule[str(day_num)] = day_out
    return schedule


def generate_html_for_file(json_path: str) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    room_id = os.path.splitext(os.path.basename(json_path))[0]
    colors = {**DEFAULT_COLORS, **data.get("colors", {})}

    if "body" in data:
        # New format: {"meta": {"branch", "teacher", "room"}, "body": {...}}
        meta = data.get("meta", {})
        schedule = normalize_schedule(data.get("body", {}))
        room = meta.get("room", room_id)
        branch = meta.get("branch", "")
        teachers = meta.get("teacher", [])
        term = data.get("term", "1/2569")
    else:
        # Legacy format: {"term", "room", "branch", "teachers", "schedule"}
        schedule = data.get("schedule", {})
        room = data.get("room", room_id)
        branch = data.get("branch", "")
        teachers = data.get("teachers", [])
        term = data.get("term", "1/2569")

    ctx = {
        "title": "ตารางเรียน",
        "subtitle": f"ภาคเรียนที่ {term}",
        "room": room,
        "branch": branch,
        "teachers": teachers,
        "color": {
            "bg": colors["bg"],
            "t1": colors["t1"],
            "t2": colors["t2"],
            "logo": colors["t1"] if colors["bg"] != "#FFF6D6" else "#FFFFFF",
        },
        "days": build_days_html_ctx(schedule, colors),
        "periods_html": build_periods_html(schedule, colors),
    }
    return render_html(ctx), room_id


def screenshot_html(page, html_str: str, output_path: str, width=2388, height=1768):
    # file:// so the @font-face relative "fonts/..." URLs resolve from disk.
    tmp_html_path = os.path.join(SCRIPT_DIR, "_render_tmp.html")
    with open(tmp_html_path, "w", encoding="utf-8") as f:
        f.write(html_str)

    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"file://{tmp_html_path}", wait_until="networkidle")
    page.screenshot(path=output_path, type="png", omit_background=True)
    os.remove(tmp_html_path)


def main():
    input_dir = sys.argv[1] if len(sys.argv) > 1 else INPUT_DIR
    output_dir = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_DIR

    if not os.path.isdir(input_dir):
        print(f"Error: input folder '{input_dir}' does not exist.")
        sys.exit(1)
    os.makedirs(output_dir, exist_ok=True)

    json_files = sorted(glob.glob(os.path.join(input_dir, "*.json")))
    if not json_files:
        print(f"No .json files found in '{input_dir}'.")
        sys.exit(0)

    print(f"Found {len(json_files)} JSON file(s). Rendering into '{output_dir}'...\n")

    success, failed = 0, 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        for json_path in json_files:
            try:
                html_str, room_id = generate_html_for_file(json_path)
                output_path = os.path.join(output_dir, f"{room_id}.png")
                screenshot_html(page, html_str, output_path)
                print(f"✅ Generated: {output_path}")
                success += 1
            except Exception as e:
                print(f"❌ Failed on {json_path}: {e}")
                failed += 1
        browser.close()

    print(f"\nDone. {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    main()
