find_path(MONGOC_INCLUDE_DIR NAMES mongo.h PATHS ${CONAN_INCLUDE_DIRS_MONGO-C-DRIVER})
find_library(MONGOC_LIBRARY NAMES ${CONAN_LIBS_MONGO-C-DRIVER} PATHS ${CONAN_LIB_DIRS_MONGO-C-DRIVER})

set(MONGOC_FOUND TRUE)
set(MONGOC_INCLUDE_DIRS ${MONGOC_INCLUDE_DIR})
set(MONGOC_STATIC_LIBRARIES mongoc z resolv)
mark_as_advanced(MONGOC_LIBRARY MONGOC_INCLUDE_DIR)
