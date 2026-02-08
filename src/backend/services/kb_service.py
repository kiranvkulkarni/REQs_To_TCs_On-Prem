import sqlite3
import faiss
import numpy as np
import json
from pathlib import Path
from typing import List, Dict

class KBService:
    def __init__(self, config: dict):
        self.config = config
        self.sqlite_db_path = Path(config["kb"]["sqlite_db_path"])
        self.faiss_index_path = Path(config["kb"]["faiss_index_path"])
        self._init_faiss()

    def _init_faiss(self):
        self.index = faiss.read_index(str(self.faiss_index_path)) if self.faiss_index_path.exists() else None

    def get_all_screenshots(self) -> List[Dict]:
        """
        Get all screenshots from SQLite
        """
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM screenshots ORDER BY created_at DESC")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()

        screenshots = []
        for row in rows:
            metadata = dict(zip(columns, row))
            # Handle the column name inconsistency (gesture vs gestures)
            if "gesture" in metadata:
                metadata["gestures"] = json.loads(metadata["gesture"]) if metadata["gesture"] else []
                # Remove the old column to avoid confusion
                del metadata["gesture"]
            else:
                metadata["gestures"] = []
                
            metadata["conditions"] = json.loads(metadata["conditions"]) if metadata["conditions"] else []
            metadata["errors"] = json.loads(metadata["errors"]) if metadata["errors"] else []
            metadata["languages"] = json.loads(metadata["languages"]) if metadata["languages"] else []
            metadata["text"] = json.loads(metadata["text"]) if metadata["text"] else []
            screenshots.append(metadata)
        return screenshots

    def get_screenshot_by_id(self, screenshot_id: int) -> Dict:
        """
        Get screenshot by ID
        """
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM screenshots WHERE id = ?", (screenshot_id,))
        row = cursor.fetchone()
        columns = [description[0] for description in cursor.description]
        conn.close()

        if not row:
            return None

        metadata = dict(zip(columns, row))
        # Handle the column name inconsistency (gesture vs gestures)
        if "gesture" in metadata:
            metadata["gestures"] = json.loads(metadata["gesture"]) if metadata["gesture"] else []
            # Remove the old column to avoid confusion
            del metadata["gesture"]
        else:
            metadata["gestures"] = []
            
        metadata["conditions"] = json.loads(metadata["conditions"]) if metadata["conditions"] else []
        metadata["errors"] = json.loads(metadata["errors"]) if metadata["errors"] else []
        metadata["languages"] = json.loads(metadata["languages"]) if metadata["languages"] else []
        metadata["text"] = json.loads(metadata["text"]) if metadata["text"] else []
        return metadata

    def update_screenshot(self, screenshot_id: int, updates: Dict):
        """
        Update screenshot metadata
        """
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [screenshot_id]
        cursor.execute(f"UPDATE screenshots SET {set_clause} WHERE id = ?", values)
        conn.commit()
        conn.close()