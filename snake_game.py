import pygame
import random

pygame.init()
pygame.mixer.init()

# ---------------- FOOD SOUND ----------------

food_sound = pygame.mixer.Sound("food.mp3")
food_sound.set_volume(0.5)


# ---------------- APPLE IMAGE ----------------

apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (20, 20))


# ---------------- PYGAME COMPONENTS ----------------

clock = pygame.time.Clock()

font = pygame.font.Font(None, 26)

screen = pygame.display.set_mode((600, 400))

pygame.display.set_caption("SnakeRush")


# ---------------- GAME VARIABLES ----------------

snake_x = 300
snake_y = 200

snake_speed = 5

score = 0
high_score = 0

snake_length = 1
snake_body = [(snake_x, snake_y)]

grow_snake = False

moved = False

# Snake starting direction
direction = "RIGHT"


# ---------------- FOOD ----------------

food_x = random.randrange(0, 600, 20)
food_y = random.randrange(0, 400, 20)


# ---------------- GAME STATES ----------------

running = True
game_over = False
game_started = False


# ==================================================
#                 START SCREEN
# ==================================================

while not game_started:

    # Light green background
    screen.fill((220, 245, 220))

    welcome_text = pygame.font.Font(None, 50).render(
        "Welcome To SNAKERUSH",
        True,
        (0, 0, 0)
    )

    start_text = pygame.font.Font(None, 30).render(
        "Press SPACE to Start",
        True,
        (0, 0, 0)
    )

    screen.blit(welcome_text, (120, 130))
    screen.blit(start_text, (190, 200))

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                game_started = True


# ==================================================
#                 MAIN GAME
# ==================================================

while True:

    # ---------------- GAME LOOP ----------------

    while running:

        # ---------------- EVENTS ----------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                game_over = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    direction = "RIGHT"

                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"

                elif event.key == pygame.K_UP:
                    direction = "UP"

                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"


        # ---------------- SNAKE MOVEMENT ----------------

        if direction == "RIGHT":
            snake_x += snake_speed

        elif direction == "LEFT":
            snake_x -= snake_speed

        elif direction == "UP":
            snake_y -= snake_speed

        elif direction == "DOWN":
            snake_y += snake_speed

        moved = True


        # ---------------- SCREEN ----------------

        # Light green background
        screen.fill((220, 245, 220))


        # ---------------- RECTANGLES ----------------

        snake_rect = pygame.Rect(
            snake_x,
            snake_y,
            20,
            20
        )

        food_rect = pygame.Rect(
            food_x,
            food_y,
            20,
            20
        )


        # ---------------- FOOD COLLISION ----------------

        if snake_rect.colliderect(food_rect):

            score += 1

            snake_length += 1

            grow_snake = True

            # Play food sound
            food_sound.play()

            # High score
            if score > high_score:
                high_score = score

            # New food position
            food_x = random.randrange(0, 600, 20)
            food_y = random.randrange(0, 400, 20)


        # ---------------- WALL COLLISION ----------------

        if (
            snake_x < 0
            or snake_x > 580
            or snake_y < 0
            or snake_y > 380
        ):

            game_over = True
            running = False


        # ---------------- UPDATE SNAKE BODY ----------------

        if moved:

            snake_body.insert(
                0,
                (snake_x, snake_y)
            )

            if grow_snake:

                grow_snake = False

            else:

                if len(snake_body) > snake_length:
                    snake_body.pop()

            moved = False


        # ---------------- SELF COLLISION ----------------

        if (snake_x, snake_y) in snake_body[1:]:

            game_over = True
            running = False


        # ==================================================
        #                 DRAW SNAKE
        # ==================================================

        for block in snake_body:

            pygame.draw.rect(
                screen,
                (0, 0, 255),
                (
                    block[0],
                    block[1],
                    20,
                    20
                )
            )


        # ---------------- DRAW APPLE ----------------

        screen.blit(
            apple_image,
            (food_x, food_y)
        )


        # ---------------- SCORE ----------------

        score_text = font.render(
            f"Score: {score}",
            True,
            (0, 0, 0)
        )

        screen.blit(
            score_text,
            (10, 10)
        )


        # ---------------- HIGH SCORE ----------------

        high_score_text = font.render(
            f"High Score: {high_score}",
            True,
            (0, 0, 0)
        )

        screen.blit(
            high_score_text,
            (10, 35)
        )


        # ---------------- UPDATE DISPLAY ----------------

        pygame.display.update()

        clock.tick(10)


    # ==================================================
    #                 GAME OVER SCREEN
    # ==================================================

    while game_over:

        # Same light green background
        screen.fill((220, 245, 220))

        game_over_text = pygame.font.Font(
            None,
            50
        ).render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        score_text = pygame.font.Font(
            None,
            28
        ).render(
            f"Final Score: {score}",
            True,
            (0, 0, 0)
        )

        restart_text = pygame.font.Font(
            None,
            28
        ).render(
            "Press R to Restart",
            True,
            (0, 0, 0)
        )

        screen.blit(
            game_over_text,
            (210, 120)
        )

        screen.blit(
            score_text,
            (235, 180)
        )

        screen.blit(
            restart_text,
            (205, 230)
        )

        pygame.display.update()


        # ---------------- GAME OVER EVENTS ----------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                game_over = False
                running = False


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    # Reset snake
                    snake_x = 300
                    snake_y = 200

                    snake_body = [
                        (snake_x, snake_y)
                    ]

                    snake_length = 1

                    # Reset score
                    score = 0

                    # Reset direction
                    direction = "RIGHT"

                    # Reset growth
                    grow_snake = False

                    moved = False

                    # New food
                    food_x = random.randrange(
                        0, 600, 20
                    )

                    food_y = random.randrange(
                        0, 400, 20
                    )

                    # Start game again
                    game_over = False
                    running = True


        clock.tick(10)


    # ---------------- CLOSE GAME ----------------

    if not game_over and not running:
        break


pygame.quit()