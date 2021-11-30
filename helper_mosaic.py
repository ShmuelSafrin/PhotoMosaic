from PIL import Image
import mosaic

def compare_tuples(tupl1, tupl2):
    """ add function by me for the function ahead -> get_best_tiles """
    return abs(tupl1[0] - tupl2[0]) + abs(tupl1[1] - tupl2[1]) + abs(tupl1[2] - tupl2[2])




def compare_pixel(pixel1, pixel2):
    return abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1]) + abs(pixel1[2] - pixel2[2])



def compare(image1, image2):
    """"  geting the 2  images as a list of lists  """
    # image1 = mosaic.load_image(image1)
    # image2 = mosaic.load_image(image2)
    height = min((len(image1), len(image2)))
    width = min(len(image1[0]), len(image2[0]))
    distance = 0
    for i in range(height):
        for j in range(width):
            distance += compare_pixel(image1[i][j], image2[i][j])
    return distance


def get_piece(image, upper_left, size):
    """ ARGS:
    image = The picture which the piece taken from(list of lists(of tuples)),
    upper_left = pixel(row, column) to start
    taken from,
    size = pixel(height, width) the amount pixels to  take
    RETURN:
         piece: The desired piece (as list of lists).
         If the desired size exceeds the image limits ,
            only the part of the original image is returned."""
    try:
        row_end = upper_left[0] + size[0]
    except IndexError:
        row_end = len(image)

    try:
        column_end = upper_left[1] + size[1]
    except IndexError:
        column_end = len(image[0])

    piece = image[upper_left[0]:row_end]
    print(piece)
    for i, row in enumerate(piece):
        piece[i] = piece[i][upper_left[1]:column_end]
    return piece

def set_piece(image, upper_left, piece):
    """
        Sets a tile within an image.

        Args:
            image(list): Picture (as list of lists) witch the piece will set in.
            upper_left(tuple): The location (row,column) of the upper-left piece's pixel.
            piece(list): The piece to be placed (as list of lists).
        """
    for i in range(len(piece)):
        try:
            current_row = image[i + upper_left[0]]
            for j in range(len(piece[i])):
                try:
                    current_row[j + upper_left[1]] = piece[i][j]
                except IndexError:
                    break
        except IndexError:
            break

def average(image):
    """ image is a lists of lists """
    r, g, b = 0, 0, 0
    width, height = len(image[0]), len(image)
    for i in range(height):
        for j in range(width):
            r += image[i][j][0]
            g += image[i][j][1]
            b += image[i][j][2]
    r /= width * height
    g /= width * height
    b /= width * height
    return r, g, b



def preprocess_tiles(tiles):
    """ for each image in the folder this function returns a tuple of the average (R, G, B) """
    return [average(tile) for tile in tiles]

def get_best_tiles(objective, tiles, averages, num_candidates):
    """ return the num_candidates tiles(list of lists) by comparing the object picture general average R,G,B
    to the most fit general averages tiles R,G,B """
    objective_average = average(objective)
    best_indices = []
    for i in range(num_candidates):
        best_index = 0
        while best_index in best_indices:
            best_index += 1
        for tile_index, tile_average in enumerate(averages):
            if tile_index in best_indices:
                continue
            if compare_pixel(tile_average, objective_average) < \
                    compare_pixel(averages[best_index], objective_average):
                best_index = tile_index
        best_indices.append(best_index)
    best_tiles = [tiles[i] for i in best_indices]
    return best_tiles






def choose_tile(piece, tiles):
    """
       Selects the appropriate tile from the list of candidates by comparing the pixels.

       Args:
           piece(list): The image segment to be replaced (as list of lists).
           tiles(list): List of candidates tiles

       Returns:
           The most suitable tile (as list of lists).
       """
    selected_tile = tiles[0]
    current_compare = compare(selected_tile, piece)
    switch = False
    for tile in tiles:
        if switch:
            current_compare, switch = compare(selected_tile, piece), False
        if compare(tile, piece) < current_compare:
            selected_tile, switch = tile, True
    return selected_tile


def make_mosaic(image, tiles, num_candidates):
    """
       Turns an image to a mosaic image.

       Args:
           image: The image that becomes a mosaic (as list of lists).
           tiles: List of tiles (as list of lists).
           num_candidates(int): The desired number of tiles in the list of candidates.
       """

    # tiles[0] = first picture in the folder of the tiles -> len(tiles[0]) = the len of the rows
    # tiles[0][0] = first row in the first picture -> len(tiles[0][0]) = the len of the columns
    image_size, tiles_size = (len(image), len(image[0])), (len(tiles[0]), len(tiles[0][0]))
    current_pixel = [0, 0]
    tiles_averages = preprocess_tiles(tiles)
    while current_pixel[0] < image_size[0]:
        current_pixel[1] = 0
        while current_pixel[1] < image_size[1]:
            pixel = tuple(current_pixel)
            piece = get_piece(image, pixel, tiles_size)
            candidates_tiles = get_best_tiles(piece, tiles, tiles_averages, num_candidates)
            set_piece(image, pixel, choose_tile(piece, candidates_tiles))
            current_pixel[1] += tiles_size[1]
        current_pixel[0] += tiles_size[0]




