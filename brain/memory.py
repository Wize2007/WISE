import json
import os
import tempfile


class WiseMemory:
    """Persistent key/value memory with safe paths and guarded file writes."""

    def __init__(self, file_path=None):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_path = os.path.join(project_root, "data", "memories.json")
        self.file_path = os.path.abspath(os.fspath(file_path or default_path))
        self._load_error = None
        self.memories = self.load_memory()

    def load_memory(self):
        """Load a JSON object without allowing a later save to erase bad data."""
        self._load_error = None
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            self._load_error = error
            print("WISE MEMORY WARNING: memory file could not be read; preserving it.")
            return {}

        if not isinstance(data, dict):
            self._load_error = ValueError("Memory JSON must contain an object.")
            print("WISE MEMORY WARNING: memory file has an invalid structure; preserving it.")
            return {}

        return data

    def save_memory(self):
        """Atomically save memory and refuse to overwrite a file that failed to load."""
        if self._load_error is not None:
            raise OSError(
                "WISE memory was not saved because the existing memory file could "
                "not be loaded. Repair or back up that file before saving again."
            ) from self._load_error

        directory = os.path.dirname(self.file_path)
        os.makedirs(directory, exist_ok=True)
        temporary_path = None

        try:
            descriptor, temporary_path = tempfile.mkstemp(
                prefix=".memories-",
                suffix=".tmp",
                dir=directory,
                text=True,
            )
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as file:
                json.dump(self.memories, file, indent=4, ensure_ascii=False)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_path, self.file_path)
            temporary_path = None
        finally:
            if temporary_path and os.path.exists(temporary_path):
                try:
                    os.remove(temporary_path)
                except OSError:
                    pass

    def remember(self, key, value):
        existed = key in self.memories
        previous_value = self.memories.get(key)
        self.memories[key] = value
        try:
            self.save_memory()
        except Exception:
            if existed:
                self.memories[key] = previous_value
            else:
                self.memories.pop(key, None)
            raise

    def recall(self, key):
        return self.memories.get(key)

    def forget(self, key):
        if key not in self.memories:
            return False

        previous_value = self.memories.pop(key)
        try:
            self.save_memory()
        except Exception:
            self.memories[key] = previous_value
            raise
        return True

    def get_all_memories(self):
        return self.memories.copy()

    def clear_memory(self):
        previous_memories = self.memories
        self.memories = {}
        try:
            self.save_memory()
        except Exception:
            self.memories = previous_memories
            raise
