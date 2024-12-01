# Re-import necessary modules due to reset
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to draw a uniform grid with numbers or empty cells
def draw_uniform_grid(c, grid, page_width, page_height, cell_size=30):
    n = len(grid)  # Grid size (n x n)
    
    # Calculate starting x and y to center the grid
    grid_width = n * cell_size
    grid_height = n * cell_size
    x_start = (page_width - grid_width) / 2
    y_start = (page_height + grid_height) / 2

    # Draw the grid
    for i in range(n + 1):  # Includes outer border
        c.setLineWidth(0.5)  # Uniform line thickness
        
        # Vertical lines
        c.line(x_start + i * cell_size, y_start, x_start + i * cell_size, y_start - n * cell_size)
        # Horizontal lines
        c.line(x_start, y_start - i * cell_size, x_start + n * cell_size, y_start - i * cell_size)
    
    # Add numbers to cells
    for row_idx, row in enumerate(grid):
        for col_idx, num in enumerate(row):
            if num:  # Add only if there is a number
                x = x_start + col_idx * cell_size + 10  # Offset for text centering
                y = y_start - row_idx * cell_size - 20  # Offset for text centering
                c.drawString(x, y, str(num))

# Create a PDF with an n x n uniform grid
def create_uniform_grid_pdf(grid, filename="uniform_grid.pdf", cell_size=30):
    c = canvas.Canvas(filename, pagesize=letter)
    page_width, page_height = letter
    
    draw_uniform_grid(c, grid, page_width, page_height, cell_size)
    
    c.save()

# Example grid (5x5 with numbers and empty cells)
example_grid = [
    [1, 0, 3, 0, 5],
    [0, 0, 0, 0, 0],
    [7, 8, 0, 10, 11],
    [0, 0, 0, 0, 0],
    [13, 0, 15, 0, 17]
]

# Generate the uniform grid PDF
output_uniform_grid_path = "/mnt/data/uniform_grid.pdf"
create_uniform_grid_pdf(example_grid, output_uniform_grid_path)
output_uniform_grid_path
