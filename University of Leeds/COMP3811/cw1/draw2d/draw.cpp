#include "draw.hpp"

#include <algorithm>

#include <cmath>

#include "surface.hpp"
#include <iostream>

void draw_line_solid( Surface& aSurface, Vec2f aBegin, Vec2f aEnd, ColorU8_sRGB aColor )
{
	int x0, x1, y0, y1; // initalise methods for Bresenham's Algorithm [Reference: https://www.cs.helsinki.fi/group/goa/mallinnus/lines/bresenh.html]

	// calculate direction of the line
	if (fabs(aEnd.x - aBegin.x) < fabs(aEnd.y - aBegin.y)) {
		x0 = aBegin.y; //if dy > dx then swap x and y values to allow drawing
		x1 = aEnd.y;
		y0 = aBegin.x;
		y1 = aEnd.x;
	} else { // otherwise initialise normally
		x0 = aBegin.x;
		x1 = aEnd.x;
		y0 = aBegin.y;
		y1 = aEnd.y;
	}

	if (x1 < x0) { // check the direction of the line and swap
		int temp = x1;
		x1 = x0;
		x0 = temp;

		temp = y1;
		y1 = y0;
		y0 = temp;
	}
	
	int dy = fabs(y1 - y0); // calculate dy
	int dx = x1 - x0; // calculate dx
	int y_step = 1; // sets the step to a positive direction
	if (y0 > y1) { // reverses step direction if the line slope is negative
		y_step = -1;
	}

	int e = dx; // calculates the error as half of dx, so if the distance to the next pixel is more than
	// half of dx then a step in the y direction needs to be made
	int y = y0; // initialise the first point in the algorithm
	int height = aSurface.get_height(), width = aSurface.get_width(); // get max width/height of the window

	for (int i = x0; i <= x1; i++) { // iterate from min_x to max_x
		if (fabs(aEnd.x - aBegin.x) < fabs(aEnd.y - aBegin.y)) { // check to see if dy < dx
			if (y >= width || i >= height || y < 0 || i < 0) { // check the pixel is within the bounds of the window
				break;
			}	
			aSurface.set_pixel_srgb(y, i, aColor); // draw the pixel
		} else {
			if (i >= width || y >= height || i < 0 || y < 0) {
				break;
			}	
			aSurface.set_pixel_srgb(i, y, aColor);
		}
		e = e - 2*dy; // subtract dy from the error and check if it is greter than 0.
		if (e < 0) { // if e < 0 then a step in the y direction needs to be taken
			y = y + y_step;
			e = e + 2*dx; // add dx to e so that steps can be taken in the x direction again until another y step must be taken
		}
	}
}

void draw_triangle_solid( Surface& aSurface, Vec2f aP0, Vec2f aP1, Vec2f aP2, ColorU8_sRGB aColor )
{

	int max_x, max_y, min_x, min_y; // find min and max (x,y) values of the bounding rectangle surrounding the triangle
	max_x = std::max(aP0.x, std::max(aP1.x, aP2.x));
	max_y = std::max(aP0.y, std::max(aP1.y, aP2.y));
	min_x = std::min(aP0.x, std::min(aP1.x, aP2.x));
	min_y = std::min(aP0.y, std::min(aP1.y, aP2.y));

	// calculate the normals for each plane, bounding the triangle
	Vec2f n_0 = {-(aP1.y - aP0.y), (aP1.x -  aP0.x)}; //AB
	Vec2f n_1 = {-(aP2.y - aP1.y), (aP2.x -  aP1.x)}; //BC
	Vec2f n_2 = {-(aP0.y - aP2.y), (aP0.x -  aP2.x)}; //CA

	// get max width and height of the window
	int height = aSurface.get_height(), width = aSurface.get_width();


	for(int i = min_x; i <= max_x; i++) { // iterate over each column inside the bounding rectangle
		for (int j = min_y; j <= max_y; j++) {

			if (i >= width || j >= height || i < 0 || j < 0) { // clip pixel if outside the bounds of the window
				continue;
			}

			// perform the half plane tests using the formula n_i * (X - P) = 0
			float half_0 = (n_0.x * (aP0.x - i)) + (n_0.y * (aP0.y - j));
			float half_1 = (n_1.x * (aP1.x - i)) + (n_1.y * (aP1.y - j));
			float half_2 = (n_2.x * (aP2.x - i)) + (n_2.y * (aP2.y - j));

			// check the result of each test was negative to confirm it lies within the triangle
			if (half_0 <= 0 && half_1 <= 0 && half_2 <= 0) {

				// draw the pixel of the triangle
				aSurface.set_pixel_srgb(i, j, aColor);
			}
		}
	}
}

