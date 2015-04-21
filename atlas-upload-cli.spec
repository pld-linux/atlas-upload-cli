#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	CLI to upload application code to Atlas
Name:		atlas-upload-cli
Version:	0.2.0
Release:	1
License:	MPL v2.0
Group:		Applications/System
Source0:	https://github.com/hashicorp/atlas-upload-cli/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	06fa00b9feb63b0a25e5331831b5b968
URL:		https://github.com/hashicorp/atlas-upload-cli
BuildRequires:	golang >= 1.2.1
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# binary stripped or something
%define		_enable_debug_packages 0

%description
The Atlas Upload CLI is a lightweight command line interface for
uploading application code to Atlas to kick off deployment processes.
This is the CLI used to power the vagrant push command and other parts
of Atlas Go with the Atlas strategy.

It can also be downloaded and used externally with other systems (such
as a CI service like Jenkins or Travis CI) to initiate Atlas-based
deploys.

%prep
%setup -q

# handle external deps:
#package github.com/hashicorp/atlas-go/archive: cannot download, $GOPATH not set. For more details see: go help gopath
#package github.com/hashicorp/atlas-go/v1: cannot download, $GOPATH not set. For more details see: go help gopath
#package github.com/hashicorp/logutils: cannot download, $GOPATH not set. For more details see: go help gopath
#package github.com/mitchellh/ioprogress: cannot download, $GOPATH not set. For more details see: go help gopath

%build
# these interfere with go download -- the git vars point to .spec repo
unset GIT_DIR GIT_WORK_TREE

export GOPATH=$(pwd)/vendor
# make -j1 because https://github.com/hashicorp/atlas-upload-cli/pull/10
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/atlas-upload $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE
%attr(755,root,root) %{_bindir}/atlas-upload
