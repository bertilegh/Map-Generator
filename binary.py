from PIL import Image
import struct

def divide_image_into_segments(image_path, output_file):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    img_gray = img.convert('L')

    # Prepare to store segment coordinates
    segments = []

    # Loop through the image in 8x8 segments
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            # Calculate the coordinates of the segment
            segment = {
                'x_start': x,
                'y_start': y,
            }
            area = img_gray.crop((x, y, x + 8, y + 8))
            pixels = list(area.getdata())
            # Count black and white pixels
            black_count = sum(1 for pixel in pixels if pixel < 128)  # Black is typically < 128 in grayscale
            white_count = sum(1 for pixel in pixels if pixel >= 128)  # White is typically >= 128 in grayscale
            # Determine majority
            segment['majority'] = 0 if black_count > white_count else 1
            segments.append(segment)

    # Write the coordinates to the output file in binary format
    with open(output_file, 'wb') as f:
        for segment in segments:
            # Pack the data as (x_start, y_start, majority) in binary format
            f.write(struct.pack('>HHB', segment['x_start'], segment['y_start'], segment['majority']))

    print(f"Segment coordinates written to {output_file} in binary format.")

# Example usage
image_path = 'map.png'  # Replace with your image path
output_file = 'segments.bin'  # Output file for segment coordinates in binary format
divide_image_into_segments(image_path, output_file)
