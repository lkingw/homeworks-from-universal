#include "glad.h"
#include "GLFW/glfw3.h"

#include <random>
#include <typeinfo>
#include <stdexcept>

#include <cstdio>
#include <cstdlib>

#include "../draw2d/surface.hpp"
#include "../draw2d/draw.hpp"
#include "../draw2d/shape.hpp"

#include "../support/error.hpp"
#include "../support/context.hpp"
#include "../support/runconfig.hpp"

#include "../vmlib/vec2.hpp"
#include "../vmlib/mat22.hpp"

namespace
{
	constexpr char const* kWindowTitle = "COMP3811-Tests: Triangles";

	void glfw_callback_error_( int, char const* );
	void glfw_callback_key_( GLFWwindow*, int, int, int, int );

	struct GLFWCleanupHelper
	{
		~GLFWCleanupHelper();
	};
	struct GLFWWindowDeleter
	{
		~GLFWWindowDeleter();
		GLFWwindow* window;
	};
}

int main( int aArgc, char* aArgv[] ) try
{
	// Parse command line arguments
	RuntimeConfig const config = parse_command_line( aArgc, aArgv );

	// Initialize GLFW
	if( GLFW_TRUE != glfwInit() )
	{
		char const* msg = nullptr;
		int ecode = glfwGetError( &msg );
		throw Error( "glfwInit() failed with '%s' (%d)", msg, ecode );
	}

	// Ensure that we call glfwTerminate() at the end of the program.
	GLFWCleanupHelper cleanupHelper;

	// Configure GLFW and create window
	glfwSetErrorCallback( &glfw_callback_error_ );

	glfwWindowHint( GLFW_SRGB_CAPABLE, GLFW_TRUE );
	glfwWindowHint( GLFW_DOUBLEBUFFER, GLFW_TRUE );

	//glfwWindowHint( GLFW_RESIZABLE, GLFW_FALSE );

	glfwWindowHint( GLFW_CONTEXT_VERSION_MAJOR, 4 );
	glfwWindowHint( GLFW_CONTEXT_VERSION_MINOR, 3 );
	glfwWindowHint( GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE );
	glfwWindowHint( GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE );

#	if !defined(NDEBUG)
	// When building in debug mode, request an OpenGL debug context. This
	// enables additional debugging features. However, this can carry extra
	// overheads. We therefore do not do this for release builds.
	glfwWindowHint( GLFW_OPENGL_DEBUG_CONTEXT, GLFW_TRUE );
#	endif // ~ !NDEBUG

	GLFWwindow* window = glfwCreateWindow(
		int(config.initialWindowWidth),
		int(config.initialWindowHeight),
		kWindowTitle,
		nullptr, nullptr
	);

	if( !window )
	{
		char const* msg = nullptr;
		int ecode = glfwGetError( &msg );
		throw Error( "glfwCreateWindow() failed with '%s' (%d)", msg, ecode );
	}

	GLFWWindowDeleter windowDeleter{ window };

	// Set up event handling
	std::size_t testId = 1;
	glfwSetWindowUserPointer( window, &testId );

	glfwSetKeyCallback( window, &glfw_callback_key_ );

	// Set up drawing stuff
	glfwMakeContextCurrent( window );
	glfwSwapInterval( 1 ); // V-Sync is on.

	// Get actual framebuffer size.
	// This can be different from the window size, as standard window
	// decorations (title bar, borders, ...) may be included in the window size
	// but not be part of the drawable surface area.
	int iwidth, iheight;
	glfwGetFramebufferSize( window, &iwidth, &iheight );

	assert( iwidth >= 0 && iheight >= 0 );
	auto fbwidth = std::size_t(iwidth) >> config.framebufferScaleShift;
	auto fbheight = std::size_t(iheight) >> config.framebufferScaleShift;

	Context context( fbwidth, fbheight );
	Surface surface( fbwidth, fbheight );

	glViewport( 0, 0, iwidth, iheight );

	// Main loop

	while( !glfwWindowShouldClose( window ) )
	{
		// Let GLFW process events
		glfwWaitEvents();
		
		// Check if window was resized.
		{
			int nwidth, nheight;
			glfwGetFramebufferSize( window, &nwidth, &nheight );

			if( 0 == nwidth || 0 == nheight )
			{
				// Window minimized? Pause until it is unminimized.
				// This is a bit of a hack.
				do
				{
					glfwWaitEvents();
					glfwGetFramebufferSize( window, &nwidth, &nheight );
				} while( 0 == nwidth || 0 == nheight );
			}

			if( iwidth != nwidth || iheight != nheight )
			{
				iwidth = nwidth;
				iheight = nheight;

				glViewport( 0, 0, iwidth, iheight );

				assert( iwidth >= 0 && iheight >= 0 );
				fbwidth = std::size_t(iwidth) >> config.framebufferScaleShift;
				fbheight = std::size_t(iheight) >> config.framebufferScaleShift;

				// Resize things
				context.resize( fbwidth, fbheight );
				surface = Surface( fbwidth, fbheight );
			}
		}

		// Update state
		// (nothing to be done here)

		// Draw scene
		surface.clear();

		switch( testId )
		{
			// Note: this always uses draw_triangle_interp(). However, until
			// you implement draw_triangle_interp(), it will just call 
			// draw_triangle_solid().

			case 1: {
				// Centered triangle
				draw_triangle_interp( surface, 
					{ fbwidth/2.f, fbheight-100.f },
					{ 100.f, 100.f },
					{ fbwidth-100.f, 100.f },
					{ 1.f, 1.f, 0.f },
					{ 1.f, 0.f, 1.f },
					{ 0.f, 1.f, 1.f }
				);
			} break;

			case 2: {
				// Centered triangle, permuted coordinates
				draw_triangle_interp( surface, 
					{ fbwidth-100.f, 100.f },
					{ fbwidth/2.f, fbheight-100.f },
					{ 100.f, 100.f },
					{ 0.f, 1.f, 1.f },
					{ 1.f, 1.f, 0.f },
					{ 1.f, 0.f, 1.f }
				);
			} break;

			case 3: {
				// Extending out of screen
				draw_triangle_interp( surface, 
					{ float(fbwidth), fbheight-100.f },
					{ fbwidth/2.f+100.f, 100.f },
					{ fbwidth*3.f/2.f-100.f, 100.f },
					{ 1.f, 1.f, 0.f },
					{ 1.f, 0.f, 1.f },
					{ 0.f, 1.f, 1.f }
				);
			} break;

			//TODO: your own tests here?
			//TODO: your own tests here?
		}
		
		context.draw( surface );

		// Display results
		glfwSwapBuffers( window );
	}

	// Cleanup.
	// For now, all objects are automatically cleaned up when they go out of
	// scope.
	
	return 0;
}
catch( std::exception const& eErr )
{
	std::fprintf( stderr, "Top-level Exception (%s):\n", typeid(eErr).name() );
	std::fprintf( stderr, "%s\n", eErr.what() );
	std::fprintf( stderr, "Bye.\n" );
	return 1;
}


