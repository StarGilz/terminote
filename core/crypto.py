import base64
import os

class CryptoManager:
    def __init__(self, storage_dir="notes"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def save_sealed(self, filename, content):
        if not filename.endswith(".txt"):
            filename += ".txt"
        sealed_data = base64.b64encode(content.encode('utf-8'))
        file_path = os.path.join(self.storage_dir, filename)
        with open(file_path, "wb") as f:
            f.write(sealed_data)
        return True

    def load_unsealed(self, filename):
        if not filename.endswith(".txt"):
            filename += ".txt"
        file_path = os.path.join(self.storage_dir, filename)
        if not os.path.exists(file_path):
            return ""
        with open(file_path, "rb") as f:
            sealed_data = f.read()
            return base64.b64decode(sealed_data).decode('utf-8')

    def get_file_list(self):
        return [f for f in os.listdir(self.storage_dir) if f.endswith(".txt")]

    def search_files(self, keyword):
        matching_files = []
        all_files = self.get_file_list()
        for filename in all_files:
            content = self.load_unsealed(filename)
            if keyword.lower() in content.lower():
                matching_files.append(filename)
        return matching_files