void draw_triangle_interp( Surface& aSurface, Vec2f aP0, Vec2f aP1, Vec2f aP2, ColorF aC0, ColorF aC1, ColorF aC2 )
{
	int max_x, max_y, min_x, min_y; // find min and max (x,y) values of the bounding rectangle surrounding the triangle
	max_x = std::max(aP0.x, std::max(aP1.x, aP2.x));
	max_y = std::max(aP0.y, std::max(aP1.y, aP2.y));
	min_x = std::min(aP0.x, std::min(aP1.x, aP2.x));
	min_y = std::min(aP0.y, std::min(aP1.y, aP2.y));

	int height = aSurface.get_height(), width = aSurface.get_width(); // get window width and height for checking

	for (int i = min_x; i <= max_x; i++) { // iterate over the columns in the bounding rectangle
		for( int j = min_y; j <= max_y; j++) {

			if (i >= width || j >= height || i < 0 || j < 0) {
				continue; // clip pixel if outside the bounds of the screen
			}

			// calculate the determinant of the matrix A (see report)
			float det_a = ((aP1.x - aP0.x)*(aP2.y - aP0.y)) - ((aP2.x - aP0.x)*(aP1.y - aP0.y));

			// mat = [e & f \\ g & h]
			float e = (aP2.y - aP0.y);
			float f = (aP0.x - aP2.x);
			float g = (aP0.y - aP1.y);
			float h = (aP1.x - aP0.x);

			// Vec2f [beta, gamma]
			Vec2f res = {((e * (i - aP0.x)) + (f * (j - aP0.y)))/det_a, ((g  * (i - aP0.x)) + (h * (j - aP0.y)))/det_a};

			// calculate alpha as a double to avoid rounding errors
			double alpha = double(1 - (res.x + res.y));

			// check the barycentric coordinates to confirm the point lies inside the triangle
			if (alpha >= 0 && res.x >= 0 && res.y >= 0 && res.x <= 1 && res.y <= 1 && alpha <= 1) {
				// calculate the colours of the pixel using the ratios from each point
				ColorU8_sRGB col = {uint8_t(((aC0.r * alpha) + (aC1.r * res.x) + (aC2.r * res.y)) * 255),
				uint8_t(((aC0.g * alpha) + (aC1.g * res.x) + (aC2.g * res.y)) * 255),
				uint8_t(((aC0.b * alpha) + (aC1.b * res.x) + (aC2.b * res.y)) * 255)};

				//set the correct pixel to col
				aSurface.set_pixel_srgb(i, j, col);
			}
		}
	}
}


void draw_rectangle_solid( Surface& aSurface, Vec2f aMinCorner, Vec2f aMaxCorner, ColorU8_sRGB aColor )
{
	//TODO: your implementation goes here
	//TODO: your implementation goes here
	//TODO: your implementation goes here

	//TODO: remove the following when you start your implementation
	(void)aSurface; // Avoid warnings about unused arguments until the function
	(void)aMinCorner;   // is properly implemented.
	(void)aMaxCorner;
	(void)aColor;
}

void draw_rectangle_outline( Surface& aSurface, Vec2f aMinCorner, Vec2f aMaxCorner, ColorU8_sRGB aColor )
{
	//TODO: your implementation goes here
	//TODO: your implementation goes here
	//TODO: your implementation goes here

	//TODO: remove the following when you start your implementation
	(void)aSurface; // Avoid warnings about unused arguments
	(void)aMinCorner;
	(void)aMaxCorner;
	(void)aColor;
}