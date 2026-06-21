from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import pygame
import random

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.age = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        if self.age < 1.0:
            self.age += dt

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_direction = random.uniform(20, 50)
        new_velocity_1 = self.velocity.rotate(random_direction) * 1.2
        new_velocity_2 = self.velocity.rotate(-random_direction) * 1.2
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_position_1 = self.position + new_velocity_1.normalize() * new_radius 
        new_position_2 = self.position - new_velocity_1.normalize() * new_radius
        Asteroid(new_position_1.x, new_position_1.y, new_radius).velocity = new_velocity_1
        Asteroid(new_position_2.x, new_position_2.y, new_radius).velocity = new_velocity_2

    def bounce(self, other: "Asteroid") -> None:
        if self.radius == other.radius:
             collision_normal = (other.position - self.position).normalize()
        else:
            collision_normal = (other.position - self.position).normalize() * (other.radius / self.radius)
        new_self_velocity = self.velocity.reflect(collision_normal)
        new_other_velocity = other.velocity.reflect(-collision_normal)
        self.velocity = new_self_velocity
        other.velocity = new_other_velocity
