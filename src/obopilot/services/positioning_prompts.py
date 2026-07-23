
def _base_prompt_rules() -> str:
    return """
    Wichtig:
    - Schreibe vollständig auf Deutsch.
    - Verwende echte deutsche Umlaute wie ä, ö, ü und ß.
    - Verwende keine Unicode-Escape-Sequenzen.
    - Gib ausschließlich strukturierte Daten gemäß Schema zurück.
    """


def target_group_prompt(
        *,
        offer: str,
        uniqueness: str,
        count: int = 10
):
    return f"""
    Du bist ein erfahrener Positionierungs- und Marketingstratege.
    
    Ermittle die {count} attraktivsten Zielgruppen für folgendes Angebot.
    
    Angebot:
    {offer}
    
    Einzigartigkeit:
    {uniqueness}
    
    Bewerte jede Zielgruppe nach:
    
    1. Marktpotenzial
    2. Kaufwahrscheinlichkeit
    3. Zahlungsbereitschaft
    4. Erreichbarkeit
    5. Passung zum Angebot
    
    Erzeuge zusätzlich:
    
    - Branche
    - Unternehmensgröße
    - typischer Entscheider
    - Leidensdruck
    - Kaufpotenzial
    
    Sortiere anschließend absteigend nach Score.
    
    {_base_prompt_rules()}
    """


def prompt_version():
    return "NORMAL PROMPTS"


def problem_prompt(
        *,
        offer: str,
        uniqueness: str,
        selected_target_group: dict,
        count: int = 10
):
    return f"""
    Du bist ein erfahrener Positionierungs- und Marketingstratege.
    
    Ermittle {count} konkrete Probleme dieser Zielgruppe, die mit dem Angebot gelöst oder reduziert werden können.
    
    Angebot:
    {offer}
    
    Einzigartigkeit:
    {uniqueness}
    
    Ausgewählte Zielgruppe:
    {selected_target_group}
    
    Priorisiere Probleme, die kaufentscheidend sein können.
    
    Bewerte jedes Problem nach:
    1. Schmerzintensität
    2. Häufigkeit
    3. wirtschaftlicher Relevanz
    4. Dringlichkeit
    5. Lösbarkeit durch das Angebot
    
    Sortiere absteigend nach Score.
    {_base_prompt_rules()}
    """


def desire_prompt(
        *,
        selected_target_group: dict,
        selected_problem: dict,
        count: int = 10
):
    return f"""
    Du bist ein erfahrener Positionierungs- und Marketingstratege.
    
    Leite aus folgender Zielgruppe und folgendem Problem {count} Wünsche ab.
    
    Zielgruppe:
    {selected_target_group}
    
    Problem:
    {selected_problem}
    
    Unterscheide rationale und emotionale Wünsche.
    
    Bewerte jeden Wunsch nach:
    1. Attraktivität
    2. Relevanz
    3. Nähe zum Angebot
    4. Kaufmotivation
    
    Sortiere absteigend nach Score.
    {_base_prompt_rules()}
    """

def transformation_prompt(
        *,
        selected_target_group: dict,
        selected_problem: dict,
        selected_desire: dict,
        count: int = 10,
):
    return f"""
    Du bist ein erfahrener Positionierungs- und Marketingstratege.
    
    Erzeuge {count} konkrete Transformationen.
    
    Zielgruppe:
    {selected_target_group}
    
    Problem:
    {selected_problem}
    
    Wunsch:
    {selected_desire}
    
    Jede Transformation beschreibt den Weg vom aktuellen Problemzustand zum gewünschten Zielzustand.
    
    Format:
    - before
    - after
    - transformation
    - customer_value
    
    Sortiere absteigend nach Score.
    {_base_prompt_rules()}
    """


