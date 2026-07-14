import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Callable
from pydantic import model_validator
from obopilot.models.positioning import PositioningRead
from obopilot.services import ai_service
from obopilot.services.positioning_service import select_option

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output"


def print_json(data: dict):
    print(json.dumps(data, indent=4, ensure_ascii=False))


def print_model_data(pos: OBOPositioning):
    print(pos.model_dump_json(indent=4, exclude={"workflow"}))


def _build_file_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"positioning_{timestamp}.json"
    return OUTPUT_DIR / fname


def file_path_exists(file_path: Path) -> bool:
    return file_path.exists() and file_path.is_file()


def save_model_to_json(pos: OBOPositioning):
    # 1. JSON-String mit Einrückung generieren
    json_data = pos.model_dump_json(indent=4, exclude={"workflow"})

    # 2. In Datei schreiben (utf-8 sorgt für korrekte Umlaute)
    with open(_build_file_path(), "w", encoding="utf-8") as f:
        f.write(json_data)


def read_from_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        json_string = f.read()

    # Klasse mit dem JSON-String initialisieren
    new_pos = OBOPositioning.model_validate_json(json_string)
    return new_pos


def choose_option(input_message="Choose option", max_option=10):
    while True:
        try:
            message = f"{input_message} [1-{max_option}]: "
            choice = int(input(message))
            if 1 <= choice <= max_option:
                return choice
        except ValueError:
            pass


def set_selected_option(pos: OBOPositioning, selected_option_name: str, selected_option: dict):
    feld_als_string = "selected_options"
    neuer_sub_key = selected_option_name
    neuer_wert = selected_option

    # 1. Prüfen, ob das Feld aktuell noch 'None' ist (über getattr)
    aktueller_wert = getattr(pos, feld_als_string)

    if aktueller_wert is None:
        # Wenn leer, initialisieren wir es zuerst mit einem leeren Dict
        setattr(pos, feld_als_string, {})

    # 2. Jetzt greifen wir auf das Dictionary zu und fügen den neuen Wert ein
    # (Nutze getattr, um das Dict zu holen, und dann [ ] für den Schlüssel)
    getattr(pos, feld_als_string)[neuer_sub_key] = neuer_wert


