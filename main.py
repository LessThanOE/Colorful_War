import pygame
import sys
from game import Game
from setting import *
from character import Character
from button import CharaButton, TextButton, ProfileButton
from tower import Tower, HealthBar
from random import randint, choice


class Main:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Colorful War")
        self.clock = pygame.time.Clock()
        self.textfont = pygame.font.Font("Font/monogram-extended.ttf", 48)
        self.captionfont = pygame.font.Font("Font/monogram-extended.ttf", 144)

        self.view = "menu"

        # text display settings
        self.caption_surf = self.captionfont.render("Colorful War", False, "black")
        self.caption_rect = self.caption_surf.get_rect(center=(640, 150))

        self.highscore = 0
        self.highscore_surf = self.textfont.render(
            f"High Score: {self.highscore}", False, "black"
        )
        self.highscore_rect = self.highscore_surf.get_rect(center=(640, 300))

        # button settings
        self.startbutton = TextButton("START", 640, 400)
        self.profilebutton = TextButton("PROFILE", 640, 500)
        self.backbutton = TextButton("FINISH", 640, 600)

        # player settings
        self.team_list = []
        self.team_is_full = False

        # profile settings
        self.charabutton = {}
        self.chara_unlock = [
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
        ]
        for i in range(0, 9):
            self.charabutton[i] = ProfileButton(self.chara_unlock[i], i)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("white")
            if self.view == "menu":
                # Menu display
                pygame.draw.line(
                    self.screen,
                    "gray",
                    (0, horizon_y + 100),
                    (WIDTH, horizon_y + 100),
                    3,
                )
                self.screen.blit(self.highscore_surf, self.highscore_rect)
                self.screen.blit(self.caption_surf, self.caption_rect)

                if self.startbutton.draw(self.screen):
                    game = Game(self.team_list)
                    gamescore = game.run()
                    if gamescore > self.highscore:
                        self.highscore = gamescore
                    self.highscore_surf = self.textfont.render(
                        f"High Score: {self.highscore}", False, "black"
                    )
                    self.highscore_rect = self.highscore_surf.get_rect(
                        center=(640, 300)
                    )

                if self.profilebutton.draw(self.screen):
                    self.view = "profile"

            elif self.view == "profile":
                if self.team_list.count("Unknown") > 0:
                    self.team_list.remove("Unknown")
                for i in range(0, 9):
                    name = chara_list[i]
                    selected = self.charabutton[i].update(
                        self.screen, self.team_is_full
                    )
                    if selected and self.team_list.count(name) == 0:
                        self.team_list.append(name)
                    if not selected and self.team_list.count(name) > 0:
                        self.team_list.remove(name)

                    if len(self.team_list) >= 5:
                        self.team_is_full = True
                    else:
                        self.team_is_full = False

                if self.backbutton.draw(self.screen):
                    while len(self.team_list) <= 5:
                        self.team_list.append("Unknown")
                    self.view = "menu"

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    main = Main()
    main.run()
