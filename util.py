from PIL import Image
import os
import shutil
import subprocess


def remove_ds_store_files():
    try:
        import platform
        if platform.system() == 'Windows':
            import glob
            import os
            ds_store_files = glob.glob('./**/.DS_Store', recursive=True)
            for file in ds_store_files:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Error removing {file}: {e}")
        else:
            subprocess.run(
                ['find', './', '-name', '.DS_Store', '-type', 'f', '-delete'],
                check=True
            )
    except Exception as e:
        print(f"Error cleaning .DS_Store: {e}")


# Stitch a directory of frames together, output as a gif file
def create_gif_from_pngs(input_dir, output_path, fps=30):
    duration = int(1000 / fps)
    
    png_files = sorted([f for f in os.listdir(input_dir) if (f.endswith('.png'))])
    png_files = png_files[:91]
    if not png_files:
        raise ValueError("No PNG images found in the specified directory.")
    
    images = [Image.open(os.path.join(input_dir, file)) for file in png_files]
    
    # Save as a GIF
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    print(f"GIF saved at {output_path}")


# Helper function to copy files to a directory
def copy_files(src_dirs, dst_dir, condition):

    for src_dir in src_dirs:
        for root, _, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".png"):
                    if condition(file):
                        print(f"Copying file: {file_path}")
                        dst_file = os.path.join(dst_dir, file)
                        shutil.copy(file_path, dst_file)
                    else:
                        print(f"Skipped file (condition not met): {file_path}")
                else:
                    print(f"Skipped file (not .png): {file_path}")


# Util function to set up train images, train results, and test images into the correct ./data directories before unet.py training
def organize_files(list_of_train_images, list_of_train_labels, list_of_tests, output_dir="./data"):

    # Output directories
    train_images_dir = os.path.join(output_dir, "train_images")
    train_results_dir = os.path.join(output_dir, "train_results")
    test_images_dir = os.path.join(output_dir, "test_images")
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_results_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)

    copy_files(list_of_train_images, train_images_dir, lambda f: len(f) == 15)
    print("Completed copying train_images.\n")

    # Copy train results (files containing "output")
    copy_files(list_of_train_labels, train_results_dir, lambda f: "output" in f)
    print("Completed copying train_results.\n")

    # Copy test images (15 characters including extension)
    copy_files(list_of_tests, test_images_dir, lambda f: len(f) == 15)
    print("Completed copying test_images.\n")


# Change this list of train images if you wish to train on different data
path_to_train_images = [
    "./UnprocessedImages/200x/Shape1",
    "./UnprocessedImages/200x/Shape2",
    "./UnprocessedImages/200x/Shape3"
]

# This list must match the above list to ensure there is a correct label for each input image
path_to_train_labels = [
    "./ProcessedImages/200x/Shape1",
    "./ProcessedImages/200x/Shape2",
    "./ProcessedImages/200x/Shape3"
]
path_to_tests = ["./UnprocessedImages/200x/Shape4"]


#organize_files(path_to_train_images, path_to_train_labels, path_to_tests)


remove_ds_store_files()


directory_path = "UnprocessedImages/200x/Shape6"
processed_dir = "example.gif"
# create_gif_from_pngs(directory_path, processed_dir, fps=30)

