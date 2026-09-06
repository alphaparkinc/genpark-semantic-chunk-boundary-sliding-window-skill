"""
Sentence-Boundary Aware Sliding Window Chunker.
Zero external dependencies, standard library only.
"""

import re
import hashlib
from typing import Dict, List, Any

class SemanticSlidingWindowChunkerClient:
    """
    Partitions long text into overlapping chunks without breaking grammatical boundaries:
    - Splits text on terminal sentence delimiters (. ? !)
    - Groups sentences up to max_token_words threshold
    - Carries forward overlap sentences to preserve semantic continuity
    """

    def __init__(self, max_words: int = 40, overlap_words: int = 10):
        self.max_words = max_words
        self.overlap_words = overlap_words

    def _split_sentences(self, text: str) -> List[str]:
        raw = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in raw if s.strip()]

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Splits narrative into overlapping sentence-boundary chunks."""
        sentences = self._split_sentences(text)
        if not sentences:
            return []

        chunks = []
        curr_sentences = []
        curr_word_count = 0
        chunk_idx = 0

        for s in sentences:
            s_words = len(s.split())
            if curr_word_count + s_words > self.max_words and curr_sentences:
                chunk_str = " ".join(curr_sentences)
                c_hash = hashlib.sha256(chunk_str.encode("utf-8")).hexdigest()[:10]
                chunks.append({
                    "chunk_index": chunk_idx,
                    "word_count": curr_word_count,
                    "content": chunk_str,
                    "chunk_hash": c_hash
                })
                chunk_idx += 1

                # Retain overlap sentences
                overlap_acc = []
                overlap_words_cnt = 0
                for prev_s in reversed(curr_sentences):
                    pw = len(prev_s.split())
                    if overlap_words_cnt + pw <= self.overlap_words or not overlap_acc:
                        overlap_acc.insert(0, prev_s)
                        overlap_words_cnt += pw
                    else:
                        break
                curr_sentences = list(overlap_acc)
                curr_word_count = overlap_words_cnt

            curr_sentences.append(s)
            curr_word_count += s_words

        if curr_sentences:
            chunk_str = " ".join(curr_sentences)
            c_hash = hashlib.sha256(chunk_str.encode("utf-8")).hexdigest()[:10]
            chunks.append({
                "chunk_index": chunk_idx,
                "word_count": curr_word_count,
                "content": chunk_str,
                "chunk_hash": c_hash
            })

        return chunks
