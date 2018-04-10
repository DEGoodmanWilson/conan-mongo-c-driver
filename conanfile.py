#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import subprocess

class MongoCDriverConan(ConanFile):
    name = "mongo-c-driver"
    version = "1.9.4"
    url = "http://github.com/DEGoodmanWilson/conan-mongo-c-driver"
    description = "A high-performance MongoDB driver for C "
    license = "https://github.com/mongodb/mongo-c-driver/blob/{0}/COPYING".format(version)
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = 'OpenSSL/1.1.0g@conan/stable', 'zlib/[~=1.2]@conan/stable'
    # TODO add cyrus-sasl

    def configure(self):
        # Because this is pure C
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("https://github.com/mongodb/mongo-c-driver/releases/download/{0}/mongo-c-driver-{0}.tar.gz".format(self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            # self.build_vs()
            self.output.fatal("No windows support yet. Sorry. Help a fellow out and contribute back?")

        with tools.chdir("sources"):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True

            # self.output.info("PKG_CONFIG = {0}".format(os.environ["PKG_CONFIG"]))

            config_args = []
            for option_name in self.options.values.fields:
                if(option_name == "shared"):
                    if(getattr(self.options, "shared")):
                        config_args.append("--enable-shared")
                        config_args.append("--disable-static")
                    else:
                        config_args.append("--enable-static")
                        config_args.append("--disable-shared")
                else:
                    activated = getattr(self.options, option_name)
                    if activated:
                        self.output.info("Activated option! %s" % option_name)
                        config_args.append("--%s" % option_name)

            config_args.append("--disable-automatic-init-and-cleanup")

            env_build.configure(args=config_args)
            env_build.make()

    def package(self):
        self.copy(pattern="COPYING*", src="sources")
        self.copy(pattern="*.h", dst="include/bson", src="sources/src/libbson/src/bson", keep_path=False)
        self.copy(pattern="*.h", dst="include/jsonsl", src="sources/src/libbson/src/jsonsl", keep_path=False)
        self.copy(pattern="*.h", dst="include/mongoc", src="sources/src/mongoc", keep_path=False)
        # self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="sources", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['mongoc', 'bson']
        if tools.os_info.is_macos:
            self.cpp_info.exelinkflags = ['-framework CoreFoundation', '-framework Security']
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags

