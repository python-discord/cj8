from .fstree.FileStructureTree import FileStructureTree
from .resources.entities.level.Level import Level


class LevelSelector:
    """Creates and stores levels"""

    def __init__(self, fsf: FileStructureTree):
        self.file_structure = fsf
        self.cur = self.file_structure.root
        self.levels = {}

    def create_level(self, door: (int, int) = (0, 0)) -> Level:
        """Creates a Level"""
        if door != (0, 0):
            # get the level that the player entered the door from
            level = self.levels[id(self.cur)]
            level.parent_door = door
            # get the node of the level the player just entered
            self.cur = level.doors[door]

            if id(self.cur) in self.levels.keys():

                level = self.levels[id(self.cur)]
                exit = level.parent_door
                level.entrance = exit
                return level

        level = Level(30, 40, self.cur)
        level.generate_level()
        level.create_doors(door)
        level.spawn_random_changers()
        level.spawn_dungeon_items(num=2)
        level.spawn_random_enemies(files=self.cur.files)

        self.levels.update({id(self.cur): level})

        return level
