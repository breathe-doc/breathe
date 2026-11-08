from __future__ import annotations

from types import SimpleNamespace

from breathe import file_state_cache


def test_merge_info():
    """The state of a parallel reader process is merged for the documents it read."""
    env = SimpleNamespace(breathe_file_state={"a.xml": (1.0, {"doc0"}), "b.xml": (1.0, {"doc0"})})
    # A reader process starts from a copy of the main state and records the documents it reads.
    other = SimpleNamespace(
        breathe_file_state={
            "a.xml": (2.0, {"doc0", "doc1"}),
            "b.xml": (1.0, {"doc0"}),
            "c.xml": (3.0, {"doc1", "doc2"}),
        }
    )

    file_state_cache._merge_info(None, env, {"doc1"}, other)

    assert env.breathe_file_state == {
        # Documents are added to those already recorded, with the latest modification time.
        "a.xml": (2.0, {"doc0", "doc1"}),
        # Files not read by the process are unchanged.
        "b.xml": (1.0, {"doc0"}),
        # Only the documents read by the process are merged.
        "c.xml": (3.0, {"doc1"}),
    }


def test_merge_info_without_state():
    """Merging works when neither environment has recorded state yet."""
    env = SimpleNamespace()
    file_state_cache._merge_info(None, env, {"doc0"}, SimpleNamespace())
    assert not hasattr(env, "breathe_file_state")

    other = SimpleNamespace(breathe_file_state={"a.xml": (1.0, {"doc0"})})
    file_state_cache._merge_info(None, env, {"doc0"}, other)
    assert env.breathe_file_state == {"a.xml": (1.0, {"doc0"})}
