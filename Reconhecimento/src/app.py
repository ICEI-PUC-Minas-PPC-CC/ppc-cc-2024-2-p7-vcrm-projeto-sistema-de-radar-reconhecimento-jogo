
import os
import cv2
import csv
from paddleocr import PaddleOCR
from lib.filters import get_grayscale
from lib.format_output import format_output


def apply_filter(plate):
    # Convert to grayscale
    gray = get_grayscale(plate)
    # Apply OTSU thresholding for binary segmentation
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def resize_image(image, scale_percent=150):
    # Resize the image moderately to enhance OCR
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)


def correct_characters(plate_number):
    corrections = {
        'I': '1',
        'L': '1',
        'O': '0',
        'S': '5',
        'Z': '2',
        'E': '3',
        'B': '8',
    }
    return ''.join(corrections.get(c, c) for c in plate_number)


from paddleocr import PaddleOCR

def scan_plate_with_paddleocr(image):
    # Inicializa o OCR com uso da CPU
    ocr = PaddleOCR(use_gpu=False, lang='en')  # Força o uso da CPU
    results = ocr.ocr(image, cls=True)

    # Processa os resultados
    if results and len(results[0]) > 0:
        plate_number = ''.join(filter(str.isalnum, results[0][0][1][0]))  # Limpa caracteres especiais
        return plate_number[:8]  # Garante até 8 caracteres
    return "UNKNOWN"


def debug_save_image(step_name, image, output_dir="debug_steps"):
    # Save intermediate images for debugging
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cv2.imwrite(os.path.join(output_dir, f"{step_name}.jpg"), image)


def show_images_with_results(images, plates_numbers):
    for i, plate in enumerate(images):
        cv2.putText(
            plate,
            plates_numbers[i],
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.imshow(f"Plate {i + 1}", plate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def validate_plate(plate_number, authorized_plate):
    if plate_number in authorized_plate:
        return 'AUTHORIZED'
    else:
        return 'NOT AUTHORIZED'


def save_results_to_csv(data, output_file="results.csv"):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Plate Number", "Status"])
        writer.writerows(data)
    print(f"Results saved to {output_file}")


def debug_log(step, message):
    print(f"[DEBUG] {step}: {message}")


def main():
    authorized_plate = ['27NZR335']

    # Load all image files in the 'images' directory
    images_path = os.path.abspath('./images/')
    images = [os.path.join(images_path, file) for file in os.listdir(images_path) if file.endswith(('.jpg', '.png'))]

    plates = []
    plates_filter_applied = []
    plates_numbers = []
    data = []

    for i, image_path in enumerate(images):
        data.append([])
        data[i].append(os.path.basename(image_path))  # Filename

        plate = cv2.imread(image_path)

        # Debugging: Log original filename
        debug_log("Filename", os.path.basename(image_path))

        # Resize image for better recognition
        plate = resize_image(plate)

        # Apply filter to the plate
        filtered_plate = apply_filter(plate)
        plates_filter_applied.append(filtered_plate)

        # Debugging: Save filtered image
        debug_save_image(f"Step_Filtered_{i + 1}", filtered_plate)

        # Extract plate number using PaddleOCR
        plate_number = scan_plate_with_paddleocr(filtered_plate)
        plates_numbers.append(plate_number)
        data[i].append(plate_number)

        # Debugging: Log extracted plate number
        debug_log("Plate Number", plate_number)

        # Validate plate number
        status = validate_plate(plate_number, authorized_plate)
        data[i].append(status)

    # Format output
    format_output(data)

    # Save results to CSV
    save_results_to_csv(data)

    # Save debug images for analysis
    for idx, plate in enumerate(plates_filter_applied):
        debug_save_image(f"Processed_Plate_{idx + 1}", plate)

    # Show images with detected plate numbers
    show_images_with_results(plates, plates_numbers)


if __name__ == "__main__":
    main()
