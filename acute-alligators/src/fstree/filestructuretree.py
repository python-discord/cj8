from os import scandir

from rich.tree import Tree

from src.fstree.node import Node


class FileStructureTree:
    """The FileSystemTree class represents the folder structure used to create the dungeon."""

    def __init__(self, path: str) -> None:
        """An FileSystemTree instance is created by passing the path which will be the root of the dungeon."""
        self.root = Node(
            None, path
        )
        self.depth = 0
        self.add_node(self.root)

    def add_node(self, node: Node) -> None:
        """Recursively adds subfolders as nodes to the tree."""
        with scandir(node.path) as it:
            for entry in it:
                if entry.name.startswith('.') or entry.name.startswith('__'):
                    continue
                if entry.is_dir():
                    if len(node.children) > 50:
                        pass
                    else:
                        node.children.append(Node(node, entry))
                else:
                    node.files.append(entry)
        for child in node.children:
            self.add_node(child)
            if child.depth > self.depth:
                self.depth = child.depth

    def display(self) -> None:
        """Prints the entire folder structure using recursive calls to the node.display() method."""
        self.root.display()

    def tree(self) -> None:
        """Creates the tree visualization of the folder structure."""
        tree = Tree(self.root.path)
        self.root.walk_dir(tree)