def positioning_prompt(
        *,
        offer: str,
        uniqueness: str,
        selected_target_group: dict,
        selected_problem: dict,
        selected_desire: dict,
        selected_transformation: dict,
        count: int = 3,
):
    return f"""
    Erstelle {count} Positionierungsvarianten.
    
    Angebot:
    {offer}
    
    Einzigartigkeit:
    {uniqueness}
    
    Zielgruppe:
    {selected_target_group}
    
    Problem:
    {selected_problem}
    
    Wunsch:
    {selected_desire}
    
    Transformation:
    {selected_transformation}
    
    Nutze diese Formel:
    Ich helfe [Zielgruppe], die unter [Problem] leidet, mit [Angebot] und [Einzigartigkeit] dabei, [Wunsch] zu erreichen, damit sie [Transformation] erleben.
    
    Erzeuge Varianten:
    1. sachlich
    2. nutzenorientiert
    3. emotional
    
    {_base_prompt_rules()}
    """


def big_idea_prompt(
        *,
        offer: str,
        uniqueness: str,
        selected_target_group: dict,
        selected_problem: dict,
        selected_desire: dict,
        selected_transformation: dict,
        selected_positioning: dict,
        count: int = 10,
):
    return f"""
    Erzeuge {count} Big Marketing Ideas.
    
    Positionierung:
    {selected_positioning}
    
    Jede Big Marketing Idea besteht aus:
    - Transformationsversprechen
    - Name eines einzigartigen Systems
    - kurze Erklärung
    - zentrale Marketingbotschaft
    
    Der Systemname soll merkfähig und professionell klingen.
    
    Mögliche Namensmuster:
    - Methode
    - Framework
    - Formel
    - Blueprint
    - System
    
    Beispiele:
    - KI-Effizienz-System™
    - Growth Blueprint™
    - Profit Formel™
    - Digitalisierungs-Methode™
    
    Sortiere absteigend nach Score.
    {_base_prompt_rules()}
    """


def pitch_prompt(
        *,
        selected_target_group: dict,
        selected_problem: dict,
        selected_desire: dict,
        selected_positioning: dict,
        selected_big_idea: dict,
        count: int = 3,
):
    return f"""
    Nutze alle bisherigen Ergebnisse und erzeuge {count} Pitch-Varianten.
    
    Zielgruppe:
    {selected_target_group}
    
    Problem:
    {selected_problem}
    
    Wunsch:
    {selected_desire}
    
    Positionierung:
    {selected_positioning}
    
    Big Marketing Idea:
    {selected_big_idea}
    
    Erzeuge:
    1. 30-Sekunden-Pitch
    2. 60-Sekunden-Pitch
    3. Website-Pitch
    
    {_base_prompt_rules()}
    """


def marketing_kit_prompt(
        *,
        offer: str,
        uniqueness: str,
        selected_target_group: dict,
        selected_problem: dict,
        selected_desire: dict,
        selected_transformation: dict,
        selected_positioning: dict,
        selected_big_idea: dict,
        selected_pitch: dict,
):
    return f"""
    Erzeuge ein sofort nutzbares Marketing-Kit.
    
    Ausgewählte Ergebnisse:
    
    Angebot:
    {offer}
    
    Einzigartigkeit:
    {uniqueness}
    
    Zielgruppe:
    {selected_target_group}
    
    Hauptproblem:
    {selected_problem}
    
    Hauptwunsch:
    {selected_desire}
    
    Transformation:
    {selected_transformation}
    
    Positionierung:
    {selected_positioning}
    
    Big Marketing Idea:
    {selected_big_idea}
    
    Elevator Pitch:
    {selected_pitch}
    
    Das Marketing-Kit enthält:
    1. One-Liner
    2. Website Headline
    3. Website Subheadline
    4. LinkedIn Bio
    5. Elevator Pitch
    6. Positionierung
    7. Zielgruppenbeschreibung
    8. Hauptproblem
    9. Hauptwunsch
    10. Transformation
    11. Big Marketing Idea
    12. Systemname
    
    Alle Texte sollen sofort einsetzbar sein.
    {_base_prompt_rules()}
    """