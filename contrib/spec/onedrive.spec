# Determine based on distribution & version what options & packages to include
%if 0%{?fedora} || 0%{?rhel} >= 7
%global with_systemd      1
%else
%global with_systemd      0
%endif

Name:       onedrive
Version:    2.4.9
Release:    1%{?dist}
Summary:    Microsoft OneDrive Client
Group:      System Environment/Network
License:    GPLv3
URL:        https://github.com/abraunegg/onedrive
Source0:    v%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dmd >= 2.083.0
BuildRequires:  sqlite-devel >= 3.7.15
BuildRequires:  libcurl-devel
Requires:       sqlite >= 3.7.15
Requires:       libcurl

%if 0%{?with_systemd}
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif

%define debug_package %{nil}

%description
Microsoft OneDrive Client for Linux

%prep

%setup -q
# This creates the directory %{_builddir}/%{name}-%{version}/

%build
# cd %{_builddir}/%{name}-%{version}
%configure 
make 

%install
%make_install PREFIX="%{buildroot}"

%clean

%files
%doc README.md LICENSE CHANGELOG.md
%config %{_sysconfdir}/logrotate.d/onedrive
%{_mandir}/man1/%{name}.1.gz
%{_docdir}/%{name}
%{_bindir}/%{name}
%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%else
%{_bindir}/onedrive_service.sh
/etc/init.d/onedrive
%endif

%changelog