class OBOPositioning(PositioningRead):
    count: int = 10
    id: int = 0
    user_id: int = 0
    project_id: int = 0

    # Define the workflow as a list of tuples (name, function)
    # default_factory=list sorgt für den leeren Startzustand vor der Validierung
    workflow: List[Tuple[str, Callable[[], None]]] = []

    # __init__ darf bei SQLModel Klassen nicht überschrieben werden!
    # Um ein 'self' zu bekommen, muss @model_validator(mode="after") verwendet werden.
    # Dieser Validator läuft AUTOMATISCH nach model_validate_json()
    @model_validator(mode="after")
    def initialize_workflow(self) -> "OBOPositioning":
        # HIER existiert 'self' jetzt perfekt!
        self.workflow = [
            ("offer", lambda: setattr(self, "offer", input("offer: "))),
            ("set_step_offer", lambda: setattr(self, "current_step", "offer")),
            ("print_offer", lambda: print(self.offer)),
            ("interrupt_offer", lambda: self.interrupt_workflow()),
            ("uniqueness", lambda: setattr(self, "uniqueness", input("uniqueness: "))),
            ("set_step_uniqueness", lambda: setattr(self, "current_step", "uniqueness")),
            ("print_uniqueness", lambda: print(self.uniqueness)),
            ("interrupt_uniqueness", lambda: self.interrupt_workflow()),
            ("target_group", lambda: setattr(
                self, "target_group_options", ai_service.generate_target_groups(
                    offer=self.offer,
                    uniqueness=self.uniqueness,
                    count=self.count,
                    )
                )
            ),
            ("print_target_group_options", lambda: print_json(self.target_group_options)),
            ("select_target_group", lambda: set_selected_option(
                self,
                "selected_target_group",
                select_option(self.target_group_options, choose_option("selected_target_group"))
                )
            ),
            ("print_selected_target_group", lambda: print_json(self.selected_options["selected_target_group"])),
            ("interrupt_target_group", lambda: self.interrupt_workflow()),
            ("problem", lambda: setattr(
                self, "problem_options", ai_service.generate_problems(
                    offer=self.offer,
                    uniqueness=self.uniqueness,
                    selected_target_group=self.selected_options["selected_target_group"],
                    count=self.count,
                    )
                )
            ),
            ("print_problem_options", lambda: print_json(self.problem_options)),
            ("select_problem", lambda: set_selected_option(
                self,
                "selected_problem",
                select_option(self.problem_options, choose_option("selected_problem"))
                )
            ),
            ("print_selected_problem", lambda: print_json(self.selected_options["selected_problem"])),
            ("interrupt_problem", lambda: self.interrupt_workflow()),
            ("desire", lambda: setattr(
                self, "desire_options", ai_service.generate_desires(
                    selected_target_group=self.selected_options["selected_target_group"],
                    selected_problem=self.selected_options["selected_problem"],
                    count=self.count,
                    )
                )
            ),
            ("print_desire_options", lambda: print_json(self.desire_options)),
            ("select_desire", lambda: set_selected_option(
                self,
                "selected_desire",
                select_option(self.desire_options, choose_option("selected_desire"))
                )
            ),
            ("print_selected_desire", lambda: print_json(self.selected_options["selected_desire"])),
            ("interrupt_desire", lambda: self.interrupt_workflow()),
            ("transformation", lambda: setattr(
                self, "transformation_options", ai_service.generate_transformations(
                    selected_target_group=self.selected_options["selected_target_group"],
                    selected_problem=self.selected_options["selected_problem"],
                    selected_desire=self.selected_options["selected_desire"],
                    count=self.count,
                    )
                )
            ),
            ("print_transformation_options", lambda: print_json(self.transformation_options)),
            ("select_transformation", lambda: set_selected_option(
                self,
                "selected_transformation",
                select_option(self.transformation_options, choose_option("selected_transformation"))
                )
            ),
            ("print_selected_transformation", lambda: print_json(self.selected_options["selected_transformation"])),
            ("interrupt_transformation", lambda: self.interrupt_workflow()),
            ("positioning", lambda: setattr(
                self, "positioning_options", ai_service.generate_positioning_options(
                    offer=self.offer,
                    uniqueness=self.uniqueness,
                    selected_target_group=self.selected_options["selected_target_group"],
                    selected_problem=self.selected_options["selected_problem"],
                    selected_desire=self.selected_options["selected_desire"],
                    selected_transformation=self.selected_options["selected_transformation"],
                    count=3,
                    )
                )
            ),
            ("print_positioning_options", lambda: print_json(self.positioning_options)),
            ("select_positioning", lambda: set_selected_option(
                self,
                "selected_positioning",
                select_option(self.positioning_options, choose_option("selected_positioning", 3))
                )
            ),
            ("print_selected_positioning", lambda: print_json(self.selected_options["selected_positioning"])),
            ("interrupt_positioning", lambda: self.interrupt_workflow()),
            ("big_idea", lambda: setattr(
                self, "big_idea_options", ai_service.generate_big_ideas(
                    selected_positioning=self.selected_options["selected_positioning"],
                    count=self.count,
                    )
                )
            ),
            ("print_big_idea_options", lambda: print_json(self.big_idea_options)),
            ("select_big_idea", lambda: set_selected_option(
                self,
                "selected_big_idea",
                select_option(self.big_idea_options, choose_option("selected_big_idea"))
                )
            ),
            ("print_selected_big_idea", lambda: print_json(self.selected_options["selected_big_idea"])),
            ("interrupt_big_idea", lambda: self.interrupt_workflow()),
            ("pitch", lambda: setattr(
                self, "pitch_options", ai_service.generate_pitch_options(
                    selected_target_group=self.selected_options["selected_target_group"],
                    selected_problem=self.selected_options["selected_problem"],
                    selected_desire=self.selected_options["selected_desire"],
                    selected_positioning=self.selected_options["selected_positioning"],
                    selected_big_idea=self.selected_options["selected_big_idea"],
                    )
                )
            ),
            ("print_pitch_options", lambda: print_json(self.pitch_options)),
            ("select_pitch", lambda: set_selected_option(
                self,
                "selected_pitch",
                select_option(self.pitch_options, choose_option("selected_pitch", 3))
                )
            ),
            ("print_selected_pitch", lambda: print_json(self.selected_options["selected_pitch"])),
            ("interrupt_pitch", lambda: self.interrupt_workflow()),
            ("marketing_kit", lambda: setattr(
                self, "marketing_kit", ai_service.generate_marketing_kit(
                    offer=self.offer,
                    uniqueness=self.uniqueness,
                    selected_target_group=self.selected_options["selected_target_group"],
                    selected_problem=self.selected_options["selected_problem"],
                    selected_desire=self.selected_options["selected_desire"],
                    selected_transformation=self.selected_options["selected_transformation"],
                    selected_positioning=self.selected_options["selected_positioning"],
                    selected_big_idea=self.selected_options["selected_big_idea"],
                    selected_pitch=self.selected_options["selected_pitch"],
                    )
                )
            ),
            ("print_marketing_kit", lambda: print_json(self.marketing_kit)),
        ]
        return self

    def interrupt_workflow(self):
        if input("interrupt_workflow [yes]: ") == "yes":
            print("Workflow abgebrochen.")
            print_model_data(self)
            save_model_to_json(self)
            exit(1)

    def run_workflow_from(self, step_name: str):
        # Index des Start-Strings finden
        start_index = next((i for i, (name, _) in enumerate(self.workflow) if name == start_step), None)

        if start_index is None:
            print(f"Fehler: '{step_name}' ist kein gültiger Startpunkt.")
            exit(1)

        # Funktionen ab dem Startpunkt ausführen (ohne Parameter zu übergeben)
        for name, workflow_step in self.workflow[start_index:]:
#            print(f"[Starte: {name}]")
            workflow_step()  # Hier wird die Lambda-Funktion aufgerufen


if __name__ == "__main__":

    filepath = OUTPUT_DIR / Path(input("filename: ") + ".json")
    if file_path_exists(filepath):
        positioning = read_from_file(filepath)
        print_model_data(positioning)
        start_step = input("start from: ")
    else:
        print("File doesn't exist. Start from scratch...")
        positioning = OBOPositioning()
        positioning.selected_options = {}
        start_step = "offer"

    positioning.run_workflow_from(start_step)

    print_model_data(positioning)
    save_model_to_json(positioning)
