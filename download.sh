BASEDIR=$(dirname $0)
mkdir $BASEDIR/test-suites
mkdir $BASEDIR/toolchain

# Download llvm project
git clone git@github.com:luxufan/llvm.git $BASEDIR/toolchain/llvm-project

# Download chromium
mkdir $BASEDIR/test-suites/chromium
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git $BASEDIR/test-suites/chromium/depot_tools

export PATH="$(realpath "$BASEDIR/test-suites/chromium/depot_tools"):$PATH"

cd $BASEDIR/test-suites/chromium
mkdir chromium && cd chromium
fetch --nohooks chromium

# Download envoy
git clone -b release/v1.31 git@github.com:envoyproxy/envoy.git $BASEDIR/test-suites/envoy

# Download blender
#
git clone -n blender-v4.2-release git@github.com:blender/blender.git $BASEDIR/test-suites/blender
