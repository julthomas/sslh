Summary:       SSL/SSH multiplexer
Name:          sslh
Version:       1.15
Release:       3%{?dist}
Group:         System Environment/Daemons
License:       GPL
URL:           http://www.rutschle.net/tech/sslh.shtml
Source0:       %{name}-%{version}.tar.gz
Source1:       sslh.init
Source2:       sslh.sysconfig
Source3:       sslh.cfg
Patch0:        config-option-transparent.patch
Requires:      libconfig
BuildRequires: libconfig-devel
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Sslh accepts connections on specified ports, and forwards
them further based on tests performed on the first data
packet sent by the remote client.

Probes for HTTP, SSL, SSH, OpenVPN, tinc, XMPP are
implemented, and any other protocol that can be tested using
a regular expression, can be recognised. A typical use case
is to allow serving several services on port 443 (e.g. to
connect to ssh from inside a corporate firewall, which
almost never block port 443) while still serving HTTPS on
that port. 

Hence sslh acts as a protocol demultiplexer, or a
switchboard. Its name comes from its original function to
serve SSH and HTTPS on the same port.

%prep
%setup
%patch0 -p0

%build
%{__make} %{?_smp_mflags} USELIBCONFIG=1 \
                          USELIBWRAP=

%install
%{__rm} -rf %{buildroot}

%{__install} -pD -m 0755 sslh-fork %{buildroot}/%{_sbindir}/sslh-fork
%{__install} -pD -m 0755 sslh-select %{buildroot}/%{_sbindir}/sslh-select
%{__install} -pD -m 0644 sslh.8.gz %{buildroot}/%{_mandir}/man8/sslh.8.gz
%{__install} -pD -m 0755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/rc.d/init.d/sslh
%{__install} -pD -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/sslh
%{__install} -pD -m 0644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/sslh.cfg
%{__install} -d -m 0755 %{buildroot}/%{_var}/run/sslh

%pre
if ! getent passwd sslh >/dev/null 2>&1; then
    useradd -r -g nobody -s /sbin/nologin -d %{_var}/run/sslh -M sslh
fi

%post
/sbin/chkconfig --add sslh

%preun
if [ $1 -eq 0 ]; then
    /sbin/service sslh stop > /dev/null 2>&1
    /sbin/chkconfig --del sslh
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc ChangeLog README
%doc %{_mandir}/man8/sslh.8*
%{_sysconfdir}/rc.d/init.d/sslh
%config(noreplace) %{_sysconfdir}/sysconfig/sslh
%config(noreplace) %{_sysconfdir}/sslh.cfg
%{_sbindir}/sslh-fork
%{_sbindir}/sslh-select
%dir %attr(-, sslh, -) %{_var}/run/sslh

%changelog
* Sun Aug 25 2013 Julien Thomas <julthomas@free.fr> 1.15-3
- Create directory /var/run/sslh writable by sslh
- Add capabilities to sysconfig file for transparent mode

* Sun Aug 25 2013 Julien Thomas <julthomas@free.fr> 1.15-2
- Create sslh user

* Sat Aug 24 2013 Julien Thomas <julthomas@free.fr> 1.15-1
- Initial package
