# Simple_Camscanner
This is a simple Camscanner projecct using openCV

## Project Steps Summary

1. **Pre-processing image to enhance document.**
2. **Corner detection to extract the corner points.**
3. **Warper to make it flat x, y direction.**
4. **Post-processing image (thresholding, denoising)**

# Implementation

## 1- Preprocessing Method

Pre-processing is an essential step in document preparation, and it can make all the difference in the quality of the final product. The goal of pre-processing is to clean up the document and make it more usable, and there are a variety of methods that can be used to achieve this.

In our preprocessing we following these steps:

- Convert to Grey level
- Denoise ( either using Gaussian Blur or fastNmeanDenoising )
- Convert to morph (can be skipped)
- Edge detection (using canny method)
- Extra processing for better result (can be skipped)

| ![Convert to Grey level](https://user-images.githubusercontent.com/87777192/222703495-b13267be-6551-499d-9c3e-0ade8e221161.png) | ![Difference between denoise and blur](https://user-images.githubusercontent.com/87777192/222703583-6f268b90-a3e3-4d03-91b5-61410a723ca6.png) |
|:--:|:--:|
| *Convert to Grey level* | *Denoise using Gaussian Blur* |

| ![Canny with and without morph](https://user-images.githubusercontent.com/87777192/222703741-223bb0af-3243-405d-887d-6334aa4df33d.png) | ![Pre-processing Code](https://user-images.githubusercontent.com/87777192/222703834-e4ac3301-6cb8-4634-a758-32e4bc42efd4.png) |
|:--:|:--:|
| *Edge detection using Canny* | *Code example for pre-processing* |

## 2. Corner detection to extract the corner points.

Once the image is pre-processed, the next step is to detect the corner points. This will help us extract the document's shape and transform it into a flat surface.

### `cornerDetector(img)`

This function takes in an image and returns an array of pixel points that correspond to the corners of the biggest contour in the image. The steps involved in this function are:

1. Initialize an empty array called `corners` to store the corner pixel points of the biggest contour.
2. Initialize a variable `maxArea` to 0 to keep track of the maximum area encountered so far.
3. Use the `findContours()` method from the OpenCV library to find all the contours in the image.
4. Loop through each contour in the image.
5. Calculate the area of the contour using the `contourArea()` method.
6. If the area of the contour is smaller than 6000, ignore it and move on to the next contour.
7. If the area of the contour is larger than `maxArea` and the contour has 4 edges (meaning it is a square such as a paper), then save the corner pixel points of this contour in the `corners` array and update the value of `maxArea`.
8. Return the `corners` array.

### `sortCorners(corners)`

This function takes in an array of corner pixel points and returns a sorted array of these points in a specific order required for further processing. The steps involved in this function are:

1. Reshape the `corners` array into a 4x2 matrix for easier manipulations.
2. Create an empty array called `sortedCorners` to store the sorted corner pixel points.
3. Calculate the sum of the width and height of each corner and store the results in an array called `add`.
4. The corner with the smallest sum corresponds to the top-left corner and is saved in `sortedCorners[0]`. The corner with the largest sum corresponds to the bottom-right corner and is saved in `sortedCorners[3]`.
5. Calculate the difference between the width and height of each corner and store the results in an array called `diff`.
6. The corner with the minimum difference corresponds to the top-right corner and is saved in `sortedCorners[1]`. The corner with the maximum difference corresponds to the bottom-left corner and is saved in `sortedCorners[2]`.
7. Return the `sortedCorners` array.

| <img src="https://user-images.githubusercontent.com/87777192/222705309-1a604f22-be81-4aeb-a717-bc1f80423237.png" width="300" height="400"> | ![image](https://user-images.githubusercontent.com/87777192/222706340-f68f03c3-5193-47c0-a12f-5dbcb974c7b0.png) | ![image](https://user-images.githubusercontent.com/87777192/222706664-1edcbdc7-7186-4cf8-9005-2e776acad3e9.png) |
|:--:|:--:|:--:|
| *Corner detection figure* | *cornerDetector code example* | *cornerDetector code example* |

## 3. Warper to make it flat x, y direction.

After extracting the corner points, we can use them to transform the document into a flat surface in both the x and y directions. This will ensure that the document is easy to read and work with.

<img src="https://user-images.githubusercontent.com/87777192/222707100-e2280702-552f-4353-8021-497a4d5a5e78.png" width="300" height="400"> 

## 4. Post-processing image (thresholding, denoising)

Finally, we will perform some post-processing on the transformed document. This will involve thresholding and denoising the image to make it even clearer and easier to work with.

<img src="https://user-images.githubusercontent.com/87777192/222707128-8e77fca8-3be2-4f4b-b67b-d1d7fd146a04.png" width="300" height="400"> 


