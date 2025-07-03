#include <opencv2/opencv.hpp>
#include <iostream>
#include <map>
#include <string>

using namespace cv;
using namespace std;

void show_main(const map<string, pair<Scalar, Scalar>>& faces_to_masks) {
    Mat img = imread("rainbow.jpg");
    if (img.empty()) {
        cout << "\nEmpty image." << endl;
        exit(EXIT_FAILURE);
    }
    for (const auto& [face, hsv_range] : faces_to_masks) {
        Scalar lo = hsv_range.first;
        Scalar hi = hsv_range.second;

        Mat image;
        cvtColor(img, image, COLOR_BGR2HSV);

        Mat mask;
        inRange(img, lo, hi, mask);

        Mat kernel = Mat::ones(20, 20, CV_8U);
        Mat highlight;
        morphologyEx(mask, highlight, MORPH_OPEN, kernel);
        morphologyEx(highlight, highlight, MORPH_CLOSE, kernel);
        Mat silenced = highlight;

        Mat highlighted;
        bitwise_and(image, image, highlighted, silenced);

        vector<vector<Point>> contours;
        findContours(silenced, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

        for(const auto& contour : contours) {
            double area =contourArea(contour);
            if (area < 1000) {
                continue;
            }
            double perimeter = arcLength(contour, true);
            vector<Point> approx;
            approxPolyDP(contour, approx, 0.05*perimeter, true);

            if (approx.size() == 4) {
                Rect rect = boudingRect(approx);
                float aspect_ratio = (float)rect.width / rect.height;
                if (aspect_ratio >= 0.8 && aspect_ratio <= 1.2) {
                    rectangle(highlighted, rect, Scalar(255, 0, 40), 2);
                }
            }
        }
        Mat show;
        cvtColor(highlighted, show, COLOR_HSV2BGR);
        resize(show, show, Size(), 0.5, 0.5);
        imshow("Face", show);
        waitKey(0);
        destroyAllWindows();
    }
}
int main() {
    map<string, pair<Scalar, Scalar>> faces_to_masks = {
        {"blue",    {Scalar(104, 66, 107),  Scalar(130, 255, 255)}},
        {"green",   {Scalar(43, 79, 64),    Scalar(80, 211, 255)}},
        {"orange",  {Scalar(10, 118, 150),  Scalar(18, 255, 255)}},
        {"red",     {Scalar(0, 118, 150),   Scalar(4, 255, 255)}},
        {"white",   {Scalar(0, 0, 237),     Scalar(167, 7, 255)}},
        {"yellow",  {Scalar(17, 67, 235),   Scalar(168, 255, 255)}}
    };
    show_main(faces_to_masks);
    return 0;
}