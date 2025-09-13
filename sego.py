import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from skimage.util import random_noise
from skimage import img_as_ubyte
import cv2

# Load input image
input_image = imageio.imread(r"stegoImage.png")

# Split the image into R, G, B channels
red_channel = input_image[:, :, 0]
green_channel = input_image[:, :, 1]
blue_channel = input_image[:, :, 2]

# Get height and width for traversing through the image to embed the data
height_rc = red_channel.shape[0]
width_rc = red_channel.shape[1]

# Number of characters of the hidden text
chars = 6

# Number of bits in the message
message_length = chars * 8

# Counter to keep track of number of bits extracted
counter = 1

ipG, jpG, ipB, jpB = 0, 0, 0, 0

# Extract bits
extracted_bits = []

# Traverse through the image
for irC in range(height_rc):
    for jrC in range(width_rc):
        # If more bits remain to be extracted
        if counter <= message_length:
            # Finding the Least Significant Bit of the current pixel
            LSB0 = red_channel[irC, jrC] % 2

            # Finding second LSB
            temp = red_channel[irC, jrC] % 4

            if temp == 2 or temp == 3:
                LSB1 = 1
            else:
                LSB1 = 0

            if LSB1 == 0 and LSB0 == 0:
                for i in range(ipG, ipG + 1):
                    for j in range(jpG + 1, jpG + 3):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(green_channel[i, j] % 2)
                            counter += 1
                            if jpG == 512:
                                ipG += 1
                                jpG = 0
                            else:
                                jpG += 1

                for i in range(ipB, ipB + 1):
                    for j in range(jpB + 1, jpB + 2):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(blue_channel[i, j] % 2)
                            counter += 1
                            if jpB == 512:
                                ipB += 1
                                jpB = 0
                            else:
                                jpB += 1

            if LSB1 == 1 and LSB0 == 0:
                for i in range(ipG, ipG + 1):
                    for j in range(jpG + 1, jpG + 4):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(green_channel[i, j] % 2)
                            counter += 1
                            if jpG == 512:
                                ipG += 1
                                jpG = 0
                            else:
                                jpG += 1

                for i in range(ipB, ipB + 1):
                    for j in range(jpB + 1, jpB + 3):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(blue_channel[i, j] % 2)
                            counter += 1
                            if jpB == 512:
                                ipB += 1
                                jpB = 0
                            else:
                                jpB += 1

            if LSB1 == 0 and LSB0 == 1:
                for i in range(ipG, ipG + 1):
                    for j in range(jpG + 1, jpG + 3):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(green_channel[i, j] % 2)
                            counter += 1
                            if jpG == 512:
                                ipG += 1
                                jpG = 0
                            else:
                                jpG += 1

                for i in range(ipB, ipB + 1):
                    for j in range(jpB + 1, jpB + 3):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(blue_channel[i, j] % 2)
                            counter += 1
                            if jpB == 512:
                                ipB += 1
                                jpB = 0
                            else:
                                jpB += 1

            if LSB1 == 1 and LSB0 == 1:
                for i in range(ipG, ipG + 1):
                    for j in range(jpG + 1, jpG + 4):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(green_channel[i, j] % 2)
                            counter += 1
                            if jpG == 512:
                                ipG += 1
                                jpG = 0
                            else:
                                jpG += 1

                for i in range(ipB, ipB + 1):
                    for j in range(jpB + 1, jpB + 3):
                        if counter > message_length:
                            break
                        else:
                            extracted_bits.append(blue_channel[i, j] % 2)
                            counter += 1
                            if jpB == 512:
                                ipB += 1
                                jpB = 0
                            else:
                                jpB += 1

# Convert the extracted bits to characters
bin_values = np.array([128, 64, 32, 16, 8, 4, 2, 1])
bin_matrix = np.reshape(extracted_bits, (len(extracted_bits) // 8, 8))
text_string = ''.join([chr(sum(bin_matrix[i] * bin_values)) for i in 
range(len(bin_matrix))])

# Print the hidden text
print("MESSAGE: ", text_string)

# Add Gaussian noise to the stego image
noisy_image = random_noise(input_image, mode='gaussian', var=0.01)
noisy_image = img_as_ubyte(noisy_image)

# Apply median filter to the noisy image
filtered_image = cv2.medianBlur(noisy_image, ksize=3)

# Load original image for comparison
im0 = imageio.imread(r"originalImage.png")
im1 = input_image

# Calculate PSNR and MSE between original and filtered images
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse))

def immse(img1, img2):
    return np.mean((img1 - img2) ** 2)

peaksnr_noisy = psnr(im0, noisy_image)
mse_val_noisy = immse(im0, noisy_image)

peaksnr_filtered = psnr(im0, filtered_image)
mse_val_filtered = immse(im0, filtered_image)

print("Noisy Image PSNR: ", peaksnr_noisy)
print("Noisy Image MSE: ", mse_val_noisy)
print("Filtered Image PSNR: ", peaksnr_filtered)
print("Filtered Image MSE: ", mse_val_filtered)

# Plot original and noisy images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(im0 / 255)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(noisy_image / 255)
plt.title('Noisy Image')
plt.axis('off')

# Plot noisy and filtered images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(noisy_image / 255)
plt.title('Noisy Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(filtered_image / 255)
plt.title('Filtered Image')
plt.axis('off')