from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

DEFAULT_URL = "https://app-texaspokerapp.com"
DEFAULT_KEYWORDS = ["德州扑克app", "online poker", "texas holdem", "mobile game"]


@dataclass
class KeywordNote:
    """Represents a single keyword note with metadata."""
    keyword: str
    note: str
    url: str = DEFAULT_URL
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def formatted_entry(self, include_timestamp: bool = True) -> str:
        """Return a formatted string representation of the note."""
        lines = [
            f"Keyword: {self.keyword}",
            f"Note:    {self.note}",
            f"URL:     {self.url}",
        ]
        if self.tags:
            tags_str = ", ".join(f"#{tag}" for tag in self.tags)
            lines.append(f"Tags:    {tags_str}")
        if include_timestamp:
            lines.append(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)


@dataclass
class KeywordNotesCollection:
    """A collection of keyword notes with formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, keyword: str, note: str, tags: Optional[List[str]] = None) -> KeywordNote:
        """Create and add a new note to the collection."""
        new_note = KeywordNote(keyword=keyword, note=note, tags=tags or [])
        self.notes.append(new_note)
        return new_note

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return all notes matching the given keyword (case-insensitive)."""
        return [n for n in self.notes if n.keyword.lower() == keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        """Return all notes that have the specified tag."""
        return [n for n in self.notes if tag.lower() in (t.lower() for t in n.tags)]

    def format_all(self) -> str:
        """Return a string containing all notes formatted with a delimiter."""
        if not self.notes:
            return "No notes in collection."
        parts = []
        for idx, note in enumerate(self.notes, start=1):
            header = f"--- Note #{idx} ---"
            body = note.formatted_entry()
            parts.append(f"{header}\n{body}")
        return "\n\n".join(parts)

    def summary(self) -> str:
        """Return a one-line summary of the collection."""
        total = len(self.notes)
        unique_keywords = len(set(n.keyword for n in self.notes))
        return f"Collection: {total} note(s) across {unique_keywords} keyword(s)"


def build_demo_collection() -> KeywordNotesCollection:
    """Create a demo collection with sample notes based on default data."""
    collection = KeywordNotesCollection()

    collection.add_note(
        keyword="德州扑克app",
        note="一款流行的移动端德州扑克游戏，支持多人在线对战。",
        tags=["poker", "mobile", "game"],
    )

    collection.add_note(
        keyword="online poker",
        note="Online poker platforms provide real-time multiplayer experiences.",
        tags=["poker", "online"],
    )

    collection.add_note(
        keyword="texas holdem",
        note="Texas Hold'em is the most popular variant of poker in casinos and online.",
    )

    collection.add_note(
        keyword="mobile game",
        note="Mobile gaming continues to grow, with poker apps being a key category.",
        tags=["mobile", "gaming"],
    )

    return collection


if __name__ == "__main__":
    demo = build_demo_collection()
    print(demo.summary())
    print()
    print(demo.format_all())
    print()
    print("--- Searching for '德州扑克app' ---")
    for note in demo.find_by_keyword("德州扑克app"):
        print(note.formatted_entry(include_timestamp=False))
    print()
    print("--- Notes tagged with 'mobile' ---")
    for note in demo.find_by_tag("mobile"):
        print(note.formatted_entry())