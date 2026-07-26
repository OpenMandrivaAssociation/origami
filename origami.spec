# Origami — analytical GEMM solution selection (TheRock 7.14)
# Shared dependency of hipBLASLt TensileLite / rocisa.

Name:		origami
Version:	7.14.0
Release:	1
Summary:	Analytical solution selection for ROCm GEMM
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-7.14/origami.tar.gz#/origami-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	pkgconfig(libdrm)

ExclusiveArch:	%{x86_64} %{aarch64}

%description
Origami provides analytical heuristics for GEMM / attention solution
selection used by hipBLASLt TensileLite and the rocisa code generator.

%package devel
Summary:	Development files for origami
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rocm-hip-devel
Provides:	cmake(origami) = %{version}

%description devel
Headers and CMake package for origami (roc::origami).

%prep
%autosetup -n origami

%build
export CC=clang
export CXX=clang++
export ROCM_PATH=%{_prefix}
export HIP_PATH=%{_prefix}
export HIP_DEVICE_LIB_PATH=%{_libdir}/amdgcn/bitcode
CXXFLAGS=$(printf '%s' "%{optflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
export LDFLAGS=$(printf '%s' "%{?__global_ldflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')

%cmake %{rocm_cmake_fhs} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=clang++ \
	-DORIGAMI_BUILD_SHARED_LIBS=ON \
	-DORIGAMI_ENABLE_PYTHON=OFF \
	-DORIGAMI_BUILD_TESTING=OFF \
	-DORIGAMI_ENABLE_FETCH=OFF \
	-DBUILD_TESTING=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build

%install
cd build
DESTDIR=%{buildroot} /usr/bin/ninja install -j%{?_smp_build_ncpus}%{!?_smp_build_ncpus:8}
cd ..
# Drop cpack / debian leftovers if any
rm -rf %{buildroot}/usr/share/doc/origami 2>/dev/null || true

%files
%license LICENSE.md
%doc README.md
%{_libdir}/liborigami.so.*

%files devel
%{_includedir}/origami/
%{_libdir}/liborigami.so
%{_libdir}/cmake/origami/
