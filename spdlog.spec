%global major 0
%global user            gabime
%global debug_package   %{nil}

Name:           spdlog
Version:        1.3.1
Release:        %mkrel 3
Summary:        Super fast C++ logging library
Group:		Development/C
License:        MIT
URL:            https://github.com/%{user}/%{name}/
Source0:        https://github.com/%{user}/%{name}/archive/v%{version}.tar.gz

BuildRequires:  ninja
BuildRequires:  fmt-devel
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  gcc

%description
This is a packaged version of the gabime/spdlog header-only C++
logging library available at Github.

%package devel
Group:		Development/C
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
Requires:       libstdc++-devel
Requires:       fmt-devel

%description devel
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
    -DSPDLOG_BUILD_EXAMPLES=OFF \
    -DSPDLOG_BUILD_BENCH=OFF \
    -DSPDLOG_BUILD_TESTS=ON \
    -DSPDLOG_FMT_EXTERNAL=ON \
 
popd
%ninja_build -C %{_target_platform}

%check
pushd %{_target_platform}
    ctest --output-on-failure
popd

%install
%ninja_install -C %{_target_platform}

%files devel
%doc README.md example/
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}.pc
