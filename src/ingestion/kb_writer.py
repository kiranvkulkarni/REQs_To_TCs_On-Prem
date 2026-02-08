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
    def _init_db(self) -> None:
        self.sqlite_db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS screenshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                feature_name TEXT,
                screens TEXT,
                transitions TEXT,
                image_path TEXT,
                version INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                embedding BLOB
            )
            """
        )
        conn.commit()
        conn.close()

    def _init_faiss(self) -> None:
        self.faiss_index_path.parent.mkdir(parents=True, exist_ok=True)
        d = 768  # LayoutLMv3 embedding dim
        self.index = faiss.IndexFlatIP(d)  # Inner product for cosine similarity
        self.ids = []

    def write(self, metadata: Dict) -> None:
        """
        Write metadata to SQLite + FAISS.
        Args:
            metadata (Dict): Structured metadata to store.
        """
        embedding = metadata.get("embedding")
        if embedding is not None:
            embedding = np.array(embedding, dtype='float32')
            faiss.normalize_L2(embedding.reshape(1, -1))

        # Insert into SQLite
        conn = sqlite3.connect(self.sqlite_db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO screenshots (
                filename, feature_name, screens, transitions, image_path, version, embedding
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                metadata["filename"],
                metadata["feature_name"],
                json.dumps(metadata["screens"]),
                json.dumps(metadata["transitions"]),
                metadata["image_path"],
                metadata["version"],
                embedding.tobytes() if embedding is not None else None
            )
        )
        metadata["id"] = cursor.lastrowid
        conn.commit()
        conn.close()

        # Add to FAISS if embedding exists
        if embedding is not None:
            self.index.add(embedding.reshape(1, -1))
            self.ids.append(metadata["id"])
            faiss.write_index(self.index, str(self.faiss_index_path))

        # Save metadata to JSON
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