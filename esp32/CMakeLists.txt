# ESP-IDF Version
set(ESP_IDF_VERSION "5.3")

# Configuration
cmake_minimum_required(3.16)

# SDK Configuration
set(SDKCONFIG_DEFAULTS "sdkconfig.defaults")

# Project Name
project(folotoy-nordic)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
