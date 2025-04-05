# cpp_dyncasts_benchmark

This repository provides a benchmark suite to evaluate the performance and memory usage of C++ applications with and without `dynamic_cast` optimizations. It includes case studies from real-world C++ projects such as LLVM, Chromium, V8, and more.

## 📦 Download Dependencies

Before building, you need to download the source code for the case studies.

To download **POV-Ray**, **Z3**, **Solidity**, **Envoy**, **Blender**, and **LLVM**:

```bash
./download.sh
```

To download **Chromium**:

```bash
./download_chromium.sh
```

To download **V8**:

```bash
./download_v8.sh
```

## 🔨 Building

Use the `build_.sh` script to build specific case studies with different configurations.

### Syntax

```bash
./build_.sh [OPTIONS]
```

### Options

```text
-llvm-case-study          Build the LLVM case study.
-chrome-case-study        Build the Chromium case study.
-b <benchmark>            Specify which benchmark to build. Options:
                          llvm, z3, solidity, povray, envoy, blender, chromium, v8
-v <version>              Specify the build variant:
                          thin            - ThinLTO without dynamic_cast optimization
                          thin-dyncastopt - ThinLTO with dynamic_cast optimization
                          lto             - Full LTO without dynamic_cast optimization
                          lto-dyncastopt  - Full LTO with dynamic_cast optimization
```

### Examples

Build the LLVM case study with ThinLTO and dynamic_cast optimization:

```bash
./build_.sh -llvm-case-study -b llvm -v thin-dyncastopt
```

Build the Chromium case study with full LTO:

```bash
./build_.sh -chrome-case-study -b chromium -v lto
```

## 📁 Project Structure

```text
.
├── benchmarks/             # Benchmark targets and configs
├── scripts/                # Download and build scripts
├── download.sh             # Download open-source projects (LLVM, Z3, etc.)
├── download_chromium.sh    # Download Chromium source
├── download_v8.sh          # Download V8 source
├── build_.sh               # Main build script
└── ...
```

## 📄 License

This project is licensed under the MIT License.