namespace
{
	void glfw_callback_error_( int aErrNum, char const* aErrDesc )
	{
		std::fprintf( stderr, "GLFW error: %s (%d)\n", aErrDesc, aErrNum );
	}

	void glfw_callback_key_( GLFWwindow* aWindow, int aKey, int, int aAction, int )
	{
		if( GLFW_KEY_ESCAPE == aKey && GLFW_PRESS == aAction )
		{
			glfwSetWindowShouldClose( aWindow, GLFW_TRUE );
			return;
		}

		auto* testid = static_cast<std::size_t*>(glfwGetWindowUserPointer( aWindow ));
		assert( testid );

		if( GLFW_PRESS == aAction )
		{
			std::size_t select = 0;
			switch( aKey )
			{
				case GLFW_KEY_1: select = 1; break;
				case GLFW_KEY_2: select = 2; break;
				case GLFW_KEY_3: select = 3; break;
				case GLFW_KEY_4: select = 4; break;
				case GLFW_KEY_5: select = 5; break;
				case GLFW_KEY_6: select = 6; break;
				case GLFW_KEY_7: select = 7; break;
				case GLFW_KEY_8: select = 8; break;
				case GLFW_KEY_9: select = 9; break;
				case GLFW_KEY_0: select = 0; break;
				default: select = *testid; break;
			}

			if( select != *testid )
			{
				*testid = select;
				std::printf( "Selected test %zu\n", select );
			}
		}
	}
}

namespace
{
	GLFWCleanupHelper::~GLFWCleanupHelper()
	{
		glfwTerminate();
	}

	GLFWWindowDeleter::~GLFWWindowDeleter()
	{
		if( window )
			glfwDestroyWindow( window );
	}
}

