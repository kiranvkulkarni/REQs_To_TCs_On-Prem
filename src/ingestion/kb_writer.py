import sqlite3
import faiss
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

class KBWriter:
    def __init__(self, config: dict):
        self.config = config
        self.sqlite_db_path = Path(config["kb"]["sqlite_db_path"])
        self.faiss_index_path = Path(config["kb"]["faiss_index_path"])
        self.metadata_json_path = Path(config["kb"]["metadata_json_path"])
        self._init_db()
        self._init_faiss()

    def _init_db(self):
        self.sqlite_db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS screenshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                feature_name TEXT,
                gesture TEXT,
                conditions TEXT,
                errors TEXT,
                languages TEXT,
                text TEXT,
                image_path TEXT,
                width INTEGER,
                height INTEGER,
                version INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                embedding BLOB
            )
        """)
        conn.commit()
        conn.close()

    def _init_faiss(self):
        self.faiss_index_path.parent.mkdir(parents=True, exist_ok=True)
        d = 768  # LayoutLMv3 embedding dim
        self.index = faiss.IndexFlatIP(d)  # Inner product for cosine similarity
        self.ids = []

    def write(self, metadata: Dict):
        """
        Write metadata to SQLite + FAISS
        """
        # Generate embedding (simulated — in real code, use LayoutLM’s last hidden state)
        embedding = np.random.rand(768).astype('float32')
        faiss.normalize_L2(embedding.reshape(1, -1))

        # Insert into SQLite
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO screenshots (
                filename, feature_name, gesture, conditions, errors, languages, text, image_path, width, height,
version, embedding
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            metadata["filename"],
            metadata["feature_name"],
            json.dumps(metadata["gestures"]),
            json.dumps(metadata["conditions"]),
            json.dumps(metadata["errors"]),
            json.dumps(metadata["languages"]),
            json.dumps(metadata["text"]),
            metadata["image_path"],
            metadata["width"],
            metadata["height"],
            metadata["version"],
            embedding.tobytes()
        ))
        metadata["id"] = cursor.lastrowid
        conn.commit()
        conn.close()

        # Add to FAISS
        self.index.add(embedding.reshape(1, -1))
        self.ids.append(metadata["id"])

        # Save FAISS index
        faiss.write_index(self.index, str(self.faiss_index_path))

        # Save metadata to JSON (for debugging)
        metadata_json = self.metadata_json_path
        if metadata_json.exists():
            with open(metadata_json, "r", encoding="utf-8") as f:
                all_metadata = json.load(f)
        else:
            all_metadata = []
        all_metadata.append(metadata)
        with open(metadata_json, "w", encoding="utf-8") as f:
            json.dump(all_metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"Metadata written for {metadata['filename']}")