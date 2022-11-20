

inline
ColorU8_sRGB_Alpha ImageRGBA::get_pixel( std::size_t aX, std::size_t aY ) const
{
	assert( aX < mWidth && aY < mHeight ); // Leave this at the top of the function.

	int index = get_linear_index(aX, aY); // gets the linear index of (x,y)
	return ColorU8_sRGB_Alpha {mData[index], mData[index+1], mData[index+2], mData[index+3]};
	// returns a ColorU8_sRGB_Alpha object containing the values of the pixel at (x,y)
}

inline
std::size_t ImageRGBA::get_width() const noexcept
{
	return mWidth;
}
inline
std::size_t ImageRGBA::get_height() const noexcept
{
	return mHeight;
}

inline
std::uint8_t* ImageRGBA::get_image_ptr() noexcept
{
	return mData;
}
inline
std::uint8_t const* ImageRGBA::get_image_ptr() const noexcept
{
	return mData;
}

inline
std::size_t ImageRGBA::get_linear_index( std::size_t aX, std::size_t aY ) const noexcept
{
	return (aY) * (mWidth * 4) + aX*4;
	// returns the index of the element representing (x,y) in the image
}