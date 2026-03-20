#
# Conditional build:
%bcond_with	tests		# build without tests

%define pkgname faraday
Summary:	HTTP/REST API client library
Name:		ruby-%{pkgname}
Version:	2.14.1
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	01e6b27ae2d0069be15fa8aec3bc81d9
URL:		https://lostisland.github.io/faraday
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
Requires:	ruby-faraday-net_http >= 2.0
Requires:	ruby-faraday-net_http < 3.5
Requires:	ruby-json
Requires:	ruby-logger
%if %{with tests}
BuildRequires:	lsof
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(multipart-post) < 3
BuildRequires:	rubygem(multipart-post) >= 1.2
BuildRequires:	rubygem(sinatra)
BuildRequires:	wget
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HTTP/REST API client library.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
# The test suite is ran by a custom bash script.
# Skip test check until this is resolved.
# https://github.com/lostisland/faraday/blob/main/script/test
%{__ruby} -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
