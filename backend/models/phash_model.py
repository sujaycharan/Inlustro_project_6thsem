# backend/models/phash_model.py

import imagehash
from PIL import Image

class PHashModel:
    def __init__(self, hash_size=16):
        self.hash_size = hash_size

    def compute_hash(self, image_path):
        """
        Compute the perceptual hash for an image.
        :param image_path: Path to the input image
        :return: Perceptual hash of the image
        """
        image = Image.open(image_path).convert("RGB")
        return imagehash.phash(image, hash_size=self.hash_size)

    def compare_hashes(self, hash1, hash2, threshold=5):
        """
        Compare two perceptual hashes to check similarity.
        :param hash1: Perceptual hash of first image
        :param hash2: Perceptual hash of second image
        :param threshold: Hamming distance threshold for similarity
        :return: Boolean indicating if images are similar
        """
        return hash1 - hash2 <= threshold

# Example Usage:
if __name__ == "__main__":
    phash_model = PHashModel()
    hash1 = phash_model.compute_hash("test1.jpg")
    hash2 = phash_model.compute_hash("test2.jpg")
    
    if phash_model.compare_hashes(hash1, hash2):
        print("Images are similar")
    else:
        print("Images are different")
