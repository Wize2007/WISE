
import os
import json


class WiseMemory:

    def __init__(self):

        self.file_path = os.path.join(
            "data",
            "memories.json"
        )

        self.memories = self.load_memory()

    # =========================
    # LOAD MEMORY
    # =========================

    def load_memory(self):

        if os.path.exists(
            self.file_path
        ):

            try:

                with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                    if isinstance(
                        data,
                        dict
                    ):

                        return data

                    return {}

            except (
                json.JSONDecodeError,
                OSError
            ):

                return {}

        return {}

    # =========================
    # SAVE MEMORY
    # =========================

    def save_memory(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.memories,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =========================
    # REMEMBER
    # =========================

    def remember(
        self,
        key,
        value
    ):

        self.memories[key] = value

        self.save_memory()

    # =========================
    # RECALL
    # =========================

    def recall(
        self,
        key
    ):

        return self.memories.get(
            key
        )

    # =========================
    # FORGET
    # =========================

    def forget(
        self,
        key
    ):

        if key in self.memories:

            del self.memories[key]

            self.save_memory()

            return True

        return False

    # =========================
    # GET ALL MEMORIES
    # =========================

    def get_all_memories(self):

        return self.memories.copy()

    # =========================
    # CLEAR ALL MEMORY
    # =========================

    def clear_memory(self):

        self.memories = {}

        self.save_memory()

