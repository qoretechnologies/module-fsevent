// Copyright (C) 2026 Qore Technologies, s.r.o.
// SPDX-License-Identifier: MIT
#include <efsw/FileSystem.hpp>
#include <exception>
#include <iostream>

int main(int argc, char** argv) {
    if (argc != 2) {
        return 2;
    }
    try {
        std::cout << efsw::FileSystem::getRealPath(argv[1]) << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
