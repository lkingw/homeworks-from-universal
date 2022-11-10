workspace "COMP3811-cw1"
	language "C++"
	cppdialect "C++17"

	platforms { "macos" }
	configurations { "debug", "release" }

	flags "NoPCH"
	flags "MultiProcessorCompile"

	startproject "main"

	debugdir "%{wks.location}"
	objdir "_build_/%{cfg.buildcfg}-%{cfg.platform}-%{cfg.toolset}"
	targetsuffix "-%{cfg.buildcfg}-%{cfg.platform}-%{cfg.toolset}"
	
	-- Default toolset options
	filter "toolset:gcc or toolset:clang"
		linkoptions { "-pthread" }
		buildoptions { "-mcpu=apple-m1", "-Wall", "-pthread" }

		-- Varriable-length arrays (VLAs) are an extension that GCC and clang
		-- have long supported. However, they are not part of the C++ standard.
		-- (MSVC will not compile code with VLAs.)
		buildoptions { "-Werror=vla" }

	filter "toolset:msc-*"
		warnings "extra" -- this enables /W4; default is /W3
		--buildoptions { "/W4" }
		buildoptions { "/utf-8" }
		buildoptions { "/permissive-" }
		defines { "_CRT_SECURE_NO_WARNINGS=1" }
		defines { "_SCL_SECURE_NO_WARNINGS=1" }
	
	filter "*"

	-- default libraries
	filter "system:linux"
		links "dl"
	
	filter "system:windows"
		links "OpenGL32"

	filter "*"

	-- default outputs
	filter "kind:StaticLib"
		targetdir "lib/"

	filter "kind:ConsoleApp"
		targetdir "bin/"
		targetextension ".exe"
	
	filter "*"

	--configurations
	filter "debug"
		symbols "On"
		defines { "_DEBUG=1" }

	filter "release"
		optimize "On"
		defines { "NDEBUG=1" }

	filter "*"

-- Third party dependencies
include "third_party" 

-- Projects
project "main"
	local sources = { 
		"main/**.cpp",
		"main/**.hpp",
		"main/**.hxx",
		"main/**.inl"
	}

	kind "ConsoleApp"
	location "main"

	files( sources )

	links "vmlib"
	links "support"
	links "draw2d"

	links "x-stb"
	links "x-glad"
	links "x-glfw"

project "draw2d"
	local sources = { 
		"draw2d/**.cpp",
		"draw2d/**.hpp",
		"draw2d/**.hxx",
		"draw2d/**.inl"
	}

	kind "StaticLib"
	location "draw2d"

	files( sources )

project "support"
	local sources = { 
		"support/**.cpp",
		"support/**.hpp",
		"support/**.hxx",
		"support/**.inl"
	}

	kind "StaticLib"
	location "support"

	files( sources )

project "vmlib"
	local sources = { 
		"vmlib/**.cpp",
		"vmlib/**.hpp",
		"vmlib/**.hxx",
		"vmlib/**.inl"
	}

	kind "StaticLib"
	location "vmlib"

	files( sources )

project "tests-line"
	local sources = { 
		"tests-line/**.cpp",
		"tests-line/**.hpp",
		"tests-line/**.hxx",
		"tests-line/**.inl"
	}

	kind "ConsoleApp"
	location "tests-line"

	files( sources )

	links "vmlib"
	links "support"
	links "draw2d"

	links "x-stb"
	links "x-glad"
	links "x-glfw"

project "tests-triangle"
	local sources = { 
		"tests-triangle/**.cpp",
		"tests-triangle/**.hpp",
		"tests-triangle/**.hxx",
		"tests-triangle/**.inl"
	}

	kind "ConsoleApp"
	location "tests-triangle"

	files( sources )

	links "vmlib"
	links "support"
	links "draw2d"

	links "x-stb"
	links "x-glad"
	links "x-glfw"


--EOF
