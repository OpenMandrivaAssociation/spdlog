%global major 1
%global user            gabime
%global debug_package   %{nil}
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Name:           spdlog
Version:	1.8.1
Release:	3
Summary:        Super fast C++ logging library
Group:		Development/C
License:        MIT
URL:            https://github.com/%{user}/%{name}/
Source0:        https://github.com/%{user}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ninja
BuildRequires:  fmt-devel
BuildRequires:  cmake

%description
This is a packaged version of the gabime/spdlog header-only C++
logging library available at Github.


%package -n %{libname}
Summary:	Super fast C++ logging library
Group:		System/Libraries

%description -n %{libname}
Super fast C++ logging library.


%package -n	%{devname}
Group:		Development/C
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
Requires:	%{libname} = %{EVRD}
Requires:       libstdc++-devel
Requires:       fmt-devel

%description -n %{devname}
The %{name}-devel package contains C++ header files for developing
applications that use %{name}.

%prep
%autosetup
mkdir -p %{_target_platform}
find . -name '.gitignore' -exec rm {} \;
sed -i -e "s,\r,," README.md
# FC compatibility:
ln -sf %{_target_platform} build

%build
pushd %{_target_platform}
    cd ..
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DSPDLOG_BUILD_SHARED=ON \
    -DSPDLOG_BUILD_EXAMPLES=OFF \
    -DSPDLOG_BUILD_BENCH=OFF \
    -DSPDLOG_BUILD_TESTS=ON \
    -DSPDLOG_FMT_EXTERNAL=ON \
 
popd
%ninja_build -C %{_target_platform}

#check
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}/%{_libdir}
#pushd %{_target_platform}
#    ctest --output-on-failure
#popd

%install
%ninja_install -C %{_target_platform}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%doc README.md example/
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/spdlog/*.cmake
