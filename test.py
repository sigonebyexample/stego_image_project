import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt

def plot_hidden_data(input_image_path):
    # Load input image
    input_image = imageio.imread(input_image_path)
    
    # Check if image has RGB channels
    if len(input_image.shape) != 3 or input_image.shape[2] < 3:
        raise ValueError("Image must have RGB channels")
    
    # Split the image into R, G, B channels
    red_channel = input_image[:, :, 0]
    green_channel = input_image[:, :, 1]
    blue_channel = input_image[:, :, 2]

    height, width = red_channel.shape

    # Extract LSBs from all pixels
    hidden_data = []
    
    for i in range(height):
        for j in range(width):
            # Extract LSB (Least Significant Bit) from each color channel
            red_lsb = red_channel[i, j] % 2
            green_lsb = green_channel[i, j] % 2
            blue_lsb = blue_channel[i, j] % 2
            
            hidden_data.append([red_lsb, green_lsb, blue_lsb])

    # Convert to numpy array for easier manipulation
    hidden_data = np.array(hidden_data)
    
    # Display the original image and extracted LSB patterns
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Original image
    axes[0, 0].imshow(input_image)
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis('off')
    
    # Red channel with LSB markers
    axes[0, 1].imshow(red_channel, cmap='Reds')
    axes[0, 1].set_title("Red Channel with LSB Markers")
    axes[0, 1].axis('off')
    
    # Mark pixels where LSB might contain hidden data
    # Create a mask for pixels with non-zero LSB values
    lsb_mask = np.zeros_like(red_channel, dtype=bool)
    
    for i in range(height):
        for j in range(width):
            if (red_channel[i, j] % 2 != 0 or 
                green_channel[i, j] % 2 != 0 or 
                blue_channel[i, j] % 2 != 0):
                lsb_mask[i, j] = True
    
    # Plot the mask
    axes[1, 0].imshow(lsb_mask, cmap='gray')
    axes[1, 0].set_title("Pixels with Non-zero LSB (Potential Hidden Data)")
    axes[1, 0].axis('off')
    
    # Show LSB values as text (first 20 pixels)
    sample_text = "First 20 pixels LSB values (R,G,B):\n"
    for idx in range(min(20, len(hidden_data))):
        sample_text += f"{hidden_data[idx]} "
    
    axes[1, 1].text(0.1, 0.5, sample_text, fontsize=9, 
                   verticalalignment='center', transform=axes[1, 1].transAxes)
    axes[1, 1].set_title("Extracted LSB Values")
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Print some statistics
    total_pixels = height * width
    pixels_with_lsb = np.sum(lsb_mask)
    print(f"Total pixels: {total_pixels}")
    print(f"Pixels with non-zero LSB: {pixels_with_lsb}")
    print(f"Percentage with potential hidden data: {pixels_with_lsb/total_pixels*100:.2f}%")
    
    return hidden_data

def decode_message_from_lsb(hidden_data, bin_values=[4, 2, 1]):
    """
    Attempt to decode message from LSB data
    bin_values: weights for converting bits to decimal (default: [4,2,1] for 3 bits)
    """
    decoded_chars = []
    
    for bits in hidden_data:
        # Convert 3 bits to decimal value
        decimal_value = sum(bits * bin_values)
        
        # Only consider printable ASCII characters (32-126)
        if 32 <= decimal_value <= 126:
            decoded_chars.append(chr(decimal_value))
        else:
            decoded_chars.append('?')  # Placeholder for non-printable
    
    decoded_message = ''.join(decoded_chars)
    
    # Try to find meaningful text
    words = decoded_message.split()
    potential_text = ' '.join([word for word in words if len(word) > 1])
    
    return decoded_message, potential_text

if __name__ == "__main__":
    input_image_path = "stegoImage.png"
    
    try:
        hidden_data = plot_hidden_data(input_image_path)
        
        # Try to decode potential message
        full_message, potential_text = decode_message_from_lsb(hidden_data)
        
        print("\n" + "="*50)
        print("DECODING ATTEMPT:")
        print("="*50)
        print("Full extracted data (first 200 chars):")
        print(full_message[:200])
        
        print("\nPotential meaningful text found:")
        print(potential_text[:500])
        
    except FileNotFoundError:
        print(f"Error: File '{input_image_path}' not found!")
        print("Please make sure the image file exists in the current directory.")
    except Exception as e:
        print(f"Error: {e}")