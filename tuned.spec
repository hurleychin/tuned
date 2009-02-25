Summary: A dynamic adaptive system tuning daemon
Name: tuned
Version: 0.1.1
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Daemons
# The source for this package was pulled from upstream git.  Use the
# following commands to get the corresponding tarball:
#  git clone git://fedorapeople.org/~pknirsch/tuned.git/
#  cd tuned
#  git checkout v%{version}
#  make archive
Source: tuned-%{version}.tar.bz2
URL: http://fedorapeople.org/~pknirsch/git/tuned.git/
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
BuildArch: noarch

%description
The tuned package contains a daemon that tunes system settings dynamically.

%package utils
Summary: Disk and net monitoring systemtap scripts
Requires: systemtap kernel-debuginfo
Group: Applications/System

%description utils
The tuned-utils package contains several systemtap scripts to allow detailed
manual monitoring of the system.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add tuned

%preun
if [ $1 = 0 ] ; then
    /sbin/service tuned stop >/dev/null 2>&1
    /sbin/chkconfig --del tuned
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service tuned condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README doc/README.txt doc/TIPS.txt
%{_initddir}/tuned
%config(noreplace) %{_sysconfdir}/tuned.conf
%{_sbindir}/tuned
%{_datadir}/tuned
%{_mandir}/man8/*

%files utils
%defattr(-,root,root,-)
%{_sbindir}/netdevstat
%{_sbindir}/diskdevstat


%changelog
* Wed Feb 25 2009 Phil Knirsch <pknirsch@redhat.com> - 0.1.1-1
- Bump release
- Fixed BuildRoot tag to use latest recommendation of FPG
- Lots of whitespace changes
- Some minor README changes
- Added a changelog rule in Makefile
- Fixed rpmlint error messages
- Add init() methods to each plugin
- Call plugin init() methods during tuned's init()
- Add support for command line parameters
      o -c conffile|--config==conffile to specify the location of the config file
      o -d to start tuned as a daemon (instead of as normal app)
- Readded the debug output in case tuned isn't started as as daemon
- Fixed initialization of max transfer values for net tuning plugin
- Added complete cleanup code in case of tuned exiting and/or
  getting a SIGTERM to restore default values
- Made the disk tuning pluging less nosy if started as non-daemon
- Fixed missing self. in the tuned.py config handling
- Added a manpage
- Fixed summary
- Added missing GPL notic to tuned.py
- Added explanation for Source entry in specfile
- Added a distarchive target for the Makefile for proper tagging in git
- Added a explanation how to create the tarball via git in the specfile
- Fixed the defattr() lines in the specfile to conform FRG

* Mon Feb 23 2009 Phil Knirsch <pknirsch@redhat.com> - 0.1.0-1
- Initial version
