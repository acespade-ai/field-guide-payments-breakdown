#!/usr/bin/env python3
"""Visual study guide: The Field Guide to Global Payments (Sophia Goldberg, Stripe Press 2022).
6-page A4 PDF. All facts sourced from the book's own framing + verified chapter summaries.
Built with reportlab (platypus + vector drawings)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether, Flowable)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.pdfbase import pdfmetrics

OUT = os.path.expanduser("~/workspace/taskmarket/field-guide-payments/field-guide-to-global-payments-visual-study-guide.pdf")

NAVY   = HexColor("#0F2A43")
NAVY2  = HexColor("#163A5C")
TEAL   = HexColor("#0E7C6B")
TEAL_L = HexColor("#DDF0EC")
AMBER  = HexColor("#E8A33D")
AMBER_L= HexColor("#FDF3DC")
GREY   = HexColor("#33475B")
GREY_L = HexColor("#F2F5F7")
GREY_M = HexColor("#D8E0E8")
RED    = HexColor("#B3402E")
RED_L  = HexColor("#FBE9E5")
BLUE_L = HexColor("#E3EEF7")
GREEN_L= HexColor("#E6F4EA")
PURPLE = HexColor("#5B4B8A")
PURPLE_L=HexColor("#ECE7F5")

W, H = A4

sTitle   = ParagraphStyle("Title",   fontName="Helvetica-Bold", fontSize=30, leading=33, textColor=NAVY, alignment=TA_LEFT)
sSub     = ParagraphStyle("Sub",     fontName="Helvetica", fontSize=12.5, leading=17, textColor=GREY)
sH1      = ParagraphStyle("H1",      fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY)
sH2      = ParagraphStyle("H2",      fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY2)
sBody    = ParagraphStyle("Body",    fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=GREY)
sBodySm  = ParagraphStyle("BodySm",  fontName="Helvetica", fontSize=8.5, leading=12, textColor=GREY)
sBullet  = ParagraphStyle("Bullet",  fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=GREY, leftIndent=12, bulletIndent=2)
sCell    = ParagraphStyle("Cell",    fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=GREY)
sCellH   = ParagraphStyle("CellH",   fontName="Helvetica-Bold", fontSize=8.5, leading=11.5, textColor=white)
sCellB   = ParagraphStyle("CellB",   fontName="Helvetica-Bold", fontSize=8.5, leading=11.5, textColor=NAVY2)
sCaption = ParagraphStyle("Caption", fontName="Helvetica-Oblique", fontSize=8, leading=10.5, textColor=HexColor("#6B7C8C"))
sKicker  = ParagraphStyle("Kicker",  fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=TEAL)
sFooter  = ParagraphStyle("Footer",  fontName="Helvetica", fontSize=7.5, leading=10, textColor=HexColor("#8A9BA8"))

def P(t, st=sBody): return Paragraph(t, st)
def bullet(t): return Paragraph(t, sBullet, bulletText="•")

def callout(title, body, bg=AMBER_L, bar=AMBER, tcolor=NAVY2):
    inner = [[Paragraph(f"<b>{title}</b>", ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=9.5, leading=12.5, textColor=tcolor)),
              Paragraph(body, ParagraphStyle("cb", fontName="Helvetica", fontSize=9, leading=12.5, textColor=GREY))]]
    t = Table(inner, colWidths=[92, W - 72 - 92 - 14])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBELOW", (0, 0), (-1, 0), 0, white),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.75, bar),
        ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
    ]))
    return t

def section_head(kicker, title, sub):
    return [P(kicker, sKicker), Spacer(1, 3), P(title, sH1), Spacer(1, 3), P(sub, sSub), Spacer(1, 10)]

def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(TEAL)
        canvas.drawString(36, H - 26, "THE FIELD GUIDE TO GLOBAL PAYMENTS  —  VISUAL STUDY GUIDE")
        canvas.setStrokeColor(GREY_M); canvas.setLineWidth(0.6)
        canvas.line(36, H - 31, W - 36, H - 31)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HexColor("#8A9BA8"))
    canvas.drawString(36, 26, "Source: Sophia Goldberg, The Field Guide to Global Payments (Stripe Press, 2022)  •  fieldguidetoglobalpayments.com")
    canvas.drawRightString(W - 36, 26, f"Page {doc.page} of 6")
    canvas.restoreState()

# ---------- diagram helpers ----------
def arrow(d, x1, y1, x2, y2, color=TEAL, width=1.6):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width))
    # simple arrowhead
    if x2 > x1:  # rightward
        d.add(Polygon([x2, y2, x2 - 7, y2 + 3.5, x2 - 7, y2 - 3.5], fillColor=color, strokeColor=color))
    elif y2 < y1:  # downward
        d.add(Polygon([x2, y2, x2 - 3.5, y2 + 7, x2 + 3.5, y2 + 7], fillColor=color, strokeColor=color))

def box(d, x, y, w, h, fill, label, sub="", tcol=white, fs=9.5, sub_fs=7.5):
    d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=fill, strokeWidth=0))
    d.add(String(x + w / 2, y + h / 2 + (6 if sub else 0), label, fontName="Helvetica-Bold",
                 fontSize=fs, fillColor=tcol, textAnchor="middle"))
    if sub:
        d.add(String(x + w / 2, y + h / 2 - 9, sub, fontName="Helvetica",
                     fontSize=sub_fs, fillColor=tcol, textAnchor="middle"))

story = []

# ================= PAGE 1 — COVER =================
story.append(Spacer(1, 26))
story.append(P("A VISUAL STUDY GUIDE", sKicker))
story.append(Spacer(1, 6))
story.append(P("The Field Guide<br/>to Global Payments", sTitle))
story.append(Spacer(1, 8))
story.append(P("How money actually moves — cards, bank rails, wallets, crypto, and the rules "
               "and business models built on top of them. The book's key points, in six pages, "
               "no cover-to-cover read required.", sSub))
story.append(Spacer(1, 6))
story.append(P("Sophia Goldberg  •  Stripe Press, 2022  •  4 sections, pp. 12–172",
               ParagraphStyle("auth", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=NAVY2)))
story.append(Spacer(1, 18))

# four-section map
sec_data = [
    [P("<b><font color=\"#FFFFFF\">1 · CARDS</font></b>", ParagraphStyle("s1", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=white)),
     P("The four-party model, the transaction lifecycle, fees, declines &amp; chargebacks.", ParagraphStyle("s1b", fontName="Helvetica", fontSize=9, leading=12.5, textColor=white)),
     P("pp. 12–72", ParagraphStyle("s1c", fontName="Helvetica", fontSize=8.5, leading=11, textColor=HexColor("#BFE3DB")))],
    [P("<b><font color=\"#FFFFFF\">2 · NON-CARD TAXONOMY</font></b>", ParagraphStyle("s2", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=white)),
     P("Bank, delayed, wallets, cash/ATM, crypto — what moves money when it's not a card.", ParagraphStyle("s2b", fontName="Helvetica", fontSize=9, leading=12.5, textColor=white)),
     P("pp. 73–122", ParagraphStyle("s2c", fontName="Helvetica", fontSize=8.5, leading=11, textColor=HexColor("#D9CFF0")))],
    [P("<b><font color=\"#FFFFFF\">3 · RULES &amp; RISK</font></b>", ParagraphStyle("s3", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=white)),
     P("Regulation, compliance &amp; fraud — the rulebook and the rule-breakers.", ParagraphStyle("s3b", fontName="Helvetica", fontSize=9, leading=12.5, textColor=white)),
     P("pp. 123–143", ParagraphStyle("s3c", fontName="Helvetica", fontSize=8.5, leading=11, textColor=HexColor("#F6D9A8")))],
    [P("<b><font color=\"#FFFFFF\">4 · BUSINESS MODELS</font></b>", ParagraphStyle("s4", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=white)),
     P("Subscriptions, marketplaces &amp; B2B — how funds flow changes the business.", ParagraphStyle("s4b", fontName="Helvetica", fontSize=9, leading=12.5, textColor=white)),
     P("pp. 144–172", ParagraphStyle("s4c", fontName="Helvetica", fontSize=8.5, leading=11, textColor=HexColor("#F2C4BC")))],
]
sec_colors = [TEAL, PURPLE, HexColor("#B07E1E"), RED]
sec_table = Table([[sec_data[0][0], sec_data[0][1], sec_data[0][2]],
                   [sec_data[1][0], sec_data[1][1], sec_data[1][2]],
                   [sec_data[2][0], sec_data[2][1], sec_data[2][2]],
                   [sec_data[3][0], sec_data[3][1], sec_data[3][2]]],
                  colWidths=[150, 268, 62])
sec_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), sec_colors[0]),
    ("BACKGROUND", (0, 1), (-1, 1), sec_colors[1]),
    ("BACKGROUND", (0, 2), (-1, 2), sec_colors[2]),
    ("BACKGROUND", (0, 3), (-1, 3), sec_colors[3]),
    ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LINEBELOW", (0, 0), (-1, 2), 4, white),
]))
story.append(sec_table)
story.append(Spacer(1, 16))
story.append(P("HOW TO USE THIS GUIDE", sH2))
story.append(Spacer(1, 4))
story.append(bullet("Page 2 maps one card transaction end-to-end — the single diagram worth memorizing."))
story.append(bullet("Pages 3–5 unpack the three other sections as tables and diagrams you can scan in a minute each."))
story.append(bullet("Page 6 compares the three business models side-by-side and ends with the ten takeaways that matter most."))
story.append(Spacer(1, 14))
story.append(callout("THE ONE-SENTENCE VERSION",
    "Every payment is the same question four ways: <b>who moves the money, who takes the risk, "
    "who sets the rules, and who gets paid for it.</b> Cards answer it one way; every other method answers it differently — "
    "and the business model decides which answer wins.",
    bg=TEAL_L, bar=TEAL))
story.append(Spacer(1, 16))
story.append(P("Prepared as a standalone visual study guide. All framing follows the book's four sections; "
               "figures (e.g. the ~85% authorization rate) are the book's own. Reference: "
               "fieldguidetoglobalpayments.com", sCaption))
story.append(PageBreak())

# ================= PAGE 2 — CARD MONEY MAP =================
story += section_head("SECTION 1 · CARDS  —  pp. 12–72",
    "One card transaction, mapped",
    "Four parties, one network in the middle, and two separate phases: authorization (a hold, in seconds) "
    "and clearing/settlement (the money, in days). Nothing is paid at the till — only promised.")

# flow diagram: Cardholder -> Merchant -> Acquirer -> Network -> Issuer
d = Drawing(523, 150)
bw, bh = 92, 46
ys = 88
labels = [("CARDHOLDER", "pays"), ("MERCHANT", "sells"), ("ACQUIRER", "merchant's bank"),
          ("NETWORK", "Visa / MC / Amex"), ("ISSUER", "cardholder's bank")]
fills = [NAVY, TEAL, NAVY2, PURPLE, RED]
for i, (lab, sub) in enumerate(labels):
    x = 6 + i * 103
    box(d, x, ys, bw, bh, fills[i], lab, sub, fs=9)
    if i < 4:
        arrow(d, x + bw + 2, ys + bh / 2, x + bw + 9, ys + bh / 2)
d.add(String(261, 138, "AUTHORIZATION REQUEST  →  (and the response comes back the same way)",
             fontName="Helvetica-Bold", fontSize=8.5, fillColor=NAVY2, textAnchor="middle"))
# settlement arrow underneath (right to left)
d.add(Line(30, 62, 498, 62, strokeColor=AMBER, strokeWidth=2))
d.add(Polygon([30, 62, 37, 58.5, 37, 65.5], fillColor=AMBER, strokeColor=AMBER))
d.add(String(261, 70, "SETTLEMENT — money flows back, issuer → network → acquirer → merchant (1–3 business days)",
             fontName="Helvetica-Bold", fontSize=8.5, fillColor=HexColor("#8A6A12"), textAnchor="middle"))
d.add(String(261, 40, "The network is the clearing house: it routes messages, sets the rules (ISO 8583), and nets out who owes whom.",
             fontName="Helvetica", fontSize=8.5, fillColor=GREY, textAnchor="middle"))
d.add(String(261, 26, "Gateways & processors sit between merchant and acquirer; ISOs and PayFacs sell merchants access to all of it.",
             fontName="Helvetica", fontSize=8.5, fillColor=GREY, textAnchor="middle"))
story.append(d)
story.append(Spacer(1, 6))

# four steps
steps = [
    [P("<b>1 · AUTHORIZATION REQUEST</b>", sCellB), P("Merchant asks the issuer, via acquirer + network, to <b>hold</b> the funds. No money moves.", sCell)],
    [P("<b>2 · AUTHORIZATION RESPONSE</b>", sCellB), P("Issuer approves or declines in 1–2 seconds. Approval = a hold on the cardholder's limit, not a payment.", sCell)],
    [P("<b>3 · CAPTURE / CLEARING</b>", sCellB), P("Merchant batches approved sales at day's end; the network clears them — agreeing what each issuer owes.", sCell)],
    [P("<b>4 · SETTLEMENT</b>", sCellB), P("Issuers pay the network, the network pays acquirers, acquirers deposit to the merchant — minus fees.", sCell)],
]
t = Table(steps, colWidths=[150, 373])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), BLUE_L),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 10))

# fee stack + declines side by side
fee_rows = [
    [P("<b>WHERE A $100 SALE GOES</b>", ParagraphStyle("fh", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=white)), P("", sCell)],
    [P("Interchange → issuer", sCell), P("Largest slice. Set by the network; varies by card type &amp; region.", sCell)],
    [P("Scheme fee → network", sCell), P("The network's cut for routing, clearing &amp; rules.", sCell)],
    [P("Acquirer markup", sCell), P("The acquirer's margin for the merchant account &amp; risk.", sCell)],
    [P("<b>Merchant keeps</b>", sCellB), P("<b>≈ $97–98 of every $100</b> after fees — before chargebacks.", sCell)],
]
ft = Table(fee_rows, colWidths=[130, 128])
ft.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY2),
    ("SPAN", (0, 0), (-1, 0)),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GREY_L]),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
decline = [
    P("<b><font color=\"#B3402E\">DECLINES &amp; LIABILITY — THE CALLOUTS</font></b>",
      ParagraphStyle("dh", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED)),
    P("Only <b>~85% of authorizations succeed</b>. Top decline reasons: insufficient funds, expired card, "
      "fraud flags. Merchants that read decline codes and retry smartly recover real revenue.", sBodySm),
    P("<b>Card-present vs card-not-present:</b> in-store (chip/PIN) the issuer bears most fraud liability; "
      "online, without 3D Secure, the merchant usually eats it. 3D Secure shifts liability back — at the cost "
      "of checkout friction.", sBodySm),
    P("<b>Chargeback:</b> the cardholder disputes, the issuer claws the money back, and the merchant pays a fee "
      "on top — even when the dispute is friendly fraud or a service issue.", sBodySm),
]
dt = Table([[decline[0]], [decline[1]], [decline[2]], [decline[3]]], colWidths=[247])
dt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), RED_L),
    ("BOX", (0, 0), (-1, -1), 0.75, RED),
    ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
combo = Table([[ft, dt]], colWidths=[258, 265])
combo.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story.append(combo)
story.append(Spacer(1, 8))
story.append(P("History in one line: “credit card” first appears in 1887 · Charg-It, the first bank card, 1946 · "
               "Diners Club &amp; Amex, 1950s · BankAmericard launches the open loop in 1958 — and becomes Visa.",
               ParagraphStyle("hist", fontName="Helvetica-Oblique", fontSize=8.5, leading=12, textColor=GREY)))
story.append(PageBreak())

# ================= PAGE 3 — CARDS DEEP DIVE =================
story += section_head("SECTION 1 · CARDS  (continued)",
    "Cards, unpacked",
    "The four-party model is the grammar; everything else in the section is vocabulary — card types, loops, "
    "acceptance environments, and the intermediaries that sell access.")

# players table
players = [
    [P("<b>PLAYER</b>", sCellH), P("<b>DOES WHAT</b>", sCellH), P("<b>GETS PAID HOW</b>", sCellH)],
    [P("<b>Cardholder</b>", sCellB), P("Buys; repays the issuer (credit) or spends own balance (debit).", sCell), P("Pays interest &amp; fees (credit); nothing per-swipe (debit).", sCell)],
    [P("<b>Merchant</b>", sCellB), P("Sells goods/services; accepts cards via an acquirer.", sCell), P("Receives sale value minus interchange, scheme &amp; acquirer fees.", sCell)],
    [P("<b>Issuer</b>", sCellB), P("Issues the card; approves/declines; holds the cardholder relationship.", sCell), P("Interchange — the largest fee slice — plus interest.", sCell)],
    [P("<b>Acquirer</b>", sCellB), P("The merchant's bank; routes auth requests; settles funds to the merchant.", sCell), P("Acquirer markup on top of interchange + scheme fees.", sCell)],
    [P("<b>Network</b>", sCellB), P("Visa / Mastercard / Amex. Routes messages, clears, sets the rules.", sCell), P("Scheme fees; also sets interchange levels.", sCell)],
    [P("<b>Gateway / Processor</b>", sCellB), P("Tech layer: moves transaction data merchant ↔ acquirer.", sCell), P("Per-transaction or monthly tech fees.", sCell)],
    [P("<b>ISO / PayFac</b>", sCellB), P("Sell &amp; underwrite merchant accounts; PayFacs onboard sub-merchants fast.", sCell), P("Revenue share of processing; PayFacs take on compliance risk.", sCell)],
]
pt = Table(players, colWidths=[105, 245, 173])
pt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GREY_L]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(pt)
story.append(Spacer(1, 10))

# card types + loops + environments, 3 columns
col1 = [P("<b>THREE CARD TYPES</b>", ParagraphStyle("c1h", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=NAVY2)),
        P("<b>Debit</b> — pulls straight from checking; low fees, most common for everyday spend.", sBodySm),
        P("<b>Credit</b> — borrow up to a limit; issuer carries the credit risk (and earns interest).", sBodySm),
        P("<b>Prepaid</b> — pre-loaded funds; gifts, payroll, the unbanked.", sBodySm)]
col2 = [P("<b>OPEN VS CLOSED LOOP</b>", ParagraphStyle("c2h", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=NAVY2)),
        P("<b>Open loop</b> (Visa, Mastercard): any merchant that accepts the network. Four parties.", sBodySm),
        P("<b>Closed loop</b> (Amex-issued, store cards): one issuer = the network. Fewer parties, tighter control.", sBodySm),
        P("Co-branded &amp; dual-branded cards mix the two for rewards and reach.", sBodySm)]
col3 = [P("<b>WHERE YOU PAY MATTERS</b>", ParagraphStyle("c3h", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=NAVY2)),
        P("<b>Card-present</b> (chip/PIN/tap): lower fraud, issuer bears most liability.", sBodySm),
        P("<b>Card-not-present</b> (online): higher fraud; liability usually sits with the merchant.", sBodySm),
        P("Customer-initiated vs merchant-initiated (recurring) changes who can retry — and who is liable.", sBodySm)]
def colbox(items, bg):
    t = Table([[x] for x in items], colWidths=[161])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.75, GREY_M),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t
trio = Table([[colbox(col1, BLUE_L), colbox(col2, GREEN_L), colbox(col3, AMBER_L)]], colWidths=[171, 171, 171])
trio.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story.append(trio)
story.append(Spacer(1, 10))
story.append(callout("ORCHESTRATION — THE QUIET UPGRADE",
    "Modern gateways don't just pass messages: orchestration platforms <b>route each transaction across processors, "
    "retry declines intelligently, and give merchants one view of every rail.</b> Same four-party model underneath — "
    "smarter traffic control on top.",
    bg=TEAL_L, bar=TEAL))
story.append(Spacer(1, 8))
story.append(P("Cross-border is where cards get expensive: currency conversion, local regulation and correspondent "
               "banking (SWIFT) stack fees and delay on top of the normal flow — one reason non-card rails exist at all.",
               sBodySm))
story.append(PageBreak())

# ================= PAGE 4 — NON-CARD TAXONOMY =================
story += section_head("SECTION 2 · NON-CARD TAXONOMY  —  pp. 73–122",
    "Everything that isn't a card",
    "Cards dominate the US. Almost everywhere else, the default is something else — and each alternative has its own "
    "flow, its own refund rules, and its own failure modes. The book's point: there is no universal rail.")

tax = [
    [P("<b><font color=\"#FFFFFF\">BANK</font></b>", ParagraphStyle("txh", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=white)),
     P("<b>ACH, wires, SEPA, instant schemes</b> (Pix, UPI, Faster Payments). Money moves account-to-account — no card network, no interchange.", sCell),
     P("Cheap per-transaction; slow (ACH) or fast (instant rails). <b>Watch-out:</b> settlement delays strain cash flow; refunds are clunky.", sCell)],
    [P("<b><font color=\"#FFFFFF\">DELAYED</font></b>", ParagraphStyle("txh2", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=white)),
     P("<b>Direct debit &amp; BNPL.</b> Direct debit: payer authorizes the payee to pull funds on a schedule. BNPL: consumer pays over time, merchant is paid up front.", sCell),
     P("Predictable revenue, lower cost than cards. Guaranteed ACH cuts NSF risk. <b>Watch-out:</b> mandates, failed pulls, BNPL credit risk sits with the lender.", sCell)],
    [P("<b><font color=\"#FFFFFF\">WALLETS</font></b>", ParagraphStyle("txh3", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=white)),
     P("<b>Apple Pay, Google Pay, PayPal, Alipay, M-Pesa.</b> Stored funds or tokenized credentials; one tap, no card details shared with the merchant.", sCell),
     P("Cuts checkout friction and lifts conversion; tokens survive card reissue. <b>Watch-out:</b> wallet = a new gatekeeper in the flow.", sCell)],
    [P("<b><font color=\"#FFFFFF\">CASH / ATM</font></b>", ParagraphStyle("txh4", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=white)),
     P("<b>Cash, cash-on-delivery, ATM networks.</b> Still the norm in much of the world — Brazil treats cash installments as standard.", sCell),
     P("Zero chargebacks, universal acceptance. <b>Watch-out:</b> no digital trail, theft &amp; handling cost, no refunds path.", sCell)],
    [P("<b><font color=\"#FFFFFF\">CRYPTO / DeFi</font></b>", ParagraphStyle("txh5", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=white)),
     P("<b>Stablecoins, on-chain settlement, DeFi rails.</b> Settlement without banks or card networks; programmable money.", sCell),
     P("Borderless and fast where rails are thin. <b>Watch-out:</b> volatility, regulation, and no chargeback mechanism at all.", sCell)],
]
tax_colors = [NAVY2, TEAL, PURPLE, HexColor("#B07E1E"), RED]
tx_rows = []
for i, row in enumerate(tax):
    tx_rows.append(row)
tt = Table(tx_rows, colWidths=[92, 235, 196])
tt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, 0), tax_colors[0]),
    ("BACKGROUND", (0, 1), (0, 1), tax_colors[1]),
    ("BACKGROUND", (0, 2), (0, 2), tax_colors[2]),
    ("BACKGROUND", (0, 3), (0, 3), tax_colors[3]),
    ("BACKGROUND", (0, 4), (0, 4), tax_colors[4]),
    ("ROWBACKGROUNDS", (1, 0), (-1, -1), [white, GREY_L]),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(tt)
story.append(Spacer(1, 10))
story.append(P("THE REGIONAL MAP — SAME PURCHASE, DIFFERENT DEFAULT", sH2))
story.append(Spacer(1, 4))
reg = [
    [P("<b>United States</b>", sCellB), P("Cards dominate; wallets rising fast.", sCell)],
    [P("<b>Germany</b>", sCellB), P("Debit &amp; online bank transfer beat credit cards.", sCell)],
    [P("<b>Japan</b>", sCellB), P("~65% of online transactions run through mobile wallets.", sCell)],
    [P("<b>Brazil</b>", sCellB), P("Cash installments are normal; BNPL is booming.", sCell)],
    [P("<b>China / India</b>", sCellB), P("Wallets &amp; QR (Alipay, Paytm, UPI) are the default rails.", sCell)],
    [P("<b>East Africa</b>", sCellB), P("Mobile money (M-Pesa) leapfrogged cards entirely.", sCell)],
]
rt = Table(reg, colWidths=[110, 413])
rt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), BLUE_L),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(rt)
story.append(Spacer(1, 8))
story.append(P("Merchant's headache, per the book: every non-card method has <b>different refund and chargeback rules</b> — "
               "or none at all — so accounts receivable gets complicated the moment you accept more than one rail.",
               sBodySm))
story.append(PageBreak())

# ================= PAGE 5 — RULES & RISK =================
story += section_head("SECTION 3 · THE RULES AND THE RULE BREAKERS  —  pp. 123–143",
    "Rules & risk cheat sheet",
    "Payments run on rules written by networks, regulators and governments — and the fraud economy exists to find "
    "the gaps between them. Know the rule, know who it protects, know what breaks when it's ignored.")

rules = [
    [P("<b>RULE / STANDARD</b>", sCellH), P("<b>WHAT IT DOES</b>", sCellH), P("<b>WHO IT HITS</b>", sCellH)],
    [P("<b>PCI DSS</b>", sCellB), P("Security standard for handling card data: encryption, access control, audits. Non-compliance = fines &amp; losing card acceptance.", sCell), P("Every merchant &amp; processor touching card data.", sCell)],
    [P("<b>Tokenization</b>", sCellB), P("Replaces real card numbers with tokens, so a breach yields useless data. Wallets run on it.", sCell), P("Merchants, gateways, wallets.", sCell)],
    [P("<b>3D Secure (3DS)</b>", sCellB), P("Extra authentication step for online payments (SCA under PSD2). Shifts fraud liability to the issuer.", sCell), P("E-commerce merchants; adds checkout friction.", sCell)],
    [P("<b>PSD2 / SCA</b>", sCellB), P("EU rule: strong customer authentication + open banking access for third parties.", sCell), P("EU merchants, banks, fintechs.", sCell)],
    [P("<b>AML / KYC</b>", sCellB), P("Anti-money-laundering + know-your-customer checks on who moves money and why.", sCell), P("Banks, PayFacs, marketplaces, crypto on-ramps.", sCell)],
    [P("<b>Network rules</b>", sCellB), P("Visa/Mastercard operating rules: chargeback windows, dispute categories, fine schedules.", sCell), P("Issuers, acquirers — and merchants, via their acquirer.", sCell)],
    [P("<b>Cross-border rules</b>", sCellB), P("Local licensing, data residency, FX controls; SWIFT + correspondent banks enforce them.", sCell), P("Anyone selling across borders.", sCell)],
]
rut = Table(rules, colWidths=[105, 283, 135])
rut.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GREY_L]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(rut)
story.append(Spacer(1, 10))
story.append(P("THE RULE-BREAKERS — FRAUD, BY TYPE", sH2))
story.append(Spacer(1, 4))
fraud = [
    [P("<b><font color=\"#FFFFFF\">CARD-NOT-PRESENT FRAUD</font></b>", ParagraphStyle("fr", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=white)),
     P("Stolen card details used online, where there's no chip or PIN to check. The merchant usually bears the loss.", sCell)],
    [P("<b><font color=\"#FFFFFF\">FRIENDLY FRAUD</font></b>", ParagraphStyle("fr2", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=white)),
     P("A real cardholder disputes a real purchase — buyer's remorse, forgotten subscriptions, family spending. Merchant pays the chargeback + fee.", sCell)],
    [P("<b><font color=\"#FFFFFF\">ACCOUNT TAKEOVER</font></b>", ParagraphStyle("fr3", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=white)),
     P("Attacker logs in as the customer (credential stuffing, phishing) and spends stored payment methods. Wallets &amp; tokens raise the bar.", sCell)],
    [P("<b><font color=\"#FFFFFF\">FIRST-PARTY / SYNTHETIC</font></b>", ParagraphStyle("fr4", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=white)),
     P("Fake identities built from real + invented data to open accounts and bust out. KYC and device signals are the defense.", sCell)],
]
frt = Table(fraud, colWidths=[150, 373])
frt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), RED),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("ROWBACKGROUNDS", (1, 0), (1, -1), [white, HexColor("#FDF0EE")]),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(frt)
story.append(Spacer(1, 10))
story.append(callout("THE TRADE-OFF THAT RUNS THE WHOLE SECTION",
    "Every security control is a tax on conversion: <b>3DS cuts fraud and adds friction; tokenization costs "
    "integration effort and kills breach risk; strict KYC slows onboarding and stops bust-outs.</b> The book's lesson "
    "isn't “more rules” — it's knowing which trade you're making, and who pays for it.",
    bg=AMBER_L, bar=AMBER))
story.append(PageBreak())

# ================= PAGE 6 — BUSINESS MODELS + TAKEAWAYS =================
story += section_head("SECTION 4 · BUSINESS MODELS  —  pp. 144–172",
    "Subscriptions vs marketplaces vs B2B",
    "Same rails, different money flow. The business model decides who holds funds, who bears the risk, and which "
    "payment features actually matter.")

bm = [
    [P("<b></b>", sCellH), P("<b>SUBSCRIPTIONS</b>", sCellH), P("<b>MARKETPLACES</b>", sCellH), P("<b>B2B</b>", sCellH)],
    [P("<b>Money flow</b>", sCellB), P("Recurring pulls from a stored credential — card-on-file, wallet token, or direct-debit mandate.", sCell), P("Buyer pays the platform; the platform splits &amp; pays out many sellers (escrow in between).", sCell), P("Invoices paid by wire / ACH; large, lumpy, scheduled — not per-click.", sCell)],
    [P("<b>What breaks</b>", sCellB), P("Involuntary churn: expired cards, failed pulls, dunning. Wallet tokens survive reissue; cards don't.", sCell), P("Splitting complexity, payout timing, seller fraud, and who holds funds (licensing!).", sCell), P("Slow settlement, FX on cross-border invoices, reconciliation across systems.", sCell)],
    [P("<b>Key payments feature</b>", sCellB), P("Stored credentials, smart retries, dunning flows, direct-debit mandates for fixed amounts.", sCell), P("Split payouts, escrow, seller onboarding + KYC, instant vs batched payouts.", sCell), P("ACH/wire rails, virtual cards for AP, net terms, FX handling.", sCell)],
    [P("<b>Who bears the risk</b>", sCellB), P("Merchant: churn + chargebacks on recurring billing.", sCell), P("Platform: it sits between buyer and seller money — and regulators notice.", sCell), P("Both sides: large tickets mean one failed payment is a real event.", sCell)],
    [P("<b>Scale signal</b>", sCellB), P("Predictable revenue; retention is the metric.", sCell), P("Take rate × GMV; payout speed is the moat.", sCell), P("Larger transaction sizes than consumer payments, by an order of magnitude.", sCell)],
]
bmt = Table(bm, colWidths=[92, 143, 144, 144])
bmt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("BACKGROUND", (0, 0), (0, -1), BLUE_L),
    ("GRID", (0, 0), (-1, -1), 0.5, GREY_M),
    ("ROWBACKGROUNDS", (1, 1), (-1, -1), [white, GREY_L]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(bmt)
story.append(Spacer(1, 12))

# key takeaways strip
story.append(P("KEY TAKEAWAYS — THE TEN THAT MATTER", sH2))
story.append(Spacer(1, 4))
takes = [
    "1. A card payment is a <b>promise</b>, not a payment — authorization holds funds; settlement moves them days later.",
    "2. Four parties + one network: cardholder, merchant, issuer, acquirer — the network routes, clears and sets the rules.",
    "3. Only <b>~85% of authorizations succeed</b>; declines are a revenue problem, not just a fraud problem.",
    "4. Fees stack: interchange (issuer) + scheme (network) + acquirer markup — the merchant keeps ~$97–98 of $100.",
    "5. Card-present vs card-not-present decides <b>who eats fraud</b>; 3DS shifts liability back to the issuer.",
    "6. Outside the US, cards are the exception: wallets, bank rails and cash are the defaults — region picks the rail.",
    "7. Every non-card method has different refund/chargeback rules — or none — which complicates accounts receivable.",
    "8. Security is a trade: 3DS, tokenization and KYC each cut fraud and cost conversion. Know which trade you're making.",
    "9. Subscriptions live or die on stored credentials; marketplaces on split payouts; B2B on large, slow, invoice rails.",
    "10. Payments aren't a back office — they're where a business's revenue <b>literally comes from</b>.",
]
tk = Table([[P(t, ParagraphStyle("tk", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=GREY))] for t in takes],
           colWidths=[523])
tk.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), TEAL_L),
    ("BOX", (0, 0), (-1, -1), 1, TEAL),
    ("LINEBELOW", (0, 0), (-1, -2), 0.5, HexColor("#BFE3DB")),
    ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(tk)
story.append(Spacer(1, 12))
story.append(P("Source: Sophia Goldberg, <i>The Field Guide to Global Payments</i> (Stripe Press, 2022) — "
               "fieldguidetoglobalpayments.com. Section page ranges per the book. Figures (e.g. ~85% authorization "
               "rate, ~65% wallet share in Japan) are the book's own. This guide is a study summary, not a substitute "
               "for the book.", sCaption))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=44, bottomMargin=36,
                        title="The Field Guide to Global Payments — Visual Study Guide",
                        author="Ace (after Sophia Goldberg)")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print("WROTE", OUT)
