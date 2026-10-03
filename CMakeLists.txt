cmake_minimum_required(VERSION 3.5...4.0)

project(qore-fsevent-module VERSION 2.0.0)

include(CheckCXXCompilerFlag)
include(CheckCXXSourceCompiles)
include(CheckCXXSymbolExists)
include(CheckIncludeFileCXX)

# Check for C++11.
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
if(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
else()
    message(FATAL_ERROR "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

# where to look first for cmake modules, before ${CMAKE_ROOT}/Modules/ is checked
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake )

# enable RPATH in macos bins (OS requires this in any case)
if (POLICY CMP0042)
    cmake_policy(SET CMP0042 NEW)
endif()

find_package(Qore 0.9 REQUIRED)
qore_find_pthreads()

if (APPLE)
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -framework CoreFoundation -framework CoreServices")
    set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -framework CoreFoundation -framework CoreServices")
endif (APPLE)


include_directories( ${CMAKE_SOURCE_DIR}/src )
include_directories( ${CMAKE_SOURCE_DIR}/src/include )
include_directories( ${CMAKE_SOURCE_DIR}/src/efsw )

set(CPP_SRC
)
set(QPP_SRC
    src/fsevent.qpp
    src/constants.qpp
    src/QC_AbstractFsWatcher.qpp
)

set(EFSW_SRC
    src/efsw/Debug.cpp
    src/efsw/DirectorySnapshot.cpp
    src/efsw/DirectorySnapshotDiff.cpp
    src/efsw/DirWatcherGeneric.cpp
    src/efsw/FileInfo.cpp
    src/efsw/FileSystem.cpp
    src/efsw/FileWatcher.cpp
    src/efsw/FileWatcherCWrapper.cpp
    src/efsw/FileWatcherGeneric.cpp
    src/efsw/FileWatcherImpl.cpp
    src/efsw/Log.cpp
    src/efsw/Mutex.hpp
    src/efsw/sophist.h
    src/efsw/String.cpp
    src/efsw/System.cpp
    src/efsw/Thread.hpp
    src/efsw/Watcher.cpp
    src/efsw/WatcherGeneric.cpp
)

if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set(EFSW_SRC ${EFSW_SRC}
        src/efsw/FileWatcherFSEvents.cpp src/efsw/WatcherFSEvents.cpp
        src/efsw/FileWatcherKqueue.cpp src/efsw/WatcherKqueue.cpp)
endif ()

if (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
    set(EFSW_SRC ${EFSW_SRC} src/efsw/FileWatcherInotify.cpp src/efsw/WatcherInotify.cpp)
endif ()

if (${CMAKE_SYSTEM_NAME} MATCHES "^.*BSD$")
    set(EFSW_SRC ${EFSW_SRC} src/efsw/FileWatcherKqueue.cpp src/efsw/WatcherKqueue.cpp)
endif ()

if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(EFSW_SRC ${EFSW_SRC} src/efsw/FileWatcherWin32.cpp src/efsw/WatcherWin32.cpp)
endif()

if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(EFSW_SRC ${EFSW_SRC}
        src/efsw/platform/win/FileSystemImpl.cpp
        src/efsw/platform/win/SystemImpl.cpp
    )
else ()
    # posix systems
    set(EFSW_SRC ${EFSW_SRC}
        src/efsw/platform/posix/FileSystemImpl.cpp
        src/efsw/platform/posix/SystemImpl.cpp
    )
endif ()

add_definitions(-DUSE_UTF8)

qore_wrap_qpp_value(QPP_SOURCES DOXLIST _dox_src METALIST QPP_META_SRC ${QPP_SRC})

SET (module_name "fsevent")

set(QORE_DOX_TMPL_SRC
  docs/mainpage.dox.tmpl
    docs/guide-fseventreleasenotes.dox.tmpl
)

add_library(${module_name} MODULE ${CPP_SRC} ${QPP_SOURCES} ${EFSW_SRC})

if (WIN32 AND MINGW AND MSYS)
    target_compile_definitions(${module_name} PUBLIC BUILDING_DLL)
endif (WIN32 AND MINGW AND MSYS)

if (DEFINED ENV{DOXYGEN_EXECUTABLE})
    set(DOXYGEN_EXECUTABLE $ENV{DOXYGEN_EXECUTABLE})
endif()

set(MODULE_DOX_INPUT "${CMAKE_BINARY_DIR}/mainpage.dox" ${_dox_src})
list(APPEND MODULE_DOX_INPUT
    ${CMAKE_CURRENT_BINARY_DIR}/guide-fseventreleasenotes.dox
)
qore_external_binary_module(${module_name} ${PROJECT_VERSION})

qore_external_user_module("qlib/FsEventPollerUtil.qm" "")
qore_external_user_module("qlib/FsEventPoller.qm" "FsEventPollerUtil")

qore_dist(${PROJECT_VERSION})

# install qpp metadata files
if (COMMAND qore_install_qpp_metadata)
    qore_install_qpp_metadata(${module_name} ${QPP_META_SRC})
else()
    install(FILES ${QPP_META_SRC}
            DESTINATION ${CMAKE_INSTALL_DATADIR}/qore/metadata)
endif()

qore_config_info()

if (DOXYGEN_FOUND)
  qore_wrap_dox(QORE_DOX_SRC ${QORE_DOX_TMPL_SRC})
  add_custom_target(QORE_MOD_DOX_FILES DEPENDS ${QORE_DOX_SRC})
  add_dependencies(docs-module QORE_MOD_DOX_FILES)
endif()

# Resolve links between the native API and all companion user modules.
if (DOXYGEN_FOUND)
    qore_binary_module_two_phase_docs(${module_name} "FsEventPoller;FsEventPollerUtil")
endif()
