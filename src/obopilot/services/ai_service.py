from typing import Any
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
client = OpenAI(api_key=OPENAI_API_KEY)


def _base_prompt_rules() -> str:
    return """
    Wichtig:
    - Schreibe vollständig auf Deutsch.
    - Verwende echte deutsche Umlaute wie ä, ö, ü und ß.
    - Verwende keine Unicode-Escape-Sequenzen.
    - Gib ausschließlich strukturierte Daten gemäß Schema zurück.
    """


def _build_option(
    option_id: int,
    name: str,
    description: str,
    reason: str,
    score: int,
) -> dict[str, Any]:
    return {
        "id": option_id,
        "name": name,
        "description": description,
        "reason": reason,
        "score": score,
    }


def _json_schema_options(schema_name: str, item_properties: dict, required: list[str], count: int) -> dict:
    return {
        "type": "object",
        "properties": {
            "options": {
                "type": "array",
                "minItems": count,
                "maxItems": count,
                "items": {
                    "type": "object",
                    "properties": item_properties,
                    "required": required,
                    "additionalProperties": False,
                },
            }
        },
        "required": ["options"],
        "additionalProperties": False,
    }


def _call_openai_options(
    prompt: str,
    schema_name: str,
    schema: dict,
    fallback: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    # print(50 * "#")
    # print(f"_call_openai_options returning fallback !!!")
    # print(50 * "#")
    # return fallback
    if not OPENAI_API_KEY:
        return fallback

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        data = json.loads(response.output_text)
        return data["options"]

    except Exception as error:
        print(f"OpenAI generation failed ({schema_name}): {error}")
        return fallback


def _generate_options(
    *,
    schema_name: str,
    prompt: str,
    item_properties: dict[str, Any],
    required: list[str],
    fallback: list[dict[str, Any]],
    count: int,
) -> list[dict[str, Any]]:
    schema = _json_schema_options(
        schema_name=schema_name,
        item_properties=item_properties,
        required=required,
        count=count,
    )

    return _call_openai_options(
        prompt=prompt,
        schema_name=schema_name,
        schema=schema,
        fallback=fallback,
    )


def generate_target_groups(
    *,
    offer: str,
    uniqueness: str,
    count: int = 10,
) -> list[dict[str, Any]]:
    fallback = [
        _build_option(
            option_id=index,
            name=f"Zielgruppe {index}",
            description=f"Potenzielle Zielgruppe für das Angebot '{offer}'.",
            reason=f"Diese Zielgruppe profitiert besonders von der Einzigartigkeit: {uniqueness}",
            score=100 - index,
        )
        for index in range(1, count + 1)
    ]

    prompt = f"""
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

    return _generate_options(
        schema_name="target_group_options",
        prompt=prompt,
        item_properties={
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "reason": {"type": "string"},
            "industry": {"type": "string"},
            "company_size": {"type": "string"},
            "decision_maker": {"type": "string"},
            "pain_level": {"type": "string"},
            "buying_potential": {"type": "string"},
            "score": {"type": "integer"},
        },
        required=[
            "id",
            "name",
            "description",
            "reason",
            "industry",
            "company_size",
            "decision_maker",
            "pain_level",
            "buying_potential",
            "score",
        ],
        fallback=fallback,
        count=count,
    )


def generate_problems(
    *,
    offer: str,
    uniqueness: str,
    selected_target_group: dict[str, Any],
    count: int = 10,
) -> list[dict[str, Any]]:
    fallback = [
        _build_option(
            option_id=index,
            name=f"Problem {index}",
            description=(
                f"Typisches Problem der Zielgruppe '{selected_target_group["name"]}'."
            ),
            reason=(
                f"Das Angebot '{offer}' kann dieses Problem durch '{uniqueness}' adressieren."
            ),
            score=100 - index,
        )
        for index in range(1, count + 1)
    ]

    prompt = f"""
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

    return _generate_options(
        schema_name="problem_options",
        prompt=prompt,
        item_properties={
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "reason": {"type": "string"},
            "problem": {"type": "string"},
            "impact": {"type": "string"},
            "buying_relevance": {"type": "string"},
            "score": {"type": "integer"},
        },
        required=[
            "id",
            "name",
            "description",
            "reason",
            "problem",
            "impact",
            "buying_relevance",
            "score",
        ],
        fallback=fallback,
        count=count,
    )


def generate_desires(
    *,
    selected_target_group: dict[str, Any],
    selected_problem: dict[str, Any],
    count: int = 10,
) -> list[dict[str, Any]]:
    fallback = [
        _build_option(
            option_id=index,
            name=f"Wunsch {index}",
            description=f"Gewünschter Zielzustand der Zielgruppe '{selected_target_group["name"]}'.",
            reason=f"Dieser Wunsch entsteht aus dem Problem: {selected_problem["name"]}",
            score=100 - index,
        )
        for index in range(1, count + 1)
    ]

    prompt = f"""
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

    return _generate_options(
        schema_name="desire_options",
        prompt=prompt,
        item_properties={
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "reason": {"type": "string"},
            "rational_reason": {"type": "string"},
            "emotional_reason": {"type": "string"},
            "score": {"type": "integer"},
        },
        required=[
            "id",
            "name",
            "description",
            "reason",
            "rational_reason",
            "emotional_reason",
            "score",
        ],
        fallback=fallback,
        count=count,
    )


def generate_transformations(
    *,
    selected_target_group: dict[str, Any],
    selected_problem: dict[str, Any],
    selected_desire: dict[str, Any],
    count: int = 10,
) -> list[dict[str, Any]]:
    fallback = [
        _build_option(
            option_id=index,
            name=f"Transformation {index}",
            description=f"Transformation von '{selected_problem["name"]}' zu '{selected_desire["name"]}'.",
            reason=f"Diese Transformation ist für '{selected_target_group["name"]}' besonders relevant.",
            score=100 - index,
        )
        for index in range(1, count + 1)
    ]

    prompt = f"""
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

    return _generate_options(
        schema_name="transformation_options",
        prompt=prompt,
        item_properties={
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "reason": {"type": "string"},
            "before": {"type": "string"},
            "after": {"type": "string"},
            "transformation": {"type": "string"},
            "customer_value": {"type": "string"},
            "score": {"type": "integer"},
        },
        required=[
            "id",
            "name",
            "description",
            "reason",
            "before",
            "after",
            "transformation",
            "customer_value",
            "score",
        ],
        fallback=fallback,
        count=count,
    )


def generate_positioning_options(
    *,
    offer: str,
    uniqueness: str,
    selected_target_group: dict[str, Any],
    selected_problem: dict[str, Any],
    selected_desire: dict[str, Any],
    selected_transformation: dict[str, Any],
    count: int = 3,
) -> list[dict[str, Any]]:
    fallback = [
        _build_option(
            option_id=index,
            name=f"Positionierung {index}",
            description=(
                f"Ich helfe {selected_target_group["name"]}, die unter '{selected_problem["name"]}' leiden, "
                f"mit '{offer}' dabei, '{selected_desire["name"]}' zu erreichen."
            ),
            reason="Diese Positionierung verbindet Angebot, Zielgruppe, Problem, Wunsch und Transformation.",
            score=100 - index,
        )
        for index in range(1, count + 1)
    ]

    prompt = f"""
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

    return _generate_options(
        schema_name="positioning_options",
        prompt=prompt,
        item_properties={
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "style": {"type": "string"},
            "description": {"type": "string"},
            "text": {"type": "string"},
            "reason": {"type": "string"},
            "score": {"type": "integer"},
        },
        required=["id", "name", "style", "description", "text", "reason", "score"],
        fallback=fallback,
        count=count,
    )


def generate_big_ideas(
    *,
    selected_positioning: dict[str, Any],
    count: int = 10,
) -> list[dict[str, Any]]:
    fallback = [
        _build_option(
            option_id=index,
            name=f"Big Marketing Idea {index}",
            description=f"Merkfähige Marketing-Idee auf Basis der Positionierung: {selected_positioning['text']}",
            reason="Eine starke Big Marketing Idea macht die Positionierung einfacher kommunizierbar.",
            score=100 - index,
        )
        for index in range(1, count + 1)
    ]

    prompt = f"""
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

    return _generate_options(
        schema_name="big_idea_options",
        prompt=prompt,
        item_properties={
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "promise": {"type": "string"},
            "system_name": {"type": "string"},
            "explanation": {"type": "string"},
            "core_message": {"type": "string"},
            "description": {"type": "string"},
            "reason": {"type": "string"},
            "score": {"type": "integer"},
        },
        required=[
            "id",
            "name",
            "promise",
            "system_name",
            "explanation",
            "core_message",
            "description",
            "reason",
            "score",
        ],
        fallback=fallback,
        count=count,
    )


def generate_pitch_options(
    *,
    selected_target_group: dict[str, Any],
    selected_problem: dict[str, Any],
    selected_desire: dict[str, Any],
    selected_positioning: dict[str, Any],
    selected_big_idea: dict[str, Any],
    count: int = 3,
) -> list[dict[str, Any]]:
    fallback = [
        _build_option(
            option_id=index,
            name=f"Pitch {index}",
            description=(
                f"Für {selected_target_group["name"]}, die mit '{selected_problem["name"]}' kämpfen, "
                f"bietet diese Lösung einen Weg zu '{selected_desire["name"]}'. "
                f"Kernidee: {selected_big_idea["name"]}"
            ),
            reason="Der Pitch verdichtet Positionierung und Big Marketing Idea in eine klare Aussage.",
            score=100 - index,
        )
        for index in range(1, count + 1)
    ]

    prompt = f"""
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

    return _generate_options(
        schema_name="pitch_options",
        prompt=prompt,
        item_properties={
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "type": {"type": "string"},
            "text": {"type": "string"},
            "description": {"type": "string"},
            "reason": {"type": "string"},
            "score": {"type": "integer"},
        },
        required=["id", "name", "type", "text", "description", "reason", "score"],
        fallback=fallback,
        count=count,
    )


def generate_marketing_kit(
    *,
    offer: str,
    uniqueness: str,
    selected_target_group: dict[str, Any],
    selected_problem: dict[str, Any],
    selected_desire: dict[str, Any],
    selected_transformation: dict[str, Any],
    selected_positioning: dict[str, Any],
    selected_big_idea: dict[str, Any],
    selected_pitch: dict[str, Any],
) -> dict[str, Any]:
    fallback = {
        "offer": offer,
        "uniqueness": uniqueness,
        "target_group": selected_target_group["name"],
        "problem": selected_problem["name"],
        "desire": selected_desire["name"],
        "transformation": selected_transformation["name"],
        "positioning": selected_positioning["text"],
        "big_marketing_idea": selected_big_idea["name"],
        "elevator_pitch": selected_pitch["text"],
    }

    if not OPENAI_API_KEY:
        return fallback

    schema = {
        "type": "object",
        "properties": {
            "one_liner": {"type": "string"},
            "website_headline": {"type": "string"},
            "website_subheadline": {"type": "string"},
            "linkedin_bio": {"type": "string"},
            "elevator_pitch": {"type": "string"},
            "positioning": {"type": "string"},
            "target_group_description": {"type": "string"},
            "main_problem": {"type": "string"},
            "main_desire": {"type": "string"},
            "transformation": {"type": "string"},
            "big_marketing_idea": {"type": "string"},
            "system_name": {"type": "string"},
        },
        "required": [
            "one_liner",
            "website_headline",
            "website_subheadline",
            "linkedin_bio",
            "elevator_pitch",
            "positioning",
            "target_group_description",
            "main_problem",
            "main_desire",
            "transformation",
            "big_marketing_idea",
            "system_name",
        ],
        "additionalProperties": False,
    }

    prompt = f"""
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

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "marketing_kit",
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        return json.loads(response.output_text)

    except Exception as error:
        print(f"OpenAI marketing kit generation failed: {error}")
        return fallback


