import csv
import os
from flask import Flask, request, redirect, url_for

app      = Flask(__name__)
CSV_FILE = "purrserecord.csv"


class InfoInput:                                                
    def __init__(self, description, mood, cost, category):      
        self.description = description                          
        self.mood        = mood                                 
        self.cost        = cost                                 
        self.category    = category                             


class InputValidator:
    CHECK_INPUT = str.isdigit

    def __init__(self):
        self.description_value = None
        self.mood_value        = None
        self.cost_value        = None
        self.error_message     = ""

    def has_numbers(self, value):
        return any(char.isdigit() for char in value)

    def validate_description(self, value):
        if not value:
            return None, "INVALID INPUT"
        if self.has_numbers(value):
            return None, "INVALID INPUT"
        return value, None

    def validate_mood(self, value):
        if not value:
            return None, "INVALID INPUT"
        if self.has_numbers(value):
            return None, "INVALID INPUT"
        return value, None

    def validate_cost(self, cost_str):
        try:
            cost = float(cost_str)
            if cost < 0:
                raise ValueError
            return cost, None
        except ValueError:
            return None, "INVALID INPUT"


class CostCalculator:
    def __init__(self, expense_list):
        self._expense_list = expense_list

    def _category_totals(self):
        totals = {}
        for expense in self._expense_list:
            cat = expense.category
            if cat not in totals:
                totals[cat] = 0.0
            totals[cat] = totals[cat] + expense.cost
        return totals

    def _grand_total(self):
        total = 0.0
        for expense in self._expense_list:
            total = total + expense.cost
        return total

    def _top_category(self):
        totals     = self._category_totals()
        top_cat    = None
        top_amount = 0.0
        for cat in totals:
            if totals[cat] > top_amount:
                top_cat    = cat
                top_amount = totals[cat]
        return top_cat, top_amount

    def get_category_totals(self):
        return self._category_totals()

    def get_grand_total(self):
        return self._grand_total()

    def get_top_category(self):
        return self._top_category()


class MoodAnalyzer:
    def __init__(self, expense_list):
        self._expense_list = expense_list
        self._mood_totals  = {}

    def analyze(self):
        self._mood_totals = {}
        for expense in self._expense_list:
            mood = expense.mood
            if mood not in self._mood_totals:
                self._mood_totals[mood] = 0.0
            self._mood_totals[mood] = self._mood_totals[mood] + expense.cost

    def get_top_mood(self):
        if not self._mood_totals:
            self.analyze()
        top_mood   = None
        top_amount = 0.0
        for mood in self._mood_totals:
            if self._mood_totals[mood] > top_amount:
                top_mood   = mood
                top_amount = self._mood_totals[mood]
        return top_mood


class Manage_Expense:
    def __init__(self, expense_list, csv_data):
        self._expense_list  = expense_list
        self._csv           = csv_data
        self._validator     = InputValidator()
        self.cost_error     = False
        self.desc_error     = False
        self.mood_error     = False
        self.cost_error_msg = ""
        self.desc_error_msg = ""
        self.mood_error_msg = ""

    def _clear_errors(self):
        self.cost_error     = False
        self.desc_error     = False
        self.mood_error     = False
        self.cost_error_msg = ""
        self.desc_error_msg = ""
        self.mood_error_msg = ""

    def add_expense(self, category, description, mood, cost_str):
        self._clear_errors()

        desc,     desc_err = self._validator.validate_description(description)
        mood_val, mood_err = self._validator.validate_mood(mood)
        cost,     cost_err = self._validator.validate_cost(cost_str)

        if desc_err:
            self.desc_error     = True
            self.desc_error_msg = desc_err
        if mood_err:
            self.mood_error     = True
            self.mood_error_msg = mood_err
        if cost_err:
            self.cost_error     = True
            self.cost_error_msg = cost_err

        if self.desc_error or self.mood_error or self.cost_error:
            return

        self._expense_list.append(InfoInput(desc, mood_val, cost, category))
        self._csv.save(self._expense_list)

    def delete_expense(self, index):
        if 0 <= index < len(self._expense_list):
            self._expense_list.pop(index)
            self._csv.save(self._expense_list)


