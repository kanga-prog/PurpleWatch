from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer, Table, TableStyle

OUT = "docs/portfolio/PurpleWatch_Rapport_Final.pdf"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#6D28D9"))
    canvas.line(2 * cm, 1.55 * cm, A4[0] - 2 * cm, 1.55 * cm)
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.drawString(2 * cm, 1.05 * cm, "PurpleWatch - Rapport final")
    canvas.drawRightString(A4[0] - 2 * cm, 1.05 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
    base = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=base["Title"], fontName="DejaVu-Bold", fontSize=25, leading=30, textColor=colors.HexColor("#4C1D95"), alignment=TA_CENTER, spaceAfter=15)
    sub = ParagraphStyle("Sub", parent=base["Normal"], fontName="DejaVu", fontSize=12, leading=17, textColor=colors.HexColor("#475569"), alignment=TA_CENTER, spaceAfter=16)
    h1 = ParagraphStyle("H1", parent=base["Heading1"], fontName="DejaVu-Bold", fontSize=16, leading=21, textColor=colors.HexColor("#4C1D95"), spaceBefore=7, spaceAfter=9)
    h2 = ParagraphStyle("H2", parent=base["Heading2"], fontName="DejaVu-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#312E81"), spaceBefore=7, spaceAfter=5)
    body = ParagraphStyle("Body", parent=base["BodyText"], fontName="DejaVu", fontSize=9.5, leading=14, spaceAfter=6)
    cell = ParagraphStyle("Cell", parent=base["BodyText"], fontName="DejaVu", fontSize=7.6, leading=10)
    boldcell = ParagraphStyle("BoldCell", parent=base["BodyText"], fontName="DejaVu-Bold", fontSize=7.6, leading=10)
    P = lambda text, style: Paragraph(text, style)
    B = lambda items: [P("• " + item, body) for item in items]

    def table(rows, widths):
        values = [[P(value, boldcell if rownum == 0 else cell) for value in row] for rownum, row in enumerate(rows)]
        result = Table(values, colWidths=widths)
        result.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4C1D95")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#F8FAFC")), ("GRID", (0,0), (-1,-1), .35, colors.HexColor("#CBD5E1")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
        return result

    story = [
        Spacer(1, 1.4*cm), P("PURPLEWATCH", title), P("Rapport final - Laboratoire Purple Team", sub), P("Simulation ATT&amp;CK, détection Wazuh et validation E2E", sub), Spacer(1, 1.2*cm),
        P("Résumé exécutif", h1),
        P("PurpleWatch est un laboratoire Purple Team isolé. Il permet de lancer des techniques MITRE ATT&amp;CK contrôlées avec Caldera, de produire une télémétrie endpoint avec Sysmon ou auditd, puis de la détecter et de l'explorer dans Wazuh.", body),
        P("Le résultat recherché n'est pas seulement l'exécution d'une commande : chaque scénario doit démontrer une chaîne de preuve complète, de l'émulation jusqu'à l'alerte enrichie de son identifiant ATT&amp;CK.", body),
        P("Périmètre validé", h2), *B(["Deux endpoints : PW-WIN11-01 et PW-LINUX-01.", "Orchestration Caldera et connectivité chiffrée Tailscale.", "Détection centralisée Wazuh avec règles PurpleWatch maintenues comme du code."]),
        PageBreak(), P("1. Architecture et déroulement E2E", h1),
        P("Caldera orchestre les abilities sur les agents Sandcat. Les exécutions génèrent des événements endpoint : Sysmon sous Windows et auditd sous Linux. Les agents Wazuh transmettent ensuite ces événements au manager Wazuh, qui applique les règles PurpleWatch avant l'indexation et la consultation dans Threat Hunting.", body),
        table([["Composant", "Rôle", "Canal principal"], ["PW-CALDERA-01", "Orchestration Caldera et C2", "HTTP 8888 via Tailscale"], ["PW-WIN11-01", "Sandcat, Sysmon, Wazuh Agent", "Wazuh 1514 vers manager"], ["PW-LINUX-01", "Sandcat, auditd, Wazuh Agent", "Wazuh 1514 vers manager"], ["PW-WAZUH-01", "Manager, indexer, dashboard", "Threat Hunting"]], [3.3*cm, 7.1*cm, 5*cm]), Spacer(1, 13), P("Chaîne de validation", h2),
        *B(["Caldera lance une ability ATT&amp;CK sur un endpoint autorisé.", "Sysmon ou auditd collecte la création du processus concerné.", "Wazuh reçoit, décode et applique la règle PurpleWatch.", "L'alerte est recherchée avec l'hôte, la règle et la technique MITRE."]),
        PageBreak(), P("2. Couverture et résultats", h1), P("Les règles PurpleWatch validées sont les suivantes.", body),
        table([["Endpoint", "Technique", "Commande observée", "Règle"], ["Windows", "T1082", "systeminfo.exe", "100100"], ["Windows", "T1057", "tasklist.exe", "100101"], ["Windows", "T1087.001", "net user", "100102"], ["Windows", "T1016", "ipconfig /all", "100103"], ["Linux", "T1082", "uname", "100104"], ["Linux", "T1057", "ps -ef / Atomic ps", "100105"]], [3*cm, 2.6*cm, 7.4*cm, 2.4*cm]), Spacer(1, 15), P("Retests mesurés", h2),
        P("Après le rétablissement du collecteur Windows, deux retests E2E ont été mesurés : T1082 a produit l'alerte 100100 en 36,817 secondes ; T1057 a produit l'alerte 100101 en 16,526 secondes. Ces chiffres distinguent le temps de l'exécution Caldera du temps d'apparition de l'alerte dans Wazuh.", body),
        P("3. Démarche Purple Team et résolution de problèmes", h1), P("Une absence d'alerte n'est pas un succès de scénario. Elle déclenche une analyse de la chaîne : exécution, collecte, transport, décodage et règle. Le correctif est ensuite retesté jusqu'à l'obtention d'une alerte exploitable.", body),
        *B(["Linux : auditd a été ciblé avec la clé purplewatch_execve ; la règle 100105 reconnaît /usr/bin/ps.", "Windows : le collecteur Wazuh a été redémarré puis la règle 100100 a été validée par retest.", "Caldera : l'agent doit être alive, trusted avant le lancement d'une opération."]),
        PageBreak(), P("4. Limites, apprentissages et prochaines étapes", h1), P("Limites connues", h2), P("La tâche planifiée Windows de persistance Sandcat a renvoyé 0x8007042B dans ce laboratoire. La procédure de démonstration utilise donc le script manuel C:\\Users\\Public\\Start-PurpleWatch-Sandcat.cmd. Cette limite est documentée et ne doit pas être présentée comme résolue.", body),
        P("Apprentissages", h2), *B(["Distinguer l'émulation d'une attaque, la télémétrie brute et la détection enrichie.", "Traiter les règles Wazuh comme du code : versionner, valider, tester et documenter.", "Préparer une démonstration avec des vérifications de santé et un scénario de secours."]),
        P("Prochaines étapes", h2), *B(["Automatiser les contrôles de santé et la mesure de latence E2E.", "Finaliser une persistance Windows testée et réversible.", "Étendre la couverture ATT&amp;CK et ajouter des tests de non-régression."]),
        P("Conclusion", h2), P("PurpleWatch démontre un cycle Purple Team concret : émuler, observer, détecter, corriger et retester. Le livrable réunit l'architecture, les règles, les preuves de validation et les limites connues pour rendre le laboratoire compréhensible et reproductible.", body),
    ]
    SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=2.1*cm, title="PurpleWatch - Rapport final", author="PurpleWatch").build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
