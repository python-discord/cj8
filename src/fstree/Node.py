from __future__ import annotations

from os import DirEntry

from rich.tree import Tree

from ..resources.entities.level.Level import Level


class Node:
    """The Node class represents a folder in the folder structure or a room in the dungeon."""

    def __init__(self, parent: Node, path: str) -> None:
        """Initialize a Node instance with a parent reference and the path to the folder instance."""
        self.parent = parent  # the folder or node which holds the current folder
        self.path = path  # the path from the root dir (e.g. ./fstree/Node.py)
        self.children: list[DirEntry] = []  # a list of folders in the current folder
        self.files: list[DirEntry] = []  # a list of files in the current folder
        self.level: Level = Level(12, 8, self.children)

    def display(self) -> None:
        """Prints the contents of the current folder. Similar to the ls command."""
        print(
            f"In {self.path}\n\tFiles: {self.files}\n\tChildren: {[c.path for c in self.children]}\n"
        )
        for child in self.children:
            child.display()

    def walk_dir(self, tree: Tree) -> None:
        """Adds the files the current directory and recursively add each folder."""
        for file in self.files:
            tree.add(file.name)
        for child in self.children:
            branch = tree.add(child.path.name)
            if child.path.name.startswith("."):
                continue
            child.walk_dir(branch)
