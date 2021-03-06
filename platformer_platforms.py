""" Platform directly from PAG with slight modifications to MovingPlatform subclass """

import pygame

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

GRASS_SINGLE          = (648, 0, 70, 70)
GRASS_LEFT            = (504, 648, 70, 70)
GRASS_RIGHT           = (504, 504, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)
STONE_SINGLE          = (792, 360, 70, 40)

STONE_TOP          = (792, 144, 70, 70)
STONE_MIDDLE       = (504, 288, 70, 70)
DIRT                  = (576, 864, 70, 70)

PURPLE_LEFT           = (70, 504, 68, 69)
PURPLE_RIGHT          = (70, 360, 68, 69)
PURPLE_MIDDLE         = (72, 433, 68, 69)
PURPLE_SINGLE         = (144, 648, 70, 70)
PURPLE_SINGLE_SMALL   = (143, 144, 70, 40)

TRACK                 = (288, 766, 23, 23)

CARPET                = (504, 0, 70, 70)

sprite_sheet = None

BOX = (0, 865, 70, 70)
BOXX = (0, 793, 70, 70)


class Platform(pygame.sprite.Sprite):
    # Platform the user can jump on #

    def __init__(self, sprite_sheet_data):
        super().__init__()

        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    # This is a fancier platform that can actually move. #
    def __init__(self, list):
        super().__init__(list)

        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        self.level = None
        self.player = None

    def update(self):
        # Move the platform.
        # If the player is in the way, it will shove the player
        # out of the way. This does NOT handle what happens if a
        # platform shoves a player into another object. Make sure
        # moving platforms have clearance to push the player around
        # or add code to handle what happens if they don't.

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        cur_pos = self.rect.bottom - self.level.shift_vert
        if cur_pos > self.boundary_bottom or cur_pos < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.shift_hori
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

# class MovingMarker(Platform):
#
#     def __init__(self):
#         super().__init__(TRACK)
