from os import scandir

from src.fstree.Node import Node


class FileStructureTree:
    """The FileSystemTree class represents the folder structure used to create the dungeon."""

    def __init__(self, path: str) -> None:
        """An FileSystemTree instance is created by passing the path which will be the root of the dungeon."""
        self.root = Node(None, path)    # root node which holds references to all the other nodes in the tree
        self.add_node(self.root)

    def add_node(self, node: Node) -> None:
        """Recursively adds subfolders as nodes to the tree."""
        with scandir(node.path) as it:
            for entry in it:
                if entry.is_dir():
                    node.children.append(Node(node, entry))
                else:
                    node.files.append(entry)
        for child in node.children:
            self.add_node(child)

    def display(self) -> None:
        """Prints the entire folder structure using recursive calls to the node.display() method."""
        self.root.display()
