import cv2
import numpy as np
from sklearn.preprocessing import Normalizer
from matplotlib.colors import Normalize

# This class represents a 2D array (square or rectangle) representing a city
# Individual cells can represent any spatial area amount
class City:

    def __init__(self, city_name="test_city", width=10, height=10, 
                       magnification=5, density='uniform'):
        """
        Initialises the world and draws the world cells
        """
        # Dimensions of the city
        self.H = height * 10 * magnification
        self.W = width * 10 * magnification
        self.cell_size = 10 * magnification
        # Name of the city for image showing and saving
        self.name = city_name
        # Initialise the image as a white square
        self.density_scheme = density.lower()
        if density.lower() == 'uniform':
            self.density = np.ones((self.H, self.W)) / (self.H * self.W)
        else:
            # TODO: Implement alternative for density spread
            raise ValueError(f"Density of '{density}' not supported. Please use 'uniform' instead.")
        self.image = np.ones((self.H, self.W), dtype=np.float64)

    def draw_lines(self):
        """
        Draws the cell limitations for the city 
        """
        # Add lines for each grid cell
        for i in range(0, max(self.H, self.W), self.cell_size):
            # Get x and y coordinate of current spot - staying in the limits             
            x = min(i, self.H)
            y = min(i, self.W)
            # Draw horizontal line
            cv2.line(self.image, (0, x), (self.W, x), 0)
            # Draw vertical line
            cv2.line(self.image, (y, 0), (y, self.H), 0)
        # Draw bottom horizontal line
        cv2.line(self.image, (0, self.H-1), (self.W, self.H-1), 0)
        # Draw right vertical line 
        cv2.line(self.image, (self.W-1, 0), (self.W-1, self.H), 0)

    def update_color(self):
        """ 
        Fills in the squares of the image with it's corresponding color value based on the cmap
        """
        # Fit the normaliser on the densities color mapping
        norm = Normalize(vmin=self.density.min(), vmax=self.density.max())
        # Iterate through each grid cell position
        for x in range(0, self.H, self.cell_size):
            for y in range(0, self.W, self.cell_size):
                # Get coordinates for the cell
                delta = self.cell_size
                tl = (x, y)
                tr = (x+delta, y)
                br = (x+delta, y+delta)
                bl = (x, y+delta)
                # Fetch the appropriate density-to-cmap
                if self.density_scheme == 'uniform':
                    color = 0.5
                else:
                    color = norm(self.density[x, y])
                # Draw the square
                cv2.fillConvexPoly(self.image, np.array([tl, tr, br, bl]), color)
        # Convert to greyscale and apply a colormapping
        self.image = (self.image * 255.0).astype(np.uint8)
        self.image = cv2.applyColorMap(self.image, cv2.COLORMAP_HOT)
        # Draw lines again to cover the overlaps
        self.draw_lines()
    
    def show(self, save=False):
        """
        Blocks the program and shows the current image
        If 'q' is pressed then we break and continue
        """
        self.update_color()
        cv2.imshow(self.name, self.image)
        print("Press 'q' to continue...")
        while (1):
            if cv2.waitKey() == ord('q'):
                if save:
                    cv2.imwrite(f"../figures/{self.name}.png", self.image)
                cv2.destroyAllWindows()
                break