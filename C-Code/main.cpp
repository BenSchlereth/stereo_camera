#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "opencv2/core/core.hpp"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <chrono>

#define MIN_AREA 100

#define LOWER_RATIO 0.6
#define UPPER_RATIO 0.8

double euclidean_distance(int x_1, int y_1, int x_2, int y_2){
    return (sqrt((x_1-x_2)*(x_1-x_2)+(y_1-y_2)*(y_1-y_2)));
}


int main( int argc, char** argv ) {
    // start time measurement
    auto start = std::chrono::high_resolution_clock::now();

    //Read image
    cv::Mat input;
    input = cv::imread("../Gerade_Links_1080p.jpg", cv::IMREAD_COLOR);
    if( input.empty() )                      // Check for invalid input
    {
        std::cout <<  "Could not open or find the image" << std::endl ;
        return -1;
    }

    //color-filter:
    cv::Mat HSV_image;
    cvtColor(input, HSV_image, cv::COLOR_BGR2HSV);
    cv::Scalar lower_Green = cv::Scalar(50, 50, 10);
    cv::Scalar upper_green = cv::Scalar(90,255,255);
    cv::Mat maskHSV, resultHSV;
    cv::inRange(HSV_image, lower_Green, upper_green, maskHSV);
    cv::bitwise_and(HSV_image, HSV_image, resultHSV, maskHSV);

    //find contours
    std::vector<std::vector<cv::Point> > contours;
    cv::Mat contourOutput = maskHSV.clone();
    cv::findContours( contourOutput, contours, cv::RETR_LIST, cv::CHAIN_APPROX_NONE );

    //delete small contours
    cv::Rect box;
    std::vector<cv::Rect> vector_of_boxes;
    for(size_t i = 0; i < contours.size(); i++){
        box = cv::boundingRect(contours[i]);
        //auto it = vector_of_boxes.insert(vector_of_boxes.end(), box);
        if (box.area()>MIN_AREA) {
            vector_of_boxes.insert(vector_of_boxes.end(), 1, box);
        }
    }

    //search top part (with ratio)
    std::vector<cv::Rect> top_boxes;
    float ratio;
    for(int i = 0; i<vector_of_boxes.size(); i++){
        ratio = float (vector_of_boxes[i].width) / float(vector_of_boxes[i].height);
        //std::cout <<  vector_of_boxes[i].width <<"and height:"<< vector_of_boxes[i].height << std::endl;
        if((LOWER_RATIO < ratio) && (ratio < UPPER_RATIO)){
            top_boxes.insert(top_boxes.end(), 1, vector_of_boxes[i]);
        }
    }

    //find bottom part
    std::vector<cv::Rect> top;
    std::vector<cv::Rect> bottom;
    std::vector<cv::Rect> cone;
    bool found = 0;
    float distance = 0;
    for(int i=0; i < top_boxes.size(); i++){
        found = 0;
        float min_distance = 5 * float(top_boxes[i].height);
        cv::Rect possible_box (0, 0, 0, 0);
        for(int j=0; j < vector_of_boxes.size(); j++){
            //bounding box is to the left, below and wider
            //std::cout << vector_of_boxes[j].x << std::endl;
            if((top_boxes[i].y < vector_of_boxes[j].y) && (top_boxes[i].area() < vector_of_boxes[j].area())) {
                distance = euclidean_distance(top_boxes[i].x, top_boxes[i].y, vector_of_boxes[j].x,
                                              vector_of_boxes[j].y);
                //std::cout << distance << std::endl;
                if (min_distance > distance) {
                    found = 1;
                    min_distance = distance;
                    possible_box = vector_of_boxes[j];
                }
            }
        if (found){
            top.insert(top.end(), top_boxes[i]);
            bottom.insert(bottom.end(), possible_box);
            cv::Rect bounding_box (possible_box.x, top_boxes[i].y, possible_box.width, possible_box.y - top_boxes[i].y + possible_box.height);
            cone.insert(cone.end(), bounding_box);
            }
        }
    }

    //draw boxes
    cv::Scalar color;
    color = cv::Scalar(0, 0, 255);
    for (auto & box : cone) {
        //cv::drawContours(input, contours, idx, color, 10);
        cv::rectangle(input, box, color, 10);
    }
    cv::Rect zero (1,100,1,1);
    cv::rectangle(input, zero, color,5);

    //show image
    cv::Mat out_image;
    cv::resize(input, out_image, cv::Size(720 ,405));
    cv::namedWindow("Display frame", cv::WINDOW_AUTOSIZE );
    cv::imshow( "Display frame", out_image );

    //calculate time
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    std::cout << "Time needed: " << duration.count() << "us" << std::endl;

    cv::waitKey(0);
    return 0;
}
