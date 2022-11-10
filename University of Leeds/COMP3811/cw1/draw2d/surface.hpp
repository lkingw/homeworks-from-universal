#ifndef SURFACE_HPP_C464AD04_D6E0_459B_BDF9_51C65C009BF3
#define SURFACE_HPP_C464AD04_D6E0_459B_BDF9_51C65C009BF3

// IMPORTANT: DO NOT CHANGE THIS FILE WHEN YOU ARE SOLVING COURSEWORK 1!
//
// For CW1, the surface.hpp file must remain exactly as it is. In particular,
// you must not change the Surface class interface.

#include <cassert>
#include <cstdint>
#include <cstdlib>

#include "color.hpp"

/** Surface - an image that we can draw to
 *
 * The surface class enacpsulates an image that we can draw to. It provides 
 * minimal functionality to do so.
 *
 * The image data stored by the surface is stored as an 32-bit RGBx format.
 * Each channel (r, g, b) uses 8 bits. There is an additional 8 bits of padding
 * for each pixel, making each pixel exactly 32-bits in size.
 *
 * The image data is further stored in the sRGB space.
 *
 * REMINDER: DO NOT CHANGE THE INTERFACE OF THIS CLASS (see comment at the top).
 */
class Surface final
{
	public:
		Surface( std::size_t aWidth, std::size_t aHeight );
		~Surface();

		// The surface is "move-only". It cannot be copied, but ownership of
		// the surface's data can be transferred from one Surface instance to
		// another. Study C++'s move semantics for further details.
		Surface( Surface const& ) = delete;
		Surface& operator= (Surface const&) = delete;

		Surface( Surface&& ) noexcept;
		Surface& operator= (Surface&&) noexcept;

	public:
		// Clear surface image data to (0,0,0) = black
		void clear() noexcept;

		// Clear surface to specified color
		void fill( ColorU8_sRGB ) noexcept;
	
		// Set the pixel at index (aX,aY) to the specified color
		void set_pixel_srgb( std::size_t aX, std::size_t aY, ColorU8_sRGB const& );

		// Get pointer to surface image data. This is mainly used when drawing
		// the surface's contents to the screen. You must not use these functions
		// when implementing your drawing functions.
		std::uint8_t const* get_surface_ptr() const noexcept;

		// Return surfac width
		std::size_t get_width() const noexcept;

		// Return surface height
		std::size_t get_height() const noexcept;

		// Compute the linear index of pixel (aX,aY)
		std::size_t get_linear_index( std::size_t aX, std::size_t aY ) const noexcept;

	private:
		std::uint8_t* mSurface; // Surface image data, sRGB, stored as RGBx8
		std::size_t mWidth, mHeight; // Surface width and height in pixels
};

#include "surface.inl"
#endif // SURFACE_HPP_C464AD04_D6E0_459B_BDF9_51C65C009BF3
