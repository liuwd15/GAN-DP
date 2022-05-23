import argparse
import os
import torch
import numpy as np

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Get coordinates in the latent space with closed form factorization eigenvectors as basis"
    )
    parser.add_argument(
        "--factor",
        type=str,
        help="name of the closed form factorization result factor file",
    )
    parser.add_argument(
        "--projection_dir",
        type=str,
        default="factor.pt", 
        help="directory of .pt files of image projections (inversion)",
    )
    parser.add_argument(
        "--out", 
        type=str, 
        default="coordinate.pt", 
        help="name of the result factor file"
    )

    args = parser.parse_args()
    
    factor = torch.load(args.factor)
    inversions = [os.path.join(args.projection_dir, f) for f in os.listdir(args.projection_dir) if f.endswith('.pt')]

    coordinates = {}
    for i in range(len(inversions)):
        inversion_i = torch.load(inversions[i])
        for img in inversion_i.keys():
            latent_code = inversion_i[img]['latent'].cpu().detach().numpy()
            coordinate = np.dot(latent_code, factor['eigvec'])
            coordinates[img] = coordinate
            
    torch.save(coordinates, args.out)
