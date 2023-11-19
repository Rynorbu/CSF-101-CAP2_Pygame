import unittest
import pygame, random

def your_collision_function(rect1, rect2):
    return rect1.colliderect(rect2)

def create_pipe(pipe_height):
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pygame.Rect(700, random_pipe_position, 100, 500)
    top_pipe = pygame.Rect(700, random_pipe_position - 300, 100, 500)
    return bottom_pipe, top_pipe



class TestGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((576, 1024))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('Images/04B_19.TTF', 40)

    def test_game_initialization(self):
        self.assertIsNotNone(pygame.display.get_surface(), "Game did not initialize")

    def test_image_loading_and_scaling(self):
        try:
            bird_surface = pygame.image.load('Images/bluebird-downflap.png').convert_alpha()
            bird_surface = pygame.transform.scale2x(bird_surface)
            self.assertIsNotNone(bird_surface, "Image did not load or scale correctly")
        except pygame.error:
            self.fail("Image did not load or scale correctly")

    def test_event_handling(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                break
        else:
            self.fail("Space key event was not posted or handled correctly")

    def test_collision_detection(self):
        bird_surface = pygame.Surface((50, 50)) 
        bird_rect = bird_surface.get_rect(center=(100, 512))

        pipe_surface = pygame.Surface((100, 300)) 
        pipe_rect = pipe_surface.get_rect(center=(200, 500))

        pipe_rect.x = bird_rect.x

        collision_result = your_collision_function(bird_rect, pipe_rect)

        self.assertTrue(collision_result)
    
    def test_create_pipe(self):
        pipe_height = [400, 600, 800] 

        random_pipe_position = random.choice(pipe_height)

        bottom_pipe, top_pipe = create_pipe([random_pipe_position])

        expected_bottom_pipe_position = (700, random_pipe_position)
        expected_top_pipe_position = (700, random_pipe_position - 300)
        expected_top_pipe_midbottom = (
            700 + top_pipe.width // 2,
            random_pipe_position - 300 + top_pipe.height
        )

        print("Expected Bottom Pipe Position:", expected_bottom_pipe_position)
        print("Actual Bottom Pipe Position:", bottom_pipe.topleft)
        print("Expected Top Pipe Position:", expected_top_pipe_position)
        print("Actual Top Pipe Position:", top_pipe.topleft)

        self.assertEqual(bottom_pipe.topleft, expected_bottom_pipe_position,
                        "Bottom pipe position is not correct")
        self.assertEqual(top_pipe.midbottom, expected_top_pipe_midbottom,
                        "Top pipe position is not correct")
        self.assertEqual(bottom_pipe.width, 100, "Bottom pipe width is not correct")
        self.assertEqual(top_pipe.width, 100, "Top pipe width is not correct")
        self.assertEqual(bottom_pipe.height, 500, "Bottom pipe height is not correct")
        self.assertEqual(top_pipe.height, 500, "Top pipe height is not correct")
   

    def tearDown(self):
        pygame.quit()

    

if __name__ == '__main__':
    unittest.main()
