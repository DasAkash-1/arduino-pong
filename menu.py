import pygame, sys


def menu(screen, clock, font, bg, title_color, p1_color, p2_color):
    width = screen.get_width()
    height = screen.get_height()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        screen.fill(bg)

        title = font.render("PONG!!!", True, title_color)
        screen.blit(title, (width / 2 - title.get_width() / 2, 150))


        # start text blink korar
        if pygame.time.get_ticks() % 1000 < 600:
            start = font.render("Press SPACE to start", True, "white")
            screen.blit(start, (width / 2 - start.get_width() / 2, 330))


        info1 = font.render("Left: W / S", True, p1_color)
        info2 = font.render("Right: UP / DOWN", True, p2_color)
        screen.blit(info1, (width / 2 - info1.get_width() / 2, 430))
        screen.blit(info2, (width / 2 - info2.get_width() / 2, 470))

        pygame.display.update()
        
        clock.tick(60)