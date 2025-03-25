Summary:	CPU INFOrmation library
Summary(pl.UTF-8):	Biblioteka odczytująca dotyczące CPU INFOrmacje
Name:		libcpuinfo
%define	gitref	aaac07ee499895770c89163ce0920ef8bb41ed23
%define	snap	20250203
Version:	0
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
Source0:	https://github.com/1480c1/cpuinfo/archive/%{gitref}/cpuinfo-%{snap}.tar.gz
# Source0-md5:	8378b8fbf8cac19ab26a09859f280da4
URL:		https://github.com/1480c1/cpuinfo
BuildRequires:	cmake >= 3.5
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpmbuild(macros) >= 1.605
# libcpuinfo.so is not versioned currently, so conflicts with development symlink
Conflicts:	cpuinfo-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cpuinfo is a library to detect essential for performance optimization
information about host CPU.

%description -l pl.UTF-8
cpuinfo to biblioteka do wykrywania istotnych przy optymalizacji
wydajności informacji o CPU, na którym działa program.

%package devel
Summary:	Header files for cpuinfo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cpuinfo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for cpuinfo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cpuinfo.

%prep
%setup -q -n cpuinfo-%{gitref}

%build
install -d build
cd build
# CMAKE_INSTALL_DATAROOTDIR is used to install (arch-dependent) cmake configs
%cmake .. \
	-DCMAKE_INSTALL_DATAROOTDIR=%{_libdir} \
	-DCPUINFO_BUILD_BENCHMARKS=OFF \
	-DCPUINFO_BUILD_MOCK_TESTS=OFF \
	-DCPUINFO_BUILD_UNIT_TESTS=OFF \
	-DUSE_SYSTEM_LIBS=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/cache-info
%attr(755,root,root) %{_bindir}/cpu-info
%attr(755,root,root) %{_bindir}/cpuid-dump
%attr(755,root,root) %{_bindir}/isa-info
%attr(755,root,root) %{_libdir}/libcpuinfo.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/cpuinfo.h
%{_pkgconfigdir}/libcpuinfo.pc
%dir %{_libdir}/cpuinfo
%{_libdir}/cpuinfo/*.cmake
