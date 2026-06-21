import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scorekeeper import Scorekeeper



def main():
    pygame.init()
    pygame.font.init()
    
    score_font = pygame.font.Font(None, 36)
    game_over_font_1 = pygame.font.Font(None, 72)
    game_over_font_2 = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    dt = 0.0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    game_over = False

    while True:
        while not game_over:
            log_state()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            screen.fill("black")
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    log_event("player_hit")
                    print("Game over!")
                    print(f"Final score: {int(Scorekeeper.get_score())}")
                    game_over = True
                    break
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
            for i in range(len(asteroids)):
                for j in range(i + 1, len(asteroids)):
                    if asteroids.sprites()[i].collides_with(asteroids.sprites()[j]):
                        asteroids.sprites()[i].bounce(asteroids.sprites()[j])
            updatable.update(dt)
            score_text = score_font.render(f"Score: {int(Scorekeeper.get_score())}", True, "white")
            screen.blit(score_text, (10, 10))
            for sprite in drawable:
                sprite.draw(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        
        while game_over:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    updatable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    asteroid_field = AsteroidField()
                    Scorekeeper.reset_score()
                    log_event("game_restart")
                    game_over = False

            game_over_text = game_over_font_1.render("Game Over", True, "white")
            final_score_text = game_over_font_2.render(f"Final Score: {int(Scorekeeper.get_score())}", True, "white")
            
            screen.blit(game_over_text,
                         (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                           SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            screen.blit(final_score_text,
                         (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2,
                           SCREEN_HEIGHT // 2 + game_over_text.get_height()))
            
            restart_text = game_over_font_2.render("Press any key to restart", True, "white")
            screen.blit(restart_text,
                         (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                           SCREEN_HEIGHT // 2 + game_over_text.get_height() + final_score_text.get_height()))
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()
