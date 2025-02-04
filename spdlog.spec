%global major 1
#global debug_package %{nil}
%define _empty_manifest_terminate_build 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Super fast C++ logging library
Name:		spdlog
Version:	1.15.1
Release:	1
Group:		Development/C
License:	MIT
URL:		https://github.com/gabime/spdlog/
Source0:	https://github.com/gabime/spdlog/archive/v%{version}/%{name}-%{version}.tar.gz
#Patch0:		276ee5f5c0eb13626bd367b006ace5eae9526d8a.patch
Patch1:		remove-unused-overload-fmt.patch
BuildRequires:	pkgconfig(fmt)
BuildSystem:	cmake
BuildOption:	-DCMAKE_BUILD_TYPE=Release
BuildOption:	-DSPDLOG_BUILD_SHARED=ON
BuildOption:	-DSPDLOG_BUILD_EXAMPLE=OFF
BuildOption:	-DSPDLOG_BUILD_BENCH=OFF
BuildOption:	-DSPDLOG_BUILD_TESTS=OFF
BuildOption:	-DSPDLOG_FMT_EXTERNAL=ON

%description
This is a packaged version of the gabime/spdlog header-only C++
logging library available at Github.


%package -n %{libname}
Summary:	Super fast C++ logging library
Group:		System/Libraries

%description -n %{libname}
Super fast C++ logging library.

%package -n %{devname}
Group:		Development/C
Summary:	Development files for %{name}
Provides:	%{name}-static = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{EVRD}
Requires:	libstdc++-devel
Requires:	pkgconfig(fmt)

%description -n %{devname}
The %{name}-devel package contains C++ header files for developing
applications that use %{name}.

%prep -a
find . -name '.gitignore' -exec rm {} \;
sed -i -e "s,\r,," README.md

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%doc README.md example/
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/spdlog/*.cmake
