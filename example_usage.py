"""
Demonstration of genpark-semantic-chunk-boundary-sliding-window-skill
"""

from client import SemanticSlidingWindowChunkerClient

def main():
    chunker = SemanticSlidingWindowChunkerClient(max_words=25, overlap_words=8)

    sample_doc = (
        "Quantum computing harnesses superposition to execute exponential state calculations. "
        "Traditional binary gates process discrete zero and one states sequentially. "
        "Cryogenic qubit stability remains the foremost engineering bottleneck in commercial scaling. "
        "Error correction topological surface codes offer promising pathways toward fault tolerance. "
        "Leading research laboratories report sub-millisecond coherence time breakthroughs."
    )

    chunks = chunker.chunk_text(sample_doc)
    print("=== SLIDING WINDOW CHUNKS PRODUCED ===")
    for c in chunks:
        print(f"\n[Chunk #{c['chunk_index']}] ({c['word_count']} words | hash: {c['chunk_hash']}):")
        print(c["content"])

if __name__ == "__main__":
    main()
