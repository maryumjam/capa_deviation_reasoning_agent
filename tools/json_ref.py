# tools/json_ref.py
import json

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

class SOPCAPAReference:
    def __init__(self, json_path):
        self.data = load_json(json_path)
        # Split data into separate lists for easier access
        self.sops = [item for item in self.data if item.get("type") == "SOP"]
        self.capas = [item for item in self.data if item.get("type") == "CAPA"]

    def find_sop_matches(self, text):
        matches = []
        for sop in self.sops:
            # We will check text against title + purpose + procedure steps
            search_fields = (
                (sop.get("title") or "") +
                " " +
                (sop.get("purpose") or "") +
                " " +
                (sop.get("procedure_steps") or "")
            ).lower()

            if any(keyword.lower() in text.lower() for keyword in search_fields.split()):
                matches.append(sop)
        return matches

    def find_capa_matches(self, text):
        matches = []
        for capa in self.capas:
            # Check text against root cause + corrective + preventive actions
            search_fields = (
                (capa.get("root_cause") or "") +
                " " +
                (capa.get("corrective_action") or "") +
                " " +
                (capa.get("preventive_action") or "")
            ).lower()

            if any(keyword.lower() in text.lower() for keyword in search_fields.split()):
                matches.append(capa)
        return matches
