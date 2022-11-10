
inline
ColorU8_sRGB_Alpha ImageRGBA::get_pixel( std::size_t aX, std::size_t aY ) const
{
	assert( aX < mWidth && aY < mHeight ); // Leave this at the top of the function.

	//TODO: your implementation goes here
	//TODO: your implementation goes here
	//TODO: your implementation goes here
	(void)aX;  // Avoid warnings about unused arguments until the function is
	(void)aY;  // properly implemented.
	return { 0, 0, 0, 0 }; //TODO: remove this line when you implement this
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
	//TODO: your implementation goes here
	//TODO: your implementation goes here
	//TODO: your implementation goes here
	(void)aX;  // Avoid warnings about unused arguments until the function is
	(void)aY;  // properly implemented.
	return 0; //TODO: remove this line when you implement this function
}
