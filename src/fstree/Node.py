from __future__ import annotations


class Node:
    """The Node class represents a folder in the folder structure or a room in the dungeon."""

    def __init__(self, parent: Node, path: str) -> None:
        """Initialize a Node instance with a parent reference and the path to the folder instance."""
        self.parent = parent  # the folder or node which holds the current folder
        self.path = path  # the path from the root dir (e.g. ./fstree/Node.py)
        self.children = []  # a list of folders in the current folder
        self.files = []  # a list of files in the current folder

    def display(self) -> None:
        """Prints the contents of the current folder. Similar to the ls command."""
        print(
            f"In {self.path}\n\tFiles: {self.files}\n\tChildren: {[c.path for c in self.children]}\n"
        )
        for child in self.children:
            child.display()
