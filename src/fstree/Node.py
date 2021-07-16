from __future__ import annotations

import os
from os import DirEntry, fspath

from rich.text import Text
from rich.tree import Tree


class Node:
    """The Node class represents a folder in the folder structure or a room in the dungeon."""

    def __init__(self, parent: Node, path: str) -> None:
        """Initialize a Node instance with a parent reference and the path to the folder instance."""
        self.parent = parent  # the folder or node which holds the current folder
        self.path = path  # the path from the root dir (e.g. ./fstree/Node.py)
        self.children: list[DirEntry] = []  # a list of folders in the current folder
        self.files: list[DirEntry] = []  # a list of files in the current folder
        self.depth = fspath(self.path).count("\\") if os.name == "nt" else fspath(self.path).count("/")

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

    def display_node(self) -> None:
        """Displays current location in directory"""
        if not isinstance(self.path, str):
            path = self.path.name
        else:
            path = self.path

        if self.parent is not None:
            if not isinstance(self.parent.path, str):
                parent_path = self.parent.path.name
            else:
                parent_path = self.parent.path
            tree = Tree(parent_path, style="bold yellow")
        else:
            tree = Tree(Text(path, style="bold yellow"))

        # checks if the path is not a string and rather an os.DirEntry

        if self.parent is not None:
            for child in self.parent.children:
                if child.path is not self.path:
                    tree.add(Text(child.path.name, style="bold yellow"))

        branch = Tree(path)
        for child in self.children:
            branch.add(Text(child.path.name, style="bold green"))

        for file in self.files:
            tree.add(Text(file.name, style="bold red"))

        tree.add(branch)

        return tree
