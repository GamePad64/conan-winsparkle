from conans import ConanFile, CMake, tools
import os


class WinsparkleConan(ConanFile):
    name = "winsparkle"
    version = "0.6.0"
    license = "MIT"
    url = "https://github.com/vslavik/winsparkle"
    description = ("WinSparkle is a heavily (to the point of being its almost-port) "
                   "inspired by the Sparkle framework originally by Andy Matuschak that"
                   " became the de facto standard for software updates on macOS.")
    topics = ("conan", "sparkle", "winsparkle", "update")
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    generators = "cmake"
    requires = [
        "wxwidgets/3.1.3@bincrafters/stable",
        "expat/2.2.9",
        "openssl/1.1.1f",
    ]
    exports_sources = ["cmake.patch"]
    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get(url="https://github.com/vslavik/winsparkle/archive/v0.6.0.zip")
        #tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file="cmake.patch")
        cmake = CMake(self)
        cmake.configure(source_folder=os.path.join(self._source_subfolder, "cmake"))
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="winsparkle")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        library_name = "WinSparkle"
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = [library_name + "d"]
        else:
            self.cpp_info.libs = [library_name]

