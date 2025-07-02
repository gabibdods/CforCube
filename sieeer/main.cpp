#include <iostream>
#include <opencv2/opencv.hpp>
#include <map>
#include <string>

using namespace cv;
using namespace std;

Mat loadImage(const string& path) {
    Mat img = imread(path);
    if (img.empty()) {
        cerr << "image failed to load" << endl;
        exit(1);
    }
    return img;
}

Mat downsizeImage(const Mat& image) {
    Mat resized;
    resize(image, resized, Size(), 0.5, 0.5);
    return resized;
}

Mat silence(const Mat& mask) {
    Mat processed;
    Mat kernel = Mat::ones(20, 20, CV_8U);
    morphologyEx(mask, processed, MORPH_OPEN, kernel);
    morphologyEx(processed, processed, MORPH_CLOSE, kernel);
    return processed;
}

void drawContour(Mat& image, const Mat& mask) {
    vector<vector<Point>> contours;
    findContours(mask, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
    for (const auto& contour : contours) {
        if (contourArea(contour) < 1000) continue;
        approxPolyDP(contour, approx, 0.05*arcLength(contour, true), true);
        if (approx.size() == 4) {
            Rect r = boundingRect(approx);
            float aspect_ratio = r.width / float()r.height;
            if (aspect_ratio >= 0.8 && aspect_ratio <= 1.2) {
                rectangle(image, r, Scalar(255, 0, 40), 2);
            }
        }
    }
}

vois showMaskWindow(const Mat& img, Scalar low, Scalar high) {
    if(img.empty()) {
        cerr << "Empty image" << endl;
        exit(1);
    }
    Mat
}

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
