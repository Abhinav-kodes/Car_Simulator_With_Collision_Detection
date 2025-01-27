# Required imports
import pygame  # For game development functionality
import math    # For mathematical calculations (cos, sin, radians)

class Car:
    """A class representing a car that can be controlled in a 2D environment"""
    
    def __init__(self, x, y, screen_width, screen_height):
        # Initialize car position
        self.x = x  # Car's x position
        self.y = y  # Car's y position
        
        # Screen boundaries
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Movement properties
        self.speed = 0                    # Current speed of the car
        self.angle = 0                    # Current angle in degrees
        self.max_speed = 10              # Maximum forward speed
        self.acceleration = 0.1          # Rate of speed increase
        self.brake_deceleration = 0.2    # Rate of speed decrease when braking
        self.natural_deceleration = 0.05 # Natural speed decay
        self.max_rotation_speed = 3      # Maximum turning speed

    def update(self, keys):
        """
        Update car's position and rotation based on keyboard input
        Returns True if car hits screen boundary, False otherwise
        """
        # Handle forward/backward movement
        if keys[pygame.K_UP]:
            # Accelerate forward up to max_speed
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN]:
            # Brake/reverse up to half max_speed
            self.speed = max(self.speed - self.brake_deceleration, -self.max_speed/3)
        else:
            # Apply natural deceleration when no input
            self.speed = (self.speed * (1 - self.natural_deceleration) 
                          if abs(self.speed) > 0.1 else 0)

        # Calculate rotation speed based on current speed
        current_rotation_speed = self.max_rotation_speed * (abs(self.speed) / self.max_speed)

        # Handle left/right rotation
        if keys[pygame.K_LEFT]:
            if self.speed < 0:
                self.angle -= current_rotation_speed  # Rotate anti-clockwise
            else:
                self.angle += current_rotation_speed  # Rotate clockwise

        if keys[pygame.K_RIGHT]:
            if self.speed < 0:
                self.angle += current_rotation_speed  # Rotate anti-clockwise
            else:
                self.angle -= current_rotation_speed  # Rotate clockwise

        # Calculate new position using trigonometry
        new_x = self.x + self.speed * math.cos(math.radians(self.angle))
        new_y = self.y - self.speed * math.sin(math.radians(self.angle))

        # Check for screen boundary collision
        if (new_x < 0 or new_x > self.screen_width or 
            new_y < 0 or new_y > self.screen_height):
            return True  # Collision detected

        # Update position if no collision
        self.x, self.y = new_x, new_y
        return False



def main():
    """Main game loop and initialization"""
    # Initialize game window
    screen_width, screen_height = 1500, 800
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Car Simulation")
    clock = pygame.time.Clock()  # For controlling frame rate

    # Create car instance at center of screen
    car = Car(100, 650, screen_width, screen_height)
    
    # Create car visual representation
    car_surface = pygame.Surface((50, 30), pygame.SRCALPHA)  # Transparent surface
    pygame.draw.rect(car_surface, (100, 100, 100), (0, 0, 50, 30))  # Car body
    pygame.draw.rect(car_surface, (255, 255, 255), (45, 5, 5, 5))   # Right headlight
    pygame.draw.rect(car_surface, (255, 255, 255), (45, 20, 5, 5))  # Left headlight

    car_mask = pygame.mask.from_surface(car_surface)    # Create mask for collision detection

    #grass
    top_grass = pygame.image.load("imgs/grass_top_right.png").convert_alpha()
    bottom_grass = pygame.image.load("imgs/grass_bottom_right.png").convert_alpha()

    top_grass_rect1 = top_grass.get_rect()
    top_grass_rect2 = top_grass.get_rect()
    bottom_grass_rect1 = bottom_grass.get_rect()
    bottom_grass_rect2 = bottom_grass.get_rect()

    top_grass_mask = pygame.mask.from_surface(top_grass)
    bottom_grass_mask = pygame.mask.from_surface(bottom_grass)

    top_mask_img = top_grass_mask.to_surface(setcolor=(255, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
    bottom_mask_img = bottom_grass_mask.to_surface(setcolor=(255, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
    
    top_grass_rect1.topleft = (0, 200)
    top_grass_rect2.topleft = (800, 200)
    bottom_grass_rect1.topleft = (0, 400)
    bottom_grass_rect2.topleft = (800, 400)

    #reward gates
    reward_gate_1 = pygame.image.load("imgs/reward_gate_1.jpg")
    reward_gate_2 = pygame.image.load("imgs/reward_gate_2.jpg")

    #Road
    road = pygame.image.load("imgs/road.png")
    

    # Game loop
    running = True
    while running:

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Get current keyboard state
        keys = pygame.key.get_pressed()
        
        # Update car and check for boundary collision
        if car.update(keys):
            pygame.quit()
            return

        # Render frame
        screen.fill((255, 255, 0))  # White background
        #road
        pygame.draw.lines(screen, (0,0,0), True, [(0,100), (1500,100), (1500,700), (0,700)], 1)

        screen.blit(road, (0, 100))

        screen.blit(top_grass, (0, 200))
        screen.blit(bottom_grass, (0, 400))
        screen.blit(top_grass, (800, 200))
        screen.blit(bottom_grass, (800, 400))

        #reward gates
        # Starting position
        start_x_1= 170
        start_x_2= 200
        start_y_1 = 610
        num_positions = 20
        coordinates1 = []
        coordinates2 = []
        for i in range(num_positions):
            reward_gate_1_x = start_x_1 + (i * 72)
            coordinates1.append((reward_gate_1_x, start_y_1))
            screen.blit(reward_gate_1, coordinates1[i] )

            reward_gate_2_x = start_x_2 + (i * 72)
            coordinates2.append((reward_gate_2_x, start_y_1))
            screen.blit(reward_gate_2, coordinates2[i] )
            
        
       
        rotated_car = pygame.transform.rotate(car_surface, car.angle)
        rect = rotated_car.get_rect(center=(car.x, car.y))
        car_mask = pygame.mask.from_surface(rotated_car)  # This mask is used for collision detection

        # For visualization only (if you want to see the mask)
        car_mask_img = car_mask.to_surface(setcolor=(100, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
        screen.blit(rotated_car, rect.topleft)

        if (rect.clipline((0,100), (1500,100)) != ()) | (rect.clipline((0,700), (1500,700)) != ()) :
            print("Collision Detected")
            pygame.quit()
            return
        
        if top_grass_mask.overlap(car_mask, (rect.topleft[0] - top_grass_rect1.topleft[0], rect.topleft[1] - top_grass_rect1.topleft[1])):
            print("Collision Detected")
            pygame.quit()
            return
        
        if top_grass_mask.overlap(car_mask, (rect.topleft[0] - top_grass_rect2.topleft[0], rect.topleft[1] - top_grass_rect2.topleft[1])):   
            print("Collision Detected")
            pygame.quit()
            return
        
        if bottom_grass_mask.overlap(car_mask, (rect.topleft[0] - bottom_grass_rect1.topleft[0], rect.topleft[1] - bottom_grass_rect1.topleft[1])):
            print("Collision Detected")
            pygame.quit()
            return
        
        if bottom_grass_mask.overlap(car_mask, (rect.topleft[0] - bottom_grass_rect2.topleft[0], rect.topleft[1] - bottom_grass_rect2.topleft[1])):
            print("Collision Detected")
            pygame.quit()
            return
        
        # Update display and maintain 60 FPS
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run the game if this file is run directly
if __name__ == "__main__":
    main()