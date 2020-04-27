import argparse
import os
import subprocess
import shutil

SRC_ENVIRON = "ARRUS_SRC_PATH"
INSTALL_ENVIRON = "ARRUS_INSTALL_PATH"


def main():
    parser = argparse.ArgumentParser(description="Configures build system.")
    parser.add_argument("--targets", dest="targets",
                        type=str, required=True, nargs="+")
    parser.add_argument("--no_swig", dest="no_swig", action="store_true")
    parser.set_defaults(no_swig=False)

    args = parser.parse_args()
    targets = args.targets
    options = ["-DARRUS_BUILD_%s=ON" % target.upper() for target in targets]
    if args.no_swig:
        options.append("-DARRUS_BUILD_SWIG=OFF")

    src_dir = os.environ.get(SRC_ENVIRON, None)
    install_dir = os.environ.get(INSTALL_ENVIRON, None)
    if src_dir is None or install_dir is None:
        raise ValueError("%s and %s environment variables should be declared"
                         % (SRC_ENVIRON, INSTALL_ENVIRON))
    options += ["-DUs4_ROOT_DIR=" + install_dir]

    build_dir = os.path.join(src_dir, "build")

    shutil.rmtree(build_dir, ignore_errors=True)
    os.makedirs(build_dir)

    cmake_generator = ""
    if os.name == "nt":
        cmake_generator = "Visual Studio 15 2017 Win64"
    else:
        cmake_generator = "Unix Makefiles"

    cmake_cmd = [
        "cmake",
        "-S", src_dir,
        "-B", build_dir,
        "-G", cmake_generator,
    ] + options
    print("Calling: %s" % (" ".join(cmake_cmd)))
    subprocess.call(cmake_cmd)


if __name__ == "__main__":
    main()