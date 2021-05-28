cmake_minimum_required (VERSION 2.8)
PROJECT (MEDCOUPLING_TES C CXX)
INCLUDE(CMakeDependentOption)
SET(MEDCOUPLING_ROOT_DIR "" CACHE PATH "Path to the MEDCOUPLING installation")
set(CMAKE_BUILD_TYPE Release CACHE STRING "")
LIST(APPEND CMAKE_MODULE_PATH "${MEDCOUPLING_ROOT_DIR}/cmake_files")

INCLUDE_DIRECTORIES(
  ${MEDCOUPLING_ROOT_DIR}/include
)
IF(WIN32)
 SET(MEDCOUPLING_LIBRARIES 
   interpkernel.lib
   InterpKernelTestUtils.lib
   medcoupling.lib
   medcouplingremapper.lib
   medloader.lib
   renumbercpp.lib
   InterpKernelTest.lib
 )
ELSE(WIN32)
 SET(MEDCOUPLING_LIBRARIES 
   libinterpkernel.so
   libInterpKernelTestUtils.so
   libmedcoupling.so
   libparamedmem.so
   libmedcouplingremapper.so
   libmedloader.so
   libparamedloader.so
   libMPIAccessTest.so
   librenumbercpp.so
   libParaMEDMEMTest.so
   libInterpKernelTest.so
 )
ENDIF(WIN32)
SET(LINK_LIBRARIES)
FOREACH(L ${MEDCOUPLING_LIBRARIES})
  FIND_LIBRARY(LIB_${L} ${L} ${MEDCOUPLING_ROOT_DIR}/lib)
  LIST(APPEND LINK_LIBRARIES ${LIB_${L}})
ENDFOREACH()

ADD_EXECUTABLE(testMED ${PROJECT_SOURCE_DIR}/src/main.cpp)
TARGET_LINK_LIBRARIES(testMED ${LINK_LIBRARIES})
