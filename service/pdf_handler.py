import os
from PIL import Image
from reportlab.pdfgen import canvas # type: ignore
from reportlab.lib.units import inch # type: ignore

def get_images_sorted_by_creation(directory):
    """
    Get a list of image files in the given directory, sorted by creation date.
    
    Args:
    directory (str): Path to the directory containing images.
    
    Returns:
    list: Sorted list of image file paths.
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')
    image_files = [
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.lower().endswith(image_extensions)
    ]
    return sorted(image_files, key=os.path.getctime)


def save_images_to_pdf(directory, output_pdf='output.pdf'):
    """
    Save all images in the given directory to a single PDF file.
    
    Args:
    directory (str): Path to the directory containing images.
    output_pdf (str): Name of the output PDF file. Defaults to 'output.pdf'.
    
    Returns:
    str: Path to the created PDF file.
    """
    image_files = get_images_sorted_by_creation(directory)
    
    if not image_files:
        print(f"No image files found in {directory}")
        return None
    
    c = canvas.Canvas(output_pdf)
    
    for img_path in image_files:
        img = Image.open(img_path)
        width, height = img.size
        
        # Adjust page size to match image size
        c.setPageSize((width, height))
        
        c.drawImage(img_path, 0, 0, width, height)
        c.showPage()
    
    c.save()
    return output_pdf


def append_images_to_pdf(directory, existing_pdf):
    """
    Append images from the given directory to an existing PDF file.
    
    Args:
    directory (str): Path to the directory containing images.
    existing_pdf (str): Path to the existing PDF file.
    
    Returns:
    str: Path to the updated PDF file.
    """
    image_files = get_images_sorted_by_creation(directory)
    
    if not image_files:
        print(f"No image files found in {directory}")
        return existing_pdf
    
    c = canvas.Canvas(existing_pdf)
    
    for img_path in image_files:
        img = Image.open(img_path)
        width, height = img.size
        
        # Adjust page size to match image size
        c.setPageSize((width, height))
        
        c.drawImage(img_path, 0, 0, width, height)
        c.showPage()
    
    c.save()
    return existing_pdf
