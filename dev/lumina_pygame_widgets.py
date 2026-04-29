import pygame


class TextField:
    """Represent field of text."""

    def __init__(self, screen, text: str, size: int, bg_color: bool | str | tuple[int, int, int] = False,
                 text_color: str | tuple[int, int, int] = "black", multi_line: bool = False, surface_width: int = 0,
                 text_pos: tuple[int, int] = (0,0)) -> None:
        """Initialize a text field on screen
        ARGS:
            screen: pygame window.
            text: string to be shown in text field.
            size: font size for text.
            bg_color: background color for rect. Default is 'False' for transparent background.
            text_color: string or RGB tuple for text color. Default is 'black'.
            multi_line: boolean to control if text is rendered in a one- or multi-line textfield. Default is 'False'.
        ARGS for use when 'multi_line=True':
            surface_width: set width for attribute 'text_surface'. Default is '0'.
            text_pos: set starting point for text in 'text_surface'. Default is '(0,0)'.
        Default position is centered on screen.
        """
        self.screen = screen
        self.screen_rect: pygame.Rect = screen.get_rect()
        self.text: str = text
        self.size: int = size
        self.bg_color: bool | str | tuple[int, int, int] = bg_color
        self.multi_line: bool = multi_line

        if text_color == "black":
            self.text_color: str | tuple[int, int, int] = "black"
        else:
            self.text_color: str | tuple[int, int, int] = text_color
        self.font: pygame.font.Font = pygame.font.Font(settings.font, self.size)

        self.padding: int = int(self.screen_rect.width / 40)

        # Get surface for mult-line text field.
        if multi_line:
            self.surface_width: int = surface_width
            self.surface_height: int = self.font.get_height()  # Starting value for use in 'render_multiline_surface()'
            self.text_pos: tuple[int, int] = text_pos
            self.text_surface: pygame.Surface = self.render_multiline_surface()
        # Get surface for standard, one-line text field.
        else:
            self.text_surface: pygame.Surface = self.font.render(self.text, True, self.text_color)

        if self.bg_color:
            self.background_rect: pygame.Rect = self.text_surface.get_rect().inflate(self.padding, self.padding)
            self.background_rect.center = self.screen_rect.center

        self.text_rect: pygame.Rect = self.text_surface.get_rect()
        self.text_rect.center = self.screen_rect.center

        # Default alpha transparency values. Not used by 'TextField' class, but can be changed and then applied using
        # '.set_alpha(self.alpha)' elsewhere to be changed to, for example, create a fade-in/fade-out effect.
        # See 'Button' and 'InteractiveText' class or methods in 'gui/credits.py' as examples.
        # NOTE: check if surface supports alpha channel (use 'pygame.SRCALPHA' argument when creating a new surface if
        # not)!
        self.fade_alpha: int = 0
        self.background_alpha: int = 255
        self.fade_speed: int = int(25 * (30 / settings.frame_rate))

    def draw_text(self) -> None:
        """Draw the text field on the screen."""
        if self.bg_color:
            self.background_rect.center = self.text_rect.center
            pygame.draw.rect(self.screen, self.bg_color, self.background_rect)

        self.screen.blit(self.text_surface, self.text_rect)

    def render_multiline_surface(self) -> pygame.Surface:
        """Render and return multi line text surface.
        The method splits the text into lines and words, renders each word using the specified font, and dynamically
        expands the surface height if a word doesn't fit the current line.
        RETURNS:
            text_surface
        """
        text_surface: pygame.Surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)

        x, y = self.text_pos
        space = self.font.size(" ")[0]
        # 2D array, each row is a list of words.
        words = [word.split(" ") for word in self.text.splitlines()]

        for line_index, line in enumerate(words, start=1):
            for word in line:
                # Render each word and check if it fits the current line.
                word_surface = self.font.render(word, True, self.text_color)
                word_width = word_surface.get_width()

                if x + word_width >= text_surface.get_width():
                    # If the word doesn't fit, create more space and move to next line.
                    text_surface, x, y = self.expand_multiline_surface(text_surface, y)

                # Draw the word and advance horizontal position.
                text_surface.blit(word_surface, (x, y))
                x += word_width + space

            # Check if we are at the last line to avoid addition of empty line at the end.
            if line_index < len(words):
                text_surface, x, y = self.expand_multiline_surface(text_surface, y)

        return text_surface

    def expand_multiline_surface(self, text_surface: pygame.Surface, y: int) -> tuple[pygame.Surface, int, int]:
        """Helper function for use in 'render_multiline_surface()' to expand 'text_surface' to accommodate new lines of
        text automatically through use of a temporary surface.
        ARGS:
            text_surface: pygame surface to be expanded for multi-line texts.
            y: current Y-position of text line.
        RETURNS:
            text_surface, x, y: new text surface and coordinates for next line.
        """
        x = self.text_pos[0]  # Reset 'x' for next line.
        y += self.font.get_height()  # Set 'y' for next line.

        # Create a temporary surface to accommodate the new line of text.
        # The new height is calculated by adding the current surface height to the font height.
        # Blit the existing text surface onto the temporary surface, then update text_surface to reference the
        # expanded surface.
        new_height = self.surface_height + self.font.get_height()
        temporary_surface = pygame.Surface((self.surface_width, new_height), pygame.SRCALPHA)
        temporary_surface.blit(text_surface, (0,0))
        text_surface = temporary_surface
        self.surface_height = new_height  # Update surface height

        return text_surface, x, y

    def render_new_text_surface(self, settings_gui: bool = False) -> None:
        """Re-render 'text_surface' attribute and get new 'text_rect'. This method is for use after an already created
        instance has its 'text' attribute changed to ensure that further changes to, for example, its position are applied
        to the modified instance.
        ARGS:
            settings_gui: argument for use when calling method 'update_text_size()' in class 'SettingsGUI' to ensure
                          screen elements in the settings screen change their text size if a new window size is selected.
                          Ignore in all other cases. Default is 'False'.
        """
        if settings_gui:
            self.font: pygame.font.Font = pygame.font.Font(settings.font, self.size)

        if self.multi_line:
            self.text_surface: pygame.Surface = self.render_multiline_surface()
        else:
            self.text_surface: pygame.Surface = self.font.render(self.text, True, self.text_color)

        self.text_rect: pygame.Rect = self.text_surface.get_rect()

    def blit_surface(self, surface: pygame.Surface, rect: pygame.Rect, color: str | tuple[int, int, int]) -> None:
        """Fill 'surface' with 'color' attribute and blit it onto the screen at 'rect'.
        ARGS:
            surface: pygame surface.
            rect: pygame rect.
            color: color attribute.
        """
        surface.fill(color)
        self.screen.blit(surface, rect)