class CSV_Data:
    def __init__(self, filepath=CSV_FILE):
        self._filepath = filepath

    def load(self):
        if not os.path.exists(self._filepath):
            return []

        loaded = []
        with open(self._filepath, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                raw  = row["cost"]
                cost = float(raw) if raw.replace(".", "", 1).isdigit() else 0.0
                loaded.append(InfoInput(row["description"], row["mood"], cost, row["category"]))
        return loaded

    def save(self, expense_list):
        with open(self._filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["category", "description", "mood", "cost"])
            writer.writeheader()
            for expense in expense_list:
                writer.writerow({
                    "category":    expense.category,
                    "description": expense.description,
                    "mood":        expense.mood,
                    "cost":        expense.cost,
                })


class MoodExpenseManager:
    
    def __init__(self, csv_data=None):
        self._csv_data     = csv_data if csv_data is not None else CSV_Data()
        self._expense_list = self._csv_data.load()
        self._calculator   = CostCalculator(self._expense_list)
        self._analyzer     = MoodAnalyzer(self._expense_list)
        self._manager      = Manage_Expense(self._expense_list, self._csv_data)

    def add_expense(self, category, description, mood, cost_str):
        self._manager.add_expense(category, description, mood, cost_str)
        self._analyzer.analyze()

    def delete_expense(self, index):
        self._manager.delete_expense(index)
        self._analyzer.analyze()

    @property
    def expense_list(self):
        return self._expense_list

    @property
    def manager(self):
        return self._manager

    @property
    def cost_calculator(self):
        return self._calculator

    @property
    def mood_analyzer(self):
        return self._analyzer


CATEGORIES = [
    ("😸🍜", "food"),
    ("😸💊", "medical"),
    ("😸🚐", "transpo"),
    ("😸🏠", "utilities"),
]


class PageBuilder:

    def build_page_start(self):
        body_style = (
            "font-family:'Comic Sans MS',cursive;"
            "min-height:100vh;"
            "background:#FDFBD4;"
            "box-sizing:border-box;"
            "margin:0;"
            "padding:0;"
        )
        wrapper_style = (
            "display:flex;"
            "flex-direction:column;"
        )
        html  = '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        html += '  <meta charset="UTF-8">\n'
        html += '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        html += '  <title>PURR$E</title>\n'
        html += '</head>\n'
        html += f'<body style="{body_style}">\n'
        html += f'  <div style="{wrapper_style}">\n'
        return html

    def build_page_end(self):
        footer_style = (
            "text-align:center;"
            "padding:18px;"
            "color:#888;"
            "font-size:11px;"
            "letter-spacing:2px;"
            "text-transform:uppercase;"
            "border-top:2px solid #ddd;"
            "background:#ffffff;"
        )
        html  = f'    <div style="{footer_style}">Spend with purrpose, spend with purrse</div>\n'
        html +=  '  </div>\n</body>\n</html>'
        return html

    def build_site_header(self):
        header_style = (
            "background:#2b2b2b;"
            "padding:18px 28px 14px;"
            "border-bottom:3px solid #111;"
        )
        title_style = (
            "color:#f5d800;"
            "font-size:28px;"
            "font-weight:bold;"
            "letter-spacing:4px;"
            "margin:0 0 2px 0;"
            "text-transform:uppercase;"
        )
        subtitle_style = (
            "color:#aaaaaa;"
            "font-size:10px;"
            "letter-spacing:3px;"
            "text-transform:uppercase;"
            "margin:0;"
        )
        html  = f'    <div style="{header_style}">\n'
        html += f'      <div style="{title_style}">PURR$E</div>\n'
        html += f'      <div style="{subtitle_style}">Expense tracker based on your mood</div>\n'
        html +=  '    </div>\n'
        return html

    def build_stats_bar(self, grand_total, top_cat, top_mood):
        top_cat_label  = top_cat.upper()  if top_cat  else "NONE"
        top_mood_label = top_mood.upper() if top_mood else "NONE"

        bar_style = (
            "display:flex;"
            "flex-direction:row;"
            "background:#1a1a1a;"
            "padding:16px 28px;"
            "gap:2px;"
            "border-bottom:3px solid #111;"
        )
        box_style = (
            "flex:1;"
            "padding:12px 16px;"
            "text-align:center;"
            "background:#1a1a1a;"
            "border:1.5px solid #333;"
        )
        label_style = (
            "display:block;"
            "color:#888;"
            "font-size:10px;"
            "letter-spacing:2px;"
            "text-transform:uppercase;"
            "margin-bottom:4px;"
        )
        value_style = (
            "display:block;"
            "color:#f5d800;"
            "font-size:20px;"
            "font-weight:bold;"
            "letter-spacing:1px;"
        )

        html = f'    <div style="{bar_style}">\n'
        for label, value in [
            ("Grand Total",         f"&#8369;{grand_total:.2f}"),
            ("Top Cat-egory",       top_cat_label),
            ("Top Mood Purr-chase", top_mood_label),
        ]:
            html += f'      <div style="{box_style}">\n'
            html += f'        <span style="{label_style}">{label}</span>\n'
            html += f'        <span style="{value_style}">{value}</span>\n'
            html +=  '      </div>\n'
        html += '    </div>\n'
        return html

    def build_input_form(self, cat_key, mgr):
        form_style = (
            "display:flex;"
            "flex-direction:column;"
            "gap:10px;"
            "margin-bottom:12px;"
        )
        label_style = (
            "color:#333;"
            "font-size:10px;"
            "font-weight:bold;"
            "letter-spacing:2px;"
            "text-transform:uppercase;"
        )
        error_style = (
            "font-size:10px;"
            "color:#cc2200;"
            "font-weight:bold;"
            "margin-top:2px;"
            "letter-spacing:0.5px;"
        )
        btn_style = (
            "background:#1a1a1a;"
            "color:#f5d800;"
            "border:none;"
            "padding:9px 10px;"
            "border-radius:0;"
            "cursor:pointer;"
            "font-family:'Comic Sans MS',cursive;"
            "font-size:12px;"
            "font-weight:bold;"
            "letter-spacing:2px;"
            "text-transform:uppercase;"
            "width:100%;"
            "margin-top:4px;"
        )

        def field(label_text, input_name, has_error, error_msg=""):
            border = "2px solid #cc2200" if has_error else "1px solid #a07800"
            bg     = "#fff0f0"           if has_error else "#fffde8"

            input_style = (
                f"padding:7px 10px;"
                f"border-radius:0;"
                f"border:{border};"
                f"width:100%;"
                f"font-family:'Comic Sans MS',cursive;"
                f"font-size:12px;"
                f"background:{bg};"
                f"box-sizing:border-box;"
                f"color:#1a1a1a;"
                f"outline:none;"
            )
            wrapper_style = (
                "display:flex;"
                "flex-direction:column;"
                "gap:3px;"
            )
            f  = f'            <div style="{wrapper_style}">\n'
            f += f'              <label style="{label_style}">{label_text}</label>\n'
            f += f'              <input type="text" name="{input_name}" style="{input_style}">\n'
            if error_msg:
                f += f'              <span style="{error_style}">{error_msg}</span>\n'
            f +=  '            </div>\n'
            return f

        html  = f'          <form style="{form_style}" action="/add" method="POST">\n'
        html += f'            <input type="hidden" name="category" value="{cat_key}">\n'
        html += field("Description", "description", mgr.desc_error, mgr.desc_error_msg if mgr.desc_error else "")
        html += field("Mood",        "mood",        mgr.mood_error, mgr.mood_error_msg if mgr.mood_error else "")
        html += field("Cost",        "cost",        mgr.cost_error, mgr.cost_error_msg if mgr.cost_error else "")
        html += f'            <button type="submit" style="{btn_style}">+ Add Expense</button>\n'
        html +=  '          </form>\n'
        return html

    def build_expense_rows(self, expense_list, cat_key):
        row_style = (
            "color:#1a1a1a;"
            "font-size:11px;"
            "padding:6px 0;"
            "border-bottom:1px solid #a07800;"
            "display:flex;"
            "align-items:center;"
            "gap:8px;"
        )
        text_style = (
            "flex:1;"
            "word-break:break-word;"
            "line-height:1.5;"
            "font-weight:bold;"
        )
        delete_style = (
            "display:inline-flex;"
            "align-items:center;"
            "justify-content:center;"
            "color:#000000;"
            "text-decoration:none;"
            "font-size:15px;"
            "flex-shrink:0;"
            "width:22px;"
            "height:22px;"
            "background:rgba(200,0,0,0.08);"
            "border:3px solid rgba(200,0,0,0.3);"
            "cursor:pointer;"
        )
        html = ""
        for index, expense in enumerate(expense_list):
            if expense.category != cat_key:
                continue
            html += f'          <div style="{row_style}">\n'
            html += f'            <span style="{text_style}">{expense.description} | {expense.mood} | &#8369;{expense.cost:.2f}</span>\n'
            html += f'            <a href="/delete/{index}" style="{delete_style}" title="Delete">&#128465;</a>\n'
            html +=  '          </div>\n'
        return html

    def build_category_card(self, emoji, name, expense_list, cat_totals, mgr):
        cat_total = cat_totals.get(name, 0.0)

        card_style = (
            "background:#f7f3d0;"
            "border-radius:0;"
            "border:2px solid #c8a800;"
            "overflow:hidden;"
        )
        card_header_style = (
            "background:#f7f3d0;"
            "padding:12px 16px 10px;"
            "display:flex;"
            "align-items:center;"
            "gap:10px;"
            "border-bottom:1.5px solid #c8a800;"
        )
        card_emoji_style = (
            "font-size:22px;"
            "line-height:1;"
        )
        card_title_style = (
            "color:#1a1a1a;"
            "font-size:15px;"
            "font-weight:bold;"
            "letter-spacing:2px;"
            "text-transform:uppercase;"
        )
        card_body_style = (
            "background:#c8930a;"
            "padding:14px 16px;"
        )
        card_footer_style = (
            "color:#1a1a1a;"
            "font-weight:bold;"
            "font-size:12px;"
            "letter-spacing:1px;"
            "text-transform:uppercase;"
            "padding:10px 16px;"
            "background:#c8930a;"
            "border-top:2px solid #c8a800;"
        )

        html  = f'      <div style="{card_style}">\n'
        html += f'        <div style="{card_header_style}">\n'
        html += f'          <span style="{card_emoji_style}">{emoji}</span>\n'
        html += f'          <span style="{card_title_style}">{name.upper()}</span>\n'
        html +=  '        </div>\n'
        html += f'        <div style="{card_body_style}">\n'
        html += self.build_input_form(name, mgr)
        html += self.build_expense_rows(expense_list, name)
        html +=  '        </div>\n'
        html += f'        <div style="{card_footer_style}">Total: &#8369;{cat_total:.2f}</div>\n'
        html +=  '      </div>\n'
        return html


class OutputRenderer:
    def __init__(self):
        self._builder = PageBuilder()

    def render(self, expense_list, cat_totals, grand_total, top_mood, top_cat, mgr):
        b        = self._builder
        sections = []

        sections.append(b.build_page_start())
        sections.append(b.build_site_header())
        sections.append(b.build_stats_bar(grand_total, top_cat, top_mood))

        grid_wrapper_style = (
            "padding:24px 28px;"
            "background:#ffffff;"
        )
        grid_style = (
            "display:grid;"
            "grid-template-columns:repeat(2,1fr);"
            "gap:20px;"
            "align-items:start;"
        )

        sections.append(f'    <div style="{grid_wrapper_style}">\n')
        sections.append(f'      <div style="{grid_style}">\n')
        for emoji, name in CATEGORIES:
            sections.append(b.build_category_card(emoji, name, expense_list, cat_totals, mgr))
        sections.append('      </div>\n    </div>\n')

        sections.append(b.build_page_end())

        return "".join(sections)


manager  = MoodExpenseManager()
renderer = OutputRenderer()


@app.route("/")
def index():
    totals      = manager.cost_calculator.get_category_totals()
    grand_total = manager.cost_calculator.get_grand_total()
    top_cat, _  = manager.cost_calculator.get_top_category()
    top_mood    = manager.mood_analyzer.get_top_mood()

    return renderer.render(
        manager.expense_list,
        totals,
        grand_total,
        top_mood,
        top_cat,
        manager.manager,
    )


@app.route("/add", methods=["POST"])
def add():
    manager.add_expense(
        request.form.get("category",    "food"),
        request.form.get("description", "").strip(),
        request.form.get("mood",        "").strip(),
        request.form.get("cost",        "").strip(),
    )
    return redirect(url_for("index"))


@app.route("/delete/<int:item_index>")
def delete(item_index):
    manager.delete_expense(item_index)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)