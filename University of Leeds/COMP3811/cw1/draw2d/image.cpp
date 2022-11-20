#include "image.hpp"

#include <memory>
#include <algorithm>

#include <cstdio>
#include <cassert>

#include <stb_image.h>

#include "surface.hpp"

#include "../support/error.hpp"

namespace
{
	struct STBImageRGBA_ : public ImageRGBA
	{
		STBImageRGBA_( std::size_t, std::size_t, std::uint8_t* );
		virtual ~STBImageRGBA_();
	};
}

ImageRGBA::ImageRGBA()
	: mWidth( 0 )
	, mHeight( 0 )
	, mData( nullptr )
{}

ImageRGBA::~ImageRGBA() = default;


std::unique_ptr<ImageRGBA> load_image( char const* aPath )
{
	assert( aPath );

	stbi_set_flip_vertically_on_load( true );

	int w, h, channels;
	stbi_uc* ptr = stbi_load( aPath, &w, &h, &channels, 4 );
	if( !ptr )
		throw Error( "Unable to load image \"%s\"", aPath );

	return std::make_unique<STBImageRGBA_>(
		std::size_t(w),
		std::size_t(h),
		ptr
	);
}

void blit_masked( Surface& aSurface, ImageRGBA const& aImage, Vec2f aPosition )
{
	int img_height = aImage.get_height(), img_width = aImage.get_width(); // get the height and width of the image
	int win_height = aSurface.get_height(), win_width = aSurface.get_width(); // get the height and width of the window

	for (int i  = 0; i < img_width; i++) { // iterate over all pixels in the image in column order
		for (int j = 0; j < img_height; j++) { // iteratoe over each pixel in the chosen column
			if (i > 0 && j > 0 && i <= img_width && j < img_height) { // check these coordinates are within the bounds of the image
				if (i + aPosition.x > 0 && j + aPosition.y > 0 && i + aPosition.x < win_width && j + aPosition.y < win_height) {
				// check if the position that the image is to be place is within the bounds of the window
					ColorU8_sRGB_Alpha col= aImage.get_pixel(i, j); // get the TGBA values stored in the image
					if (col.a > 128) { // only draw pixels with an alpha value higher than 128
						aSurface.set_pixel_srgb(i + aPosition.x, j + aPosition.y, ColorU8_sRGB{col.r, col.g, col.b});
						// set the corresponding pixel to the value from the image
					}
				}
			}
		}
	}
}

namespace
{
	STBImageRGBA_::STBImageRGBA_( std::size_t aWidth, std::size_t aHeight, std::uint8_t* aPtr )
	{
		mWidth = aWidth;
		mHeight = aHeight;
		mData = aPtr;
	}

	STBImageRGBA_::~STBImageRGBA_()
	{
		if( mData )
			stbi_image_free( mData );
	}
}